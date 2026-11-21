# AGENTS.md — instructions for AI coding agents

These rules apply to every AI agent (Claude, Codex, Copilot, Cursor, etc.) working in
this repository. A human maintainer (Maralbekuly Yersaiyn) reviews and approves every change.

## 1. Purpose
`expense-splitter` is a small Python command-line tool that records shared expenses
between friends and calculates who owes whom. It stores data in a local JSON file.
Amounts are money: correctness of splitting and balances matters more than features.

## 2. Architecture
| Path | Role |
|---|---|
| `expense_splitter/__main__.py` | Entry point for `python -m expense_splitter` |
| `expense_splitter/cli.py` | Argument parsing and printing only (no business rules) |
| `expense_splitter/calculator.py` | Business logic: splits, balances, category totals |
| `expense_splitter/models.py` | `Expense` dataclass |
| `expense_splitter/storage.py` | Load/save JSON file |
| `tests/` | pytest tests (unit + CLI acceptance tests) |
| `scripts/check.sh` | Runs all quality gates |
| `scripts/*_probe.py` | Read-only scripts that reproduce risk findings |

Rules: keep business logic out of `cli.py`. Keep storage free of calculation logic.
Runtime code uses the **standard library only**.

## 3. Setup
```sh
python -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt      # pinned: pytest, ruff, mypy
```

## 4. Safe commands (may be run without asking)
```sh
sh scripts/check.sh                      # pytest + ruff + mypy + compileall
python -m pytest -q
ruff check .                             # read-only; do NOT use --fix without review
mypy expense_splitter
python -m expense_splitter --file /tmp/<name>.json <command>   # always use a temp file
PYTHONPATH=. python scripts/risk_probe.py
git status / git diff / git log
```

## 5. Coding conventions
- Python ≥ 3.10, PEP 8, max line length 100 (enforced by ruff config in `pyproject.toml`).
- Type hints on new or changed functions.
- Money: shares of one expense must always add up exactly to the expense amount (cents).
- Invalid input raises `ValueError` with a clear message; the CLI turns it into an error
  message and exit code 2. Never fail silently.
- Do not change CLI command names, options or output format without approval
  (acceptance criterion AC2).
- Do not change the JSON file format without a migration (AC3).

## 6. Test expectations
- Every bug fix comes with a test that fails before the fix and passes after it.
- Every behaviour change updates or adds tests in `tests/`.
- `sh scripts/check.sh` must pass before you report work as done. Paste its real output.
- Never claim a test passed if you did not run it. Never edit a test only to make it pass.

## 7. Forbidden actions (never do these)
- Adding, committing or printing secrets, tokens, passwords or real personal data.
- Production deployment, publishing packages, pushing tags or releases.
- Destructive commands: `rm -rf`, `git push --force`, `git reset --hard`,
  `git clean -fdx`, rewriting history, deleting branches, deleting user data files
  (`expenses.json`).
- Adding, removing or upgrading dependencies (`pip install <pkg>`, editing
  `requirements*.txt` / `pyproject.toml` dependencies) without explicit human approval.
- Network access from code or tests.
- Running the CLI against the real default `expenses.json` (use a temp file).
- Disabling or weakening lint, type checks or tests.

## 8. Review gates
1. Work on a separate branch (`agent/<short-task>`), never directly on `main`.
2. Keep diffs small: one concern per commit.
3. Deliver: change summary, `git diff`, output of `sh scripts/check.sh`, risk notes.
4. A human reviews the diff and the test output before merge. Agents never merge.

## 9. When unsure
Stop and ask. Write assumptions explicitly as "ASSUMPTION:" in your summary and mark
unverified claims as "UNVERIFIED".
