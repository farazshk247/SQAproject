"""BackEndApp: top-level controller that loads, processes and saves all files."""

from account_file import AccountFile
from collection_file import CollectionFile
from daily_transaction_file import DailyTransactionFile
from error_log import ErrorLog, FatalFileError
from game_file import GameFile
from transaction_processor import TransactionProcessor

# Number of file paths the program expects on the command line.
EXPECTED_ARGUMENT_COUNT = 7


class BackEndApp:
    """Runs one Back End pass: read the old files, apply the day's
    transactions, and write the new files."""

    def __init__(self):
        """Create empty in-memory copies of every file the Back End uses."""
        self.accounts = AccountFile()
        self.games = GameFile()
        self.collection = CollectionFile()
        self.daily_transactions = DailyTransactionFile()
        self.error_log = ErrorLog()

    def start(self, arguments):
        """Check the arguments, run the Back End, and return an exit code
        (0 for success, 1 for bad arguments or a fatal file error)."""
        if len(arguments) != EXPECTED_ARGUMENT_COUNT:
            self.error_log.report_usage(
                "usage: main.py <accounts> <games> <collection> "
                "<daily_transactions> <new_accounts> <new_games> <new_collection>")
            return 1

        (accounts_path, games_path, collection_path, daily_path,
         new_accounts_path, new_games_path, new_collection_path) = arguments

        try:
            self.load_files(accounts_path, games_path, collection_path, daily_path)
            self.process_transactions()
            self.save_files(new_accounts_path, new_games_path, new_collection_path)
        except FatalFileError as error:
            # A malformed input file means the results can't be trusted,
            # so stop without writing any output files.
            self.error_log.report_fatal(str(error))
            return 1

        return 0

    def load_files(self, accounts_path, games_path, collection_path, daily_path):
        """Read all four input files into memory."""
        self.accounts.load(accounts_path)
        self.games.load(games_path)
        self.collection.load(collection_path)
        self.daily_transactions.load(daily_path)

    def process_transactions(self):
        """Apply every daily transaction, in order, to the in-memory files."""
        processor = TransactionProcessor(
            self.accounts, self.games, self.collection, self.error_log)
        for record in self.daily_transactions.get_records():
            processor.apply(record)

    def save_files(self, new_accounts_path, new_games_path, new_collection_path):
        """Write the updated accounts, games and collection files."""
        self.accounts.save(new_accounts_path)
        self.games.save(new_games_path)
        self.collection.save(new_collection_path)
