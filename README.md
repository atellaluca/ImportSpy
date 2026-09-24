# ImportSpy

**Policy-as-code admission for Python modules and dependencies.**

Decide whether Python source satisfies your module, dependency, and runtime policies before admitting it for execution.

![ImportSpy banner](https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/docs/assets/importspy-banner_500px.png)

[![PyPI](https://img.shields.io/pypi/v/importspy)](https://pypi.org/project/importspy/)
[![Tests](https://img.shields.io/github/actions/workflow/status/atellaluca/ImportSpy/ci.yml?branch=main)](https://github.com/atellaluca/ImportSpy/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/atellaluca/ImportSpy)](LICENSE)

## See a denial before execution

Install ImportSpy with Python 3.10 or newer:

```bash
pip install importspy
```

Create `plugin.py`:

```python
import packaging
import typer

print("THIS MUST NOT RUN")
```

Create `plugin.importspy.yml`:

```yaml
schema_version: 1
dependencies:
  packaging:
    allowed: true
    version: ">=24"
  typer:
    allowed: false
```

Both dependencies are installed with ImportSpy. Run:

```bash
importspy check plugin.py
```

The report includes:

```text
ISPY-D101 [error] Dependency `typer` is not permitted by policy.
Decision: DENY
Target module was not executed.
```

The command exits with code **1**. The print statement never runs.
The [complete example](examples/admission/) and [automated regression test](tests/test_examples.py)
verify this behavior. A successful `check` also leaves the target unexecuted.

## Start with your own module

```bash
importspy init path/to/plugin.py
# Review path/to/plugin.importspy.yml and edit its dependency approvals.
importspy check path/to/plugin.py
importspy check path/to/plugin.py --format json
```

`init` inspects source without importing it. The starter contract records source
declarations and installed dependency identities; review it and add your own
version, origin, environment, and evidence requirements. Unresolved imports are
denied until reviewed.

## One admission pipeline

```text
Source → static preflight → dependency resolution → evidence → policy → ADMIT / DENY
                                                                          │
                                                    explicit load after ADMIT
                                                                          │
                                               execution → runtime validation
```

- **Structure:** require functions, parameters, annotations, classes, and literal declarations.
- **Dependencies:** resolve import names to distributions, including namespace contributors.
  Enforce allow/deny, required presence, versions, declarations, origins, and editable policy.
- **Host runtime:** constrain Python, operating system, architecture, implementation, and environment.
- **Evidence:** consume observations from explicitly selected providers and require verified signals.
- **Decisions:** use the same structured facts and violations for human, JSON, and SARIF reports.

Checks that cannot establish a required static fact fail closed. A computed value
or dynamically constructed interface is reported as unknown; ImportSpy does not
execute the target to fill the gap.

## A module and dependency contract

```yaml
schema_version: 1
policy_id: payments-plugin
filename: plugin.py
functions:
  - name: process
    arguments:
      - name: amount
        annotation: int
    return_annotation: str
runtime:
  python: ">=3.10"
  environment:
    PAYMENT_MODE: production
dependencies:
  requests:
    version: ">=2.32,<3"
    declared: true
  internal-payment-sdk:
    origin:
      type: vcs
      repository: https://github.com/acme/payment-sdk
    editable: false
dependency_options:
  unresolved: deny
  undeclared: deny
  unlisted: deny
```

Distribution names are distinct from import names. Origin metadata is an
observation, not verified provenance; missing direct-URL metadata does not prove
installation from PyPI. Read the [dependency reference](docs/dependencies.md)
for declaration modes, namespace behavior, and uncertainty.

## Embed admission in a loader

```python
from pathlib import Path
from importspy.domain import AdmissionRequest
from importspy.engine import AdmissionEngine

request = AdmissionRequest(
    subject=Path("plugin.py"),
    contract=Path("plugin.importspy.yml"),
)
engine = AdmissionEngine()
decision = engine.check(request)  # No target execution.
if decision.admitted:
    module, executed_decision = engine.load(request)  # Fresh admission, then execution.
```

`load` performs fresh admission and executes the inspected source bytes. Optional
runtime validators run after execution and cannot undo side effects. It does not
freeze the environment or recursively admit every transitive import. See the
[library workflow](docs/modes/embedded.md) and [security model](docs/security-model.md).

## Evidence and integrations

Supply-chain tools produce signals. ImportSpy turns relevant signals into
admission decisions. Providers can integrate vulnerability results, attestations,
or provenance without turning core into a scanner:

```yaml
dependencies:
  cryptography:
    provenance:
      required: true
```

When `cryptography` is observed, this denies admission unless the selected provider
supplies sufficient verified evidence. Add `required: true` if the dependency must
also be present. ImportSpy does not manufacture cryptographic verification from package
metadata. The [extension API](docs/extensions.md) documents `EvidenceProvider`,
`PolicyValidator`, `RuntimeValidator`, `Reporter`, and explicit entry-point loading.

Core checks work offline, with no account or telemetry. Network providers require
explicit selection and network authorization. Plugins are trusted Python code.

## CI

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"
- run: python -m pip install importspy
- run: importspy check plugin.py --contract plugin.importspy.yml
```

Use `--format json` for automation or `--format sarif` for code-scanning
integration. Exit codes are **0 admitted**, **1 denied**, **2 invalid configuration**,
and **3 tool failure**. `importspy check .` checks explicit project subjects.
See [CI integration](docs/ci.md).

## Scope and community

ImportSpy enforces policy at Python admission boundaries. It is not a sandbox,
vulnerability scanner, package manager, or proof that admitted code is safe.
It complements tools such as pip-audit, OSV, Sigstore, and SLSA by consuming
their evidence through providers.
- [Quickstart](docs/intro/quickstart.md) · [Contract reference](docs/contracts/syntax.md)
- [Architecture](docs/architecture.md) · [Static preflight](docs/static-preflight.md)
- [Migration from 0.4](docs/migration-0.5.md) · [Examples](examples/admission/)
- [Contributing](CONTRIBUTING.md) · [Security reporting](SECURITY.md)

## Case studies and talks

- **[The Missing Admission Layer in Python Plugin Systems](https://dev.to/atellaluca/case-study-the-missing-admission-layer-in-python-plugin-systems-4k80)**  
  A case study on the architectural problem behind ImportSpy: why importability is
  not the same as compatibility, and how the project evolved from import validation
  toward policy-driven admission boundaries.

- **[ImportSpy — GDG Basilicata talk](https://profile.atellaluca.com/assets/talks/importspy-gdg-basilicata-it.pdf)**  
  A presentation of ImportSpy's earlier runtime-contract generation. The current
  0.5 workflow begins with static admission before execution.

![ImportSpy logo](https://raw.githubusercontent.com/atellaluca/ImportSpy/refs/heads/main/docs/assets/importspy-logo_100px.png)

MIT licensed. Created by Luca Atella.
