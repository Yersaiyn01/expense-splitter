"""Read-only probes used to confirm/refute candidate risk findings (Task 04)."""
import os
import tempfile

from expense_splitter import storage
from expense_splitter.calculator import balances, split_expense
from expense_splitter.models import Expense


def run(label, fn):
    print(f"--- {label}")
    try:
        print("result:", fn())
    except Exception as ex:
        print("EXCEPTION:", type(ex).__name__, ex)


e = Expense("Dinner", 100.0, "Ali", ["Ali", "Dana", "Timur"])
run("R1 equal split 100/3, sum of shares",
    lambda: (split_expense(e), round(sum(split_expense(e).values()), 2)))
run("R1 balances sum (should be 0)", lambda: round(sum(balances([e]).values()), 2))
e2 = Expense("Taxi", 50.0, "Ali", ["Ali", "Dana"], "percent", {"Ali": 60, "Dana": 60})
run("R2 percent 60+60", lambda: split_expense(e2))
run("R2b negative amount", lambda: split_expense(Expense("x", -40.0, "Ali", ["Ali", "Dana"])))
e3 = Expense("Typo", 30.0, "Ali", ["Ali", "Dana"], "equl")
run("R3 unknown mode 'equl' -> split", lambda: split_expense(e3))
run("R3 balances with typo mode", lambda: balances([e3]))
run("R4 empty participants", lambda: split_expense(Expense("x", 10.0, "Ali", [])))
p = os.path.join(tempfile.mkdtemp(), "e.json")
with open(p, "w") as fh:
    fh.write('[{"description": "Pizza", "amount": 20')
run("R5 load truncated JSON", lambda: storage.load(p))
run("R6 shares mode missing weight",
    lambda: split_expense(Expense("x", 10.0, "Ali", ["Ali", "Dana"], "shares", {"Ali": 1})))
