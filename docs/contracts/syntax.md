# Contract syntax

An admission contract is a YAML mapping validated as `AdmissionPolicy`. It extends
the existing `SpyModel` structural fields with host runtime, dependency, and
evidence policy. `importspy check plugin.py` uses `plugin.importspy.yml` when it
exists; pass `--contract policy.yml` to select another file.

Unknown fields, unsupported schema versions, duplicate YAML keys, and Python
object tags are rejected. Annotation text is never evaluated as Python.

## Identity and structure

```yaml
schema_version: 1
policy_id: payments-plugin
filename: plugin.py
version: "1.2.3"
variables:
  - name: MODE
    annotation: str
    value: production
functions:
  - name: process
    arguments:
      - name: amount
        annotation: int
      - name: currency
        value: EUR
    return_annotation: str
classes:
  - name: Plugin
    attributes:
      - name: kind
        type: class
        value: payments
    methods:
      - name: run
        arguments:
          - name: self
        return_annotation: str
    superclasses:
      - name: BasePlugin
```

| Field | Meaning |
| --- | --- |
| `schema_version` | Contract schema, currently `1`; defaults to `1`. |
| `policy_id` | Optional policy identity recorded in decisions. |
| `filename` | Expected source basename, such as `plugin.py`. |
| `version` | Expected module `__version__` literal; unrelated to schema version. |
| `variables` | Required module declarations, with optional annotation and scalar value. |
| `functions` | Required function names, parameter names, annotations, and represented defaults. |
| `classes` | Required classes, class attributes, methods, and lexical base references. |

All variable, argument, function, class, and attribute entries require `name`.
Attributes also require `type: class` or `type: instance`. Superclasses are
mappings with a `name`, not bare strings.

These are requirement lists: extra declarations and parameters are allowed.
Parameter kinds are recorded by inspection, but this schema does not express
full signature equivalence or calling convention constraints. Annotations are
compared as text, including strings such as `list[User] | None`; ImportSpy does
not perform type checking or resolve annotation identities.

Supported contract values are strings, integers, floats, booleans, and `null`.
Omitting a variable's `value` imposes no value constraint; setting it to `null`
requires a known `None` value. Collection or computed values are not evaluated.
Class instance attributes and inherited implementations require runtime facts;
requesting them during static admission produces an unknown-fact denial.

A base requirement matches its written reference or final dotted name; it does
not prove runtime inheritance identity. Decorators, conditional declarations,
and explicit dynamic namespace operations can also make structure unknown.
See [static preflight](../static-preflight.md) for the complete boundary.

## Host runtime

Host constraints do not execute the target:

```yaml
runtime:
  python: ">=3.10,<4"
  os: [linux, darwin]
  architecture: [x86_64, arm64, aarch64]
  implementation: [CPython]
  environment:
    APP_MODE: production
    SERVICE_TOKEN: null
```

`python` is a PEP 440 version range. The list fields accept exact host identifiers;
empty lists impose no restriction. `os` comes from lowercase `platform.system()`,
architecture from lowercase `platform.machine()`, and implementation from
`platform.python_implementation()`.

Environment values are strings: `APP_MODE` must equal `production`. A `null`
requirement checks presence only. Reports record whether the requirement passed,
not the environment value. Do not place secret literal values in policy files;
use presence checks or a trusted external validation mechanism.

## Dependencies and origins

```yaml
dependencies:
  requests:
    allowed: true
    required: true
    version: ">=2.32,<3"
    declared: true
  legacy-package:
    allowed: false
  internal-payment-sdk:
    origin:
      type: vcs
      repository: https://github.com/acme/payment-sdk
      commit: "0123456789abcdef"
    editable: false
  import:pickle:
    allowed: false
dependency_options:
  unresolved: deny
  undeclared: allow
  unlisted: allow
```

Distribution keys are normalized package names. `import:<name>` explicitly
addresses a top-level import, including a stdlib import. Multiple namespace
contributors are evaluated individually. An import allow rule does not replace
a required distribution entry when `unlisted: deny` is enabled.

`allowed` defaults to true. `required` means observed in the source inventory,
not merely installed. `declared` compares observed dependencies with supported
project metadata. An allowed dependency is not automatically required.

The options shown above are defaults. They control unresolved imports,
undeclared or unknown declarations, and external distributions missing a policy
entry. Optional/conditional imports are still evaluated.

Origin fields include `type`, `url`, `repository`, and `commit`; `editable` is a
separate dependency constraint. Missing metadata stays unknown. Credentials,
queries, and fragments are removed from compared/reported origin URLs. These
facts are metadata observations, not cryptographic provenance. See the
[dependency reference](../dependencies.md) for resolution and declaration limits.

## Evidence requirements

```yaml
evidence_requirements:
  - kind: distribution.provenance
    subject: cryptography
    provider: trusted-verifier
    status: verified
```

Each requirement names an evidence `kind` and `subject`. Optional `provider`
restricts the provider identity; `status` accepts `verified` (the default) or
`observed`. The evidence must have a truthy observation. A verified observation
also satisfies an `observed` requirement; unknown or unavailable evidence does
not.

For an observed dependency, `provenance: true` or
`provenance: {required: true}` is shorthand for required verified
`distribution.provenance` evidence. It does not make an absent dependency
required. No built-in cryptographic verifier is implied; select an appropriate
trusted [evidence provider](../extensions.md).

## Legacy deployment alternatives

Existing `deployments` remain supported alongside the newer `runtime` section:

```yaml
deployments:
  - arch: x86_64
    systems:
      - os: linux
        environment:
          secrets: [SERVICE_TOKEN]
        pythons:
          - interpreter: CPython
            modules:
              - filename: plugin.py
```

`arch`, `systems`, `os`, `pythons`, and each Python entry's `modules` are required
at their respective levels. A Python entry may also specify an exact, quoted
version, such as `"3.12.9"`. Nested module constraints apply to the inspected
subject; they do not instruct ImportSpy to import additional modules.

Admission requires one matching legacy deployment/system/Python alternative.
Top-level structure and the newer `runtime` requirements also apply. Prefer
`runtime.python` for a range instead of encoding a partial version as an exact
legacy version. Read [migration](../migration-0.5.md) before updating a 0.4 file.
