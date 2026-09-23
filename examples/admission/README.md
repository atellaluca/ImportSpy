# Admission examples

Run these commands from the repository root after installing ImportSpy and the
project's dependencies. The example project declares `packaging`, while
`typer` is installed with ImportSpy but intentionally undeclared here.

| Example | Command | Expected result |
| --- | --- | --- |
| Launch denial | `importspy check examples/admission/plugin.py` | DENY, `ISPY-D101`, no print from the target. |
| Structure | `importspy check examples/admission/structural_plugin.py` | ADMIT without execution. |
| Version and declaration | `importspy check examples/admission/versioned_plugin.py` | ADMIT with installed packaging >=24. |
| Undeclared dependency | `importspy check examples/admission/plugin.py -s examples/admission/undeclared.yml` | DENY, `ISPY-D105` for typer. |
| Required provenance | `importspy check examples/admission/versioned_plugin.py -s examples/admission/provenance.yml` | DENY, `ISPY-P101` without a verifying provider. |
| Offline extension | `python -m examples.admission.extension_demo` | ADMIT with observed inventory and a pure custom validator. |

The runtime example requires an environment value. On a POSIX shell:

```bash
IMPORTSPY_EXAMPLE_MODE=production importspy check examples/admission/structural_plugin.py -s examples/admission/runtime.yml
```

Without that variable, admission is denied with `ISPY-R103`. Values are redacted
from reports.

`origin_plugin.py`, `vcs-origin.yml`, and `local-origin.yml` demonstrate policies
for a private `company-payment-sdk` distribution that provides `company_sdk`.
They are tested against temporary realistic `.dist-info` records; no such SDK is
downloaded or included. Running them directly without that installation correctly
reports an unresolved import. A VCS metadata match is not cryptographic provenance.

`tests/test_examples.py` tests these examples and extracts the actual source and
policy blocks from README.md for the launch regression. It verifies the DENY
decision, exit code, and absence of `THIS MUST NOT RUN` output.
