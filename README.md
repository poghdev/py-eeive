# py-eeive

Monitor your Python scripts with **one decorator** — automatic retries, timing, and smart error explanations.

No external dependencies. Works with sync and async functions.

## Install

```bash
pip install py-eeive
```

## Usage

```python
from py_eeive import monitor

@monitor(retries=3, retry_delay=5, log=True, language="english")
def main():
    # your script here
    ...

main()
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `retries` | `1` | How many times to retry on failure |
| `retry_delay` | `5` | Seconds to wait between retries |
| `log` | `True` | Save error log to `logs/` folder as JSON |
| `language` | `"english"` | Output language: `"english"` or `"russian"` |
| `custom_errors` | `None` | Your own error explanations (dict) |
| `exponential_backoff` | `False` | Double the delay on each retry |
| `retry_on` | `(Exception,)` | Only retry on these specific exceptions |

## Example output — success

```
[py-eeive] Starting: main
──────────────────────────────────────────────────
[py-eeive] ✅ Finished in 2.4 sec
```

## Example output — failure

```
[py-eeive] Starting: main
──────────────────────────────────────────────────
[py-eeive] ❌ Attempt 1/3 — Line 12 — ZeroDivisionError: division by zero
[py-eeive] 🔄 Retrying in 5 sec...
[py-eeive] ❌ Attempt 2/3 — Line 12 — ZeroDivisionError: division by zero
[py-eeive] 🔄 Retrying in 5 sec...
[py-eeive] ❌ Attempt 3/3 — Line 12 — ZeroDivisionError: division by zero

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💥 Script failed permanently
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Error:   ZeroDivisionError: division by zero
  Line:    12 in file main.py
  Cause:   You are dividing a number by zero.
  Fix:     Check that the denominator is not 0 before dividing.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⏱  15.3 sec
  📄 Log saved: logs/main_2026-04-24_12-00-00.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Custom error explanations

```python
MY_ERRORS = {
    "MyCustomError": {
        "cause": "Something specific to my app went wrong.",
        "fix": "Check the config file."
    }
}

@monitor(retries=2, custom_errors=MY_ERRORS)
def main():
    ...
```

## Async support

Works with async functions out of the box:

```python
@monitor(retries=3, retry_delay=2)
async def fetch_data():
    ...
```

## Retry only on specific exceptions

```python
@monitor(retries=5, retry_on=(ConnectionError, TimeoutError))
def main():
    ...
```

## License

MIT