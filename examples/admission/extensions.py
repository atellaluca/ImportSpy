"""Offline evidence and pure policy examples; no provenance is asserted."""

from collections.abc import Iterable

from packaging.utils import canonicalize_name

from importspy.domain import AdmissionContext, Dependency, Evidence, Violation
from importspy.policy import AdmissionPolicy


class InventoryProvider:
    name = "example-inventory"
    requires_network = False

    def collect(
        self, context: AdmissionContext, dependencies: list[Dependency]
    ) -> Iterable[Evidence]:
        names = sorted(
            {dist.name for dependency in dependencies for dist in dependency.distributions}
        )
        yield Evidence(
            kind="example.inventory",
            subject="dependencies",
            observed={"distributions": [name for name in names]},
            provider=self.name,
            status="observed",
            detail="Names copied from installed metadata; not provenance verification.",
        )


class DistributionAllowlist:
    """Evaluate an inventory collected by the selected provider without IO."""

    def __init__(self, allowed: frozenset[str] = frozenset({"packaging"})):
        self.allowed = frozenset(canonicalize_name(name) for name in allowed)

    def evaluate(
        self,
        policy: AdmissionPolicy,
        evidence: list[Evidence],
        dependencies: list[Dependency],
        context: AdmissionContext,
    ) -> Iterable[Violation]:
        inventories = [
            item.observed
            for item in evidence
            if item.kind == "example.inventory"
            and item.subject == "dependencies"
            and item.provider == "example-inventory"
            and item.status in {"observed", "verified"}
        ]
        if len(inventories) != 1 or not isinstance(inventories[0], dict):
            yield Violation(
                code="EXAMPLE-P001",
                category="example-policy",
                subject=str(context.subject),
                message="The selected inventory provider did not supply one usable inventory.",
            )
            return
        names = inventories[0].get("distributions")
        if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
            yield Violation(
                code="EXAMPLE-P001",
                category="example-policy",
                subject=str(context.subject),
                message="The collected inventory has an invalid shape.",
            )
            return
        for name in names:
            if isinstance(name, str) and canonicalize_name(name) not in self.allowed:
                yield Violation(
                    code="EXAMPLE-P002",
                    category="example-policy",
                    subject=name,
                    message=f"Distribution `{name}` is outside the application allowlist.",
                    expected=[str(allowed) for allowed in sorted(self.allowed)],
                    observed=name,
                )
