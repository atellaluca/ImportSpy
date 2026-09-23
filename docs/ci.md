# CI and GitHub Actions

Run admission in the same dependency environment that will host your code.
`check` never executes its subjects, even when admitted. Install your project and
its dependencies first; ImportSpy reads their installed packaging metadata.

```yaml
name: Admission
on: [push, pull_request]
permissions:
  contents: read
jobs:
  admission:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python -m pip install . importspy
      - run: importspy check . --format json
```

Pin ImportSpy and your environment in your project's lockfile for repeatable CI.
The workflow above is a minimal integration example; no ImportSpy account is
needed and checks need no network after environment installation.

## Configure exact project subjects

`importspy check .` reads explicit entries from `pyproject.toml`; it does not
recursively scan virtual environments, import packages, or discover arbitrary
files. All configured paths must stay inside the project directory.

```toml
[tool.importspy]
subjects = [
  {path = "plugins/payment.py", contract = "contracts/payment.yml"},
  {path = "plugins/report.py", contract = "contracts/report.yml"},
]
```

Directory JSON output is an array of decisions. Exit codes are `0` admitted,
`1` denied, `2` invalid policy/configuration and `3` tool failure; the highest
code determines a multi-subject run's status. Do not ignore failure exit codes.
For a single source, use `importspy check plugin.py --contract policy.yml`.

## SARIF in code scanning

If your repository supports GitHub code scanning, write SARIF and upload it even
when admission denies a subject. Add `security-events: write` only to the job
that uploads the report. Fork pull requests may lack that permission.

```yaml
- name: Admission report
  id: admission
  continue-on-error: true
  run: importspy check . --format sarif > importspy.sarif
- name: Upload results
  if: always() && steps.admission.outcome != 'skipped'
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: importspy.sarif
- name: Enforce admission result
  if: always() && steps.admission.outcome != 'success'
  run: exit 1
```

Violations have stable rule codes and actual source locations when known; missing
locations are omitted. Reports include policy/source identity and evidence through
JSON; SARIF focuses on violations and decision outcomes.

## ImportSpy's own quality gates

The repository workflow runs tests on Python 3.10–3.14, Ruff, mypy, strict MkDocs,
a wheel/sdist build, and a clean installed-wheel CLI smoke test. The configured
policy in `contracts/importspy-domain.yml` admits ImportSpy's domain models and
checks that Pydantic is declared and satisfies the supported version range.
The `tests` aggregate requires every Python matrix job to pass.

See [release engineering](release.md) before tagging or publishing a distribution.
