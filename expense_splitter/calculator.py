"""Business logic: how much each person owes for each expense.

Split modes use the Strategy pattern: each mode is one small class with a
``label`` and a ``weights`` method, registered in ``SPLIT_STRATEGIES``.
Adding a mode = adding one class + one registry entry (no if/elif chains).

Money rule (risk R1): a strategy only says *in which proportion* to split;
``_allocate_cents`` turns the proportions into whole cents that always add
up exactly to the expense amount (largest-remainder method).
"""
from __future__ import annotations

from decimal import ROUND_FLOOR, Decimal
from typing import Protocol

from .models import Expense

CENT = Decimal("0.01")


class SplitStrategy(Protocol):
    label: str

    def weights(self, expense: Expense) -> dict[str, Decimal]: ...


def _required_weights(expense: Expense) -> dict[str, Decimal]:
    missing = [p for p in expense.participants if p not in expense.weights]
    if missing:
        raise ValueError(f"missing weight for: {', '.join(missing)}")
    w = {p: Decimal(str(expense.weights[p])) for p in expense.participants}
    if any(v < 0 for v in w.values()) or sum(w.values()) <= 0:
        raise ValueError("weights must be non-negative and their total positive")
    return w


class EqualSplit:
    label = "split equally"

    def weights(self, expense: Expense) -> dict[str, Decimal]:
        return {p: Decimal(1) for p in expense.participants}


class PercentSplit:
    label = "split by percent"

    def weights(self, expense: Expense) -> dict[str, Decimal]:
        w = _required_weights(expense)
        if sum(w.values()) != 100:
            raise ValueError(f"percentages must add up to 100 (got {sum(w.values())})")
        return w


class SharesSplit:
    label = "split by shares"

    def weights(self, expense: Expense) -> dict[str, Decimal]:
        return _required_weights(expense)


SPLIT_STRATEGIES: dict[str, SplitStrategy] = {
    "equal": EqualSplit(),
    "percent": PercentSplit(),
    "shares": SharesSplit(),
}


def validate(expense: Expense) -> SplitStrategy:
    """Raise ValueError for an invalid expense (risk R3); return its strategy."""
    strategy = SPLIT_STRATEGIES.get(expense.mode)
    if strategy is None:
        raise ValueError(f"unknown split mode {expense.mode!r}; "
                         f"use one of: {', '.join(SPLIT_STRATEGIES)}")
    if not expense.participants:
        raise ValueError("an expense needs at least one participant")
    if expense.amount <= 0:
        raise ValueError("amount must be positive")
    strategy.weights(expense)  # weight checks for percent/shares
    return strategy


def _allocate_cents(amount: float, weights: dict[str, Decimal]) -> dict[str, float]:
    total_cents = int((Decimal(str(amount)) / CENT).to_integral_value())
    total_w = sum(weights.values())
    exact = {p: Decimal(total_cents) * w / total_w for p, w in weights.items()}
    cents = {p: int(v.to_integral_value(rounding=ROUND_FLOOR)) for p, v in exact.items()}
    leftover = total_cents - sum(cents.values())
    # give the remaining cents to the largest fractional parts (ties: input order)
    order = sorted(weights, key=lambda p: exact[p] - cents[p], reverse=True)
    for p in order[:leftover]:
        cents[p] += 1
    return {p: float(Decimal(c) * CENT) for p, c in cents.items()}


def split_expense(expense: Expense) -> dict[str, float]:
    """Return {person: share} for one expense; shares sum exactly to the amount."""
    strategy = validate(expense)
    return _allocate_cents(expense.amount, strategy.weights(expense))


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
    return {p: round(v, 2) + 0.0 for p, v in bal.items()}


def total_by_category(expenses: list[Expense]) -> dict[str, float]:
    totals: dict[str, float] = {}
    for e in expenses:
        totals[e.category] = totals.get(e.category, 0) + e.amount
    return totals
