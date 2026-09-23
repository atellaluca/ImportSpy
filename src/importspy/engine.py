"""Admission orchestration and the separate explicit execution boundary."""

import platform
import sys
from pathlib import Path
from types import ModuleType

from .dependencies import DependencyResolver, collect_dependency_evidence
from .domain import (
    AdmissionContext,
    AdmissionDecision,
    AdmissionRequest,
    Evidence,
    Violation,
)
from .extensions import EvidenceProvider, PolicyValidator, RuntimeValidator
from .inspection import SourceInspection, SourceInspector
from .policy import AdmissionPolicy, PolicyEngine, collect_runtime_evidence, load_policy
from .version import __version__


class AdmissionDenied(ValueError):
    def __init__(self, decision: AdmissionDecision):
        self.decision = decision
        super().__init__(f"Admission denied for {decision.subject}")


class ExecutionFailed(RuntimeError):
    def __init__(self, decision: AdmissionDecision):
        self.decision = decision
        super().__init__(f"Admitted target raised during execution: {decision.subject}")


def project_root_for(subject: Path) -> Path:
    for parent in subject.resolve().parents:
        if (parent / "pyproject.toml").is_file():
            return parent
    return subject.resolve().parent


class AdmissionEngine:
    def __init__(
        self,
        *,
        providers: tuple[EvidenceProvider, ...] = (),
        validators: tuple[PolicyValidator, ...] = (),
        runtime_validators: tuple[RuntimeValidator, ...] = (),
        allow_network: bool = False,
    ):
        names = [provider.name for provider in providers]
        if any(not name or name.startswith("importspy") for name in names):
            raise ValueError(
                "Provider names must be nonempty and cannot use the reserved importspy prefix."
            )
        if len(set(names)) != len(names):
            raise ValueError(
                "Provider names must be unique within an admission engine."
            )
        self.providers = providers
        self.validators = validators
        self.runtime_validators = runtime_validators
        self.allow_network = allow_network
        self._resolvers: dict[Path, DependencyResolver] = {}

    def check(self, request: AdmissionRequest) -> AdmissionDecision:
        """Inspect and decide without executing target code, whether admitted or denied."""
        return self._check(request)[0]

    def _check(
        self, request: AdmissionRequest
    ) -> tuple[AdmissionDecision, SourceInspection]:
        subject = request.subject.resolve()
        root = (request.project_root or project_root_for(subject)).resolve()
        policy, digest = (
            load_policy(request.contract)
            if request.contract
            else (AdmissionPolicy(), None)
        )
        context = AdmissionContext(
            subject=subject,
            project_root=root,
            network_allowed=self.allow_network,
            environment={
                "python": platform.python_version(),
                "os": platform.system().lower(),
                "architecture": platform.machine().lower(),
                "implementation": platform.python_implementation(),
            },
        )
        inspection = SourceInspector().inspect(subject)
        decision = AdmissionDecision(
            subject=str(subject),
            source_hash=inspection.source_hash,
            contract_identity=policy.policy_id
            or (str(request.contract) if request.contract else None),
            contract_hash=digest,
            engine_version=__version__,
            environment=context.environment,
            evidence=list(inspection.evidence),
            violations=list(inspection.violations),
            phases=["static"],
        )
        if any(item.severity == "error" for item in inspection.violations):
            return decision, inspection
        if root not in self._resolvers:
            self._resolvers[root] = DependencyResolver(root)
        resolver = self._resolvers[root]
        decision.dependencies = resolver.resolve(inspection.imports, subject)
        decision.evidence.extend(collect_dependency_evidence(decision.dependencies))
        decision.evidence.extend(collect_runtime_evidence(policy, context))
        decision.phases.extend(["resolve", "evidence", "host-runtime"])
        for provider in self.providers:
            if provider.requires_network and not self.allow_network:
                decision.evidence.append(
                    Evidence(
                        kind="provider.availability",
                        subject=provider.name,
                        provider=provider.name,
                        phase="external",
                        status="unavailable",
                        detail="Network access was not enabled.",
                    )
                )
                continue
            try:
                collected = list(
                    provider.collect(
                        context.model_copy(deep=True),
                        [item.model_copy(deep=True) for item in decision.dependencies],
                    )
                )
                if not all(isinstance(item, Evidence) for item in collected):
                    raise TypeError("Provider must yield Evidence")
                decision.evidence.extend(
                    item.model_copy(deep=True, update={"provider": provider.name})
                    for item in collected
                )
            except Exception:
                # Do not leak provider exceptions: URLs, tokens or payloads may contain secrets.
                decision.evidence.append(
                    Evidence(
                        kind="provider.availability",
                        subject=provider.name,
                        provider=provider.name,
                        phase="external",
                        status="unavailable",
                        detail="Provider failed to collect evidence.",
                    )
                )
        decision.violations.extend(
            PolicyEngine().evaluate(
                policy, inspection, decision.dependencies, decision.evidence, context
            )
        )
        for validator in self.validators:
            decision.violations.extend(
                validator.evaluate(
                    policy.model_copy(deep=True),
                    [item.model_copy(deep=True) for item in decision.evidence],
                    [item.model_copy(deep=True) for item in decision.dependencies],
                    context.model_copy(deep=True),
                )
            )
        decision.phases.append("policy")
        decision.runtime_required = any(
            item.code == "ISPY-S103" for item in decision.violations
        )
        decision.decision = (
            "DENY"
            if any(item.severity == "error" for item in decision.violations)
            else "ADMIT"
        )
        return decision, inspection

    def load(
        self, request: AdmissionRequest, *, name: str | None = None
    ) -> tuple[ModuleType, AdmissionDecision]:
        """Freshly admit, execute the inspected bytes once, then validate runtime objects.

        This executes arbitrary Python. It is not a sandbox. Runtime checks happen
        after top-level effects and must never be described as static preflight.
        """
        # Execution must not reuse dependency metadata from a previous check.
        self._resolvers.clear()
        decision, inspection = self._check(request)
        if not decision.admitted:
            raise AdmissionDenied(decision)
        module_name = name or Path(decision.subject).stem
        if module_name in sys.modules:
            raise ValueError(
                f"Module name {module_name!r} is already loaded; choose an unused name."
            )
        module = ModuleType(module_name)
        module.__file__ = decision.subject
        module.__package__ = module_name.rpartition(".")[0]
        code = compile(
            inspection.source_bytes, decision.subject, "exec", dont_inherit=True
        )
        sys.modules[module_name] = module
        decision.target_executed = True
        decision.phases.append("execution")
        try:
            exec(code, module.__dict__)
            for validator in self.runtime_validators:
                decision.violations.extend(
                    validator.validate(module, decision.model_copy(deep=True))
                )
            if self.runtime_validators:
                decision.phases.append("runtime-validation")
            if any(item.severity == "error" for item in decision.violations):
                decision.decision = "DENY"
                raise AdmissionDenied(decision)
        except AdmissionDenied:
            sys.modules.pop(module_name, None)
            raise
        except BaseException as exc:
            sys.modules.pop(module_name, None)
            decision.decision = "DENY"
            decision.violations.append(
                Violation(
                    code="ISPY-R201",
                    category="runtime",
                    phase="runtime",
                    subject=decision.subject,
                    message="Target execution failed (details withheld).",
                )
            )
            if not isinstance(exc, Exception):
                raise
            raise ExecutionFailed(decision) from exc
        return module, decision
