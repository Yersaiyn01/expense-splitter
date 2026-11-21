from expense_splitter.calculator import balances, split_expense, total_by_category
from expense_splitter.models import Expense


def test_equal_split_two_people():
    e = Expense("Pizza", 20.0, "Ali", ["Ali", "Dana"])
    assert split_expense(e) == {"Ali": 10.0, "Dana": 10.0}


def test_percent_split():
    e = Expense("Taxi", 50.0, "Ali", ["Ali", "Dana"], "percent", {"Ali": 60, "Dana": 40})
    assert split_expense(e) == {"Ali": 30.0, "Dana": 20.0}


def test_balances_simple():
    e = Expense("Pizza", 20.0, "Ali", ["Ali", "Dana"])
    assert balances([e]) == {"Ali": 10.0, "Dana": -10.0}


def test_total_by_category():
    es = [Expense("A", 5.0, "Ali", ["Ali"], category="food"),
          Expense("B", 7.0, "Ali", ["Ali"], category="food")]
    assert total_by_category(es) == {"food": 12.0}
