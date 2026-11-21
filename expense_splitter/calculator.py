"""Business logic: how much each person owes for each expense.

Split modes use the Strategy pattern: each mode is one small class with a
``label`` and a ``split`` method, registered in ``SPLIT_STRATEGIES``.
Adding a mode = adding one class + one registry entry (no if/elif chains).
"""
from __future__ import annotations

from typing import Protocol

from .models import Expense


class SplitStrategy(Protocol):
    label: str

    def split(self, expense: Expense) -> dict[str, float]: ...


class EqualSplit:
    label = "split equally"

    def split(self, expense: Expense) -> dict[str, float]:
        share = round(expense.amount / len(expense.participants), 2)
        return {p: share for p in expense.participants}


class PercentSplit:
    label = "split by percent"

    def split(self, expense: Expense) -> dict[str, float]:
        return {p: round(expense.amount * expense.weights[p] / 100, 2)
                for p in expense.participants}


class SharesSplit:
    label = "split by shares"

    def split(self, expense: Expense) -> dict[str, float]:
        total = sum(expense.weights[p] for p in expense.participants)
        return {p: round(expense.amount * expense.weights[p] / total, 2)
                for p in expense.participants}


SPLIT_STRATEGIES: dict[str, SplitStrategy] = {
    "equal": EqualSplit(),
    "percent": PercentSplit(),
    "shares": SharesSplit(),
}


def split_expense(expense: Expense) -> dict[str, float]:
    """Return {person: share} for one expense."""
    strategy = SPLIT_STRATEGIES.get(expense.mode)
    if strategy is None:
        return {}  # behaviour preserved from v0.1.0 (see risk R3, fixed separately)
    return strategy.split(expense)


def describe_mode(expense: Expense) -> str:
    """Human readable label used by the CLI 'list' command."""
    strategy = SPLIT_STRATEGIES.get(expense.mode)
    return strategy.label if strategy else "unknown"


def balances(expenses: list[Expense]) -> dict[str, float]:
    """Net balance per person: positive = should receive, negative = owes."""
    bal: dict[str, float] = {}
    for e in expenses:
        bal[e.payer] = bal.get(e.payer, 0) + e.amount
        for person, share in split_expense(e).items():
            bal[person] = bal.get(person, 0) - share
    return {p: round(v, 2) for p, v in bal.items()}


def total_by_category(expenses: list[Expense]) -> dict[str, float]:
    totals: dict[str, float] = {}
    for e in expenses:
        totals[e.category] = totals.get(e.category, 0) + e.amount
    return totals
