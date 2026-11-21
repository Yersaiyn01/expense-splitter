import argparse
import sys

from . import storage
from .calculator import balances, describe_mode, total_by_category, validate
from .models import Expense


def parse_weights(raw):
    weights = {}
    if raw:
        for pair in raw.split(","):
            name, value = pair.split("=")
            weights[name] = float(value)
    return weights


def main(argv=None):
    parser = argparse.ArgumentParser(prog="expense-splitter")
    parser.add_argument("--file", default=storage.DEFAULT_FILE)
    sub = parser.add_subparsers(dest="command")

    add = sub.add_parser("add")
    add.add_argument("description")
    add.add_argument("amount", type=float)
    add.add_argument("--payer", required=True)
    add.add_argument("--with", dest="participants", required=True)
    add.add_argument("--mode", default="equal")
    add.add_argument("--weights", default="")
    add.add_argument("--category", default="general")

    sub.add_parser("list")
    sub.add_parser("balance")
    sub.add_parser("report")

    args = parser.parse_args(argv)
    try:
        return run(args, parser)
    except ValueError as ex:  # invalid user input or invalid stored expense
        print(f"error: {ex}", file=sys.stderr)
        return 2


def run(args, parser):
    expenses = storage.load(args.file)

    if args.command == "add":
        e = Expense(
            description=args.description,
            amount=args.amount,
            payer=args.payer,
            participants=args.participants.split(","),
            mode=args.mode,
            weights=parse_weights(args.weights),
            category=args.category,
        )
        validate(e)  # reject before anything is written to disk
        expenses.append(e)
        storage.save(expenses, args.file)
        print(f"Added: {e.description} ({e.amount:.2f})")
    elif args.command == "list":
        for i, e in enumerate(expenses, 1):
            print(f"{i}. {e.description}: {e.amount:.2f} paid by {e.payer}, "
                  f"{describe_mode(e)}")
    elif args.command == "balance":
        for person, value in sorted(balances(expenses).items()):
            print(f"{person}: {value:+.2f}")
    elif args.command == "report":
        for cat, value in total_by_category(expenses).items():
            print(f"{cat}: {value:.2f}")
    else:
        parser.print_help()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
