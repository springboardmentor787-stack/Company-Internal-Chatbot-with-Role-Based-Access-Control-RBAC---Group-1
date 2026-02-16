# Copilot instructions for this repository ✅

## Quick summary
- This repo holds a small document ingestion project used to load financial and marketing reports into an LLM/data pipeline. The codebase is minimal: a top-level `scripts/` folder with `load_documents.py` and a `Fintech-data/` directory containing the source documents (Markdown/CSV/text).

## What an AI coding agent should know 🔧
- Single entrypoint for data ingestion: `scripts/load_documents.py` — it recursively walks `Fintech-data/` and uses `TextLoader` for `.md`/`.txt` and `CSVLoader` for `.csv` from `langchain_community`.
- Data layout: `Fintech-data/<category>/*.md` or `*.csv` (e.g., `Fintech-data/marketing/market_report_q4_2024.md` and `Fintech-data/HR/hr_data.csv`). New documents should be added to the appropriate category.
- Dependencies are not tracked in a project-level `requirements.txt` or `pyproject.toml`; there is a `venv/requirements.txt` listing key packages used during development: `langchain`, `langchain-community`, `sentence-transformers`, `chromadb`, `pandas`, `unstructured`.

## Local dev / common commands ▶️
- Create and activate a virtualenv and install packages (example):
  - `python -m venv venv` then `venv\Scripts\Activate.ps1` (Windows) and `pip install -r venv/requirements.txt`.
- Run ingestion to sanity-check loaders: `python scripts/load_documents.py` — prints a total count and a sample document.

## Conventions & patterns to follow 🧭
- File-type dispatch in `load_documents.py` is extension-based. If you add support for new formats, update that script and keep loader initialization close to file discovery logic.
- Keep dataset files under `Fintech-data/` in logical subfolders (category-based). Avoid adding large binaries to the repo.

## Important gotchas / findings ⚠️
- `Fintech-data/.git` exists: this is a nested git repository (data repo). Avoid making repository-level changes inside `Fintech-data` unless you intend to manage it as a sub-repo/submodule.
- There is no `tests/` directory or CI workflows present; changes that affect behavior should include a small, local test or a validation script (e.g., a short unit test for loaders) so reviewers can verify changes.

## When asked to implement a change (practical checklist) ✅
1. Update or add code in `scripts/` (e.g., add a new loader or conversion). Reference existing loader patterns.
2. Add a small reproducible test or script that demonstrates the change (run `python scripts/load_documents.py` with sample files).
3. Document the change in a top-level `README.md` or add a short note to this file if it affects dev workflow.
4. Do not modify `Fintech-data/.git` unless explicitly requested.

---

If something is unclear or you want this to include templates for PR descriptions or tests, tell me which areas to expand and I’ll iterate. 💡