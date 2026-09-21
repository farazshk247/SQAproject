# CSCI 3060U — Phase 1 Test Case Table

**Project:** Digital Games Distribution System — Front End
**Team:** _[fill in team name and member names before submitting]_

Each row corresponds to one folder under `test_cases/`. "Intention" states what
requirement or behavior the test case is meant to verify, referencing the
transaction codes and constraints from the project handout.

| # | Category | Test Case | Intention |
|---|---|---|---|
| 1 | Login | Valid login | An existing user can log in with a correct username and start a session. |
| 2 | Login | Invalid login | A username not present in the Current User Accounts File is rejected and no session starts. |
| 3 | Login | Login before other transactions | No transaction other than `login` is accepted before a session has started. |
| 4 | Login | Login while already logged in | A second `login` is rejected while a session is already active; the first session continues. |
| 5 | Login | Non-admin login restrictions | After logging in as a non-admin (buy-standard) user, privileged transactions like `create` are rejected. |
| 6 | Login | Admin login privileges | After logging in as an admin, privileged transactions (e.g. `create`) are accepted. |
| 7 | Logout | Valid logout | A logged-in user can log out; the session ends and a Daily Transaction File is written. |
| 8 | Logout | Logout before login | `logout` is rejected when no session is active; no Daily Transaction File is written. |
| 9 | Logout | Transaction after logout | No transaction other than `login` is accepted after `logout`, until a new session starts. |
| 10 | Logout | Login after logout | A user can log in again after a prior logout, starting an independent second session. |
| 11 | Create User | Create full-standard user | Admin can create a new user with full-standard (`FS`) privileges. |
| 12 | Create User | Create buy-standard user | Admin can create a new user with buy-standard (`BS`) privileges. |
| 13 | Create User | Create sell-standard user | Admin can create a new user with sell-standard (`SS`) privileges. |
| 14 | Create User | Create admin user | Admin can create a new user with admin (`AA`) privileges. |
| 15 | Create User | Duplicate username | Creating a user whose name matches an existing user is rejected. |
| 16 | Create User | Username over 15 characters | Creating a user whose name exceeds the 15-character limit is rejected. |
| 17 | Create User | Create user as non-admin | A non-admin user cannot perform the privileged `create` transaction. |
| 18 | Create User | Invalid user type | Creating a user with a type other than `AA`/`FS`/`BS`/`SS` is rejected. |
| 19 | Delete User | Delete existing user | Admin can delete an existing user; the deletion is recorded in the Daily Transaction File. |
| 20 | Delete User | Delete nonexistent user | Deleting a username that does not exist is rejected. |
| 21 | Delete User | Delete current user | An admin cannot delete the username they are currently logged in as. |
| 22 | Delete User | Delete user as non-admin | A non-admin user cannot perform the privileged `delete` transaction. |
| 23 | Delete User | Delete user with games for sale | Deleting a user who has games listed for sale succeeds and cancels further transactions on that inventory. |
| 24 | Delete User | Deactivate existing user | Exercises the same "remove a user account" path as `delete` (see `NOTES.txt` — "deactivate" is not a separately defined transaction in the handout). |
| 25 | Sell Game | Valid game sale | A sell-standard (or higher) user can list a new, uniquely-named game at a valid price. |
| 26 | Sell Game | Sell as buy-standard | A buy-standard user cannot perform the `sell` transaction. |
| 27 | Sell Game | Game name over 25 characters | Listing a game whose name exceeds the 25-character limit is rejected. |
| 28 | Sell Game | Price over $999.99 | Listing a game priced above the $999.99 maximum is rejected. |
| 29 | Sell Game | Duplicate game name | Listing a game whose name matches an already-listed game is rejected. |
| 30 | Sell Game | Transaction on newly listed game | A game just listed for sale in one session is not yet purchasable in a following session on the same day, since the master Available Games File is only updated by the overnight Back End run. |
| 31 | Buy Game | Valid purchase | A buy-eligible user can purchase an existing, available game they can afford and don't already own. |
| 32 | Buy Game | Buy as sell-standard | A sell-standard user cannot perform the `buy` transaction. |
| 33 | Buy Game | Game does not exist | Buying a game name not present in the Available Games File is rejected. |
| 34 | Buy Game | Insufficient credit | Buying a game whose price exceeds the buyer's available credit is rejected. |
| 35 | Buy Game | Already own game | Buying a game already present in the buyer's Game Collection File is rejected. |
| 36 | Buy Game | Verify buyer and seller credit changes | A valid purchase's recorded transaction correctly reflects the price to be debited from the buyer and credited to the seller (materialized later by the Back End). |
| 37 | Refund | Valid refund | Admin can transfer a specified credit amount from a seller's balance to a buyer's balance. |
| 38 | Refund | Refund as non-admin | A non-admin user cannot perform the privileged `refund` transaction. |
| 39 | Refund | Invalid buyer or seller | A refund naming a buyer or seller that is not a current user is rejected. |
| 40 | Add Credit | Valid add credit | A standard-account user can add credit to their own account, up to the session limit. |
| 41 | Add Credit | Add credit to nonexistent user | In admin mode, adding credit to a username that does not exist is rejected. |
| 42 | Add Credit | Add more than $1,000 in one session | A single `addcredit` request exceeding the $1,000.00 session cap is rejected. |
| 43 | Add Credit | Multiple additions over $1,000 | The $1,000.00 session cap is enforced cumulatively across multiple `addcredit` transactions in the same session, not just per-transaction. |
| 44 | LIST | List available games | Listing available games for sale displays the current inventory (see `NOTES.txt` — `list` is not one of the 8 transaction codes defined in the provided handout excerpt). |
| 45 | LIST | LIST with no games for sale | Listing available games when the Available Games File contains only the `END` sentinel reports that no games are available. |
| 46 | General | Invalid transaction code | An unrecognized transaction code is reported as an error and does not crash the program. |
| 47 | General | Invalid input | Non-numeric input supplied where a numeric field (e.g. price) is expected is rejected gracefully. |
| 48 | General | Program handles bad input without crashing | Blank lines and garbage tokens interleaved with valid transactions are reported and skipped without crashing or corrupting subsequent transaction processing. |
| 49 | Daily Transaction File | Verify transaction output format | A single session exercising every transaction code (`00`–`06`) is used to check that every Daily Transaction File record is formatted, padded, and delimited exactly per spec. |
| 50 | Daily Transaction File | Verify end-of-session transaction | Checks the exact byte layout of the terminating `00` (end-of-session) record written at logout. |
