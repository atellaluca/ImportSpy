# Security model and limits

ImportSpy decides whether inspected source and available evidence satisfy a
policy. ADMIT is a policy result, not proof that arbitrary Python behavior is
safe. The engine is not a sandbox, vulnerability scanner, package manager, or
cryptographic verifier bundled under another name.

## The no-execution boundary

`SourceInspector` reads and hashes source, parses its AST, and compiles the tree
to validate syntax and scope rules. It does not execute the compiled code.
`AdmissionEngine.check`, CLI `check`, and `init` do not import the target or its
observed dependencies, whether admission succeeds or fails.

Static evidence verifies lexical facts: a declaration, annotation text, literal
value, or import reference in the inspected source. It does not establish the
behavior or identity of every resulting runtime object. Decorators, metaclasses,
conditional declarations, dynamic namespace operations, and computed values can
leave required facts unknown. Those structural requirements fail closed with
`ISPY-S103`; the engine does not execute code to resolve the uncertainty.

Tests cover source attempting output, filesystem writes, environment mutation,
subprocess execution, and socket operations. They also cover explicit execution
using the inspected snapshot. See [static preflight](static-preflight.md) and
the repository's `tests/admission` suite.

## Explicit execution

`AdmissionEngine.load` performs fresh admission with refreshed dependency
metadata, then executes the captured source bytes. It does not trust a previously
returned decision as permission to execute a changed file. It rejects a module
name already registered in `sys.modules`.

Once execution begins, target code and ordinary Python imports can cause side
effects. Optional runtime validators run after module initialization; a denial
then cannot undo those effects. Removing a failed module's registration is not
rollback. The loader does not freeze installed packages, import hooks, files,
network services, or the surrounding process between inspection and execution.

Admission inventories imports in the selected source; it does not recursively
validate every transitive dependency, intercept all dynamic imports, or guarantee
that execution follows the resolver's classification under arbitrary custom
import behavior. Configure the normal runtime import environment appropriately.
Use independent process/container isolation when the application requires it.

`Spy.importspy` and `SpyModel.from_module` are legacy runtime introspection of
already executed modules. Dynamic attributes can execute Python during that
inspection. Embedding them inside a module cannot prevent earlier top-level
side effects. See [migration](migration-0.5.md).

## Dependency metadata and provenance

Import/distribution mapping, installed versions, declaration metadata, and
PEP 610 origins are local observations. Namespace mappings can have several
contributors; unresolved imports remain explicit and default to denial.
Neither metadata presence nor an origin URL establishes artifact integrity.
Missing direct-URL metadata does not prove installation from PyPI.

Installed metadata can be stale or altered, and custom metadata finders already
present in the host are trusted host code. Resolver caches represent an engine's
metadata snapshot. Create a new engine after changing installations for
independent `check` requests; `load` refreshes its resolver state.

A provenance requirement needs a selected trusted provider to verify the exact
artifact and identity required by policy. An attestation being available is
different from a verified attestation, and verified provenance does not prove
absence of malicious behavior or vulnerabilities. ImportSpy does not manufacture
cryptographic verification from package metadata. Read [supply-chain evidence](supply-chain.md).

## Trusted extensions and network access

Providers, custom policy validators, runtime validators, and reporters execute
trusted Python code selected by the application. Entry-point loading imports a
provider package and constructs its factory. The engine does not automatically
load every installed provider.

Core admission has no network requirement or telemetry. A provider declaring
`requires_network = True` is not collected unless network access is explicitly
allowed. This flag is a cooperation boundary, not a firewall: plugin import,
initialization, or incorrectly implemented plugins can perform their own I/O.
Choose and review extensions as executable dependencies.

Provider names must be unique in an engine, and the `importspy` prefix is
reserved for core facts. The engine assigns collected evidence to its configured
provider identity. This prevents accidental mixing of provider/core namespaces;
it does not protect against malicious trusted Python code running in the same
process. See [extensions](extensions.md).

## Contracts, paths, and resource limits

Contracts use safe YAML, reject unknown fields and duplicate keys, and do not
evaluate arbitrary Python expressions. Annotations are text comparisons.
Directory checking uses an explicit project subject/contract list instead of
recursively importing files.

The caller selects source, contract, and project paths. The library is not an
access-control layer over the filesystem. AST parsing, YAML loading, metadata
reading, and provider execution consume process resources; isolate and limit
hostile or excessively large inputs at the application's boundary.

## Reports and sensitive data

Core environment evidence contains presence/match outcomes rather than actual
or expected environment values. Legacy environment error messages redact values.
Reported origin URLs omit user information, query strings, and fragments;
provider failure details are withheld from decisions.

Reports can still contain subject paths, package identities, source constants,
contract identity, and explicitly supplied provider observations. URL path
segments can themselves contain sensitive identifiers. Providers and applications
must avoid putting credentials or sensitive payloads into those fields, and
review reports before publishing them.

The legacy runtime model retains environment values in memory for comparison;
do not serialize a full `SpyModel.from_module` snapshot as a public report.
Application exception causes and custom extension tracebacks also need review
before sharing; redaction of structured decisions does not sanitize arbitrary
application diagnostics.

Report vulnerabilities privately to **info@atellaluca.com**. See the repository's
[security reporting policy](https://github.com/atellaluca/ImportSpy/blob/main/SECURITY.md)
for the reporting process.
