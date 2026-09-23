"""Small explicit extension boundaries. Loading a plugin executes trusted plugin code."""

from collections.abc import Iterable
from importlib.metadata import entry_points
from types import ModuleType
from typing import Protocol

from .domain import AdmissionContext, AdmissionDecision, Dependency, Evidence, Violation
from .policy import AdmissionPolicy


class EvidenceProvider(Protocol):
    name: str
    requires_network: bool

    def collect(
        self, context: AdmissionContext, dependencies: list[Dependency]
    ) -> Iterable[Evidence]: ...


class PolicyValidator(Protocol):
    def evaluate(
        self,
        policy: AdmissionPolicy,
        evidence: list[Evidence],
        dependencies: list[Dependency],
        context: AdmissionContext,
    ) -> Iterable[Violation]: ...


class RuntimeValidator(Protocol):
    """Runs only after explicit, admitted module execution; cannot undo side effects."""

    def validate(
        self, module: ModuleType, decision: AdmissionDecision
    ) -> Iterable[Violation]: ...


class Reporter(Protocol):
    def render(self, decision: AdmissionDecision) -> str: ...


def load_provider(name: str) -> EvidenceProvider:
    """Load exactly one user-selected entry point, never all installed providers."""
    matches = list(entry_points(group="importspy.evidence_providers", name=name))
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one evidence provider named {name!r}.")
    provider: EvidenceProvider = matches[0].load()()
    provider_name = getattr(provider, "name", None)
    if (
        not isinstance(provider_name, str)
        or not provider_name.strip()
        or not isinstance(getattr(provider, "requires_network", None), bool)
        or not callable(getattr(provider, "collect", None))
    ):
        raise ValueError("Evidence provider does not implement the public protocol.")
    return provider
