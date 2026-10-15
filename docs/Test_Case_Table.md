# CSCI 3060U Final Test Case Table

**Project:** Digital Games Distribution System Front End

**Team:** Sabre Inc.

The original, highly granular suite was consolidated into 16 independently runnable test directories. Related valid, invalid, boundary, and permission scenarios are combined where they share compatible input state. Each row below corresponds to one directory under `test_cases/`.

| # | Test directory | Purpose | Main behaviours and constraints covered |
|---|---|---|---|
| 1 | `test_01_valid_login_logout` | Verify a normal session lifecycle. | Existing administrator can log in and log out; logout writes the exact `00` end-of-session record. |
| 2 | `test_02_invalid_session_operations` | Verify invalid session-state handling. | Reject logout and transactions before login, reject an unknown username, reject a second login during an active session, and reject a transaction after logout. Only the successful logout writes `00`. |
| 3 | `test_03_account_privilege_restrictions` | Verify privileged-operation access. | Administrator can perform `create`; a non-admin is rejected from `create`, `delete`, `refund`, and the assumed `listaccounts` command. Rejected operations create no records. |
| 4 | `test_04_create_valid_user_types` | Verify valid account creation. | Administrator creates one `FS`, `BS`, `SS`, and `AA` account; each creates a correctly formatted `01` record. |
| 5 | `test_05_create_invalid_inputs` | Verify invalid account creation. | Reject duplicate username, username longer than 15 characters, and invalid user type; no `01` records are written. |
| 6 | `test_06_delete_user_behaviours` | Verify valid and invalid deletion. | Delete an existing user, reject nonexistent and currently logged-in users, delete a seller with listed inventory, and reject a later transaction on that cancelled inventory. Only valid deletions write `02`. |
| 7 | `test_07_sell_behaviours` | Verify selling and its constraints. | Accept a valid sale; reject a buy-standard seller, a game name over 25 characters, a price over `$999.99`, and a duplicate game name. Only the valid sale writes `03`. |
| 8 | `test_08_buy_behaviours` | Verify buying and its constraints. | Accept a valid purchase; reject a sell-standard buyer, nonexistent game, insufficient credit, and an already-owned game. Only the valid purchase writes `04` with game, seller, buyer, and price. |
| 9 | `test_09_newly_listed_game_next_session` | Verify the session boundary for new listings. | Reject a transaction on a newly listed game during the listing session, then accept it in the next session. Records are ordered `03`, `00`, `04`, `00`. |
| 10 | `test_10_refund_behaviours` | Verify refund processing. | Administrator completes a refund and receives rejections for a nonexistent buyer and nonexistent seller. Only the valid refund writes `05`. |
| 11 | `test_11_standard_addcredit_behaviours` | Verify standard-user credit additions. | Standard user supplies only an amount; reject a single amount over `$1000.00`, accept `$600.00`, and reject a later amount that would exceed the cumulative session limit. |
| 12 | `test_12_admin_addcredit_behaviours` | Verify administrator-targeted credit additions. | Administrator supplies amount followed by username; accept an existing target and reject a nonexistent target. Only the valid addition writes `06`. |
| 13 | `test_13_list_available_games` | Cover the professor-added game-list transaction. | `list` prints every currently available game with seller and price; the read-only command creates no transaction record. |
| 14 | `test_14_list_no_available_games` | Cover the empty state of the game-list transaction. | With an `END`-only Available Games File, `list` reports that no games are available and creates no transaction record. |
| 15 | `test_15_list_active_accounts` | Cover the professor-added privileged active-account listing. | Administrator lists every active account with username, user type, and available credit; the read-only command creates no transaction record. |
| 16 | `test_16_malformed_input_recovery` | Verify graceful recovery from malformed input. | Handle blank input, unknown command, garbage token, and nonnumeric price without crashing; a later valid `create` proves recovery and writes the only non-`00` record. |

## Professor-added transactions

- `list` is covered by Tests 13 and 14 for populated and empty Available Games Files.
- The privileged active-account listing is covered by administrator success in Test 15 and non-admin rejection in Test 3.

The professor did not provide an exact keyword, terminal layout, or Daily Transaction File behavior for the active-account transaction. The fixtures currently assume the keyword `listaccounts`, show username, user type, and available credit, and treat the operation as read-only and unlogged. The command name, exact output layout, and unlogged behavior must be adjusted if the professor or TA provides authoritative details.
