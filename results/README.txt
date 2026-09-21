This folder is intentionally empty in the submitted package.

Each time scripts/run_tests.sh (or run_tests.bat) is run, it creates a new
timestamped subfolder here, e.g.:

    results/run_20261002_143000/
        summary.txt
        test_01_valid_login/
            actual_console_output.txt
            actual_daily_transaction_file.txt
            diff_console.txt
            diff_daily_transaction.txt
            RESULT.txt
        test_02_invalid_login/
            ...
        ...

Because runs are timestamped rather than overwritten, every run's results are
kept side by side, so you can diff summary.txt between two runs (e.g. before
and after a bug fix) to see exactly which test cases changed status. See
docs/Test_Plan.md for the full explanation.
