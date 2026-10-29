#!/bin/bash
# run_tests.sh - runs all of our front end tests (CSCI 3060U, Phase 3)
#
# For every folder in ../test_cases it runs the front end, then compares what
# it printed and the daily transaction file it wrote against the expected
# files. Everything gets saved in ../results/run_<date_time>.
#
# How to run (from the scripts folder):
#   ./run_tests.sh [-v] [path-to-frontend]
#     -v   show the diffs for the failed tests at the end
#   the default front end is ../front_end/frontend
#   TEST_TIMEOUT=30 ./run_tests.sh   changes the 10 second limit per test
#
# The front end gets called like this:
#   frontend <accounts_file> <games_file> <collection_file> <daily_output_file>
#   (commands come in on stdin, prompts and messages go to stdout)
#
# Exit code: 0 = everything passed, 1 = some tests failed, 2 = couldn't run

set -u

usage() {
    echo "Usage: $0 [-v] [path-to-frontend-executable]"
    echo "  -v   print the diffs of failing tests at the end"
}

VERBOSE=0
while getopts "vh" opt; do
    case "$opt" in
        v) VERBOSE=1 ;;
        h) usage; exit 0 ;;
        *) usage >&2; exit 2 ;;
    esac
done
shift $((OPTIND - 1))

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
FRONTEND_EXE="${1:-${ROOT_DIR}/front_end/frontend}"
TEST_ROOT="${ROOT_DIR}/test_cases"
TEST_TIMEOUT="${TEST_TIMEOUT:-10}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
RESULTS_ROOT="${ROOT_DIR}/results"
RESULTS_DIR="${RESULTS_ROOT}/run_${TIMESTAMP}"
SUMMARY="${RESULTS_DIR}/summary.txt"

# ---- sanity checks -------------------------------------------------------
if [ ! -f "$FRONTEND_EXE" ] || [ ! -x "$FRONTEND_EXE" ]; then
    echo "ERROR: Front End executable not found or not executable: $FRONTEND_EXE" >&2
    echo "Build it first, or pass its path:  $0 path/to/frontend" >&2
    exit 2
fi
if [ ! -d "$TEST_ROOT" ]; then
    echo "ERROR: test directory not found: $TEST_ROOT" >&2
    exit 2
fi

# Use a per-test time limit if the system has timeout (gtimeout on macOS+brew).
TIMEOUT_CMD=""
if command -v timeout >/dev/null 2>&1; then
    TIMEOUT_CMD="timeout"
elif command -v gtimeout >/dev/null 2>&1; then
    TIMEOUT_CMD="gtimeout"
fi
RUNNER=()
if [ -n "$TIMEOUT_CMD" ]; then
    RUNNER=("$TIMEOUT_CMD" "$TEST_TIMEOUT")
fi

mkdir -p "$RESULTS_DIR"
PASS_COUNT=0
FAIL_COUNT=0
FAILED_TESTS=()

{
    echo "CSCI 3060U Phase 3 Test Run - ${TIMESTAMP}"
    echo "Front End under test: ${FRONTEND_EXE}"
    echo ""
    printf "%-45s %-6s %s\n" "Test Case" "Result" "Notes"
    printf -- "---------------------------------------------------------------------------\n"
} > "$SUMMARY"

# ---- run every test_* directory -----------------------------------------
for TEST_DIR in "$TEST_ROOT"/test_*/ ; do
    [ -d "$TEST_DIR" ] || continue
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

    RESULT="PASS"
    NOTES=""

    # Run the Front End (${RUNNER[@]+...} keeps old bash 3.2 on macOS happy).
    ${RUNNER[@]+"${RUNNER[@]}"} "$FRONTEND_EXE" "$ACCOUNTS" "$GAMES" "$COLLECTION" "$ACT_DAILY" \
        < "$STREAM" > "$ACT_CONSOLE" 2>&1
    STATUS=$?

    if [ "$STATUS" -eq 124 ] && [ -n "$TIMEOUT_CMD" ]; then
        RESULT="FAIL"; NOTES="${NOTES}timed out after ${TEST_TIMEOUT}s; "
    elif [ "$STATUS" -ge 128 ]; then
        RESULT="FAIL"; NOTES="${NOTES}crashed (signal $((STATUS - 128))); "
    fi

    # Console output
    if [ -f "$EXP_CONSOLE" ]; then
        diff -u "$EXP_CONSOLE" "$ACT_CONSOLE" > "${OUT_DIR}/diff_console.txt" 2>&1
        if [ -s "${OUT_DIR}/diff_console.txt" ]; then
            RESULT="FAIL"; NOTES="${NOTES}console output differs; "
        fi
    else
        echo "Missing expected file: $EXP_CONSOLE" > "${OUT_DIR}/diff_console.txt"
        RESULT="FAIL"; NOTES="${NOTES}missing expected console file; "
    fi

    # Daily Transaction File
    if [ ! -f "$EXP_DAILY" ]; then
        echo "Missing expected file: $EXP_DAILY" > "${OUT_DIR}/diff_daily_transaction.txt"
        RESULT="FAIL"; NOTES="${NOTES}missing expected daily file; "
    elif grep -q "^N/A" "$EXP_DAILY" 2>/dev/null; then
        # No daily file content was expected for this case.
        if [ -s "$ACT_DAILY" ]; then
            echo "Daily transaction file was written but none was expected." \
                > "${OUT_DIR}/diff_daily_transaction.txt"
            RESULT="FAIL"; NOTES="${NOTES}unexpected daily file; "
        else
            : > "${OUT_DIR}/diff_daily_transaction.txt"
        fi
    else
        diff -u "$EXP_DAILY" "$ACT_DAILY" > "${OUT_DIR}/diff_daily_transaction.txt" 2>&1
        if [ -s "${OUT_DIR}/diff_daily_transaction.txt" ]; then
            RESULT="FAIL"; NOTES="${NOTES}daily file differs; "
        fi
    fi

    echo "$RESULT" > "${OUT_DIR}/RESULT.txt"
    printf "%-45s %-6s %s\n" "$TEST_NAME" "$RESULT" "${NOTES%; }" >> "$SUMMARY"

    if [ "$RESULT" = "PASS" ]; then
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        FAIL_COUNT=$((FAIL_COUNT + 1))
        FAILED_TESTS+=("$TEST_NAME")
    fi
done

TOTAL=$((PASS_COUNT + FAIL_COUNT))
if [ "$TOTAL" -eq 0 ]; then
    echo "ERROR: no test_* directories found in $TEST_ROOT" >&2
    exit 2
fi

{
    echo ""
    echo "Total: ${TOTAL}   Passed: ${PASS_COUNT}   Failed: ${FAIL_COUNT}"
} >> "$SUMMARY"

# Handy shortcut to the newest results (ignored if the file system has no symlinks).
ln -sfn "run_${TIMESTAMP}" "${RESULTS_ROOT}/latest" 2>/dev/null || true

cat "$SUMMARY"
echo ""
echo "Full results stored in: ${RESULTS_DIR}"

if [ "$FAIL_COUNT" -gt 0 ]; then
    echo ""
    echo "Failing tests (see diff_console.txt / diff_daily_transaction.txt in each folder):"
    for T in "${FAILED_TESTS[@]}"; do
        echo "  - $T"
        if [ "$VERBOSE" -eq 1 ]; then
            for F in diff_console.txt diff_daily_transaction.txt; do
                if [ -s "${RESULTS_DIR}/${T}/${F}" ]; then
                    echo "    --- ${F}"
                    sed 's/^/    /' "${RESULTS_DIR}/${T}/${F}"
                fi
            done
        fi
    done
    exit 1
fi
exit 0