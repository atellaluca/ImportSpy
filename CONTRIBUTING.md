# Contributing to ImportSpy

ImportSpy evaluates Python modules and dependency evidence against admission
policy. Contributions must preserve its main boundary: a static admission check
must not import or execute the target, whether the decision is ADMIT or DENY.

Bug reports, reproducible packaging cases, documentation, and external evidence
providers are welcome. Read the [code of conduct](CODE_OF_CONDUCT.md) and use
[SECURITY.md](SECURITY.md) for vulnerabilities instead of a public issue.

## Set up a checkout

Use Python 3.10 or newer and Poetry. Work in a virtual environment; dependency
resolution observes the installed distributions in that environment.

```bash
git clone https://github.com/atellaluca/ImportSpy.git
cd ImportSpy
poetry install --with dev
poetry run importspy --help
poetry run pytest -q
```

`pyproject.toml` defines supported Python versions and the development tools;
`poetry.lock` records the resolved environment. Keep both consistent when changing
dependencies. Do not commit virtual environments, generated reports, `site/`,
`dist/`, credentials, or local configuration.

## Validate a change

Run the focused tests while developing, then run the complete checks before a PR:

```bash
poetry run pytest -q
poetry run ruff check src tests
poetry run mypy src
poetry run mkdocs build --strict
poetry build
git diff --check
```

Useful focused suites are `tests/admission`, `tests/dependencies`, and
`tests/test_legacy.py tests/validators`. Tests must run offline and use temporary
files and controlled metadata fixtures. Mock network providers rather than
relying on live services. A source-inspection change needs a regression test
showing that denied target code did not print, mutate the environment, write a
file, create a subprocess, or open a socket, as appropriate to the regression.

Check new behavior on the lowest supported Python version as well as your local
version. Do not disable checks, add broad ignores, or delete failing coverage to
make a change pass. Build artifacts and generated documentation are validation
outputs, not source files.

## Find the right component

| Component | Responsibility |
| --- | --- |
| `domain.py` | Serializable requests, context, dependencies, evidence, violations, decisions |
| `inspection.py` | AST inspection, structural facts, starter contracts, structural evaluation |
| `dependencies.py` | Import/distribution mapping, declaration and origin metadata, dependency policy |
| `policy.py` | Contract validation, host runtime evidence, pure policy evaluation |
| `engine.py` | Collection and evaluation orchestration; explicit execution after admission |
| `extensions.py` | Provider, policy validator, runtime validator, and reporter protocols |
| `reporters.py` / `cli.py` | Shared decision rendering and the `check` / `init` workflows |
| `models.py` / `s.py` / `validators.py` | Deprecated runtime compatibility API |

Read [static preflight](docs/static-preflight.md),
[dependency policies](docs/dependencies.md), and
[the migration guide](docs/migration-0.5.md) before changing those boundaries.
`AdmissionEngine.check` never executes its target. `AdmissionEngine.load` performs
a fresh admission before explicitly executing inspected bytes; runtime validators
run afterwards and cannot undo side effects.

## Add a validator

Keep policy evaluation deterministic and independent of network operations.
For an extension, implement `PolicyValidator.evaluate(policy, evidence,
dependencies, context)` from `importspy.extensions`, returning an iterable of
`Violation`. Register the instance explicitly through
`AdmissionEngine(validators=(your_validator,))`. Use a stable code namespace for
your extension, concise messages, and source locations only when known.

For a built-in rule, extend the appropriate policy model and evaluator together.
Reject misspelled or malformed configuration. Distinguish an unknown fact from a
verified failure or success, and test admission, denial, missing evidence, and
invalid configuration. If a check needs target execution, implement the separate
`RuntimeValidator.validate(module, decision)` protocol and pass it through
`runtime_validators`; never call it during preflight.

## Add an evidence provider

A provider collects facts; policy decides what those facts permit. This complete
offline example counts observed distribution identities without treating the
count as a security or provenance claim:

```python
from collections.abc import Iterable
from pathlib import Path

from importspy.domain import AdmissionContext, AdmissionRequest, Dependency, Evidence
from importspy.engine import AdmissionEngine


class DependencyCountProvider:
    name = "example-dependency-count"
    requires_network = False

    def collect(
        self, context: AdmissionContext, dependencies: list[Dependency]
    ) -> Iterable[Evidence]:
        names = {
            distribution.name
            for dependency in dependencies
            for distribution in dependency.distributions
        }
        yield Evidence(
            kind="example.distribution_count",
            subject=str(context.subject),
            observed=len(names),
            provider=self.name,
            phase="external",
            status="observed",
        )


engine = AdmissionEngine(providers=(DependencyCountProvider(),))
decision = engine.check(AdmissionRequest(subject=Path("plugin.py")))
```

To package it for explicit CLI discovery, expose the provider class as a
zero-argument factory:

```toml
[project.entry-points."importspy.evidence_providers"]
dependency-count = "your_package.provider:DependencyCountProvider"
```

The user selects it with `importspy check plugin.py --provider dependency-count`.
Providers are trusted Python code, and loading an entry point executes that code.
The engine does not automatically load every installed provider. Set
`requires_network = True` for a network provider; the user must explicitly opt in
with `--allow-network` or `AdmissionEngine(allow_network=True)` before collection.
That flag is an API contract, not a sandbox around plugin code.

Give network clients timeouts and response limits. Keep credentials out of
URLs, evidence, diagnostics, and fixtures. Explain cache freshness, unavailable
states, and identity binding in the provider documentation. Do not label evidence
`verified` merely because an API returned it; cryptographic verification needs a
real verification procedure and artifact binding.

## Add a reporter

Implement `Reporter.render(decision: AdmissionDecision) -> str`. Consume the
existing decision without evaluating policy again or collecting new evidence.
A third-party reporter can be used directly by application code; registering a
new built-in CLI format also requires updating the CLI format enumeration.

Test admitted and denied decisions, multiple violations, unknown locations,
Unicode, and deterministic rendering of the same decision. Preserve the
meaning of severity, phase, and verification status. Avoid inventing locations
or exposing environment values.

## Documentation and pull requests

Update the relevant `docs/` page, runnable examples, and migration notes with
behavior changes. Keep documentation claims no stronger than the implementation.
Run `poetry run mkdocs serve` for local preview and the strict build before
submission. Public API examples should be exercised in tests where practical.

Use English Conventional Commits, for example `feat: enforce dependency origin`
or `fix: preserve unknown annotation evidence`. Keep commits scoped to a coherent
change and include its tests and documentation. A PR should explain the concrete
problem, resulting behavior, validation performed, compatibility implications,
and any evidence or execution boundary affected. Small documentation changes do
not require a speculative implementation plan.

The [community roadmap](docs/community-roadmap.md) provides scoped integration
ideas with acceptance criteria. Discuss substantial protocol or DSL changes in
an issue before implementing them so maintainers and provider authors can agree
on compatibility. Contributions remain under the repository's existing MIT
license.
