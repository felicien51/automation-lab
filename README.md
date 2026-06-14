# 🛠️ Automation Tool — Pip, PyPI & Scripting Lab

A lightweight, modular Python automation script that:

- Fetches data from a public API using the `requests` package (installed via pip)
- Writes structured output to a timestamped log file using File I/O
- Tracks dependencies in `requirements.txt`
- Is fully testable with `pytest`

---

## Setup

### Requirements

- Python 3.10+
- pip

### Install dependencies

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## How to Run

```bash
python generate_log.py
```

This will:
1. Write a list of sample log entries to `log_YYYYMMDD.txt` (today's date).
2. Fetch a sample post from a public API (`jsonplaceholder.typicode.com`) and print its title.

Example output:
```
Log written to log_20260614.txt
Fetched Post Title: sunt aut facere repellat provident occaecati...
```

---

## Features

| Function | Description |
|----------|-------------|
| `generate_log(log_data, directory=".")` | Writes a list of strings to `log_YYYYMMDD.txt`, one entry per line. Raises `ValueError` if `log_data` is not a list. Prints a confirmation message including the filename. |
| `fetch_data()` | Uses `requests` to GET a sample post from a public placeholder API and returns the JSON response. |

---

## Running Tests

```bash
pytest tests/ -v
```

Expected output: **7 passed**.

The test suite covers:
- File creation with the correct timestamped filename (`log_YYYYMMDD.txt`)
- File contents matching the input list exactly
- `ValueError` raised on non-list input
- Empty list still produces a valid, empty log file
- Confirmation message printed with the filename
- Clean creation and removal of log files (no leftover files after tests)

---

## Project Structure

```
automation_lab/
├── generate_log.py        # Main automation script
├── requirements.txt        # Dependencies (requests, pytest)
├── README.md
└── tests/
    ├── __init__.py
    └── test_generate_log.py
```

---

## Known Issues

- `fetch_data()` returns an empty dict if the API is unreachable or returns a non-200 status, so the script never crashes due to network issues — it just prints "No title found".
- Log files are written to the current working directory by default; pass a `directory` argument to `generate_log()` to write elsewhere.
