# CSCI 3060U Phase 1 Test Plan

**Project:** Digital Games Distribution System Front End
**Team:** Sabre Inc.
## 1. Overview

This document describes how the 50 test cases in `docs/Test_Case_Table.md` are
organized on disk, how they are run against the Front End, and how run results
are stored so they can be compared across repeated runs (e.g. before/after a
bug fix, or run-to-run as the Front End is built out in later phases).

## 2. Directory structure

```
project/
|-- docs/
|   |-- Test_Case_Table.md          <- Part 1: table of all 50 cases and intentions
|   |-- Test_Plan.md                <- this document
|   `-- generate_fixtures.py        <- script that generated test_cases/ (for provenance)
|-- scripts/
|   |-- run_tests.sh                <- test harness for Linux/macOS
|   `-- run_tests.bat               <- test harness for Windows
|-- test_cases/
|   |-- test_01_valid_login/
|   |-- test_02_invalid_login/
|   |-- ...
|   `-- test_50_verify_end_of_session_transaction/
`-- results/
    `-- run_<timestamp>/            <- created automatically each time the harness runs
```

Actual top-level listing of the submitted package:

```
.
|-- docs
|   `-- generate_fixtures.py
|-- results
|   `-- README.txt
|-- scripts
|   |-- run_tests.bat
|   `-- run_tests.sh
`-- test_cases
    |-- test_01_valid_login
    |-- test_02_invalid_login
    |-- test_03_login_before_other_transactions
    |-- test_04_login_while_already_logged_in
    |-- test_05_non_admin_login_restrictions
    |-- test_06_admin_login_privileges
    |-- test_07_valid_logout
    |-- test_08_logout_before_login
    |-- test_09_transaction_after_logout
    |-- test_10_login_after_logout
    |-- test_11_create_full_standard_user
    |-- test_12_create_buy_standard_user
    |-- test_13_create_sell_standard_user
    |-- test_14_create_admin_user
    |-- test_15_duplicate_username
    |-- test_16_username_over_15_characters
    |-- test_17_create_user_as_non_admin
    |-- test_18_invalid_user_type
    |-- test_19_delete_existing_user
    |-- test_20_delete_nonexistent_user
    |-- test_21_delete_current_user
    |-- test_22_delete_user_as_non_admin
    |-- test_23_delete_user_with_games_for_sale
    |-- test_24_deactivate_existing_user
    |-- test_25_valid_game_sale
    |-- test_26_sell_as_buy_standard
    |-- test_27_game_name_over_25_characters
    |-- test_28_price_over_999_99
    |-- test_29_duplicate_game_name
    |-- test_30_transaction_on_newly_listed_game
    |-- test_31_valid_purchase
    |-- test_32_buy_as_sell_standard
    |-- test_33_game_does_not_exist
    |-- test_34_insufficient_credit
    |-- test_35_already_own_game
    |-- test_36_verify_buyer_and_seller_credit_changes
    |-- test_37_valid_refund
    |-- test_38_refund_as_non_admin
    |-- test_39_invalid_buyer_or_seller
    |-- test_40_valid_add_credit
    |-- test_41_add_credit_to_nonexistent_user
    |-- test_42_add_more_than_1000_in_one_session
    |-- test_43_multiple_additions_over_1000
    |-- test_44_list_available_games
    |-- test_45_list_with_no_games_for_sale
    |-- test_46_invalid_transaction_code
    |-- test_47_invalid_input
    |-- test_48_handles_bad_input_without_crashing
    |-- test_49_verify_transaction_output_format
    `-- test_50_verify_end_of_session_transaction

55 directories, 4 files
```

Each individual test case folder has the same shape, for example:

```
test_cases/test_49_verify_transaction_output_format
|-- NOTES.txt
|-- expected_console_output.txt
|-- expected_daily_transaction_file.txt
|-- input_available_games.txt
|-- input_current_user_accounts.txt
|-- input_game_collection.txt
`-- input_transaction_stream.txt

1 directory, 7 files
```

| File | Role |
|---|---|
| `input_current_user_accounts.txt` | Current User Accounts File fed to the Front End at login |
| `input_available_games.txt` | Available Games File fed to the Front End at login |
| `input_game_collection.txt` | Game Collection File fed to the Front End at login |
| `input_transaction_stream.txt` | The exact lines of text a tester would type at the console, in order (piped to stdin) |
| `expected_console_output.txt` | The prompts/success/error messages the Front End should print |
| `expected_daily_transaction_file.txt` | The Daily Transaction File the Front End should write at logout (or the literal text `N/A ...` if the session never reaches a successful logout) |
| `NOTES.txt` | Present only where the case relies on an assumption or a fixture built specifically for it |

## 3. How the tests are run

Two equivalent harnesses are provided so the suite can run on any team
member's machine or on the TA's:

- **`scripts/run_tests.sh`** — Bash, for Linux/macOS
- **`scripts/run_tests.bat`** — Batch file, for Windows

**Usage:**
```
cd scripts
./run_tests.sh   [path-to-frontend-executable]     # Linux/macOS, defaults to ../front_end/frontend
run_tests.bat    [path-to-frontend.exe]             # Windows, defaults to ..\front_end\frontend.exe
```

**Assumed Front End command-line contract** (both scripts invoke the Front
End the same way — update this section and the invocation line in both
scripts once Phase 2/3 finalizes the real interface):

```
frontend <accounts_file> <games_file> <collection_file> <daily_output_file>
```
- reads the transaction stream on **stdin**
- writes prompts/messages to **stdout**
- writes the Daily Transaction File to the path given as the 4th argument

For each `test_cases/test_NN_*/` folder, the harness:
1. Runs the Front End with that test's three input files and stream, capturing
   stdout to `actual_console_output.txt` and the Daily Transaction File to
   `actual_daily_transaction_file.txt`.
2. Diffs `actual_console_output.txt` against `expected_console_output.txt`.
3. Diffs `actual_daily_transaction_file.txt` against
   `expected_daily_transaction_file.txt` (or, for cases marked `N/A`, checks
   that no daily file was actually produced).
4. Records `PASS` or `FAIL` for that case and appends it to the run's
   `summary.txt`.

### `scripts/run_tests.sh` (full text)

```bash
#!/bin/bash
# run_tests.sh - CSCI 3060U Phase 1 test harness (bash / Linux & macOS)
#
# Runs the Front End executable against every test case in ../test_cases,
# compares actual output to the expected files, and stores a timestamped
# results folder under ../results for reporting and comparison across runs.
#
# Usage:
#   ./run_tests.sh [path-to-frontend-executable]
#
# Assumed Front End command-line contract (update this file + the invocation
# below once Phase 2/3's real CLI is finalized):
#   frontend <accounts_file> <games_file> <collection_file> <daily_output_file>
#   - reads the transaction stream on stdin
#   - writes prompts/messages to stdout

set -u

FRONTEND_EXE="${1:-../front_end/frontend}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEST_ROOT="${SCRIPT_DIR}/../test_cases"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
RESULTS_DIR="${SCRIPT_DIR}/../results/run_${TIMESTAMP}"
SUMMARY="${RESULTS_DIR}/summary.txt"

mkdir -p "$RESULTS_DIR"
PASS_COUNT=0
FAIL_COUNT=0

{
    echo "CSCI 3060U Phase 1 Test Run - ${TIMESTAMP}"
    echo "Front End under test: ${FRONTEND_EXE}"
    echo ""
    printf "%-45s %-6s\n" "Test Case" "Result"
    printf -- "-------------------------------------------------------------\n"
} > "$SUMMARY"

for TEST_DIR in "$TEST_ROOT"/test_*/ ; do
    TEST_NAME="$(basename "$TEST_DIR")"
    OUT_DIR="${RESULTS_DIR}/${TEST_NAME}"
    mkdir -p "$OUT_DIR"

    ACCOUNTS="${TEST_DIR}input_current_user_accounts.txt"
    GAMES="${TEST_DIR}input_available_games.txt"
    COLLECTION="${TEST_DIR}input_game_collection.txt"
    STREAM="${TEST_DIR}input_transaction_stream.txt"
    EXP_CONSOLE="${TEST_DIR}expected_console_output.txt"
    EXP_DAILY="${TEST_DIR}expected_daily_transaction_file.txt"

    ACT_CONSOLE="${OUT_DIR}/actual_console_output.txt"
    ACT_DAILY="${OUT_DIR}/actual_daily_transaction_file.txt"

    "$FRONTEND_EXE" "$ACCOUNTS" "$GAMES" "$COLLECTION" "$ACT_DAILY" \
        < "$STREAM" > "$ACT_CONSOLE" 2>&1

    RESULT="PASS"

    if [ -f "$EXP_CONSOLE" ]; then
        diff -u "$EXP_CONSOLE" "$ACT_CONSOLE" > "${OUT_DIR}/diff_console.txt"
        [ -s "${OUT_DIR}/diff_console.txt" ] && RESULT="FAIL"
    fi

    if grep -q "^N/A" "$EXP_DAILY" 2>/dev/null; then
        # No daily file was expected for this case; fail if one appeared anyway.
        if [ -s "$ACT_DAILY" ]; then
            echo "Daily transaction file was written but none was expected." \
                > "${OUT_DIR}/diff_daily_transaction.txt"
            RESULT="FAIL"
        fi
    else
        diff -u "$EXP_DAILY" "$ACT_DAILY" > "${OUT_DIR}/diff_daily_transaction.txt" 2>&1
        [ -s "${OUT_DIR}/diff_daily_transaction.txt" ] && RESULT="FAIL"
    fi

    echo "$RESULT" > "${OUT_DIR}/RESULT.txt"
    printf "%-45s %-6s\n" "$TEST_NAME" "$RESULT" >> "$SUMMARY"

    if [ "$RESULT" = "PASS" ]; then
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
done

{
    echo ""
    echo "Total: $((PASS_COUNT + FAIL_COUNT))   Passed: ${PASS_COUNT}   Failed: ${FAIL_COUNT}"
} >> "$SUMMARY"

cat "$SUMMARY"
echo ""
echo "Full results stored in: ${RESULTS_DIR}"
```

### `scripts/run_tests.bat` (full text)

```bat
@echo off
setlocal EnableDelayedExpansion

REM run_tests.bat - CSCI 3060U Phase 1 test harness (Windows)
REM
REM Runs the Front End executable against every test case in ..\test_cases,
REM compares actual output to the expected files, and stores a timestamped
REM results folder under ..\results for reporting and comparison across runs.
REM
REM Usage:
REM   run_tests.bat [path-to-frontend.exe]
REM
REM Assumed Front End command-line contract (update this file + the invocation
REM below once Phase 2/3's real CLI is finalized):
REM   frontend.exe <accounts_file> <games_file> <collection_file> <daily_output_file>
REM   - reads the transaction stream on stdin
REM   - writes prompts/messages to stdout

set FRONTEND_EXE=%1
if "%FRONTEND_EXE%"=="" set FRONTEND_EXE=..\front_end\frontend.exe

set SCRIPT_DIR=%~dp0
set TEST_ROOT=%SCRIPT_DIR%..\test_cases

for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set DATESTAMP=%%c%%a%%b
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set TIMESTAMP=%%a%%b
set STAMP=%DATESTAMP%_%TIMESTAMP%

set RESULTS_DIR=%SCRIPT_DIR%..\results\run_%STAMP%
mkdir "%RESULTS_DIR%" 2>nul

set SUMMARY=%RESULTS_DIR%\summary.txt
echo CSCI 3060U Phase 1 Test Run - %STAMP% > "%SUMMARY%"
echo Front End under test: %FRONTEND_EXE% >> "%SUMMARY%"
echo. >> "%SUMMARY%"

set PASS_COUNT=0
set FAIL_COUNT=0

for /d %%T in ("%TEST_ROOT%\test_*") do (
    set TEST_NAME=%%~nxT
    set OUT_DIR=%RESULTS_DIR%\!TEST_NAME!
    mkdir "!OUT_DIR!" 2>nul

    set ACCOUNTS=%%T\input_current_user_accounts.txt
    set GAMES=%%T\input_available_games.txt
    set COLLECTION=%%T\input_game_collection.txt
    set STREAM=%%T\input_transaction_stream.txt
    set EXP_CONSOLE=%%T\expected_console_output.txt
    set EXP_DAILY=%%T\expected_daily_transaction_file.txt
    set ACT_CONSOLE=!OUT_DIR!\actual_console_output.txt
    set ACT_DAILY=!OUT_DIR!\actual_daily_transaction_file.txt

    "%FRONTEND_EXE%" "!ACCOUNTS!" "!GAMES!" "!COLLECTION!" "!ACT_DAILY!" < "!STREAM!" > "!ACT_CONSOLE!" 2>&1

    set RESULT=PASS

    fc "!EXP_CONSOLE!" "!ACT_CONSOLE!" > "!OUT_DIR!\diff_console.txt"
    if not !errorlevel! == 0 set RESULT=FAIL

    findstr /b "N/A" "!EXP_DAILY!" >nul
    if !errorlevel! == 0 (
        if exist "!ACT_DAILY!" (
            echo Daily transaction file was written but none was expected. > "!OUT_DIR!\diff_daily_transaction.txt"
            set RESULT=FAIL
        )
    ) else (
        fc "!EXP_DAILY!" "!ACT_DAILY!" > "!OUT_DIR!\diff_daily_transaction.txt"
        if not !errorlevel! == 0 set RESULT=FAIL
    )

    echo !RESULT! > "!OUT_DIR!\RESULT.txt"
    echo !TEST_NAME! - !RESULT! >> "%SUMMARY%"

    if "!RESULT!"=="PASS" (
        set /a PASS_COUNT+=1
    ) else (
        set /a FAIL_COUNT+=1
    )
)

echo. >> "%SUMMARY%"
echo Passed: %PASS_COUNT%  Failed: %FAIL_COUNT% >> "%SUMMARY%"

type "%SUMMARY%"
echo.
echo Full results stored in: %RESULTS_DIR%
```

## 4. How output is stored and organized for reporting and comparison

Every invocation of either harness creates a **new, timestamped** folder
under `results/`, named `run_<YYYYMMDD_HHMMSS>/`. Nothing is ever overwritten,
so every historical run stays available side by side:

```
results/
|-- run_20261002_140000/
|   |-- summary.txt
|   |-- test_01_valid_login/
|   |   |-- actual_console_output.txt
|   |   |-- actual_daily_transaction_file.txt
|   |   |-- diff_console.txt
|   |   |-- diff_daily_transaction.txt
|   |   `-- RESULT.txt
|   |-- test_02_invalid_login/
|   |   `-- ...
|   `-- ... (one folder per test case)
`-- run_20261005_091500/
    `-- ... (same structure, from a later run)
```

- **`summary.txt`** one line per test case (`test_NN_name  PASS|FAIL`) plus a
  final pass/fail count. This is the file to read first for a quick report,
  and the file to `diff` between two `results/run_*/` folders to see exactly
  which test cases changed status between runs (e.g. after fixing a bug).
- **`actual_console_output.txt` / `actual_daily_transaction_file.txt`** raw
  captured output from that run, kept for archival/debugging even on a pass.
- **`diff_console.txt` / `diff_daily_transaction.txt`** unified diff
  (`diff -u` on Linux/macOS, `fc` output on Windows) against the expected
  files; empty on a pass, non-empty and human-readable on a failure.
- **`RESULT.txt`** single word, `PASS` or `FAIL`, for easy scripting/grepping.

To compare two runs at a glance:
```
diff results/run_20261002_140000/summary.txt results/run_20261005_091500/summary.txt
```

## 5. Assumptions and open items

- The Front End's exact command-line interface is not finalized until later
  phases; the harnesses assume
  `frontend <accounts> <games> <collection> <daily_output> < transactions > console_output`.
  Once Phase 2/3 fixes the real interface, update the single invocation line
  in each script (marked with a comment) rather than restructuring the harness.
- Byte-exact field widths used in the expected output files follow the
  convention documented in `test_cases/*/NOTES.txt`-adjacent material (see the
  fixture generator, `docs/generate_fixtures.py`) — reconcile with the TA's
  clarification if the handout's stated widths are corrected before Phase 3.
- `list` (test cases 44–45) is treated as an unlogged, read-only transaction
  since it is not one of the 8 transaction codes defined in the provided
  handout excerpt; confirm its real behavior before relying on these two
  cases for grading purposes.
