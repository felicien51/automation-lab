"""
generate_log.py - Lightweight automation tool.

This script demonstrates:
- Using an externally installed package (requests) to fetch data from a public API.
- Writing structured output to a timestamped log file using File I/O.
- Modular functions wrapped in a main entry point for command-line execution.

Usage:
    python generate_log.py
"""

import os
from datetime import datetime

import requests


def generate_log(log_data, directory="."):
    """
    Write a list of log entries to a timestamped log file.

    The output filename follows the pattern: log_YYYYMMDD.txt
    (using the current date), written one entry per line.

    Args:
        log_data (list): A list of strings representing log entries.
            Each entry is written to its own line in the file.
        directory (str, optional): Directory in which to create the
            log file. Defaults to the current working directory.

    Returns:
        str: The full filepath of the created log file.

    Raises:
        ValueError: If `log_data` is not a list.

    Examples:
        >>> generate_log(["User logged in", "Report exported"])
        Log written to log_20260614.txt
        'log_20260614.txt'

        >>> generate_log([])  # empty list still creates a valid file
        Log written to log_20260614.txt
        'log_20260614.txt'
    """
    if not isinstance(log_data, list):
        raise ValueError("log_data must be a list of strings.")

    filename = f"log_{datetime.now().strftime('%Y%m%d')}.txt"
    filepath = os.path.join(directory, filename)

    with open(filepath, "w") as file:
        for entry in log_data:
            file.write(f"{entry}\n")

    print(f"Log written to {filename}")
    return filepath


def fetch_data():
    """
    Fetch a sample post from a public placeholder API using `requests`.

    Demonstrates use of an externally installed package (pip install requests).

    Returns:
        dict: The JSON response body if the request succeeds (HTTP 200),
              otherwise an empty dict.
    """
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    if response.status_code == 200:
        return response.json()
    return {}


if __name__ == "__main__":
    # Demonstrate File I/O: write a sample log file
    log_data = ["User logged in", "User updated profile", "Report exported"]
    generate_log(log_data)

    # Demonstrate use of an installed package: fetch data from a public API
    post = fetch_data()
    print("Fetched Post Title:", post.get("title", "No title found"))
