# Static preflight

`SourceInspector.inspect(path)` reads and hashes Python source, parses its AST,
and compiles the tree to check syntax and scope rules. It never executes that
code, imports the target, imports its dependencies, or evaluates expressions.
The exact inspected bytes remain available to the explicit execution boundary.

The inspector records imports, functions, parameter names and kinds, annotations,
literal defaults, classes, base references, class attributes, module variables,
and a literal `__version__`. Every import statement is recorded, including
imports inside functions, optional branches, and exception handlers. References
inside conditional control flow or function bodies are marked optional; this
records uncertainty and does not authorize that dependency.

`evaluate_structure(contract, inspection)` is a pure comparison against the
existing module contract fields. It returns structured violations together,
without changing the source facts or importing anything. Checks use names and
exact represented values/annotations. Unspecified values impose no value
constraint; an explicit YAML `null` requires a known `None` value.
For function parameters, an explicit value also requires a default to exist:
`value: null` matches `def run(value=None)`, but not `def run(value)`. Parameter
and class-attribute annotation requirements match written annotations; a literal
default or attribute value does not supply a missing annotation. Module-variable
annotation requirements retain compatibility with type inference from a known
scalar literal when no annotation is written.

Evidence marked `verified` in the static phase verifies a source declaration.
It does not claim that arbitrary execution will leave an equivalent runtime
object. Decorated definitions, conditional definitions, dynamic namespace
operations, computed values, instance attributes, and inherited implementations
can require runtime verification. A structural requirement depending on those
facts fails closed with `ISPY-S103`. Missing declarations use `ISPY-S101`,
mismatches use `ISPY-S102`, and invalid or unreadable source uses `ISPY-S001`.

Decorated functions are always uncertain, including decorators that happen to
be harmless in a particular runtime. Metaclasses and class decorators are also
uncertain. Base class references can be matched as written, but resolving the
base object's inherited implementation requires runtime evidence. The inspector
does not invoke decorators, metaclasses, annotation expressions, or defaults.
Explicit namespace mutation in definition expressions, class suites, and
control-flow headers is tracked conservatively. This includes calls such as
`globals()` in a default expression and module bindings declared `global` inside
a class. Calls buried in unexecuted function bodies are not treated as observed
definition-time effects.

Static inspection is not a sandbox or a full interpreter. It does not establish
that a module is safe to execute, predict arbitrary mutations performed by
called code, discover every dynamic `__import__`/`importlib` target, recursively
inspect dependency code, or verify runtime identities. Python imports may execute
dependency code when execution is explicitly requested after admission. AST
parsing also consumes local resources; hostile, excessively large input requires
resource isolation outside this library.

`starter_contract(inspection)` generates editable filename, function, class, and
method requirements. It retains uncertain declarations as requirements so an
unknown decorated declaration is not silently approved. Generation cannot infer
which dependencies should be trusted or which policy is appropriate for a project.

Tests in `tests/admission/test_inspection.py` include source attempting terminal
output, file writes, environment changes, subprocess execution, and socket
connections. Inspection and a denying structural evaluation trigger none of
those effects. Tests also cover compiler-invalid scope syntax, encoding,
conditional imports, decorators, dynamic defaults, inheritance, and exact source
hashes.
