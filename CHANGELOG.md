# Changelog

## 0.5.0 — release candidate

ImportSpy becomes a policy-as-code admission engine for Python modules and
observed dependencies. The open-source engine works offline and needs no account.

- Inspect Python source through AST without importing or executing the target.
  Unknown structural facts fail closed; explicit `load` freshly admits and
  executes the exact inspected bytes, then runs optional runtime validators.
- Resolve stdlib, project, external, namespace, direct/VCS/local and unresolved
  imports from source paths and installed metadata. Enforce distribution and
  import allow/deny rules, required imports, PEP 440 versions, declarations,
  origins and editable-install requirements.
- Collect separate source, host, dependency and provider evidence. Structured
  decisions carry identities/hashes, phases, timestamps and stable violations.
  Provenance requirements need real verified evidence from a selected provider;
  metadata alone does not satisfy them.
- Add `init`, `check`, explicit project subjects and human/JSON/SARIF output with
  stable exit semantics. Add public provider, validator and reporter protocols,
  explicit entry-point selection, and network opt-in.
- Remove repeated module execution from legacy runtime introspection. Deprecate
  `Spy.importspy` for removal in 1.0; reject unknown contract fields; accept
  annotation strings; use safe YAML and redact environment diagnostics.
- Restore lint/type gates, expand tests and supported-Python CI, exercise installed
  artifacts, update documentation/examples, and provide contributor/security and
  integration-roadmap guidance.
- Use one package version source and modern package metadata. Move documentation
  dependencies out of runtime dependencies; update PyMdown Extensions for its
  published security fixes. Public contact: info@atellaluca.com.

See [migration guidance](docs/migration-0.5.md) for compatibility details and
[release engineering](docs/release.md) for the remaining publication procedure.
OSV, Sigstore, CycloneDX, SPDX, GitHub evidence and cryptographic PyPI attestation
verification are extension roadmap work, not bundled verifiers in this release.

## 0.4.x

The preceding runtime-contract architecture remains documented through the
migration guide and Git history. Its runtime compatibility API is retained in
0.5 without the former repeated reloads.
