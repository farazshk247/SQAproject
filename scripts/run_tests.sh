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
