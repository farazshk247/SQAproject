"""Error reporting for the Back End."""


class FatalFileError(Exception):
    """Raised when an input file is missing or malformed, so the Back End
    has to stop without writing any output."""


class ErrorLog:
    """Prints Back End error messages to the terminal in one consistent format."""

    def report_constraint(self, transaction_code, message):
        """Report a transaction that broke a rule; that transaction is skipped."""
        print(f"ERROR: transaction {transaction_code} - {message}")

    def report_fatal(self, message):
        """Report a fatal file problem that stops the Back End."""
        print(f"ERROR: fatal - {message}")

    def report_usage(self, message):
        """Report that the program was started with the wrong arguments."""
        print(f"ERROR: {message}")
