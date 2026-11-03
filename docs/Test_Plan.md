# CSCI 3060U Final Test Plan

**Project:** Digital Games Distribution System Front End

**Team:** Sabre Inc.

## 1. Scope and current status

This plan describes the final 17-case Front End test suite. The suite was consolidated from a larger set of narrowly focused proposed cases; related scenarios now share a test when they can use compatible initial state and remain understandable.

The fixtures and expected files have been statically checked for structure, transaction coverage, record formatting, and session boundaries. They have not yet been executed against the C++ Front End because no executable is currently present in this repository. Expected prompts, messages, and transaction records therefore remain test oracles that must be confirmed during runtime testing.

## 2. Final repository structure

```text
.
|-- docs/
|   |-- AI_Usage_History.md
|   |-- Test_Case_Table.md
|   `-- Test_Plan.md
|-- results/
|   `-- README.txt
|-- scripts/
|   |-- run_tests.bat
|   `-- run_tests.sh
`-- test_cases/
    |-- test_01_valid_login_logout/
    |-- test_02_invalid_session_operations/
    |-- test_03_account_privilege_restrictions/
    |-- test_04_create_valid_user_types/
    |-- test_05_create_invalid_inputs/
    |-- test_06_delete_user_behaviours/
    |-- test_07_sell_behaviours/
    |-- test_08_buy_behaviours/
    |-- test_09_newly_listed_game_next_session/
    |-- test_10_refund_behaviours/
    |-- test_11_standard_addcredit_behaviours/
    |-- test_12_admin_addcredit_behaviours/
    |-- test_13_list_available_games/
    |-- test_14_list_no_available_games/
    |-- test_15_list_active_accounts/
    |-- test_16_malformed_input_recovery/
    |-- test_17_search_behaviours/
    `-- common/
```

See `docs/Test_Case_Table.md` for the requirement coverage of each case.

## 3. Files in each test case

Every test directory contains these three files:

| File | Role |
|---|---|
| `input.txt` | The user input supplied to the Front End through standard input. |
| `expected_output.txt` | Expected prompts, success messages, errors, and listing output. |
| `expected_transactions.txt` | Complete expected Daily Transaction File for the entire input. |

All tests share one starting state in `test_cases/common/`: `current_user_accounts.txt`, `available_games.txt`, and `game_collection.txt`.

## 4. Sessions and Daily Transaction File records

Some consolidated tests contain multiple login/logout sessions in a single transaction stream. The Front End is invoked once per test case and receives the entire stream. Its one Daily Transaction File must contain all successful transaction records and successful session-ending `00` records in chronological order.

Examples:

- A two-session test normally contains two `00` records.
- A rejected `logout` does not create `00`; Test 2 contains two literal `logout` commands but only one succeeds.
- Rejected transactions do not create Daily Transaction File records.
- Read-only `list`, `search`, and assumed `listaccounts` operations are unlogged because no transaction-record format was specified for them.

The runners compare the complete actual daily file with the complete expected file. They do not split session output, so multiple ordered `00` records require no special runner branch.

## 5. Running the suite

### Assumed Front End interface

Both runners currently use this provisional command-line contract:

```text
frontend <accounts_file> <games_file> <collection_file> <daily_output_file>
```

The Front End reads the test's `input.txt` from standard input, writes terminal output to standard output, and writes the combined Daily Transaction File to the fourth path. Confirm this interface when the executable becomes available.

### Linux/macOS

From `scripts/`:

```bash
./run_tests.sh [path-to-frontend-executable]
```

The default executable is `../front_end/frontend`.

### Windows

From `scripts\`:

```bat
run_tests.bat [path-to-frontend.exe]
```

The default executable is `..\front_end\frontend.exe`.

For every `test_*` directory, the runners:

1. Pass the three shared state files from `common/` and a daily-output path to the Front End.
2. Pipe `input.txt` to standard input.
3. Capture console output.
4. Compare console output with `expected_output.txt`.
5. Compare the complete daily output with `expected_transactions.txt`.
6. Store `PASS` or `FAIL`, actual files, and human-readable differences under a timestamped `results/run_*` directory.

The scripts discover test directories dynamically, so the change to 17 cases requires no hard-coded test-count update. Their full-file comparisons already support expected daily files containing multiple `00` records.

## 6. Results and verification status

Each run creates a separate timestamped results directory containing:

```text
results/run_<timestamp>/
|-- summary.txt
|-- test_01_valid_login_logout/
|   |-- actual_console_output.txt
|   |-- actual_daily_transaction_file.txt
|   |-- diff_console.txt
|   |-- diff_daily_transaction.txt
|   `-- RESULT.txt
`-- ...
```

Read `summary.txt` first for the overall result. Use the diff files to investigate mismatched prompts or records, and compare summaries from different runs when checking a change or bug fix.

Current status is static verification only. Do not report these cases as runtime passes until the suite has been run against the actual C++ Front End.

## 7. Professor-added requirements and assumptions

The suite includes all three professor-added requirements:

1. `list` prints all currently available games and relevant seller/price information. Test 13 covers a populated list; Test 14 covers the empty case after every seller is deleted.
2. A privileged transaction prints all active accounts and relevant information. Test 15 covers administrator success, while Test 3 covers non-admin rejection.
3. `search` prints all games and users whose names contain the query, hiding administrators who are not selling games from non-admin users. Test 17 covers a non-admin search, a no-match search, and an admin search.

The exact active-account command, output layout, and Daily Transaction File behavior were not supplied. The suite currently assumes:

- command: `listaccounts`
- fields: username, user type, and available credit
- behavior: privileged, read-only, and unlogged

The command name, exact output layout, and unlogged behavior in Tests 3 and 15 must be adjusted if the professor or TA supplies authoritative details.

The exact SEARCH output layout was not supplied. The suite assumes the command `search` followed by the query on the next line; output `Search results for '<query>':` followed by a `Games:` section (same format as `list`) and a `Users:` section (usernames only), with `  (none)` for an empty section; and read-only, unlogged behavior.
