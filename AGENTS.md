# AGENTS.md

## Status (verified against repo 2026-10-08)
Phase 0 skeleton only. Tracked files are just `.gitignore`, `.dockerignore`,
`.gitattributes`, `.python-version`, `pyproject.toml`, `README.md`,
`requirements.txt`, `src/__init__.py`, `AGENTS.md`.
`README.md`, `requirements.txt`, `src/__init__.py` are empty stubs; `tests/`
is empty (no `__init__.py`, no test files). No CI, pre-commit, `configs/`,
`scripts/`, `docker/`, `data/`, `.env.example` yet. Do not assume business logic exists.

## Source of truth
- Build spec is `Guide/invoice2json_phase0.md` (~375-line checklist: packaging →
  src tree → smoke test → configs/scripts/docker/data → pre-commit → CI → README).
- Gotcha: `.gitignore:75` has a bare `Guide` entry (verified: `git check-ignore`
  matches it), so `Guide/` is untracked and never pushed. Fresh clones / CI will
  not have it — implement its checklist into tracked files, never import from it.
- Branch is `master`, but Guide §§0/11/13 assumes `main` (CI triggers on `main`).
  Reconcile before writing CI workflow or push instructions.

## Planned architecture (not yet created)
- Flat `src.*` layout, not `src/invoice2json/`: Guide §1 pins
  `[tool.setuptools.packages.find] where=["."], include=["src*"]`, imports are
  `import src.data, src.template, ...`. Sub-packages: `data`, `template`,
  `training`, `evaluation`, `registry`, `serving`, `monitoring`, `utils`
  (see Guide §2 for per-phase module names).
- `src` imports must have zero side effects: no file reads, env access, network,
  or logging config at import time.
- Every `src/` `__init__.py` needs a docstring naming its phase/modules; smoke test
  (`tests/unit/test_smoke.py`, to be created) asserts `module.__doc__ is not None`
  for all 9 packages (`src` + 8 sub-packages).
- `data/raw|processed|quarantine/` are never committed (only `.gitkeep`); secrets
  live in gitignored `.env`, documented via committed `.env.example`.

## Python / toolchain drift — reconcile before coding
- `.python-version` = `3.12`, `pyproject.toml` `requires-python = ">=3.12"`, but Guide
  mandates `3.11.9` with `requires-python = ">=3.11,<3.12"`. `.venv/` already exists
  with Python 3.12.13; system `python3` is 3.14. Pick one and align `.python-version`,
  `pyproject.toml`, Guide, and `.venv` together.
- `pyproject.toml` is a 7-line stub (`dependencies = []`). Guide §1 is the full spec:
  `[build-system]` setuptools, `[project.scripts]` (`invoice2json-train`,
  `invoice2json-eval`), Ruff (`target-version py311`, `line-length 100`,
  `src = ["src","tests"]`), pytest (`testpaths=["tests"]`, `--strict-markers
  --strict-config`, markers `gpu,slow,integration`), coverage on `src/`.
- No `pip` on system PATH; global `ruff` is 0.15.20 and `pytest` is 9.1.1 (Guide pins
  0.6.9 / 8.3.3). Use `.venv/bin/python -m pip` or `source .venv/bin/activate` first.

## Commands (Guide §§13–14; no CI/pre-commit exists yet to enforce these)
- Install: `source .venv/bin/activate && pip install --upgrade pip==24.2 && pip install -e ".[dev]"`
- Verify: `ruff check . && ruff format --check . && pytest tests/ -v --cov=src --cov-report=term-missing`
  (currently collects 0 tests — `tests/` is empty).
- Import check (after §2): `python -c "import src, src.data, src.template, src.training, src.evaluation, src.registry, src.serving, src.monitoring, src.utils"`
- YAML check (after §4): `python -c "import yaml, glob; [yaml.safe_load(open(f)) for f in glob.glob('configs/*.yaml')]"`

## Conventions (Guide §14 — follow now, enforced by CI/pre-commit once added)
- Every `.py` in `src/` and `tests/` has a module docstring; every test function has
  docstring + full type hints.
- No `print()` in `src/` (structured logging only); no bare `except:`; no env-var
  reads at import time.
- `pyproject.toml` is the single dependency source; `requirements.txt` (Kaggle flat
  pins) must match the `train` extra exactly.
- Pre-commit once added: `trailing-whitespace, end-of-file-fixer, check-yaml/toml/json,
  check-added-large-files --maxkb=500, check-merge-conflict, detect-private-key,
  mixed-line-ending --fix=lf`, `ruff` v0.6.9 + `ruff-format`, `gitleaks` v8.20.1.
