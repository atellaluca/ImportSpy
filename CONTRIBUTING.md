# Contributing to ImportSpy

🎉 Thank you for considering a contribution to **ImportSpy** — a project designed to bring structure, security, and clarity to Python imports.

We welcome all kinds of contributions: new features, bug fixes, tests, documentation, and even thoughtful ideas. Your involvement makes the project better.

---

## 📢 How to Contribute

### 1. Open an Issue  
If you encounter a bug, have a feature suggestion, or want to propose a change, please [open an issue](https://github.com/atellaluca/ImportSpy/issues). Use clear and descriptive titles.

You can use labels such as:
- `bug`: for broken functionality
- `enhancement`: for feature requests
- `question`: for clarification or design discussions

### 2. Fork and Branch Strategy

- Create a **fork** of the repository.
- Work in a dedicated **feature branch** off `main`.
- Use consistent branch naming:

| Purpose         | Branch Name Format            |
|----------------|-------------------------------|
| Feature         | `feature/short-description`   |
| Bug fix         | `fix/issue-description`       |
| Documentation   | `docs/section-description`    |
| Tests           | `test/feature-or-bug-name`    |

> 💡 Keep pull requests focused and small. This helps reviewers and speeds up merging.

---

## ✅ Code Standards

### Python Style Guide
ImportSpy follows:
- [PEP8](https://peps.python.org/pep-0008/)
- Type hints throughout the codebase
- `black` + `ruff` for formatting and linting
- `pydantic` for data models

### Linting & Tests

To run tests and lint checks:

```bash
poetry install
pytest
ruff check .
black --check .
```

---

## 📄 Commit Conventions

We use **[Conventional Commits](https://www.conventionalcommits.org/)** for readable history and automatic changelog generation.

| Type     | Use For                       |
|----------|-------------------------------|
| `feat:`  | New feature                   |
| `fix:`   | Bug fix                       |
| `docs:`  | Documentation only            |
| `refactor:` | Code change w/o new feature or fix |
| `test:`  | Adding or updating tests      |
| `chore:` | Internal tooling or CI        |

**Example:**
```bash
git commit -m "feat: support multiple Python interpreters in contract"
```

---

## 🧪 Test Philosophy

Tests live in `tests/validators/` and should:
- Cover core logic (validators, spymodel, contract violations)
- Include both positive and negative cases
- Be fast, deterministic, and isolated

---

## ✍️ Docs Contributions

We use **MkDocs + Material** for documentation. Docs live under:

```
docs/
```

To preview locally:

```bash
poetry install
mkdocs serve
```

New pages should be added to `mkdocs.yml` under the right section.

---

## 🙌 Join the Community

While we don’t yet have a Discord or forum, we encourage:
- Sharing feedback via GitHub Issues
- Discussing architecture via PRs and comments
- Connecting with the maintainer via LinkedIn or GitHub

---

## 💬 Need Help?

Open an issue with the `question` label or ping @atellaluca in your PR.

---

## 📜 License

By contributing, you agree your work will be released under the MIT License.

---

**Let your modules enforce their own rules — and thank you for helping ImportSpy grow!**
