#!/bin/bash
# Runs every test in ../test_cases against the front end.
# Usage: ./run_tests.sh [-v] [path-to-frontend]   (-v prints the diffs of failed tests)

set -u

VERBOSE=0
if [ "${1:-}" = "-v" ]; then VERBOSE=1; shift; fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEFAULT_EXE="$ROOT/front_end/frontend"
EXE="${1:-$DEFAULT_EXE}"
TESTS="$ROOT/test_cases"
COMMON="$TESTS/common"
LIMIT="${TEST_TIMEOUT:-10}"
RESULTS="$ROOT/results/run_$(date +%Y%m%d_%H%M%S)"
SUMMARY="$RESULTS/summary.txt"

mkdir -p "$RESULTS"

if [ "$EXE" = "$DEFAULT_EXE" ] && [ ! -x "$EXE" ]; then
    echo "Building front end..."
    g++ -std=c++17 -Wall -o "$EXE" "$ROOT"/front_end/*.cpp > "$RESULTS/build.log" 2>&1 \
        || { echo "Build failed, see $RESULTS/build.log"; exit 2; }
fi
[ -x "$EXE" ] || { echo "Front end not found: $EXE"; exit 2; }

TIMEOUT=""
command -v timeout >/dev/null 2>&1 && TIMEOUT="timeout $LIMIT"
command -v gtimeout >/dev/null 2>&1 && TIMEOUT="gtimeout $LIMIT"

pass=0
fail=0
failed=""

printf "%-40s %-6s %s\n" "Test" "Result" "Notes" | tee "$SUMMARY"

for dir in "$TESTS"/test_*/; do
    [ -d "$dir" ] || continue
    name="$(basename "$dir")"
    out="$RESULTS/$name"
    rm -rf "$out"
    mkdir -p "$out"
    cp "$COMMON"/*.txt "$out"/

    $TIMEOUT "$EXE" "$out/current_user_accounts.txt" "$out/available_games.txt" \
        "$out/game_collection.txt" "$out/actual_transactions.txt" \
        < "$dir/input.txt" > "$out/actual_output.txt" 2>&1
    code=$?

    notes=""
    [ "$code" -eq 124 ] && notes="timed out; "
    [ "$code" -ge 128 ] && notes="${notes}crashed; "

    diff -u "$dir/expected_output.txt" "$out/actual_output.txt" \
        > "$out/diff_output.txt" 2>&1 || notes="${notes}output differs; "

    touch "$out/actual_transactions.txt"
    diff -u "$dir/expected_transactions.txt" "$out/actual_transactions.txt" \
        > "$out/diff_transactions.txt" 2>&1 || notes="${notes}transactions differ; "

    if [ -z "$notes" ]; then
        result="PASS"; pass=$((pass + 1))
    else
        result="FAIL"; fail=$((fail + 1)); failed="$failed $name"
    fi
    printf "%-40s %-6s %s\n" "$name" "$result" "${notes%; }" | tee -a "$SUMMARY"
done

if [ $((pass + fail)) -eq 0 ]; then
    echo "No tests found in $TESTS"
    exit 2
fi

echo
echo "Passed: $pass  Failed: $fail" | tee -a "$SUMMARY"
echo "Results saved in $RESULTS"

if [ "$fail" -gt 0 ]; then
    echo
    echo "Failed tests:"
    for name in $failed; do
        echo "  $name"
        if [ "$VERBOSE" -eq 1 ]; then
            cat "$RESULTS/$name"/diff_*.txt | sed 's/^/      /'
        fi
    done
    exit 1
fi