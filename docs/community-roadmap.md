# Community roadmap

These are scoped contribution briefs for work after the 0.5 admission engine.
They describe proposed integrations, not features already shipped or issues
already opened. Copy a relevant brief into an integration proposal and agree on
scope with maintainers before starting substantial work.

All integrations should use the public evidence, validator, and reporter
protocols. The core remains useful offline, and network collection stays
explicit. Supply-chain tools produce signals; ImportSpy evaluates those signals
against admission policy. A provider must describe what it actually verified.

Labels below are suggested categories for maintainers, not claims that those
labels already exist in the repository.

| Proposal | Suggested categories |
| --- | --- |
| OSV / pip-audit evidence adapter | `help wanted`, `evidence-provider`, `integration` |
| Sigstore verification provider | `help wanted`, `evidence-provider`, `integration` |
| PyPI attestation provider | `help wanted`, `evidence-provider`, `integration` |
| CycloneDX inventory adapter | `help wanted`, `evidence-provider`, `integration` |
| SPDX inventory adapter | `help wanted`, `evidence-provider`, `integration` |
| GitHub metadata provider | `help wanted`, `evidence-provider`, `integration` |
| Additional reporters | `good first issue`, `integration` |
| Editor and pre-commit workflows | `help wanted`, `integration`, `documentation` |
| Dependency resolver coverage and performance | `help wanted`, `dependency-resolver` |
| Provider author examples | `good first issue`, `documentation` |

## OSV / pip-audit evidence adapter

**Problem:** Admission policy cannot consume an existing vulnerability assessment
unless its findings are mapped to the observed distribution inventory.

**Scope:** Start with an offline adapter for a documented scanner result format.
Match normalized distribution identity and version, retain advisory identifiers,
assessment time, and input inventory identity. Keep live querying optional and
separate from evaluation; do not build another vulnerability database.

**Acceptance:** Fixtures cover affected and unaffected exact versions, unmatched
packages, incomplete results, stale assessments, and unavailable data. A policy
must not interpret an absent or unmatched scan as a clean result. Document the
scanner format/version and how the user controls acceptable freshness.

## Sigstore verification provider

**Problem:** Policies need verified artifact/publisher facts rather than a flag
that a signature exists.

**Scope:** Use the established Sigstore verification implementation. Require the
exact artifact digest, a trust-root strategy, and the expected signer identity.
Separate bundle collection from verification and policy evaluation.

**Acceptance:** Tests include valid and invalid fixtures, mismatched artifact
bytes, unexpected signer identity, missing verification material, and offline
behavior. Emit `verified` only after the complete verification procedure succeeds.
Document what remains trusted and whether transparency-log material is required.

## PyPI attestation provider

**Problem:** PyPI attestation availability is useful evidence, but it is distinct
from verified provenance for the exact artifact admitted to the environment.

**Scope:** Build a provider around documented provenance APIs and PEP 740 data.
Record artifact identity, digest, publisher, repository, and workflow when the
source supports those claims. Integrate a maintained verifier or explicitly
report availability as observed evidence without claiming verification.

**Acceptance:** Mock network responses for missing attestations, malformed data,
multiple artifacts, timeouts, and digest mismatches. Define how an installed
package binds to its source artifact; if that binding is unavailable, preserve
unknown status. Add bounded requests and explicit cache/freshness handling.

## CycloneDX inventory adapter

**Problem:** Organizations already have a CycloneDX inventory and need its facts
available at the admission boundary.

**Scope:** Consume an existing document, normalize package identities, and expose
matched inventory facts. Do not generate an SBOM or treat inventory membership
as proof of integrity. Keep document trust distinct from package identity.

**Acceptance:** Cover multiple versions, ambiguous identities, unsupported schema
versions, malformed documents, and installed distributions absent from the
inventory. Preserve source document identity and explain which component fields
are used for matching.

## SPDX inventory adapter

**Problem:** SPDX package records need a documented mapping to observed Python
distributions before admission policy can evaluate them.

**Scope:** Begin with one documented SPDX serialization and schema version.
Expose package identity, version, available checksums, and document identity as
facts; preserve unknown mappings rather than guessing from file names.

**Acceptance:** Include exact and ambiguous matches, missing versions, malformed
identifiers, checksum mismatches, and unsupported documents. State the difference
between an asserted checksum and a checksum verified against artifact bytes.

## GitHub metadata provider

**Problem:** Some policies need repository, commit, or workflow facts associated
with dependency origin evidence.

**Scope:** Collect explicitly requested repository metadata using a documented
API. Normalize the dependency repository identity first, use minimally scoped
credentials, and retain observation time and immutable commit identities where
available. Mutable branch names alone do not establish artifact provenance.

**Acceptance:** Cover renamed repositories, redirects, rate limits, private
repositories, unavailable commits, and expired cached data. Credentials and URL
secrets must never enter reports. Require explicit network opt-in and mock all
network calls in the default test suite.

## Additional reporters

**Problem:** Teams may need formats beyond human, JSON, and SARIF output.

**Scope:** Implement a small reporter such as JUnit XML from the existing
`AdmissionDecision`. Define how warning severity and unavailable evidence map to
the destination format without rerunning validation.

**Acceptance:** Tests cover admission, multiple denials, Unicode, escaping,
missing locations, and stable output for the same decision. Validate the output
with a standard parser and document any information the destination cannot carry.

## Editor and pre-commit workflows

**Problem:** Developers need fast local feedback before CI.

**Scope:** Begin with a documented pre-commit hook or editor task invoking the
existing CLI. Define source/contract selection and the Python environment used
for distribution resolution. Reuse stable exit codes and structured reports.

**Acceptance:** Demonstrate a denied file with no target side effects, a passing
file, a malformed contract, and paths containing spaces. Do not claim that the
hook's isolated environment is the application's dependency inventory. Editor
integrations must preserve unknown locations and avoid running target modules.

## Dependency resolver coverage and performance

**Problem:** Namespace, editable, direct, and ambiguous installations expose
packaging edge cases that benefit from reproducible fixtures.

**Scope:** Add a minimal packaging fixture for a documented failure, then improve
resolution without importing the target or candidate dependency. Measure
metadata calls before introducing or expanding caches.

**Acceptance:** Preserve many-to-many mappings, explicit unresolved states, and
stdlib/project shadowing behavior. Test reuse across repeated checks and define
cache lifetime when installations change. Provide a benchmark or call-count test
showing the claimed improvement without hiding stale observations.

## Provider author examples

**Problem:** A new contributor needs a small working example of unavailable
facts, artifact binding, and pure policy evaluation.

**Scope:** Add an executable offline provider example with focused tests and a
short guide. Use synthetic, clearly labeled evidence and show its corresponding
policy requirement. Avoid toy examples that label unverified facts as verified.

**Acceptance:** The example runs without credentials or network access, exercises
ADMIT and DENY, and can be copied into an external package using the documented
entry-point group. Explain which code runs at plugin load time and which code
runs during evidence collection.

See [CONTRIBUTING.md](https://github.com/atellaluca/ImportSpy/blob/main/CONTRIBUTING.md)
for setup and extension guidance, and the migration guide for API compatibility.
