"""Validate a wheel installed in a clean interpreter, without importing the checkout."""

import importlib.metadata
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    import importspy

    version = importlib.metadata.version("importspy")
    assert importspy.__version__ == version
    with tempfile.TemporaryDirectory(prefix="importspy-smoke-") as directory:
        root = Path(directory)

        def run(*arguments: str, expected: int = 0) -> str:
            result = subprocess.run(
                [sys.executable, "-m", "importspy.cli", *arguments],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            assert result.returncode == expected, (
                arguments,
                result.returncode,
                result.stdout,
                result.stderr,
            )
            return result.stdout

        assert version in run("--version")
        assert "check" in run("--help")
        source = root / "plugin.py"
        source.write_text(
            "def run(value: int) -> int:\n    return value\nprint('TARGET EXECUTED')\n"
        )
        run("init", str(source))
        assert "Target module was not executed." in run("check", str(source))
        decision = json.loads(run("check", str(source), "--format", "json"))
        assert decision["decision"] == "ADMIT" and not decision["target_executed"]
        assert (
            json.loads(run("check", str(source), "--format", "sarif"))["version"]
            == "2.1.0"
        )
        source.write_text("import packaging\nimport typer\nprint('TARGET EXECUTED')\n")
        source.with_suffix(".importspy.yml").write_text(
            "dependencies:\n  typer:\n    allowed: false\n"
        )
        denied = run("check", str(source), "--format", "json", expected=1)
        assert "TARGET EXECUTED" not in denied
        assert json.loads(denied)["decision"] == "DENY"
        source.with_suffix(".importspy.yml").write_text("schema_version: 99\n")
        assert json.loads(run("check", str(source), "--format", "json", expected=2))[
            "violations"
        ]
    print(
        f"Installed ImportSpy {version}: version/help/init/check, JSON/SARIF and exit codes passed."
    )


if __name__ == "__main__":
    main()
