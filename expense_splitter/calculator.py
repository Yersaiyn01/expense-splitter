"""Business logic: how much each person owes for each expense."""


def split_expense(expense):
    """Return {person: share} for one expense."""
    result = {}
    if expense.mode == "equal":
        share = round(expense.amount / len(expense.participants), 2)
        for p in expense.participants:
            result[p] = share
    elif expense.mode == "percent":
        for p in expense.participants:
            result[p] = round(expense.amount * expense.weights[p] / 100, 2)
    elif expense.mode == "shares":
        total = sum(expense.weights[p] for p in expense.participants)
        for p in expense.participants:
            result[p] = round(expense.amount * expense.weights[p] / total, 2)
    return result


def describe_mode(expense):
    """Human readable label used by the CLI 'list' command."""
    if expense.mode == "equal":
        return "split equally"
    elif expense.mode == "percent":
        return "split by percent"
    elif expense.mode == "shares":
        return "split by shares"
    return "unknown"


def balances(expenses):
    """Net balance per person: positive = should receive, negative = owes."""
    bal = {}
    for e in expenses:
        bal[e.payer] = bal.get(e.payer, 0) + e.amount
        for person, share in split_expense(e).items():
            bal[person] = bal.get(person, 0) - share
    return {p: round(v, 2) for p, v in bal.items()}


def total_by_category(expenses):
    totals = {}
    for e in expenses:
        totals[e.category] = totals.get(e.category, 0) + e.amount
    return totals
