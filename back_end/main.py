"""
Digital Games Distribution System - Back End
CSCI 3060U, Fall 2026 - Team Sabre Inc.

Intention:
    The Back End runs once at the end of each day. It reads the previous
    day's system files and the merged Daily Transaction File written by all
    Front End sessions, applies every transaction in order, and writes the
    updated system files for the next day.

Input files:
    1. Current User Accounts File   (old)
    2. Available Games File         (old)
    3. Game Collection File         (old)
    4. Merged Daily Transaction File

Output files:
    5. New Current User Accounts File
    6. New Available Games File
    7. New Game Collection File

Terminal output:
    One "ERROR: ..." line for each transaction that breaks a constraint
    (the transaction is skipped and processing continues), or one
    "ERROR: fatal - ..." line if an input file is malformed (nothing is
    written and the program exits with code 1).

How to run (from the project folder):
    python3 back_end/main.py <accounts> <games> <collection> <daily_transactions> \\
        <new_accounts> <new_games> <new_collection>
"""

import sys

from backend_app import BackEndApp


def main():
    """Pass the command-line arguments to the Back End and return its exit code."""
    app = BackEndApp()
    return app.start(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
