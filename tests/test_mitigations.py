"""Regression tests for the two mitigated risks (Task 07).

R1 - rounding: shares of an expense must add up exactly to its amount.
R3 - invalid input (unknown mode, bad percents, missing weights, empty
     participants, non-positive amount) must be rejected, never silently accepted.
"""
import pytest

from expense_splitter.calculator import balances, split_expense
from expense_splitter.cli import main
from expense_splitter.models import Expense


# ---------- M1 / R1: exact cent allocation ----------
@pytest.mark.parametrize("amount,people", [(100.0, 3), (10.0, 3), (0.05, 2), (1234.57, 7)])
def test_equal_shares_sum_to_amount(amount, people):
    names = [f"P{i}" for i in range(people)]
    shares = split_expense(Expense("x", amount, names[0], names))
    assert round(sum(shares.values()), 2) == amount
    assert max(shares.values()) - min(shares.values()) <= 0.01 + 1e-9


def test_shares_mode_sums_to_amount():
    e = Expense("x", 100.0, "A", ["A", "B", "C"], "shares", {"A": 1, "B": 1, "C": 1})
    assert round(sum(split_expense(e).values()), 2) == 100.0


def test_balances_sum_to_zero():
    es = [Expense("Dinner", 100.0, "Ali", ["Ali", "Dana", "Timur"]),
          Expense("Taxi", 10.0, "Dana", ["Ali", "Dana", "Timur"])]
    assert round(sum(balances(es).values()), 2) == 0.0


# ---------- M2 / R3 (+R2, R4, R6): input validation ----------
@pytest.mark.parametrize("expense,message", [
    (Expense("x", 30.0, "A", ["A", "B"], "equl"), "unknown split mode"),
    (Expense("x", 50.0, "A", ["A", "B"], "percent", {"A": 60, "B": 60}), "must add up to 100"),
    (Expense("x", 10.0, "A", ["A", "B"], "shares", {"A": 1}), "missing weight"),
    (Expense("x", 10.0, "A", []), "at least one participant"),
    (Expense("x", -40.0, "A", ["A", "B"]), "amount must be positive"),
    (Expense("x", 10.0, "A", ["A", "B"], "shares", {"A": 0, "B": 0}), "positive"),
])
def test_invalid_expense_rejected(expense, message):
    with pytest.raises(ValueError, match=message):
        split_expense(expense)


def test_cli_rejects_typo_mode_and_does_not_save(tmp_path, capsys):
    f = tmp_path / "e.json"
    code = main(["--file", str(f), "add", "Taxi", "30", "--payer", "Ali",
                 "--with", "Ali,Dana", "--mode", "equl"])
    assert code == 2
    assert "unknown split mode" in capsys.readouterr().err
    assert not f.exists()
