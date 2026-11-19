"""DailyTransactionFile: reads the merged Daily Transaction File into records."""

from error_log import FatalFileError
from fixed_width import (CREDIT_WIDTH, END_MARKER, GAME_NAME_WIDTH,
                         PRICE_WIDTH, USER_TYPE_WIDTH, USERNAME_WIDTH,
                         read_field, read_lines, read_money)

FILE_NAME = "Daily Transaction File"

# Transaction codes written by the Front End.
END_OF_SESSION = "00"
CREATE = "01"
DELETE = "02"
SELL = "03"
BUY = "04"
REFUND = "05"
ADD_CREDIT = "06"

# Every record starts with a 2-character code and a space.
FIELDS_START = 3


class TransactionRecord:
    """One parsed line of the Daily Transaction File. Only the fields that
    the record's code uses are filled in; the rest stay None."""

    def __init__(self, code):
        """Create an empty record for the given two-digit transaction code."""
        self.code = code
        self.username = None    # 00, 01, 02, 06
        self.user_type = None   # 00, 01, 02, 06
        self.amount = None      # credit (01, 02, 06), price (03, 04) or refund (05)
        self.game_name = None   # 03, 04
        self.seller = None      # 03, 04, 05
        self.buyer = None       # 04, 05


class DailyTransactionFile:
    """Reads the merged Daily Transaction File and turns each line into a
    TransactionRecord, in the order the transactions happened."""

    def __init__(self):
        """Start with no records."""
        self.records = []

    def load(self, path):
        """Read every record from the file at path, or raise FatalFileError
        if a line is malformed."""
        self.records = []
        for line in read_lines(path, FILE_NAME):
            # Skip blank lines and stop at an optional END line.
            if not line.strip():
                continue
            if line.startswith(END_MARKER):
                break
            self.records.append(self.parse_line(line))

    def parse_line(self, line):
        """Pick the right parser for the line's transaction code."""
        code = line[:2]
        parsers = {
            END_OF_SESSION: self.parse_account_record,
            CREATE: self.parse_account_record,
            DELETE: self.parse_account_record,
            ADD_CREDIT: self.parse_account_record,
            SELL: self.parse_sell_record,
            BUY: self.parse_buy_record,
            REFUND: self.parse_refund_record,
        }
        if code not in parsers:
            raise FatalFileError(f"{FILE_NAME}: unknown transaction code in '{line}'")
        return parsers[code](code, line)

    def parse_account_record(self, code, line):
        """Parse XX UUUUUUUUUUUUUUU TT CCCCCCCCC (codes 00, 01, 02, 06)."""
        type_start = FIELDS_START + USERNAME_WIDTH + 1
        credit_start = type_start + USER_TYPE_WIDTH + 1

        record = TransactionRecord(code)
        record.username = read_field(line, FIELDS_START, USERNAME_WIDTH)
        record.user_type = read_field(line, type_start, USER_TYPE_WIDTH)
        record.amount = read_money(line, credit_start, CREDIT_WIDTH, FILE_NAME)
        return record

    def parse_sell_record(self, code, line):
        """Parse 03 NNNNNNNNNNNNNNNNNNNNNNNNN SSSSSSSSSSSSSSS PPPPPP."""
        seller_start = FIELDS_START + GAME_NAME_WIDTH + 1
        price_start = seller_start + USERNAME_WIDTH + 1

        record = TransactionRecord(code)
        record.game_name = read_field(line, FIELDS_START, GAME_NAME_WIDTH)
        record.seller = read_field(line, seller_start, USERNAME_WIDTH)
        record.amount = read_money(line, price_start, PRICE_WIDTH, FILE_NAME)
        return record

    def parse_buy_record(self, code, line):
        """Parse 04 NNNNNNNNNNNNNNNNNNNNNNNNN SSSSSSSSSSSSSSS UUUUUUUUUUUUUUU PPPPPP."""
        seller_start = FIELDS_START + GAME_NAME_WIDTH + 1
        buyer_start = seller_start + USERNAME_WIDTH + 1
        price_start = buyer_start + USERNAME_WIDTH + 1

        record = TransactionRecord(code)
        record.game_name = read_field(line, FIELDS_START, GAME_NAME_WIDTH)
        record.seller = read_field(line, seller_start, USERNAME_WIDTH)
        record.buyer = read_field(line, buyer_start, USERNAME_WIDTH)
        record.amount = read_money(line, price_start, PRICE_WIDTH, FILE_NAME)
        return record

    def parse_refund_record(self, code, line):
        """Parse 05 UUUUUUUUUUUUUUU SSSSSSSSSSSSSSS CCCCCCCCC."""
        seller_start = FIELDS_START + USERNAME_WIDTH + 1
        amount_start = seller_start + USERNAME_WIDTH + 1

        record = TransactionRecord(code)
        record.buyer = read_field(line, FIELDS_START, USERNAME_WIDTH)
        record.seller = read_field(line, seller_start, USERNAME_WIDTH)
        record.amount = read_money(line, amount_start, CREDIT_WIDTH, FILE_NAME)
        return record

    def get_records(self):
        """Return every record in file order."""
        return self.records
