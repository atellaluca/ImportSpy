"""Inspect Python declarations without importing, evaluating, or executing source.

Facts describe source declarations, not guarantees about the resulting runtime
objects. Unknown facts remain explicit and cannot satisfy structural requirements.
"""

from __future__ import annotations

import ast
import hashlib
import io
import tokenize
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .domain import Evidence, ImportReference, Location, Violation
from .models import Class, Function, Module, Variable


@dataclass
class VariableFact:
    name: str
    line: int
    annotation: str | None = None
    value: Any = None
    value_known: bool = False
    certain: bool = True


@dataclass
class ArgumentFact(VariableFact):
    kind: str = "positional_or_keyword"
    has_default: bool = False


@dataclass
class FunctionFact:
    name: str
    line: int
    arguments: dict[str, ArgumentFact] = field(default_factory=dict)
    return_annotation: str | None = None
    certain: bool = True
    asynchronous: bool = False


@dataclass
class ClassFact:
    name: str
    line: int
    variables: dict[str, VariableFact] = field(default_factory=dict)
    functions: dict[str, FunctionFact] = field(default_factory=dict)
    classes: dict[str, ClassFact] = field(default_factory=dict)
    bases: list[str] = field(default_factory=list)
    certain: bool = True
    dynamic_namespace: bool = False
    uncertain_names: set[str] = field(default_factory=set)


@dataclass
class SourceInspection:
    path: Path
    source_hash: str | None = None
    source_bytes: bytes = b""
    imports: list[ImportReference] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    violations: list[Violation] = field(default_factory=list)
    variables: dict[str, VariableFact] = field(default_factory=dict)
    functions: dict[str, FunctionFact] = field(default_factory=dict)
    classes: dict[str, ClassFact] = field(default_factory=dict)
    dynamic_namespace: bool = False
    uncertain_names: set[str] = field(default_factory=set)


Scope = SourceInspection | ClassFact


def _annotation(node: ast.expr | None) -> str | None:
    if node is None:
        return None
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return ast.unparse(node)


def _literal(node: ast.expr | None) -> tuple[bool, Any]:
    if node is None:
        return False, None
    try:
        value = ast.literal_eval(node)
    except (ValueError, TypeError, SyntaxError, RecursionError, MemoryError):
        return False, None
    # The existing structural DSL only represents scalar values. Containers,
    # bytes, complex values and arbitrary objects remain unknown to that DSL.
    if value is None or type(value) in (str, bool, int, float):
        return True, value
    return False, None


def _function(
    node: ast.FunctionDef | ast.AsyncFunctionDef, certain: bool
) -> FunctionFact:
    result = FunctionFact(
        node.name,
        node.lineno,
        return_annotation=_annotation(node.returns),
        certain=certain and not node.decorator_list,
        asynchronous=isinstance(node, ast.AsyncFunctionDef),
    )
    positional = [*node.args.posonlyargs, *node.args.args]
    defaults: list[ast.expr | None] = [None] * (
        len(positional) - len(node.args.defaults)
    )
    defaults.extend(node.args.defaults)
    parameters = [
        (
            arg,
            default,
            "positional_only"
            if index < len(node.args.posonlyargs)
            else "positional_or_keyword",
        )
        for index, (arg, default) in enumerate(zip(positional, defaults))
    ]
    if node.args.vararg:
        parameters.append((node.args.vararg, None, "var_positional"))
    parameters.extend(
        (arg, default, "keyword_only")
        for arg, default in zip(node.args.kwonlyargs, node.args.kw_defaults)
    )
    if node.args.kwarg:
        parameters.append((node.args.kwarg, None, "var_keyword"))
    for arg, default, kind in parameters:
        known, value = _literal(default)
        result.arguments[arg.arg] = ArgumentFact(
            name=arg.arg,
            line=arg.lineno,
            annotation=_annotation(arg.annotation),
            value=value,
            value_known=known or default is None,
            certain=result.certain,
            kind=kind,
            has_default=default is not None,
        )
    return result


def _bound_names(node: ast.AST) -> set[str]:
    return {
        child.id
        for child in ast.walk(node)
        if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Store)
    }


def _replace(scope: Scope, name: str, certain: bool) -> None:
    scope.variables.pop(name, None)
    scope.functions.pop(name, None)
    scope.classes.pop(name, None)
    if certain:
        scope.uncertain_names.discard(name)
    else:
        scope.uncertain_names.add(name)


def _expression_effects(
    node: ast.AST, scope: Scope, module_scope: SourceInspection
) -> None:
    """Track explicit namespace mutation without evaluating an expression."""
    for child in ast.walk(node):
        if isinstance(child, ast.NamedExpr):
            for name in _bound_names(child.target):
                _replace(scope, name, False)
        if isinstance(child, ast.Call):
            call = ast.unparse(child.func)
            if call in {
                "exec",
                "eval",
                "globals",
                "locals",
                "vars",
                "setattr",
                "delattr",
            }:
                scope.dynamic_namespace = True
                # Class bodies and method-definition expressions can mutate
                # module globals too. We cannot resolve exec/eval payloads.
                module_scope.dynamic_namespace = True


def _statement_expression_effects(
    node: ast.AST, scope: Scope, module_scope: SourceInspection
) -> None:
    """Inspect statement headers, including AST wrappers, without body traversal.

    Arguments/defaults, keywords, with-items, exception types and match guards
    use wrapper nodes rather than direct expression children. Nested statements
    are handled by scope traversal; function bodies are never visited here.
    """
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.stmt):
            continue
        if isinstance(child, ast.expr):
            _expression_effects(child, scope, module_scope)
        else:
            _statement_expression_effects(child, scope, module_scope)


def _scan_scope(
    statements: list[ast.stmt],
    scope: Scope,
    module_scope: SourceInspection,
    certain: bool = True,
) -> None:
    for statement in statements:
        if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
            _replace(scope, statement.name, certain)
            scope.functions[statement.name] = _function(statement, certain)
        elif isinstance(statement, ast.ClassDef):
            _replace(scope, statement.name, certain)
            class_fact = ClassFact(
                statement.name,
                statement.lineno,
                bases=[ast.unparse(base) for base in statement.bases],
                certain=certain
                and not statement.decorator_list
                and not statement.keywords,
            )
            _scan_scope(statement.body, class_fact, module_scope)
            scope.classes[statement.name] = class_fact
        elif isinstance(statement, ast.Global) and isinstance(scope, ClassFact):
            # A class suite executes during definition. A global declaration
            # routes its bindings to the module, not the class namespace.
            scope.dynamic_namespace = True
            for name in statement.names:
                _replace(module_scope, name, False)
        elif isinstance(statement, (ast.Assign, ast.AnnAssign)):
            targets = (
                statement.targets
                if isinstance(statement, ast.Assign)
                else [statement.target]
            )
            for target in targets:
                names = _bound_names(target)
                for name in names:
                    _replace(scope, name, certain)
                    known, value = _literal(statement.value)
                    scope.variables[name] = VariableFact(
                        name,
                        statement.lineno,
                        _annotation(statement.annotation)
                        if isinstance(statement, ast.AnnAssign)
                        else None,
                        value,
                        known and isinstance(target, ast.Name),
                        certain and statement.value is not None,
                    )
                if not names and not isinstance(target, ast.Name):
                    scope.dynamic_namespace = True
        elif isinstance(statement, (ast.Import, ast.ImportFrom)):
            for alias in statement.names:
                if alias.name == "*":
                    scope.dynamic_namespace = True
                else:
                    name = alias.asname or (
                        alias.name.split(".")[0]
                        if isinstance(statement, ast.Import)
                        else alias.name
                    )
                    _replace(scope, name, False)
        elif isinstance(statement, (ast.AugAssign, ast.Delete)):
            targets = (
                [statement.target]
                if isinstance(statement, ast.AugAssign)
                else statement.targets
            )
            for target in targets:
                names = {
                    child.id
                    for child in ast.walk(target)
                    if isinstance(child, ast.Name)
                }
                for name in names:
                    _replace(scope, name, False)
        else:
            # Definitions in any control-flow block are conditional. We do not
            # evaluate conditions, even apparently constant ones.
            for _, value in ast.iter_fields(statement):
                if isinstance(value, list):
                    _scan_scope(
                        [child for child in value if isinstance(child, ast.stmt)],
                        scope,
                        module_scope,
                        False,
                    )
                    for child in value:
                        if isinstance(child, (ast.ExceptHandler, ast.match_case)):
                            _scan_scope(child.body, scope, module_scope, False)
                            if isinstance(child, ast.ExceptHandler) and child.name:
                                _replace(scope, child.name, False)
                            if isinstance(child, ast.match_case):
                                for capture in ast.walk(child.pattern):
                                    if (
                                        isinstance(
                                            capture, (ast.MatchAs, ast.MatchStar)
                                        )
                                        and capture.name
                                    ):
                                        _replace(scope, capture.name, False)
            if isinstance(statement, (ast.For, ast.AsyncFor)):
                for name in _bound_names(statement.target):
                    _replace(scope, name, False)
            if isinstance(statement, (ast.With, ast.AsyncWith)):
                for item in statement.items:
                    if item.optional_vars:
                        for name in _bound_names(item.optional_vars):
                            _replace(scope, name, False)
        # Include defaults/decorators/annotations/bases: these can be evaluated
        # while a definition is created. Deferred annotation semantics vary by
        # Python version, so potentially dynamic annotations stay conservative.
        _statement_expression_effects(statement, scope, module_scope)


class _ImportVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.references: list[ImportReference] = []
        self.optional = False

    def visit_Import(self, node: ast.Import) -> None:
        self.references.extend(
            ImportReference(
                name=alias.name,
                line=node.lineno,
                column=node.col_offset + 1,
                optional=self.optional,
            )
            for alias in node.names
        )

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        names = [node.module] if node.module else [alias.name for alias in node.names]
        self.references.extend(
            ImportReference(
                name=name,
                line=node.lineno,
                column=node.col_offset + 1,
                level=node.level,
                optional=self.optional,
            )
            for name in names
        )

    def generic_visit(self, node: ast.AST) -> None:
        previous = self.optional
        if (
            isinstance(
                node,
                (
                    ast.If,
                    ast.Try,
                    ast.For,
                    ast.AsyncFor,
                    ast.While,
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                    ast.Match,
                ),
            )
            or type(node).__name__ == "TryStar"
        ):
            self.optional = True
        super().generic_visit(node)
        self.optional = previous


class SourceInspector:
    """Collect AST facts from a file without executing it or its dependencies."""

    def inspect(self, path: Path) -> SourceInspection:
        path = Path(path)
        result = SourceInspection(path)
        try:
            raw = path.read_bytes()
            result.source_bytes = raw
            result.source_hash = hashlib.sha256(raw).hexdigest()
            encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
            source = raw.decode(encoding)
            tree = ast.parse(source, filename=str(path))
            # AST parsing alone accepts some invalid contexts (e.g. a top-level
            # return). Compilation checks them without executing any code.
            compile(tree, str(path), "exec")
        except (
            OSError,
            UnicodeError,
            SyntaxError,
            ValueError,
            RecursionError,
        ) as error:
            result.violations.append(
                Violation(
                    code="ISPY-S001",
                    category="source",
                    subject=str(path),
                    message=f"Source could not be parsed: {error}",
                    location=Location(
                        path=str(path),
                        line=getattr(error, "lineno", None),
                        column=getattr(error, "offset", None),
                    ),
                    remediation="Provide a readable Python source file with valid syntax and encoding.",
                )
            )
            return result
        visitor = _ImportVisitor()
        visitor.visit(tree)
        result.imports = visitor.references
        _scan_scope(tree.body, result, result)
        result.evidence.append(
            Evidence(
                kind="source.syntax",
                subject=str(path),
                observed="valid",
                status="verified",
            )
        )
        for kind, facts in (
            ("function", result.functions),
            ("class", result.classes),
            ("variable", result.variables),
        ):
            for name, fact in facts.items():
                known = fact.certain and not result.dynamic_namespace
                result.evidence.append(
                    Evidence(
                        kind=f"module.{kind}.present",
                        subject=name,
                        observed=True,
                        status="verified" if known else "unknown",
                        detail="Unconditional source declaration."
                        if known
                        else "Runtime structure requires verification.",
                    )
                )
        for reference in result.imports:
            result.evidence.append(
                Evidence(
                    kind="module.import",
                    subject=reference.name,
                    observed=reference.model_dump(mode="json"),
                    status="observed",
                )
            )
        if result.dynamic_namespace:
            result.evidence.append(
                Evidence(
                    kind="module.namespace",
                    subject=str(path),
                    status="unknown",
                    detail="Dynamic namespace operations cannot be resolved statically.",
                )
            )
        return result


def evaluate_structure(
    expected: Module, inspection: SourceInspection
) -> list[Violation]:
    """Compare contract requirements to static facts; unknowns fail closed.

    Inspection failures are available separately in ``inspection.violations``.
    This function does not mutate inspection evidence or perform any I/O.
    """
    violations: list[Violation] = []
    if inspection.violations:
        return violations

    def issue(
        code: str,
        subject: str,
        message: str,
        line: int | None = None,
        expected_value: Any = None,
        observed: Any = None,
    ) -> None:
        violations.append(
            Violation(
                code=code,
                category="structure",
                subject=subject,
                message=message,
                location=Location(path=str(inspection.path), line=line),
                expected=expected_value,
                observed=observed,
                remediation="Use a statically inspectable declaration or review the requirement for explicit runtime validation."
                if code == "ISPY-S103"
                else "Update the source or structural contract to match the required interface.",
            )
        )

    def unknown(name: str, line: int | None = None) -> None:
        issue(
            "ISPY-S103",
            name,
            f"Structural requirement for `{name}` is unknown and requires runtime verification.",
            line,
        )

    def lookup(scope: Scope, mapping: dict[str, Any], name: str) -> Any:
        fact = mapping.get(name)
        unresolved_binding = (
            fact is None
            and name in scope.variables
            and not scope.variables[name].value_known
        )
        if (
            scope.dynamic_namespace
            or name in scope.uncertain_names
            or unresolved_binding
            or (fact is not None and not fact.certain)
        ):
            unknown(name, fact.line if fact else None)
            return None
        if fact is None:
            issue("ISPY-S101", name, f"Required declaration `{name}` is missing.")
        return fact

    def variable(
        requirement: Variable, fact: VariableFact, *, infer_annotation: bool = False
    ) -> None:
        if requirement.annotation:
            annotation = fact.annotation
            if (
                infer_annotation
                and annotation is None
                and fact.value_known
                and fact.value is not None
            ):
                annotation = type(fact.value).__name__
            if annotation is None and infer_annotation:
                unknown(requirement.name, fact.line)
            elif annotation != requirement.annotation:
                issue(
                    "ISPY-S102",
                    requirement.name,
                    f"Annotation for `{requirement.name}` does not match.",
                    fact.line,
                    requirement.annotation,
                    annotation,
                )
        if "value" in requirement.model_fields_set:
            if isinstance(fact, ArgumentFact) and not fact.has_default:
                issue(
                    "ISPY-S102",
                    requirement.name,
                    f"Required default for parameter `{requirement.name}` is missing.",
                    fact.line,
                    requirement.value,
                    "no default",
                )
            elif not fact.value_known:
                unknown(requirement.name, fact.line)
            elif fact.value != requirement.value:
                issue(
                    "ISPY-S102",
                    requirement.name,
                    f"Value for `{requirement.name}` does not match.",
                    fact.line,
                    requirement.value,
                    fact.value,
                )

    def function(requirement: Function, fact: FunctionFact) -> None:
        for argument in requirement.arguments or []:
            observed = fact.arguments.get(argument.name)
            if observed is None:
                issue(
                    "ISPY-S101",
                    argument.name,
                    f"Required parameter `{argument.name}` is missing from `{requirement.name}`.",
                    fact.line,
                )
            else:
                variable(argument, observed)
        if requirement.return_annotation:
            if fact.return_annotation is None:
                issue(
                    "ISPY-S102",
                    requirement.name,
                    f"Return annotation for `{requirement.name}` is missing.",
                    fact.line,
                    requirement.return_annotation,
                )
            elif requirement.return_annotation != fact.return_annotation:
                issue(
                    "ISPY-S102",
                    requirement.name,
                    f"Return annotation for `{requirement.name}` does not match.",
                    fact.line,
                    requirement.return_annotation,
                    fact.return_annotation,
                )

    def class_requirements(requirement: Class, fact: ClassFact) -> None:
        for attribute in requirement.attributes or []:
            if attribute.type == "instance":
                unknown(f"{requirement.name}.{attribute.name}", fact.line)
            else:
                observed = lookup(fact, fact.variables, attribute.name)
                if observed is not None:
                    variable(attribute, observed)
        for method in requirement.methods or []:
            if method.name not in fact.functions and fact.bases:
                unknown(f"{requirement.name}.{method.name}", fact.line)
                continue
            observed_function = lookup(fact, fact.functions, method.name)
            if observed_function is not None:
                function(method, observed_function)
        for base in requirement.superclasses or []:
            matching = next(
                (
                    name
                    for name in fact.bases
                    if name == base.name or name.rsplit(".", 1)[-1] == base.name
                ),
                None,
            )
            if matching is None:
                issue(
                    "ISPY-S101",
                    base.name,
                    f"Required base reference `{base.name}` is missing from `{requirement.name}`.",
                    fact.line,
                )
            elif base.attributes or base.methods or base.superclasses:
                unknown(base.name, fact.line)

    if expected.filename and expected.filename != inspection.path.name:
        issue(
            "ISPY-S102",
            str(inspection.path),
            "Source filename does not match the contract.",
            expected_value=expected.filename,
            observed=inspection.path.name,
        )
    if expected.version:
        version = lookup(inspection, inspection.variables, "__version__")
        if version is not None:
            if not version.value_known:
                unknown("__version__", version.line)
            elif version.value != expected.version:
                issue(
                    "ISPY-S102",
                    "__version__",
                    "Module version does not match the contract.",
                    version.line,
                    expected.version,
                    version.value,
                )
    for requirement in expected.variables or []:
        fact = lookup(inspection, inspection.variables, requirement.name)
        if fact is not None:
            variable(requirement, fact, infer_annotation=True)
    for required_function in expected.functions or []:
        function_fact = lookup(inspection, inspection.functions, required_function.name)
        if function_fact is not None:
            function(required_function, function_fact)
    for required_class in expected.classes or []:
        class_fact = lookup(inspection, inspection.classes, required_class.name)
        if class_fact is not None:
            class_requirements(required_class, class_fact)
    return violations


def starter_contract(inspection: SourceInspection) -> dict[str, Any]:
    """Generate an editable structural contract; never turn unknowns into approvals.

    Only names are generated for signatures because the legacy annotation/value
    DSL cannot represent every Python signature. Decorated and conditional
    declarations remain requirements and therefore fail closed until reviewed.
    """
    result: dict[str, Any] = {"filename": inspection.path.name}
    if inspection.functions:
        result["functions"] = [{"name": name} for name in inspection.functions]
    if inspection.classes:
        result["classes"] = [
            {
                "name": name,
                **(
                    {"methods": [{"name": method} for method in fact.functions]}
                    if fact.functions
                    else {}
                ),
            }
            for name, fact in inspection.classes.items()
        ]
    return result
