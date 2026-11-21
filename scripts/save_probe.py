"""Probe: does a failed save destroy previously saved data? (Task 04, R7)"""
import os
import tempfile

from expense_splitter import storage
from expense_splitter.models import Expense

p = os.path.join(tempfile.mkdtemp(), "e.json")
storage.save([Expense("Pizza", 20.0, "Ali", ["Ali", "Dana"])], p)
print("before:", len(storage.load(p)), "expense(s) on disk")
bad = Expense("Bad", 5.0, "Ali", ["Ali"], weights={"Ali": object()})  # not JSON-serialisable
try:
    storage.save([*storage.load(p), bad], p)
except TypeError as ex:
    print("save failed:", ex)
print("file size after failed save:", os.path.getsize(p), "bytes")
try:
    print("after:", len(storage.load(p)), "expense(s)")
except Exception as ex:
    print("after: load fails ->", type(ex).__name__, ex)
