# Contract examples

These policies use the [0.5 contract syntax](syntax.md). Static checks leave the
target unexecuted whether they admit or deny it.

## Structural admission

Save `plugin.py`:

```python
MODE = "production"

class Plugin:
    kind = "payments"

    def run(self, amount: int) -> str:
        return str(amount)
```

Save `plugin.importspy.yml`:

```yaml
schema_version: 1
filename: plugin.py
variables:
  - name: MODE
    value: production
classes:
  - name: Plugin
    attributes:
      - name: kind
        type: class
        value: payments
    methods:
      - name: run
        arguments:
          - name: amount
            annotation: int
        return_annotation: str
```

`importspy check plugin.py` admits these source declarations. It does not call
`run` or instantiate `Plugin`.

## Host requirements

```yaml
runtime:
  python: ">=3.10"
  os: [linux, darwin, windows]
  implementation: [CPython]
  environment:
    APP_MODE: production
    SERVICE_TOKEN: null
```

Run in a host that satisfies the policy. The token is checked for presence;
its value is not included in the report. Host inspection needs no target import.

## Deny a dependency before its importer runs

```python
import packaging
import typer

print("THIS MUST NOT RUN")
```

```yaml
schema_version: 1
dependencies:
  packaging:
    version: ">=24"
  typer:
    allowed: false
```

Checking this source with that policy returns DENY and exit code 1 without
running the print statement. Both packages are dependencies of ImportSpy; the
[quickstart](../intro/quickstart.md) supplies the complete invocation.

## Require declared dependencies

```yaml
dependencies:
  requests:
    required: true
    version: ">=2.32,<3"
    declared: true
dependency_options:
  undeclared: deny
  unresolved: deny
```

The source must import the distribution, it must be installed at a permitted
version, and supported project metadata must declare it. Being installed only
as a transitive dependency does not satisfy `declared: true`. An unknown
declaration context also fails that requirement.

## Restrict a VCS origin

```yaml
dependencies:
  internal-payment-sdk:
    origin:
      type: vcs
      repository: https://github.com/acme/payment-sdk
      commit: "0123456789abcdef"
    editable: false
```

This example is an origin policy template: substitute your distribution and
revision. PEP 610 metadata must establish the required fields. It does not
verify the artifact's cryptographic provenance.

## Require external verification

```yaml
evidence_requirements:
  - kind: distribution.provenance
    subject: cryptography
    provider: trusted-verifier
    status: verified
```

The requirement fails until a selected provider supplies matching verified
evidence. This is an integration boundary, not a bundled verifier. See
[evidence](../evidence.md), [extensions](../extensions.md), and the
[community roadmap](../community-roadmap.md).

Executable scenarios and their requirements are maintained in the repository's
[admission examples](https://github.com/atellaluca/ImportSpy/tree/main/examples/admission).
