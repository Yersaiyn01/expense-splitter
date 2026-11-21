# Expense Splitter

Small command-line tool to record shared expenses between friends and
calculate who owes whom.

## Install

    pip install -r requirements-dev.txt   # pinned test/lint tools

## Usage

    python -m expense_splitter add "Pizza" 20 --payer Ali --with Ali,Dana
    python -m expense_splitter list
    python -m expense_splitter balance
    python -m expense_splitter report

## Tests

    sh scripts/check.sh     # tests + lint + types + compile

## Known limitations (v0.1.0 + fixes)

- **Back up `expenses.json` before use.** Saving is not yet atomic: if the program
  crashes while writing, the file can be left broken (risk R7, open).
- Files containing an invalid expense (e.g. a misspelled `--mode`) now make
  `balance` stop with `error: ...`; fix the entry in the JSON file by hand.
