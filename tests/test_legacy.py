"""Regression coverage for the runtime-only 0.4 compatibility API."""

import importlib.util
import logging
import sys
from types import ModuleType

import pytest
from pydantic import ValidationError

from importspy.constants import Constants, Contexts, Errors
from importspy.models import Class, Environment, Function, SpyModel, Variable
from importspy.persistences import PersistenceError, YamlParser
from importspy.s import Spy
from importspy.utilities.module_util import ModuleUtil
from importspy.validators import ClassValidator, SystemValidator
from importspy.violation_systems import Bundle, ModuleContractViolation


@pytest.fixture
def loaded_module(tmp_path, monkeypatch):
    marker = tmp_path / "executions.txt"
    source = tmp_path / "legacy_plugin.py"
    source.write_text(
        "import pathlib\n"
        f"pathlib.Path({str(marker)!r}).write_text(\n"
        f"    pathlib.Path({str(marker)!r}).read_text() + 'x'\n"
        f"    if pathlib.Path({str(marker)!r}).exists() else 'x'\n"
        ")\n"
        "value: int = 42\n"
        "def greet(name: str) -> str:\n"
        "    return name\n",
        encoding="utf-8",
    )
    spec = importlib.util.spec_from_file_location("legacy_plugin", source)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, module.__name__, module)
    spec.loader.exec_module(module)
    assert marker.read_text() == "x"
    return module, marker


def test_from_module_keeps_runtime_state_without_reexecution(
    loaded_module, monkeypatch
):
    module, marker = loaded_module
    module.value = 43

    def forbidden(*args, **kwargs):
        pytest.fail("Runtime introspection must not load or unload its target")

    monkeypatch.setattr(ModuleUtil, "load_module", forbidden)
    monkeypatch.setattr(ModuleUtil, "unload_module", forbidden)
    model = SpyModel.from_module(module)
    assert next(value for value in model.variables if value.name == "value").value == 43
    assert any(function.name == "greet" for function in model.functions)
    assert (
        model.deployments[0].systems[0].pythons[0].modules[0].variables
        == model.variables
    )
    assert marker.read_text() == "x"
    assert sys.modules[module.__name__] is module


@pytest.mark.parametrize("with_deployments", [False, True])
def test_spy_warns_and_returns_same_module(loaded_module, tmp_path, with_deployments):
    module, marker = loaded_module
    contract = SpyModel.from_module(module)
    if with_deployments:
        contract.deployments[0].systems[0].environment = None
    else:
        contract.deployments = None
    contract_path = tmp_path / "contract.yaml"
    YamlParser().save(
        contract.model_dump(mode="json", exclude_none=True), str(contract_path)
    )
    with pytest.warns(DeprecationWarning, match="already executed"):
        returned = Spy().importspy(filepath=str(contract_path), info_module=module)
    assert returned is module
    assert sys.modules[module.__name__] is module
    assert marker.read_text() == "x"


def test_runtime_model_accepts_module_without_file():
    module = ModuleType("memory_module")
    model = SpyModel.from_module(module)
    assert model.filename is None


def test_yaml_rejects_python_object_construction(tmp_path):
    marker = tmp_path / "must_not_exist"
    contract = tmp_path / "unsafe.yaml"
    payload = f"__import__('pathlib').Path({str(marker)!r}).touch()"
    contract.write_text(
        f"!!python/object/apply:builtins.eval\n- {payload!r}\n", encoding="utf-8"
    )
    with pytest.raises(PersistenceError):
        YamlParser().load(str(contract))
    assert not marker.exists()


@pytest.mark.parametrize("content", ["", "[]", "scalar", "name: first\nname: second\n"])
def test_yaml_rejects_non_mapping_or_duplicate_keys(tmp_path, content):
    contract = tmp_path / "invalid.yaml"
    contract.write_text(content, encoding="utf-8")
    with pytest.raises(PersistenceError):
        YamlParser().load(str(contract))


def test_yaml_round_trip_uses_unicode_safely(tmp_path):
    contract = tmp_path / "contract.yaml"
    data = {
        "filename": "modulo.py",
        "variables": [{"name": "message", "value": "caffè"}],
    }
    parser = YamlParser()
    parser.save(data, str(contract))
    assert parser.load(str(contract)) == data


def test_contract_models_reject_nested_unknown_fields():
    with pytest.raises(ValidationError, match="Extra inputs"):
        SpyModel.model_validate({"functions": [{"name": "run", "returns": "str"}]})


def test_structural_annotations_accept_arbitrary_text_and_old_enums():
    assert (
        Variable(name="result", annotation="list[User] | None").annotation
        == "list[User] | None"
    )
    assert (
        Function(
            name="run", return_annotation=Constants.SupportedAnnotations.STR
        ).return_annotation
        == "str"
    )


def test_environment_diagnostics_never_include_values(caplog):
    expected = Environment(
        variables=[Variable(name="SERVICE_TOKEN", value="expected-secret")]
    )
    observed = Environment(
        variables=[Variable(name="SERVICE_TOKEN", value="actual-secret")]
    )
    caplog.set_level(logging.DEBUG)
    with pytest.raises(ValueError) as error:
        SystemValidator.EnvironmentValidator().validate(expected, observed, Bundle())
    text = str(error.value) + caplog.text + str(expected)
    assert "SERVICE_TOKEN" in text
    assert "expected-secret" not in text
    assert "actual-secret" not in text
    assert "[redacted]" in str(error.value)


def test_missing_environment_collection_does_not_include_values():
    expected = Environment(variables=[Variable(name="SERVICE_TOKEN", value="secret")])
    with pytest.raises(ValueError) as error:
        SystemValidator.EnvironmentValidator().validate(expected, None, Bundle())
    assert "secret" not in str(error.value)


def test_class_attribute_mismatch_uses_attribute_context():
    expected = Class.model_validate(
        {
            "name": "Plugin",
            "attributes": [{"name": "level", "type": "class", "value": 2}],
        }
    )
    observed = Class.model_validate(
        {
            "name": "Plugin",
            "attributes": [{"name": "level", "type": "class", "value": 1}],
        }
    )
    bundle = Bundle({Errors.KEY_FILE_NAME: "plugin.py"})
    with pytest.raises(ValueError, match='class attribute "level"'):
        ClassValidator().validate(
            [expected],
            [observed],
            ModuleContractViolation(Contexts.CLASS_CONTEXT, bundle),
        )
