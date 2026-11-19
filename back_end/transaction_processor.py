"""TransactionProcessor: applies each daily transaction to the system files."""

from daily_transaction_file import (ADD_CREDIT, BUY, CREATE, DELETE,
                                    END_OF_SESSION, REFUND, SELL)
from models import Game, UserAccount


class TransactionProcessor:
    """Applies one TransactionRecord at a time to the accounts, games and
    collection. A transaction that breaks a rule is reported to the
    ErrorLog and skipped; the rest of the day's transactions still run."""

    def __init__(self, accounts, games, collection, error_log):
        """Keep references to the in-memory files and the error log."""
        self.accounts = accounts
        self.games = games
        self.collection = collection
        self.error_log = error_log

        # One handler method for each transaction code.
        self.handlers = {
            END_OF_SESSION: self.apply_end_of_session,
            CREATE: self.apply_create,
            DELETE: self.apply_delete,
            SELL: self.apply_sell,
            BUY: self.apply_buy,
            REFUND: self.apply_refund,
            ADD_CREDIT: self.apply_add_credit,
        }

    def apply(self, record):
        """Send the record to the handler for its transaction code."""
        self.handlers[record.code](record)

    def reject(self, record, message):
        """Report that a transaction broke a rule and was skipped."""
        self.error_log.report_constraint(record.code, message)

    def apply_end_of_session(self, record):
        """End of session (00): marks where a session ended; nothing to change."""

    def apply_create(self, record):
        """Create (01): add a new account with the given type and credit."""
        if self.accounts.find(record.username) is not None:
            self.reject(record, f"user '{record.username}' already exists")
            return

        self.accounts.add(UserAccount(record.username, record.user_type, record.amount))

    def apply_delete(self, record):
        """Delete (02): remove the account and every game it has for sale."""
        if self.accounts.find(record.username) is None:
            self.reject(record, f"user '{record.username}' does not exist")
            return

        self.accounts.remove(record.username)
        self.games.remove_by_seller(record.username)

    def apply_sell(self, record):
        """Sell (03): put a new game up for sale."""
        if self.games.find(record.game_name) is not None:
            self.reject(record, f"game '{record.game_name}' already exists")
            return

        self.games.add(Game(record.game_name, record.seller, record.amount))

    def apply_buy(self, record):
        """Buy (04): move the price from buyer to seller and give the buyer the game."""
        buyer = self.accounts.find(record.buyer)
        seller = self.accounts.find(record.seller)

        if buyer is None or seller is None:
            self.reject(record, "buyer or seller does not exist")
            return

        buyer.remove_credit(record.amount)
        seller.add_credit(record.amount)
        self.collection.add(record.buyer, record.game_name)

    def apply_refund(self, record):
        """Refund (05): move the amount from the seller back to the buyer."""
        buyer = self.accounts.find(record.buyer)
        seller = self.accounts.find(record.seller)

        if buyer is None or seller is None:
            self.reject(record, "buyer or seller does not exist")
            return

        seller.remove_credit(record.amount)
        buyer.add_credit(record.amount)

    def apply_add_credit(self, record):
        """Add credit (06): add the recorded amount to the user's balance."""
        account = self.accounts.find(record.username)

        if account is None:
            self.reject(record, f"user '{record.username}' does not exist")
            return

        account.add_credit(record.amount)
