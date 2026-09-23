"""Run with python -m examples.admission.extension_demo from the checkout."""

from pathlib import Path

from examples.admission.extensions import DistributionAllowlist, InventoryProvider
from importspy.domain import AdmissionRequest
from importspy.engine import AdmissionEngine
from importspy.reporters import HumanReporter


def main() -> int:
    root = Path(__file__).parent
    engine = AdmissionEngine(
        providers=(InventoryProvider(),),
        validators=(DistributionAllowlist(),),
    )
    decision = engine.check(
        AdmissionRequest(
            subject=root / "versioned_plugin.py",
            contract=root / "custom-evidence.yml",
            project_root=root,
        )
    )
    print(HumanReporter().render(decision))
    return 0 if decision.admitted else 1


if __name__ == "__main__":
    raise SystemExit(main())
