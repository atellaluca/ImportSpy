# Dependency admission

ImportSpy maps imports to installed distributions before evaluating dependency policy.
It reads source paths and packaging metadata without importing the target or its
dependencies. No network access is needed.

```yaml
schema_version: 1
dependencies:
  requests:
    allowed: true
    version: ">=2.32,<3"
    declared: true
  legacy-package:
    allowed: false
  import:legacy_module:
    allowed: false
dependency_options:
  unresolved: deny
  undeclared: deny
  unlisted: allow
```

Distribution policy keys use packaging name normalization: `My_Package`,
`my.package`, and `my-package` identify the same distribution. Import names remain
case sensitive. `import:<top-level-name>` explicitly addresses an import, including
an unresolved import; this avoids guessing a distribution name from an import.

## Resolution and inventory

The resolver uses `importlib.metadata.packages_distributions()` and distribution
metadata. On Python 3.10 it uses the maintained
[`importlib-metadata` backport](https://importlib-metadata.readthedocs.io/en/latest/api.html)
so wheels without `top_level.txt` can be mapped using their `RECORD` file too.
This handles import/distribution name differences such as `yaml` and
`PyYAML` without special cases. One import can map to multiple distributions, and
one distribution can provide several imports. All mapped contributors are retained
and evaluated. The inventory is conservative: importing one child of a namespace
checks every contributor mapped to that namespace's top-level name.
See the [Python metadata documentation](https://docs.python.org/3/library/importlib.metadata.html#mapping-import-to-distribution-packages).

Dependencies are classified as:

| Kind | Meaning |
| --- | --- |
| `stdlib` | A built-in or standard-library top-level import in the checking interpreter. |
| `internal` | A matching source file or package directory under the selected project root, its `src` directory, or the subject's directory. |
| `external` | An installed distribution identified by metadata. |
| `namespace` | Multiple installed distributions, or a local namespace with installed contributors, associated with one import. |
| `direct` | One distribution with VCS, local-directory, or archive origin metadata. |
| `unresolved` | No complete supported source or distribution mapping is available. |

Regular project source takes precedence over standard-library names except built-ins.
That includes dotted imports whose top-level name is shadowed by a local source
module or regular package. Local namespace directories retain installed contributors
when metadata identifies them.
Relative imports are checked against their source package location. Symlinks
escaping the project root are unresolved, rather than classified as project source
or silently attributed to an unrelated installed distribution.

Resolution never calls `find_spec()` on dotted names, which can import a parent
package. Some editable installations omit the metadata needed to map import names;
these remain unresolved. Installed custom metadata finders are trusted host code.
Resolution does not emulate arbitrary import hooks, package `__path__` mutations,
zip source trees, or dynamic imports. It does not prove that every submodule or
imported attribute exists. A relative `from . import value` may remain unresolved
when `value` is a package attribute rather than a source module.

The inventory includes imports observed in the inspected file, including imports
inside functions and conditional branches. The `optional` flag records conditional
observations; it does not bypass policy. ImportSpy does not recursively inspect
every imported file or resolve a package manager's transitive dependency graph.

`DependencyResolver(project_root)` caches the import mapping and distribution
metadata per instance. Reuse an instance for a batch, and create a new one after
changing installed packages or project declarations.

## Rules and defaults

| Rule | Semantics |
| --- | --- |
| `allowed: false` | Reject any observed matching distribution/import. Defaults to `true`. |
| `required: true` | Require a matching dependency in the source inventory, not merely an installed package. |
| `version: ">=2,<3"` | Apply a PEP 440 specifier to the installed version. Unknown/invalid versions fail. |
| `declared: true` | Require a matching project declaration; unknown declaration context fails. |
| `declared: false` | Require known absence from supported project declarations. |
| `origin` | Match explicitly specified origin fields; unknown facts fail the comparison. |
| `editable: false` | Require metadata establishing a non-editable installation. Unknown is not false. |
| `provenance: {required: true}` | Require verified evidence through the admission engine's evidence policy. |

Version constraints use `packaging.SpecifierSet`, including its normal prerelease
rules. A range such as `>=2,<3` does not automatically admit prereleases. Poetry's
caret version syntax is not valid in an admission version rule.

Global `dependency_options` provide independent constraints:

- `unresolved: deny` is the default. Set `allow` explicitly when unresolved imports
  are acceptable for the use case.
- `undeclared: allow` is the default. `deny` rejects external distributions that are
  undeclared **or whose declaration context is unknown**.
- `unlisted: allow` is the default. `deny` requires an explicit distribution rule
  for each observed external distribution, including all namespace contributors.

Import rules do not bypass these constraints. For example, an import allow rule
does not establish the identity of an unresolved distribution and does not satisfy
`unlisted: deny`. Standard-library and internal imports are outside external
distribution allowlists, but may be denied using explicit import rules.

## Declared, observed, and installed

Declaration detection reads only `pyproject.toml` in the selected project root.
It does not infer ownership from an unrelated installed package, execute
`setup.py`, or search arbitrary parent directories.

Supported declaration contexts are:

- PEP 621 `[project].dependencies` and all `[project.optional-dependencies]` groups.
- Legacy Poetry `[tool.poetry.dependencies]`, including optional dependencies.
  Development dependency groups are excluded.

A declaration means the distribution is named somewhere in those runtime/optional
requirements. Environment markers are parsed as part of PEP 508 requirements but
are not evaluated to select an active environment. All optional extras are counted
as declarations; their activation is not inferred. This is intentional because
static source inspection also observes inactive branches. Declared status does
not prove a dependency should be installed for a particular selected extra or
platform, and does not enforce the project's dependency version specifiers.
Use explicit admission version rules for that purpose.

Missing, malformed, unsupported, or dynamically supplied dependency declarations
produce `declared: null`. PEP 621 metadata takes precedence over legacy Poetry
metadata when both tables exist. A valid static `[project]` without dependency
entries means an empty declaration set. Each namespace distribution has its own
declaration state; the import-level state is true only when all contributors are
declared, false when a contributor is undeclared, and unknown when the context is
unknown.

## Origin and editable installations

```yaml
dependencies:
  internal-payment-sdk:
    origin:
      type: vcs
      repository: https://github.com/acme/payment-sdk
      commit: 0123456789abcdef
    editable: false
```

The resolver reads [PEP 610 direct URL metadata](https://packaging.python.org/en/latest/specifications/direct-url-data-structure/):

- VCS origin: repository URL and commit identifier.
- Local directory: file URL and editable flag.
- Archive origin: URL and recorded hashes, including the legacy single hash form.

These are metadata observations, not cryptographic verification of installed
files. A missing `direct_url.json` produces unknown origin and editable state.
It does **not** prove installation from PyPI or any particular index. The domain
can represent index evidence, but core resolution does not fabricate it.

Origin URLs remove userinfo, query strings, and fragments before inclusion in
decisions. Scheme and host are normalized; default HTTP(S) ports and trailing
slashes are removed. Repository comparison also removes a terminal `.git` suffix.
Paths retain case and are not percent-decoded. Arbitrary secrets embedded inside
a path are not detectable; avoid credential-bearing URL paths in package metadata.
Malformed metadata is represented as unknown, never as verified provenance.

Origin matching supports `type`, `url`, `repository`, and `commit` fields.
Provenance verification belongs to explicitly supplied evidence providers. The
engine requires evidence of kind `distribution.provenance`, with the canonical
distribution name as `subject`, `status: verified`, and a truthy `observed` value.
`provenance: true` is shorthand for `provenance: {required: true}`. Merely
finding a direct URL, a commit, or an archive hash cannot satisfy verified
provenance policy.

## Library boundary and violation codes

```python
from pathlib import Path
from importspy.dependencies import (
    DependencyOptions, DependencyResolver, DependencyRule,
    collect_dependency_evidence, evaluate_dependencies,
)
from importspy.domain import ImportReference

root = Path.cwd()
dependencies = DependencyResolver(root).resolve(
    [ImportReference(name="yaml")], root / "plugin.py"
)
evidence = collect_dependency_evidence(dependencies)
violations = evaluate_dependencies(
    dependencies, {"pyyaml": DependencyRule(version=">=6")},
    DependencyOptions(), str(root / "plugin.py"),
)
```

`evaluate_dependencies` is pure and performs no file or network access. It handles
dependency facts; provenance requirements are evaluated against provider evidence
by the admission engine.

| Code | Meaning |
| --- | --- |
| `ISPY-D101` | Dependency denied by a rule. |
| `ISPY-D102` | Unresolved import denied. |
| `ISPY-D103` | Required dependency absent from the inventory. |
| `ISPY-D104` | Version constraint not established. |
| `ISPY-D105` | Declaration constraint not established. |
| `ISPY-D106` | Origin mismatch or missing origin fact. |
| `ISPY-D107` | Editable constraint not established. |
| `ISPY-D108` | Unlisted external distribution denied. |
