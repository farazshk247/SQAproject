# CSCI 3060U Final Test Plan

**Project:** Digital Games Distribution System Front End

**Team:** Sabre Inc.

## 1. Scope and current status

This plan describes the final 16-case Front End test suite. The suite was consolidated from a larger set of narrowly focused proposed cases; related scenarios now share a test when they can use compatible initial state and remain understandable.

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
    `-- test_16_malformed_input_recovery/
```

See `docs/Test_Case_Table.md` for the requirement coverage of each case.

## 3. Files in each test case

Every test directory contains these six standard files:

| File | Role |
|---|---|
| `input_current_user_accounts.txt` | Initial users, account types, and available credit. |
| `input_available_games.txt` | Games initially available for purchase, including seller and price. |
| `input_game_collection.txt` | Initial game ownership used by purchase validation. |
| `input_transaction_stream.txt` | Console commands and responses supplied to the Front End through standard input. |
| `expected_console_output.txt` | Expected prompts, success messages, errors, and listing output. |
| `expected_daily_transaction_file.txt` | Complete expected Daily Transaction File for the entire input stream. |

## 4. Sessions and Daily Transaction File records

Some consolidated tests contain multiple login/logout sessions in a single transaction stream. The Front End is invoked once per test case and receives the entire stream. Its one Daily Transaction File must contain all successful transaction records and successful session-ending `00` records in chronological order.

Examples:

- A two-session test normally contains two `00` records.
- A rejected `logout` does not create `00`; Test 2 contains two literal `logout` commands but only one succeeds.
- Rejected transactions do not create Daily Transaction File records.
- Read-only `list` and assumed `listaccounts` operations are unlogged because no transaction-record format was specified for them.

The runners compare the complete actual daily file with the complete expected file. They do not split session output, so multiple ordered `00` records require no special runner branch.

## 5. Running the suite

### Assumed Front End interface

Both runners currently use this provisional command-line contract:

```text
frontend <accounts_file> <games_file> <collection_file> <daily_output_file>
```

The Front End reads `input_transaction_stream.txt` from standard input, writes terminal output to standard output, and writes the combined Daily Transaction File to the fourth path. Confirm this interface when the executable becomes available.

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

1. Pass the three state files and a daily-output path to the Front End.
2. Pipe the transaction stream to standard input.
3. Capture console output.
4. Compare console output with `expected_console_output.txt`.
5. Compare the complete daily output with `expected_daily_transaction_file.txt`.
6. Store `PASS` or `FAIL`, actual files, and human-readable differences under a timestamped `results/run_*` directory.

The scripts discover test directories dynamically, so the change to 16 cases requires no hard-coded test-count update. Their full-file comparisons already support expected daily files containing multiple `00` records.

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

The suite includes both professor-added requirements:

1. `list` prints all currently available games and relevant seller/price information. Tests 13 and 14 cover populated and empty inventory.
2. A privileged transaction prints all active accounts and relevant information. Test 15 covers administrator success, while Test 3 covers non-admin rejection.

The exact active-account command, output layout, and Daily Transaction File behavior were not supplied. The suite currently assumes:

- command: `listaccounts`
- fields: username, user type, and available credit
- behavior: privileged, read-only, and unlogged

The command name, exact output layout, and unlogged behavior in Tests 3 and 15 must be adjusted if the professor or TA supplies authoritative details.
