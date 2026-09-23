# Quickstart

A static admission check tells you whether source satisfies your policy without
running the target. Python 3.10 or newer is required.

```bash
pip install importspy
```

## Try a dependency denial

Save this as `plugin.py`:

```python
import packaging
import typer

print("THIS MUST NOT RUN")
```

Both packages are installed with ImportSpy. Save `plugin.importspy.yml` beside it:

```yaml
schema_version: 1
dependencies:
  packaging:
    version: ">=24"
  typer:
    allowed: false
```

Run:

```bash
importspy check plugin.py
```

The report includes `ISPY-D101`, `Decision: DENY`, and
`Target module was not executed.` The command exits with code 1. The print
statement never runs. This example is covered by the repository's automated tests.

## Generate a contract for your code

For a different source file without an existing sidecar:

```bash
importspy init my_plugin.py
```

This creates `my_plugin.importspy.yml` using source declarations and installed
metadata. It will not overwrite an existing file. Review generated approvals,
then add version constraints, runtime requirements, or evidence policy.

```bash
importspy check my_plugin.py
importspy check my_plugin.py --format json
importspy check my_plugin.py --contract team-policy.yml --format sarif
```

A successful check exits with code 0 and still does not execute the target.
Unresolved imports default to denial, including imports in optional branches.
A required computed value or dynamic definition can produce an unknown-static-fact
denial; see [static preflight](../static-preflight.md).

## Execute only after admission

An application can use [AdmissionEngine.load](../modes/embedded.md) for fresh
admission followed by explicit execution. That operation runs arbitrary Python.
Runtime validation after loading cannot undo effects.

Continue with [contract syntax](../contracts/syntax.md),
[dependency policy](../dependencies.md), or [CI integration](../ci.md).
