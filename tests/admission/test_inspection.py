"""Static source inspection never executes source or dependency imports."""

import hashlib
import os
import socket
import subprocess
from pathlib import Path

import pytest

from importspy.inspection import SourceInspector, evaluate_structure, starter_contract
from importspy.models import Module


def inspect_source(tmp_path: Path, source: str):
    path = tmp_path / "plugin.py"
    path.write_text(source)
    return SourceInspector().inspect(path)


def test_static_admission_does_not_execute_side_effects(tmp_path, monkeypatch, capsys):
    marker = tmp_path / "executed"
    calls = []
    monkeypatch.delenv("IMPORTSPY_SIDE_EFFECT_TEST", raising=False)
    monkeypatch.setattr(
        subprocess, "run", lambda *args, **kwargs: calls.append("subprocess")
    )
    monkeypatch.setattr(
        socket, "socket", lambda *args, **kwargs: calls.append("socket")
    )
    source = (
        "import os, subprocess, socket\n"
        "print('TARGET EXECUTED')\n"
        f"open({str(marker)!r}, 'w').write('executed')\n"
        "os.environ['IMPORTSPY_SIDE_EFFECT_TEST'] = 'executed'\n"
        "subprocess.run(['echo', 'executed'])\n"
        "socket.socket().connect(('127.0.0.1', 1))\n"
    )
    inspection = inspect_source(tmp_path, source)
    violations = evaluate_structure(
        Module(functions=[{"name": "required_entrypoint"}]), inspection
    )
    assert violations
    assert not marker.exists()
    assert "IMPORTSPY_SIDE_EFFECT_TEST" not in os.environ
    assert calls == []
    assert capsys.readouterr().out == ""
    assert inspection.source_bytes == source.encode()
    assert inspection.source_hash == hashlib.sha256(source.encode()).hexdigest()


def test_importing_dependencies_is_never_attempted(tmp_path):
    inspection = inspect_source(tmp_path, "import nonexistent_importspy_fixture\n")
    assert not inspection.violations
    assert inspection.imports[0].name == "nonexistent_importspy_fixture"


@pytest.mark.parametrize(
    "source", ["def broken(:\n", "return 4\n", "break\n", "continue\n", "nonlocal x\n"]
)
def test_invalid_source_is_a_structured_violation(tmp_path, source):
    inspection = inspect_source(tmp_path, source)
    assert len(inspection.violations) == 1
    violation = inspection.violations[0]
    assert violation.code == "ISPY-S001"
    assert violation.location.path == str(tmp_path / "plugin.py")
    assert violation.location.line == 1


def test_unreadable_source_is_a_structured_violation(tmp_path):
    inspection = SourceInspector().inspect(tmp_path / "missing.py")
    assert inspection.violations[0].code == "ISPY-S001"


def test_python_source_encoding_is_respected(tmp_path):
    path = tmp_path / "plugin.py"
    path.write_bytes(b"# coding: latin-1\nlabel = 'caf\xe9'\n")
    inspection = SourceInspector().inspect(path)
    assert not inspection.violations
    assert inspection.variables["label"].value == "caf\xe9"


def test_functions_signatures_classes_and_safe_literals(tmp_path):
    inspection = inspect_source(
        tmp_path,
        """
__version__ = "1.2.0"
limit: int = 4
def process(first: str, /, count: int = 2, *items, enabled: bool = True, **options) -> str:
    return first
async def consume(event):
    pass
class Plugin(base.Plugin):
    kind: str = "static"
    def run(self, value: int) -> str:
        return str(value)
""",
    )
    assert not inspection.violations
    function = inspection.functions["process"]
    assert function.certain
    assert function.arguments["first"].kind == "positional_only"
    assert function.arguments["items"].kind == "var_positional"
    assert function.arguments["enabled"].kind == "keyword_only"
    assert function.arguments["options"].kind == "var_keyword"
    assert function.arguments["count"].value == 2
    assert function.arguments["count"].has_default
    assert inspection.functions["consume"].asynchronous
    assert inspection.classes["Plugin"].bases == ["base.Plugin"]
    expected = Module(
        filename="plugin.py",
        version="1.2.0",
        variables=[{"name": "limit", "annotation": "int", "value": 4}],
        functions=[
            {
                "name": "process",
                "arguments": [{"name": "count", "value": 2}],
                "return_annotation": "str",
            }
        ],
        classes=[
            {
                "name": "Plugin",
                "superclasses": [{"name": "Plugin"}],
                "attributes": [{"name": "kind", "type": "class", "value": "static"}],
                "methods": [{"name": "run", "return_annotation": "str"}],
            }
        ],
    )
    assert evaluate_structure(expected, inspection) == []


def test_import_references_include_conditional_nested_and_relative_imports(tmp_path):
    inspection = inspect_source(
        tmp_path,
        """
import os.path as p
from package.submodule import value
from . import sibling
from ..parent import value
if TYPE_CHECKING:
    import typing_only
try:
    import optional_package
except ImportError:
    pass
def run():
    import delayed
""",
    )
    references = {reference.name: reference for reference in inspection.imports}
    assert set(references) == {
        "os.path",
        "package.submodule",
        "sibling",
        "parent",
        "typing_only",
        "optional_package",
        "delayed",
    }
    assert references["sibling"].level == 1
    assert references["parent"].level == 2
    assert not references["os.path"].optional
    assert all(
        references[name].optional
        for name in ["typing_only", "optional_package", "delayed"]
    )


@pytest.mark.parametrize(
    "source",
    [
        "@decorator\ndef run(): pass\n",
        "if enabled:\n    def run(): pass\n",
        "run = factory()\n",
        "from other import run\n",
        "exec('def run(): pass')\n",
        "from other import *\n",
    ],
)
def test_dynamic_functions_are_not_statically_approved(tmp_path, source):
    inspection = inspect_source(tmp_path, source)
    violations = evaluate_structure(Module(functions=[{"name": "run"}]), inspection)
    assert violations
    assert violations[0].code in {"ISPY-S101", "ISPY-S103"}
    assert not any(
        e.kind == "module.function.present" and e.status == "verified"
        for e in inspection.evidence
    )


def test_decorated_function_evidence_is_unknown(tmp_path):
    inspection = inspect_source(
        tmp_path, "@changes_signature\ndef run(x: int) -> str: pass\n"
    )
    assert not inspection.functions["run"].certain
    assert inspection.evidence[1].status == "unknown"
    violations = evaluate_structure(
        Module(functions=[{"name": "run", "arguments": [{"name": "x"}]}]), inspection
    )
    assert [v.code for v in violations] == ["ISPY-S103"]


@pytest.mark.parametrize(
    "source",
    [
        "run = factory()\n",
        "result = exec('def run(): pass')\n",
        "def run(): pass\n(run := factory())\n",
        "def run(): pass\nfor run in values: pass\n",
        "run: object\n",
    ],
)
def test_dynamic_binding_operations_produce_unknowns(tmp_path, source):
    inspection = inspect_source(tmp_path, source)
    assert (
        evaluate_structure(Module(functions=[{"name": "run"}]), inspection)[0].code
        == "ISPY-S103"
    )


def test_value_expressions_and_default_expressions_are_unknown(tmp_path):
    inspection = inspect_source(
        tmp_path, "value = dangerous()\ndef run(option=dangerous()): pass\n"
    )
    assert not inspection.variables["value"].value_known
    assert not inspection.functions["run"].arguments["option"].value_known
    expected = Module(
        variables=[{"name": "value", "value": 1}],
        functions=[{"name": "run", "arguments": [{"name": "option", "value": None}]}],
    )
    assert [v.code for v in evaluate_structure(expected, inspection)] == [
        "ISPY-S103",
        "ISPY-S103",
    ]


def test_omitted_variable_value_is_not_an_expected_none(tmp_path):
    inspection = inspect_source(tmp_path, "value = 42\n")
    assert evaluate_structure(Module(variables=[{"name": "value"}]), inspection) == []
    assert (
        evaluate_structure(
            Module(variables=[{"name": "value", "value": None}]), inspection
        )[0].code
        == "ISPY-S102"
    )


def test_rebound_and_deleted_declarations_are_not_approved(tmp_path):
    inspection = inspect_source(tmp_path, "def run(): pass\nrun = 4\n")
    assert evaluate_structure(Module(functions=[{"name": "run"}]), inspection)
    inspection = inspect_source(tmp_path, "def run(): pass\ndel run\n")
    assert evaluate_structure(Module(functions=[{"name": "run"}]), inspection)


@pytest.mark.parametrize(
    "source",
    [
        "@decorator\nclass Plugin: pass\n",
        "class Plugin(metaclass=Meta): pass\n",
        "if enabled:\n    class Plugin: pass\n",
    ],
)
def test_dynamic_classes_require_runtime_verification(tmp_path, source):
    inspection = inspect_source(tmp_path, source)
    assert (
        evaluate_structure(Module(classes=[{"name": "Plugin"}]), inspection)[0].code
        == "ISPY-S103"
    )


def test_instance_and_inherited_attributes_require_runtime_verification(tmp_path):
    inspection = inspect_source(
        tmp_path,
        "class Plugin(Base):\n    def __init__(self):\n        self.value = 1\n",
    )
    expected = Module(
        classes=[
            {
                "name": "Plugin",
                "attributes": [{"name": "value", "type": "instance"}],
                "methods": [{"name": "inherited"}],
            }
        ]
    )
    assert [v.code for v in evaluate_structure(expected, inspection)] == [
        "ISPY-S103",
        "ISPY-S103",
    ]


def test_multiple_mismatches_are_returned_together(tmp_path):
    inspection = inspect_source(tmp_path, "value = 1\ndef run() -> int: pass\n")
    expected = Module(
        filename="different.py",
        variables=[{"name": "value", "value": 2}],
        functions=[{"name": "run", "return_annotation": "str"}],
    )
    assert len(evaluate_structure(expected, inspection)) == 3


def test_starter_contract_preserves_unknown_declaration_requirements(tmp_path):
    inspection = inspect_source(
        tmp_path, "@decorator\ndef run(): pass\nclass Plugin:\n    def go(self): pass\n"
    )
    generated = starter_contract(inspection)
    assert generated == {
        "filename": "plugin.py",
        "functions": [{"name": "run"}],
        "classes": [{"name": "Plugin", "methods": [{"name": "go"}]}],
    }
    assert evaluate_structure(Module(**generated), inspection)[0].code == "ISPY-S103"


def test_structure_evaluation_does_not_mutate_evidence(tmp_path):
    inspection = inspect_source(tmp_path, "value = 1\n")
    before = [e.model_dump() for e in inspection.evidence]
    expected = Module(variables=[{"name": "value", "value": 2}])
    first = evaluate_structure(expected, inspection)
    second = evaluate_structure(expected, inspection)
    assert first == second
    assert before == [e.model_dump() for e in inspection.evidence]
