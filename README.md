# Expense Splitter

Small command-line tool to record shared expenses between friends and
calculate who owes whom.

## Install

    pip install -r requirements.txt

## Usage

    python -m expense_splitter add "Pizza" 20 --payer Ali --with Ali,Dana
    python -m expense_splitter list
    python -m expense_splitter balance
    python -m expense_splitter summary

## Tests

    pytest
