# AGENTS.md

## Status
Phase 0 skeleton only. `README.md`, `requirements.txt`, `src/__init__.py` are empty stubs; `tests/` is empty; no CI, lint, pre-commit, configs, scripts, or data dirs exist yet. Do not assume any business logic exists.

## Source of truth
- Build spec is `Guide/invoice2json_phase0.md` (374-line checklist: packaging → src tree → smoke test → configs/scripts/docker/data → pre-commit → CI → README).
- Gotcha: `.gitignore` contains a bare `Guide` entry, so `Guide/` is untracked and never pushed. Fresh clones / CI will not have it — implement its checklist into tracked files, don't reference it from code.

## Planned architecture (not yet created)
- Package `invoice2json`, code under `src/` with sub-packages: `data`, `template`, `training`, `evaluation`, `registry`, `serving`, `monitoring`, `utils` (each maps to a later phase; see Guide §2 for module names).
- `src` imports must have zero side effects: no file reads, env access, network, or logging config at import time.
- Every `src/` `__init__.py` needs a docstring naming its phase/modules; smoke test (`tests/unit/test_smoke.py`) asserts `module.__doc__ is not None` for all 9 packages.
- `data/raw|processed|quarantine/` are never committed (only `.gitkeep`); secrets live in gitignored `.env`, documented via committed `.env.example`.

## Python / toolchain drift — reconcile before coding
- `.python-version` = `3.12`, `pyproject.toml` `requires-python = ">=3.12"`, but Guide mandates `3.11.9` with `requires-python = ">=3.11,<3.12"` (Phase 2 verifies 3.12 compat). System here is Python 3.14. Pick one and align all three files.
- `pyproject.toml` is currently 8 lines with `dependencies = []`. Guide §1 is the full spec: `[build-system]` setuptools, `[project.scripts]` (`invoice2json-train`, `invoice2json-eval`), Ruff (`target-version py311`, `line-length 100`, `src = ["src","tests"]`), pytest (`testpaths=["tests"]`, `--strict-markers --strict-config`, markers `gpu,slow,integration`), coverage on `src/`.
- No venv or `pip` on PATH in this environment; `ruff`/`pytest` exist globally. Create `.venv` with the pinned Python before `pip install -e ".[dev]"`.

## Commands (Guide §§13–14; CI installs dev extras only, no torch/vLLM)
- Install: `pip install --upgrade pip==24.2 && pip install -e ".[dev]"`
- Verify: `ruff check . && ruff format --check . && pytest tests/ -v --cov=src --cov-report=term-missing`
- Single package import check: `python -c "import src, src.data, src.template, src.training, src.evaluation, src.registry, src.serving, src.monitoring, src.utils"`
- YAML check: `python -c "import yaml, glob; [yaml.safe_load(open(f)) for f in glob.glob('configs/*.yaml')]"`

## Conventions (Guide §14 — enforced by CI/pre-commit once added)
- Every `.py` in `src/` and `tests/` has a module docstring; every test function has docstring + full type hints.
- No `print()` in `src/` (structured logging only); no bare `except:`; no env-var reads at import time.
- `pyproject.toml` is the single dependency source; `requirements.txt` (Kaggle flat pins) must match the `train` extra exactly.
- Pre-commit once added: `trailing-whitespace, end-of-file-fixer, check-yaml/toml/json, check-added-large-files --maxkb=500, check-merge-conflict, detect-private-key, mixed-line-ending --fix=lf`, `ruff` v0.6.9 + `ruff-format`, `gitleaks` v8.20.1.
