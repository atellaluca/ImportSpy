# Release engineering

The authoritative version is `[project].version` in `pyproject.toml`.
`importspy.__version__` and CLI `--version` read installed package metadata;
uninstalled source checkouts fall back to the same project file. Reinstall an
editable development package after changing metadata. The license remains MIT.

## Validate the candidate

```bash
poetry install --with dev
poetry check --strict
poetry run pytest -q
poetry run ruff check src tests examples/admission
poetry run mypy src
poetry run mkdocs build --strict
poetry run importspy check . --format json
poetry build
```

Use the CI matrix to verify Python 3.10–3.14. Test each built wheel in a clean
virtual environment: install it and run `python scripts/smoke_package.py` with
that environment's Python. The script checks installed version identity,
`--help`, `init`, human/JSON/SARIF output, admission/denial/configuration exits,
and target nonexecution. Build an sdist as well and verify its metadata.
Generated `dist/` and `site/` output is ignored and must not be committed.

Build inputs are the reviewed source, `pyproject.toml`, the build backend and the
locked contributor environment. The consumer wheel uses declared dependency
ranges; `poetry.lock` is not a lock for downstream applications. Bit-for-bit
reproducibility across unrelated environments is not claimed.

## Publish only after maintainer authorization

This repository's CI builds downloadable artifacts but does not automatically
publish on a branch push. A maintainer should review the final green commit,
release notes, migration guidance and wheel smoke test, then create the `v0.5.0`
tag/GitHub release and publish the matching artifacts to PyPI through their
approved release process. Publishing and account configuration are separate
external actions; do not put tokens or private keys in the repository.

For a future automated publishing workflow, prefer
[PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) with an
explicit protected GitHub environment. The maintainer must configure the
publisher identity in the PyPI project and GitHub environment before enabling
that workflow. Use the official PyPA publish action's attestation support where
applicable; do not label a local package build as attested or cryptographically
verified. See [PyPI's attestation documentation](https://docs.pypi.org/attestations/).

No PyPI publisher or GitHub protected environment is provisioned by the 0.5
implementation. Check account configuration before choosing the publication path.

Read the Docs uses the standard `.readthedocs.yaml` configuration and the same
locked Poetry environment to build MkDocs. This replaces the historical
`readthedocs.yml` file that referenced nonexistent Sphinx inputs.
