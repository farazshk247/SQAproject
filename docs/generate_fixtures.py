#!/usr/bin/env python3
"""
CSCI 3060U Phase 1 - Test Case Fixture Generator
Generates input files and expected-output files (as text printouts) for all 50 test cases.
"""
import os
import shutil

ROOT = "/home/claude/build/output"
if os.path.exists(ROOT):
    shutil.rmtree(ROOT)
os.makedirs(ROOT)

# ---------- Field width convention (see README) ----------
U_W = 15   # username field
T_W = 2    # user type field
C_W = 9    # credit field, format DDDDDD.DD
G_W = 25   # game name field
P_W = 6    # price field, format DDD.DD

def uf(s):
    return (s or "").ljust(U_W)[:U_W]

def tf(s):
    return (s or "").ljust(T_W)[:T_W]

def cf(amount):
    if amount is None:
        return "0" * C_W
    return f"{amount:0{C_W}.2f}"

def cf_blank():
    return " " * C_W

def gf(s):
    return (s or "").ljust(G_W)[:G_W]

def pf(amount):
    if amount is None:
        return "0" * P_W
    return f"{amount:0{P_W}.2f}"

SP = " "

# ---------- Master file line builders ----------
def account_line(username, utype, credit):
    return f"{uf(username)}{SP}{tf(utype)}{SP}{cf(credit)}"

def account_end_line():
    return f"{uf('END')}{SP}{tf('')}{SP}{cf_blank()}"

def game_line(name, seller, price):
    return f"{gf(name)}{SP}{uf(seller)}{SP}{pf(price)}"

def game_end_line():
    return f"{gf('END')}{SP}{uf('')}{SP}{pf(None)}"

def collection_line(name, owner):
    return f"{gf(name)}{SP}{uf(owner)}"

def collection_end_line():
    return f"{gf('END')}{SP}{uf('')}"

# ---------- Daily Transaction File line builders ----------
def txn_create(username, utype, credit=0.0):
    return f"01{SP}{uf(username)}{SP}{tf(utype)}{SP}{cf(credit)}"

def txn_delete(username):
    return f"02{SP}{uf(username)}{SP}{tf('')}{SP}{cf(None)}"

def txn_sell(game, seller, price):
    return f"03{SP}{gf(game)}{SP}{uf(seller)}{SP}{pf(price)}"

def txn_buy(game, seller, buyer, price):
    return f"04{SP}{gf(game)}{SP}{uf(seller)}{SP}{uf(buyer)}{SP}{pf(price)}"

def txn_refund(buyer, seller, amount):
    return f"05{SP}{uf(buyer)}{SP}{uf(seller)}{SP}{cf(amount)}"

def txn_addcredit(username, amount):
    return f"06{SP}{uf(username)}{SP}{tf('')}{SP}{cf(amount)}"

def txn_end():
    return f"00{SP}{uf('')}{SP}{tf('')}{SP}{cf(None)}"

# ---------- Default fixtures ----------
DEFAULT_ACCOUNTS = [
    account_line("admin1", "AA", 1000.00),
    account_line("fulluser1", "FS", 500.00),
    account_line("buyer1", "BS", 300.00),
    account_line("seller1", "SS", 200.00),
    account_end_line(),
]

DEFAULT_GAMES = [
    game_line("Stardew_Valley", "seller1", 15.00),
    game_line("Hollow_Knight", "seller1", 10.00),
    game_end_line(),
]

EMPTY_GAMES = [
    game_end_line(),
]

DEFAULT_COLLECTION = [
    collection_end_line(),
]

def write_lines(path, lines):
    with open(path, "w", newline="\n") as f:
        for line in lines:
            f.write(line + "\n")

def write_text(path, text):
    with open(path, "w", newline="\n") as f:
        f.write(text)

def make_case(num, slug, *, accounts=None, games=None, collection=None,
              stdin_lines, console_lines, daily_files, notes=""):
    """
    daily_files: list of transaction-line-lists, one per logout in the session
                 (usually 0 or 1; test 10 has 2). Empty list => no daily file produced.
    """
    dirname = os.path.join(ROOT, f"test_{num:02d}_{slug}")
    os.makedirs(dirname, exist_ok=True)

    accounts = accounts if accounts is not None else DEFAULT_ACCOUNTS
    games = games if games is not None else DEFAULT_GAMES
    collection = collection if collection is not None else DEFAULT_COLLECTION

    write_lines(os.path.join(dirname, "input_current_user_accounts.txt"), accounts)
    write_lines(os.path.join(dirname, "input_available_games.txt"), games)
    write_lines(os.path.join(dirname, "input_game_collection.txt"), collection)
    write_lines(os.path.join(dirname, "input_transaction_stream.txt"), stdin_lines)
    write_lines(os.path.join(dirname, "expected_console_output.txt"), console_lines)

    if not daily_files:
        write_text(os.path.join(dirname, "expected_daily_transaction_file.txt"),
                    "N/A -- no logout was successfully processed in this session, "
                    "so no Daily Transaction File is written.\n")
    elif len(daily_files) == 1:
        write_lines(os.path.join(dirname, "expected_daily_transaction_file.txt"), daily_files[0])
    else:
        for i, dfile in enumerate(daily_files, start=1):
            write_lines(os.path.join(dirname, f"expected_daily_transaction_file_session{i}.txt"), dfile)

    if notes:
        write_text(os.path.join(dirname, "NOTES.txt"), notes.strip() + "\n")

# ============================================================
# LOGIN
# ============================================================

make_case(1, "valid_login",
    stdin_lines=["login", "admin1", "logout"],
    console_lines=[
        "Username: ",
        "Login successful. Welcome admin1 (admin).",
        "Logged out. Daily transaction file written.",
    ],
    daily_files=[[txn_end()]],
)

make_case(2, "invalid_login",
    stdin_lines=["login", "ghostuser"],
    console_lines=[
        "Username: ",
        "Error: invalid username. Login failed.",
    ],
    daily_files=[],
    notes="No user named 'ghostuser' exists in input_current_user_accounts.txt. "
          "Front End should reject the login and remain awaiting a new transaction code.",
)

make_case(3, "login_before_other_transactions",
    stdin_lines=["sell", "Celeste", "12.50", "login", "admin1", "logout"],
    console_lines=[
        "Error: you must login before any other transaction.",
        "Username: ",
        "Login successful. Welcome admin1 (admin).",
        "Logged out. Daily transaction file written.",
    ],
    daily_files=[[txn_end()]],
    notes="The leading 'sell' transaction is issued before any login and must be rejected "
          "and not recorded; the subsequent login/logout should proceed normally.",
)

make_case(4, "login_while_already_logged_in",
    stdin_lines=["login", "admin1", "login", "fulluser1", "logout"],
    console_lines=[
        "Username: ",
        "Login successful. Welcome admin1 (admin).",
        "Error: already logged in. Login ignored.",
        "Logged out. Daily transaction file written.",
    ],
    daily_files=[[txn_end()]],
    notes="Second 'login' attempt while admin1's session is active must be rejected; "
          "session remains admin1's, and the eventual logout closes admin1's session.",
)

make_case(5, "non_admin_login_restrictions",
    stdin_lines=["login", "buyer1", "create", "newuser1", "FS", "logout"],
    console_lines=[
        "Username: ",
        "Login successful. Welcome buyer1 (buy-standard).",
        "Error: insufficient privileges for 'create'.",
        "Logged out. Daily transaction file written.",
    ],
    daily_files=[[txn_end()]],
    notes="buyer1 is buy-standard (non-admin); the privileged 'create' transaction must be rejected.",
)

make_case(6, "admin_login_privileges",
    stdin_lines=["login", "admin1", "create", "newuser2", "FS", "logout"],
    console_lines=[
        "Username: ",
        "Login successful. Welcome admin1 (admin).",
        "User 'newuser2' created successfully.",
        "Logged out. Daily transaction file written.",
    ],
    daily_files=[[txn_create("newuser2", "FS", 0.00), txn_end()]],
)

# ============================================================
# LOGOUT
# ============================================================

make_case(7, "valid_logout",
    stdin_lines=["login", "fulluser1", "logout"],
    console_lines=[
        "Username: ",
        "Login successful. Welcome fulluser1 (full-standard).",
        "Logged out. Daily transaction file written.",
    ],
    daily_files=[[txn_end()]],
)

make_case(8, "logout_before_login",
    stdin_lines=["logout"],
    console_lines=[
        "Error: not logged in. Logout ignored.",
    ],
    daily_files=[],
)

make_case(9, "transaction_after_logout",
    stdin_lines=["login", "admin1", "logout", "create", "newuser3", "FS"],
    console_lines=[
        "Username: ",
        "Login successful. Welcome admin1 (admin).",
        "Logged out. Daily transaction file written.",
        "Error: you must login before any other transaction.",
    ],
    daily_files=[[txn_end()]],
    notes="'create' issued after logout, with no new login, must be rejected and not recorded.",
)

make_case(10, "login_after_logout",
    stdin_lines=["login", "admin1", "logout", "login", "fulluser1", "logout"],
    console_lines=[
        "Username: ",
        "Login successful. Welcome admin1 (admin).",
        "Logged out. Daily transaction file written.",
        "Username: ",
        "Login successful. Welcome fulluser1 (full-standard).",
        "Logged out. Daily transaction file written.",
    ],
    daily_files=[[txn_end()], [txn_end()]],
    notes="Two full login/logout cycles in one run; each logout writes its own Daily Transaction File.",
)

# ============================================================
# CREATE USER
# ============================================================

make_case(11, "create_full_standard_user",
    stdin_lines=["login", "admin1", "create", "fsuser1", "FS", "logout"],
    console_lines=["Username: ", "Login successful. Welcome admin1 (admin).",
                   "User 'fsuser1' created successfully.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_create("fsuser1", "FS", 0.00), txn_end()]],
)

make_case(12, "create_buy_standard_user",
    stdin_lines=["login", "admin1", "create", "bsuser1", "BS", "logout"],
    console_lines=["Username: ", "Login successful. Welcome admin1 (admin).",
                   "User 'bsuser1' created successfully.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_create("bsuser1", "BS", 0.00), txn_end()]],
)

make_case(13, "create_sell_standard_user",
    stdin_lines=["login", "admin1", "create", "ssuser1", "SS", "logout"],
    console_lines=["Username: ", "Login successful. Welcome admin1 (admin).",
                   "User 'ssuser1' created successfully.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_create("ssuser1", "SS", 0.00), txn_end()]],
)

make_case(14, "create_admin_user",
    stdin_lines=["login", "admin1", "create", "admin2", "AA", "logout"],
    console_lines=["Username: ", "Login successful. Welcome admin1 (admin).",
                   "User 'admin2' created successfully.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_create("admin2", "AA", 0.00), txn_end()]],
)

make_case(15, "duplicate_username",
    stdin_lines=["login", "admin1", "create", "admin1", "FS", "logout"],
    console_lines=["Username: ", "Login successful. Welcome admin1 (admin).",
                   "Error: username 'admin1' already exists.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
)

make_case(16, "username_over_15_characters",
    stdin_lines=["login", "admin1", "create", "ThisUsernameIsWayTooLong", "FS", "logout"],
    console_lines=["Username: ", "Login successful. Welcome admin1 (admin).",
                   "Error: username exceeds 15 characters.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
)

make_case(17, "create_user_as_non_admin",
    stdin_lines=["login", "fulluser1", "create", "newuser4", "FS", "logout"],
    console_lines=["Username: ", "Login successful. Welcome fulluser1 (full-standard).",
                   "Error: insufficient privileges for 'create'.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
)

make_case(18, "invalid_user_type",
    stdin_lines=["login", "admin1", "create", "newuser5", "XX", "logout"],
    console_lines=["Username: ", "Login successful. Welcome admin1 (admin).",
                   "Error: invalid user type 'XX'.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
)

# ============================================================
# DELETE USER
# ============================================================

make_case(19, "delete_existing_user",
    stdin_lines=["login", "admin1", "delete", "fulluser1", "logout"],
    console_lines=["Username: ", "Login successful. Welcome admin1 (admin).",
                   "User 'fulluser1' deleted successfully.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_delete("fulluser1"), txn_end()]],
)

make_case(20, "delete_nonexistent_user",
    stdin_lines=["login", "admin1", "delete", "ghostuser", "logout"],
    console_lines=["Username: ", "Login successful. Welcome admin1 (admin).",
                   "Error: user 'ghostuser' does not exist.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
)

make_case(21, "delete_current_user",
    stdin_lines=["login", "admin1", "delete", "admin1", "logout"],
    console_lines=["Username: ", "Login successful. Welcome admin1 (admin).",
                   "Error: cannot delete the currently logged in user.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
)

make_case(22, "delete_user_as_non_admin",
    stdin_lines=["login", "fulluser1", "delete", "buyer1", "logout"],
    console_lines=["Username: ", "Login successful. Welcome fulluser1 (full-standard).",
                   "Error: insufficient privileges for 'delete'.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
)

make_case(23, "delete_user_with_games_for_sale",
    stdin_lines=["login", "admin1", "delete", "seller1", "logout"],
    console_lines=["Username: ", "Login successful. Welcome admin1 (admin).",
                   "User 'seller1' deleted successfully. Associated games for sale removed.",
                   "Logged out. Daily transaction file written."],
    daily_files=[[txn_delete("seller1"), txn_end()]],
    notes="seller1 has Stardew_Valley and Hollow_Knight listed in input_available_games.txt; "
          "deletion must cancel further transactions on that inventory.",
)

make_case(24, "deactivate_existing_user",
    stdin_lines=["login", "admin1", "delete", "buyer1", "logout"],
    console_lines=["Username: ", "Login successful. Welcome admin1 (admin).",
                   "User 'buyer1' deleted successfully.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_delete("buyer1"), txn_end()]],
    notes="'Deactivate' is not a transaction code defined in the project spec handout (only "
          "login/logout/create/delete/sell/buy/refund/addcredit are defined). This case is built "
          "as an additional 'delete' scenario -- confirm with your TA whether a distinct "
          "deactivate (soft-delete) transaction is actually expected.",
)

# ============================================================
# SELL GAME
# ============================================================

make_case(25, "valid_game_sale",
    stdin_lines=["login", "seller1", "sell", "Celeste", "12.50", "logout"],
    console_lines=["Username: ", "Login successful. Welcome seller1 (sell-standard).",
                   "Game 'Celeste' listed for sale at $12.50.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_sell("Celeste", "seller1", 12.50), txn_end()]],
)

make_case(26, "sell_as_buy_standard",
    stdin_lines=["login", "buyer1", "sell", "Celeste", "12.50", "logout"],
    console_lines=["Username: ", "Login successful. Welcome buyer1 (buy-standard).",
                   "Error: insufficient privileges for 'sell'.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
)

make_case(27, "game_name_over_25_characters",
    stdin_lines=["login", "seller1", "sell", "ThisGameNameIsDefinitelyWayTooLong", "10.00", "logout"],
    console_lines=["Username: ", "Login successful. Welcome seller1 (sell-standard).",
                   "Error: game name exceeds 25 characters.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
)

make_case(28, "price_over_999_99",
    stdin_lines=["login", "seller1", "sell", "ExpensiveGame", "1500.00", "logout"],
    console_lines=["Username: ", "Login successful. Welcome seller1 (sell-standard).",
                   "Error: price exceeds maximum of $999.99.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
)

make_case(29, "duplicate_game_name",
    stdin_lines=["login", "seller1", "sell", "Stardew_Valley", "20.00", "logout"],
    console_lines=["Username: ", "Login successful. Welcome seller1 (sell-standard).",
                   "Error: game 'Stardew_Valley' already exists.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
)

make_case(30, "transaction_on_newly_listed_game",
    stdin_lines=["login", "seller1", "sell", "Celeste", "12.50", "logout",
                 "login", "buyer1", "buy", "Celeste", "seller1", "logout"],
    console_lines=[
        "Username: ", "Login successful. Welcome seller1 (sell-standard).",
        "Game 'Celeste' listed for sale at $12.50.", "Logged out. Daily transaction file written.",
        "Username: ", "Login successful. Welcome buyer1 (buy-standard).",
        "Error: game 'Celeste' does not exist.", "Logged out. Daily transaction file written.",
    ],
    daily_files=[[txn_sell("Celeste", "seller1", 12.50), txn_end()], [txn_end()]],
    notes="A game listed via 'sell' only appears in the Available Games File after the overnight "
          "Back End batch run. A second Front End session on the same day still reads the old "
          "input_available_games.txt, so 'Celeste' is correctly not purchasable yet.",
)

# ============================================================
# BUY GAME
# ============================================================

make_case(31, "valid_purchase",
    stdin_lines=["login", "buyer1", "buy", "Stardew_Valley", "seller1", "logout"],
    console_lines=["Username: ", "Login successful. Welcome buyer1 (buy-standard).",
                   "Purchased 'Stardew_Valley' from seller1 for $15.00.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_buy("Stardew_Valley", "seller1", "buyer1", 15.00), txn_end()]],
)

make_case(32, "buy_as_sell_standard",
    accounts=DEFAULT_ACCOUNTS[:-1] + [account_line("ssuser1", "SS", 300.00), account_end_line()],
    stdin_lines=["login", "ssuser1", "buy", "Hollow_Knight", "seller1", "logout"],
    console_lines=["Username: ", "Login successful. Welcome ssuser1 (sell-standard).",
                   "Error: insufficient privileges for 'buy'.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
    notes="ssuser1 is sell-standard, added to input_current_user_accounts.txt specifically for this case.",
)

make_case(33, "game_does_not_exist",
    stdin_lines=["login", "buyer1", "buy", "NoSuchGame", "seller1", "logout"],
    console_lines=["Username: ", "Login successful. Welcome buyer1 (buy-standard).",
                   "Error: game 'NoSuchGame' does not exist.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
)

make_case(34, "insufficient_credit",
    accounts=DEFAULT_ACCOUNTS[:-1] + [account_line("poorbuyer", "BS", 5.00), account_end_line()],
    stdin_lines=["login", "poorbuyer", "buy", "Stardew_Valley", "seller1", "logout"],
    console_lines=["Username: ", "Login successful. Welcome poorbuyer (buy-standard).",
                   "Error: insufficient credit to purchase 'Stardew_Valley' ($15.00).",
                   "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
    notes="poorbuyer has $5.00, less than Stardew_Valley's $15.00 price.",
)

make_case(35, "already_own_game",
    collection=[collection_line("Stardew_Valley", "buyer1"), collection_end_line()],
    stdin_lines=["login", "buyer1", "buy", "Stardew_Valley", "seller1", "logout"],
    console_lines=["Username: ", "Login successful. Welcome buyer1 (buy-standard).",
                   "Error: you already own 'Stardew_Valley'.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
    notes="input_game_collection.txt pre-seeded to show buyer1 already owns Stardew_Valley.",
)

make_case(36, "verify_buyer_and_seller_credit_changes",
    stdin_lines=["login", "buyer1", "buy", "Stardew_Valley", "seller1", "logout"],
    console_lines=["Username: ", "Login successful. Welcome buyer1 (buy-standard).",
                   "Purchased 'Stardew_Valley' from seller1 for $15.00.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_buy("Stardew_Valley", "seller1", "buyer1", 15.00), txn_end()]],
    notes="Credit balances themselves are only materialized in the Current User Accounts File by "
          "the Back End (Phase 4/5), not by the Front End. This case's Daily Transaction File "
          "record is what the Back End will use to apply: buyer1 300.00 -> 285.00, "
          "seller1 200.00 -> 215.00. Expected post-Back-End account lines:\n"
          f"  {account_line('buyer1', 'BS', 285.00)}\n"
          f"  {account_line('seller1', 'SS', 215.00)}",
)

# ============================================================
# REFUND
# ============================================================

make_case(37, "valid_refund",
    stdin_lines=["login", "admin1", "refund", "buyer1", "seller1", "10.00", "logout"],
    console_lines=["Username: ", "Login successful. Welcome admin1 (admin).",
                   "Refund of $10.00 processed from seller1 to buyer1.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_refund("buyer1", "seller1", 10.00), txn_end()]],
)

make_case(38, "refund_as_non_admin",
    stdin_lines=["login", "fulluser1", "refund", "buyer1", "seller1", "10.00", "logout"],
    console_lines=["Username: ", "Login successful. Welcome fulluser1 (full-standard).",
                   "Error: insufficient privileges for 'refund'.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
)

make_case(39, "invalid_buyer_or_seller",
    stdin_lines=["login", "admin1", "refund", "ghostbuyer", "seller1", "10.00", "logout"],
    console_lines=["Username: ", "Login successful. Welcome admin1 (admin).",
                   "Error: buyer 'ghostbuyer' does not exist.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
)

# ============================================================
# ADD CREDIT
# ============================================================

make_case(40, "valid_add_credit",
    stdin_lines=["login", "buyer1", "addcredit", "50.00", "logout"],
    console_lines=["Username: ", "Login successful. Welcome buyer1 (buy-standard).",
                   "Added $50.00 credit to your account.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_addcredit("buyer1", 50.00), txn_end()]],
    notes="Standard (non-admin) accounts only supply the amount; the username in the transaction "
          "record is the logged-in user (buyer1).",
)

make_case(41, "add_credit_to_nonexistent_user",
    stdin_lines=["login", "admin1", "addcredit", "50.00", "ghostuser", "logout"],
    console_lines=["Username: ", "Login successful. Welcome admin1 (admin).",
                   "Error: user 'ghostuser' does not exist.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
    notes="Admin mode order per spec: amount is asked first, then the target username.",
)

make_case(42, "add_more_than_1000_in_one_session",
    stdin_lines=["login", "buyer1", "addcredit", "1500.00", "logout"],
    console_lines=["Username: ", "Login successful. Welcome buyer1 (buy-standard).",
                   "Error: cannot add more than $1000.00 of credit in a single session.",
                   "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
)

make_case(43, "multiple_additions_over_1000",
    stdin_lines=["login", "buyer1", "addcredit", "600.00", "addcredit", "500.00", "logout"],
    console_lines=["Username: ", "Login successful. Welcome buyer1 (buy-standard).",
                   "Added $600.00 credit to your account.",
                   "Error: cannot add more than $1000.00 of credit in a single session "
                   "(600.00 already added this session).",
                   "Logged out. Daily transaction file written."],
    daily_files=[[txn_addcredit("buyer1", 600.00), txn_end()]],
    notes="Session cumulative total is tracked across multiple addcredit transactions; "
          "600.00 + 500.00 = 1100.00 exceeds the $1000.00 session cap, so only the first is recorded.",
)

# ============================================================
# LIST
# ============================================================

make_case(44, "list_available_games",
    stdin_lines=["login", "buyer1", "list", "logout"],
    console_lines=["Username: ", "Login successful. Welcome buyer1 (buy-standard).",
                   "Available games:",
                   "  Stardew_Valley - seller1 - $15.00",
                   "  Hollow_Knight - seller1 - $10.00",
                   "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
    notes="'list' is NOT one of the 8 transaction codes defined in the project handout excerpt "
          "provided (login/logout/create/delete/sell/buy/refund/addcredit). It is not part of the "
          "documented Daily Transaction File format either, so it is treated here as a read-only, "
          "unlogged transaction. Confirm this behavior with your TA/course Slack before relying on it.",
)

make_case(45, "list_with_no_games_for_sale",
    games=EMPTY_GAMES,
    stdin_lines=["login", "buyer1", "list", "logout"],
    console_lines=["Username: ", "Login successful. Welcome buyer1 (buy-standard).",
                   "No games currently available for sale.",
                   "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
    notes="input_available_games.txt contains only the END sentinel line.",
)

# ============================================================
# GENERAL REQUIREMENTS
# ============================================================

make_case(46, "invalid_transaction_code",
    stdin_lines=["login", "admin1", "frobnicate", "logout"],
    console_lines=["Username: ", "Login successful. Welcome admin1 (admin).",
                   "Error: 'frobnicate' is not a recognized transaction code.",
                   "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
)

make_case(47, "invalid_input",
    stdin_lines=["login", "seller1", "sell", "Celeste", "abc", "logout"],
    console_lines=["Username: ", "Login successful. Welcome seller1 (sell-standard).",
                   "Error: 'abc' is not a valid price.", "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
)

make_case(48, "handles_bad_input_without_crashing",
    stdin_lines=["login", "admin1", "", "???", "", "create", "newuser6", "FS", "logout"],
    console_lines=["Username: ", "Login successful. Welcome admin1 (admin).",
                   "Error: empty input ignored.",
                   "Error: '???' is not a recognized transaction code.",
                   "Error: empty input ignored.",
                   "User 'newuser6' created successfully.",
                   "Logged out. Daily transaction file written."],
    daily_files=[[txn_create("newuser6", "FS", 0.00), txn_end()]],
    notes="Blank lines and garbage tokens must be reported and skipped without the program "
          "crashing or losing its place in the transaction stream.",
)

# ============================================================
# DAILY TRANSACTION FILE
# ============================================================

make_case(49, "verify_transaction_output_format",
    stdin_lines=[
        "login", "admin1",
        "create", "formatuser", "FS",
        "delete", "buyer1",
        "sell", "TestGame", "25.50",
        "buy", "Hollow_Knight", "seller1",
        "refund", "formatuser", "seller1", "5.00",
        "addcredit", "20.00", "formatuser",
        "logout",
    ],
    console_lines=[
        "Username: ", "Login successful. Welcome admin1 (admin).",
        "User 'formatuser' created successfully.",
        "User 'buyer1' deleted successfully.",
        "Game 'TestGame' listed for sale at $25.50.",
        "Purchased 'Hollow_Knight' from seller1 for $10.00.",
        "Refund of $5.00 processed from seller1 to formatuser.",
        "Added $20.00 credit to formatuser's account.",
        "Logged out. Daily transaction file written.",
    ],
    daily_files=[[
        txn_create("formatuser", "FS", 0.00),
        txn_delete("buyer1"),
        txn_sell("TestGame", "admin1", 25.50),
        txn_buy("Hollow_Knight", "seller1", "admin1", 10.00),
        txn_refund("formatuser", "seller1", 5.00),
        txn_addcredit("formatuser", 20.00),
        txn_end(),
    ]],
    notes="admin1 is not buy-standard or sell-standard, so it is permitted to both sell and buy "
          "as well as perform every privileged transaction; this single session exercises every "
          "transaction code (01, 02, 03, 04, 05, 06, 00) so all field-formatting rules "
          "(left-justified/space-padded text, zero-padded and '.00'-suffixed money, fixed widths) "
          "can be checked against expected_daily_transaction_file.txt line by line.",
)

make_case(50, "verify_end_of_session_transaction",
    stdin_lines=["login", "fulluser1", "logout"],
    console_lines=["Username: ", "Login successful. Welcome fulluser1 (full-standard).",
                   "Logged out. Daily transaction file written."],
    daily_files=[[txn_end()]],
    notes="Focused check of the terminating '00' record's exact byte layout: transaction code "
          "'00', followed by the username field blank (15 spaces), user type field blank "
          "(2 spaces), and credit field zero-filled (9 zero characters) -- "
          f"i.e. the single line should read exactly:\n  \"{txn_end()}\"\n"
          f"(length {len(txn_end())} characters, excluding the newline).",
)

print(f"Generated {len(os.listdir(ROOT))} test case folders under {ROOT}")
