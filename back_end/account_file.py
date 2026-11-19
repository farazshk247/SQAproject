"""AccountFile: the Current User Accounts File held in memory."""

from error_log import FatalFileError
from fixed_width import (CREDIT_WIDTH, END_MARKER, USER_TYPE_WIDTH,
                         USERNAME_WIDTH, format_money, is_end_line, pad_text,
                         read_field, read_lines, read_money, write_lines)
from models import UserAccount

FILE_NAME = "Current User Accounts File"

# Line layout: UUUUUUUUUUUUUUU TT CCCCCCCCC
TYPE_START = USERNAME_WIDTH + 1
CREDIT_START = TYPE_START + USER_TYPE_WIDTH + 1
LINE_LENGTH = CREDIT_START + CREDIT_WIDTH


class AccountFile:
    """Loads, updates and saves every user account, keyed by username."""

    def __init__(self):
        """Start with no accounts (keeps the order they were added in)."""
        self.users = {}

    def load(self, path):
        """Read the accounts file at path, or raise FatalFileError if it is malformed."""
        self.users = {}
        for line in read_lines(path, FILE_NAME):
            if is_end_line(line, USERNAME_WIDTH):
                return
            account = self.parse_line(line)
            self.users[account.username] = account
        raise FatalFileError(f"{FILE_NAME}: missing END line")

    def parse_line(self, line):
        """Turn one fixed-width line into a UserAccount."""
        username = read_field(line, 0, USERNAME_WIDTH)
        user_type = read_field(line, TYPE_START, USER_TYPE_WIDTH)
        credit = read_money(line, CREDIT_START, CREDIT_WIDTH, FILE_NAME)
        return UserAccount(username, user_type, credit)

    def save(self, path):
        """Write every account, then the END line, to the file at path."""
        lines = [self.format_line(account) for account in self.users.values()]
        lines.append(pad_text(END_MARKER, LINE_LENGTH))
        write_lines(path, lines)

    def format_line(self, account):
        """Turn one UserAccount into its fixed-width line."""
        return (pad_text(account.username, USERNAME_WIDTH) + " "
                + account.user_type + " "
                + format_money(account.credit, CREDIT_WIDTH))

    def find(self, username):
        """Return the account with this username, or None."""
        return self.users.get(username)

    def add(self, account):
        """Add a new account."""
        self.users[account.username] = account

    def remove(self, username):
        """Delete the account with this username."""
        del self.users[username]
