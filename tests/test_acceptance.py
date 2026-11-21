"""Characterization / acceptance tests written BEFORE any refactoring.

They pin current, intended behaviour so later changes can be checked against it.
AC = acceptance criterion from docs/REPORT (AC1..AC5).
"""
import json

from expense_splitter import storage
from expense_splitter.calculator import describe_mode, split_expense
from expense_splitter.cli import main
from expense_splitter.models import Expense


# AC5 - valid splits that divide evenly keep their current results
def test_shares_split():
    e = Expense("Hotel", 90.0, "Dana", ["Ali", "Dana"], "shares", {"Ali": 1, "Dana": 2})
    assert split_expense(e) == {"Ali": 30.0, "Dana": 60.0}


def test_describe_mode_labels():
    modes = ("equal", "percent", "shares")
    labels = [describe_mode(Expense("x", 1.0, "A", ["A"], m)) for m in modes]
    assert labels == ["split equally", "split by percent", "split by shares"]


# AC2 - CLI command names and output format stay the same
def test_cli_add_list_balance_report(tmp_path, capsys):
    f = str(tmp_path / "e.json")
    assert main(["--file", f, "add", "Pizza", "20", "--payer", "Ali", "--with", "Ali,Dana",
                 "--category", "food"]) == 0
    assert main(["--file", f, "list"]) == 0
    assert main(["--file", f, "balance"]) == 0
    assert main(["--file", f, "report"]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out == [
        "Added: Pizza (20.00)",
        "1. Pizza: 20.00 paid by Ali, split equally",
        "Ali: +10.00",
        "Dana: -10.00",
        "food: 20.00",
    ]


# AC3 - data files written by v0.1.0 still load
def test_v010_file_format_loads(tmp_path):
    f = tmp_path / "e.json"
    f.write_text(json.dumps([{
        "description": "Pizza", "amount": 20.0, "payer": "Ali",
        "participants": ["Ali", "Dana"], "mode": "equal", "weights": {}, "category": "general",
    }]))
    [e] = storage.load(str(f))
    assert (e.description, e.amount, e.participants) == ("Pizza", 20.0, ["Ali", "Dana"])
