# Senior Clean Code Radar — Practical Examples

Empirical Before/After case studies for `senior_coding_laws.md`.

---

## 1. Step 1: Boundary & Standard Library

### Before (Over-engineered dependency)
```python
import pandas as pd

def sum_sales(path: str) -> float:
    df = pd.read_csv(path)
    return float(df["amount"].sum())
```

### After (Standard Library First)
```python
import csv

def sum_sales(path: str) -> float:
    with open(path, newline="", encoding="utf-8") as f:
        return sum(float(row["amount"]) for row in csv.DictReader(f))
```

---

## 2. Step 2: Pure Core & Constrained States

### Before (Mixed side effects & mutable defaults)
```python
def process_orders(orders: list, status_log: list = []) -> list:
    for order in orders:
        if order["status"] == "ok":
            status_log.append(order["id"])
            db.update_order(order["id"])  # Inline side effect inside pure calculation
    return status_log
```

### After (Pure functional core & strict enum)
```python
from enum import StrEnum

class OrderStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"

def filter_completed_order_ids(orders: list[dict]) -> list[str]:
    return [o["id"] for o in orders if o.get("status") == OrderStatus.COMPLETED]
```

---

## 3. Step 3: Flattened Flow & Keyword-Only Arguments

### Before (Deep nesting & boolean blindness)
```python
def dispatch_task(task: dict, force: bool):
    if task:
        if task.get("ready"):
            if force or task.get("priority") > 10:
                execute(task)
```

### After (Guard clauses & keyword-only flags)
```python
def dispatch_task(task: dict | None, *, force: bool = False) -> None:
    if not task or not task.get("ready"):
        return
    if not (force or task.get("priority", 0) > 10):
        return
    execute(task)
```

---

## 4. Step 4: Useful Errors & Context Chaining

### Before (Silent swallowing or uninformative generic exception)
```python
try:
    data = load_remote_config(url)
except Exception:
    pass  # Silently swallows error
```

### After (Explicit domain exception with causality chaining)
```python
try:
    data = load_remote_config(url)
except urllib.error.URLError as err:
    raise ConfigLoadError(f"Failed to fetch config from {url}") from err
```

---

## 5. Step 5: Delete-List & Subtractive Engineering

### Before (Sprawling wrapper layers)
```python
class TextSanitizerFactory:
    def create_sanitizer(self): ...
class TextSanitizerWrapper:
    def sanitize(self, text): ...
```

### After (Direct root invocation: net negative lines)
```python
def sanitize_text(text: str) -> str:
    return text.strip().replace("\r\n", "\n")
```
