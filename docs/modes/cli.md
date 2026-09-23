# Command-line admission

`importspy check` inspects Python source and evaluates its admission policy
without executing the target. The same command is suitable for local review and
CI. An `ADMIT` result means the requested policy passed using available evidence;
it does not execute the module or prove arbitrary Python code is safe.

## First use

```bash
importspy --version
importspy init plugin.py
importspy check plugin.py
```

`init` creates `plugin.importspy.yml` beside the source. Review that file, add
requirements appropriate to the project, and commit it with the source. It
contains the filename and statically discovered function/class/method names.
Installed external distributions receive editable approval entries; unresolved
imports receive denial entries. These are starting policy choices, not security
or provenance verification. Decorated or conditional declarations remain
requirements that can fail as unknown until reviewed.

Generation never executes the target and never overwrites a destination. Select
a different filename with:

```bash
importspy init plugin.py --output contracts/plugin.yml
importspy check plugin.py --contract contracts/plugin.yml
```

The parent directory for `--output` must already exist.

## Check a module

```bash
importspy check plugin.py
importspy check plugin.py --contract policy.yml
importspy check plugin.py --project-root .
```

Without `--contract`, a matching `plugin.importspy.yml` sidecar is selected when
present. Otherwise, the default policy applies: unresolved imports are denied;
no application-specific structure, version, origin, or provenance requirement is
inferred. A sidecar and an explicitly passed contract are not merged.

`--project-root` controls the project metadata and local dependency boundary.
Otherwise, ImportSpy uses the nearest ancestor containing `pyproject.toml`, or
the source directory when no project file is found.

| Option | Meaning |
| --- | --- |
| `--contract`, `--spymodel`, `-s` | YAML policy to evaluate |
| `--format`, `-f` | `human` (default), `json`, or `sarif` |
| `--project-root` | Project root for dependency classification/declarations |
| `--provider` | Explicitly select an installed evidence provider; repeatable |
| `--allow-network` | Permit collection by selected providers declaring network use |

The human report shows source/preflight status, the contract, dependency
classifications, host runtime facts, evidence, violations, and the decision.
Unknown structural requirements fail closed; `check` does not execute the target
to resolve them. Invalid contracts are reported without claiming source preflight
completed.

## Machine-readable reports

```bash
importspy check plugin.py --format json > decision.json
importspy check plugin.py --format sarif > results.sarif
```

JSON serializes the underlying `AdmissionDecision`, including source/contract
hashes, engine version, dependency inventory, evidence, violations, phases,
timestamp, and whether the target executed. Rendering the same decision is
stable; separate checks have their own timestamps.

SARIF 2.1.0 reports use the same violations and stable rule codes. Known source
paths and positive line/column positions are included. Unknown positions are
omitted. A passing policy can produce an empty SARIF result list.

## Check configured project subjects

Directory checks use explicit configuration, avoiding recursive scans of virtual
environments or unrelated files. Add entries to `pyproject.toml`:

```toml
[tool.importspy]
subjects = [
  { path = "plugins/formatter.py", contract = "contracts/formatter.yml" },
  { path = "plugins/exporter.py", contract = "contracts/exporter.yml" },
]
```

Then run:

```bash
importspy check .
importspy check . --format json
importspy check . --format sarif
```

Each entry requires exactly `path` and `contract`. Paths are relative to the
checked directory, and both must resolve inside that directory; escaping paths
and symlinks are rejected. Directory checks do not accept `--contract`.

Project JSON is always an array, including a project with one subject. Project
SARIF combines results into one run. The project exit status is the highest
failure code encountered, so configuration/tool failures take precedence over
ordinary policy denials.

## Evidence providers

```bash
importspy check plugin.py --provider company-evidence
importspy check plugin.py --provider company-evidence --allow-network
```

The provider must be installed under the `importspy.evidence_providers` entry
point group. Only explicitly selected providers load. Loading a provider executes
trusted extension code, so review providers before selecting them.

Without `--allow-network`, providers declaring `requires_network = True` are
skipped and recorded as unavailable. The flag governs provider collection; it is
not an operating-system network sandbox for plugin import or constructor code.
Provider failures are recorded without exposing exception details. Missing
required evidence denies admission, while unavailable evidence that no policy
requires does not independently deny it. No provider or network access is needed
for the core local admission workflow.

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Policy admitted the subject, or `init` completed successfully |
| `1` | Admission denied, including unreadable/invalid source during `check` |
| `2` | Invalid contract/configuration or CLI usage; invalid source/destination during `init` |
| `3` | Unexpected tool failure; sensitive exception details are withheld |

Use the exit status in CI rather than parsing human output. JSON and SARIF are
written to standard output for `check`, including structured policy/configuration
failures. Typer usage errors, such as an invalid command-line option, use its
normal error output rather than an admission decision.

## Migrating an existing invocation

The installed command still accepts the 0.4 positional form:

```bash
importspy plugin.py -s spymodel.yml
```

It emits a deprecation message on standard error and routes to static `check`.
Use `importspy check plugin.py -s spymodel.yml` for new integrations. The old
`--log-level`/`-l` option is no longer supported. See the
[migration guide](../migration-0.5.md) for Python API changes and the
[contract syntax](../contracts/syntax.md) for policy fields.
