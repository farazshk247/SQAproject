This folder is intentionally empty until the Front End test suite is executed.

Each run of scripts/run_tests.sh or scripts/run_tests.bat creates a timestamped
subfolder, for example:

    results/run_20261007_143000/
        summary.txt
        test_01_valid_login_logout/
            actual_console_output.txt
            actual_daily_transaction_file.txt
            diff_console.txt
            diff_daily_transaction.txt
            RESULT.txt
        test_02_invalid_session_operations/
            ...
        ...
        test_16_malformed_input_recovery/
            ...

Runs are stored side by side rather than intentionally overwritten. Read
summary.txt first, inspect the per-test diff files for failures, and compare
summaries from separate runs when checking a change or bug fix.

No runtime results are currently recorded here. The fixtures have been
statically verified, but the suite still needs to be run against the C++ Front
End executable. See docs/Test_Plan.md for the full procedure and assumptions.
