# Supply-chain admission

ImportSpy enforces supply-chain policies at Python module admission boundaries.
Specialized tools produce signals; ImportSpy evaluates those signals alongside
structural, dependency, and runtime requirements.

Core is not a vulnerability scanner, SBOM generator, package manager, or
cryptographic verifier. It works offline with local source and installed metadata.
No ImportSpy account, telemetry, or SaaS connection is required.

## What core establishes

The resolver maps observed import names to installed distributions and exposes
versions, project declaration state, direct-install origins, editable state, and
recorded archive hashes. Policies can deny packages, require versions and declared
dependencies, and match origin metadata.

```yaml
schema_version: 1
dependencies:
  internal-payment-sdk:
    version: ">=1,<2"
    declared: true
    origin:
      type: vcs
      repository: https://github.com/acme/payment-sdk
    editable: false
dependency_options:
  unresolved: deny
  undeclared: deny
```

A repository URL, commit identifier, or hash from `direct_url.json` is a packaging
metadata observation. It does not prove that installed files came from that
repository or still match an authenticated artifact. Missing direct-URL metadata
does not prove a PyPI/index origin. See [dependency resolution](dependencies.md)
for namespace, declaration, and normalization limits.

## Provenance policy

```yaml
schema_version: 1
dependencies:
  cryptography:
    required: true
    provenance:
      required: true
evidence_requirements:
  - kind: distribution.provenance
    subject: cryptography
    provider: company-pypi-verifier
    status: verified
```

The dependency shorthand requires verified, truthy `distribution.provenance`
evidence for each observed matching distribution. `required: true` separately
requires that distribution in the source inventory. The explicit evidence
requirement pins the trusted provider.

ImportSpy 0.5 ships the provider and policy boundary, not a built-in PyPI attestation
downloader or cryptographic verifier. This example therefore denies admission
until the application supplies a suitable trusted provider. No metadata fallback
silently turns a missing verifier into a successful provenance check.

## PyPI and PEP 740 boundary

[PEP 740](https://peps.python.org/pep-0740/) defines index distribution of digital
attestations and provenance objects associated with individual release files.
The [current packaging specification](https://packaging.python.org/en/latest/specifications/index-hosted-attestations/)
and [PyPI attestation documentation](https://docs.pypi.org/attestations/) describe
the data and verification ecosystem. Availability and successful verification
are different facts.

An integration must identify an exact artifact. Package name and version alone
are insufficient because a release can contain several wheels and an sdist.
The provider must establish the relationship between the installed distribution
being admitted and the artifact whose bytes/digest were verified. If the checking
environment cannot establish that binding, report unknown rather than verified
distribution provenance.

Use a maintained verifier for the attestation format, trust roots, signature,
certificate identity, transparency material, and subject digest. Define the
publisher/repository/workflow acceptance rules separately and retain enough
artifact and verifier identity for audit. Core does not infer those checks from
an HTTPS response or an attestation's presence.

## Exact evidence mapping for an integration

The following is a recommended provider mapping. Only
`distribution.provenance` has built-in dependency shorthand; the other kinds are
extension conventions that a generic requirement or custom validator can consume.

| Collected result | Evidence kind | Status/result |
| --- | --- | --- |
| A provenance object exists for a matched artifact | `pypi.attestation.available` | `observed`, true; does not satisfy provenance policy. |
| Exact artifact verification and installed-artifact binding both succeeded | `distribution.provenance` | `verified`, true; subject is the canonical distribution name. |
| Publisher/repository/workflow claims authenticated by that verification | `pypi.publisher.identity`, `pypi.repository.identity`, `pypi.workflow.identity` | `verified` only for the specific established claim. |
| Artifact identity is incomplete or binding to the installation is ambiguous | `distribution.provenance` | `unknown`, null. |
| Verification established an invalid signature, digest, or disallowed identity | `distribution.provenance` | false result; must not satisfy the requirement. |
| Collector/verifier cannot run or its network access is disabled | `provider.availability` or relevant fact | `unavailable`, null. |

Every distribution subject must be normalized consistently with the resolver.
The provider receives the observed distribution name/version/origin; it is
responsible for matching fresh evidence to that exact installation. Core's
shorthand matches kind, subject, status, and truthiness, and does not independently
validate artifact digests or reinterpret a third-party verifier's result.

Use `observed: true` only for the success predicate actually established.
A nonempty JSON object such as `{"verified": false}` is truthy and is unsuitable
as the success value. Store detailed audit data as separate evidence and let a
custom policy validator evaluate structured identity fields.

An offline adapter for a cached external verification result would still need
authenticated input, exact artifact binding, freshness, and verifier trust rules.
Core does not ship a generic JSON-to-verified adapter because reading a
`verified: true` flag would not establish any of those properties.

## Other ecosystems

| Ecosystem | Appropriate provider responsibility |
| --- | --- |
| OSV / pip-audit | Match assessment results to exact versions and retain advisory IDs and assessment freshness. |
| Sigstore | Verify artifact identity and signer claims through its maintained implementation. |
| SLSA / in-toto | Validate provenance statements and expose the specific authenticated build claims. |
| CycloneDX / SPDX | Consume existing inventory documents and preserve uncertain package matches. |
| GitHub | Collect explicitly requested immutable repository/workflow facts; metadata alone is not provenance. |

These are extension opportunities, not integrations bundled in 0.5. The
[community roadmap](community-roadmap.md#pypi-attestation-provider) includes an
attestation-provider contribution brief with artifact binding, malformed-response,
timeout, unavailable-evidence, and cache/freshness acceptance criteria.
See the [tested offline extension example](extensions.md) to implement the protocol.

## Trust and execution

A verified publisher identity does not prove that code is harmless. A clean
vulnerability result does not prove absence of unknown vulnerabilities. Static
admission evaluates the selected source and observed import inventory; it does
not recursively inspect every installed package or sandbox later execution.

Providers and metadata finders already installed in the host are trusted Python
code. Select providers explicitly, grant network access deliberately, and keep
credentials out of evidence and reports. See [security boundaries](security-model.md).
