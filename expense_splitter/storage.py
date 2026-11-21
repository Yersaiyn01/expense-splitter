import json
import os

from .models import Expense

DEFAULT_FILE = "expenses.json"


def load(path=DEFAULT_FILE):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        data = json.load(f)
    return [Expense(**item) for item in data]


def save(expenses, path=DEFAULT_FILE):
    with open(path, "w") as f:
        json.dump([e.__dict__ for e in expenses], f, indent=2)
