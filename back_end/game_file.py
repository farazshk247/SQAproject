"""GameFile: the Available Games File held in memory."""

from error_log import FatalFileError
from fixed_width import (END_MARKER, GAME_NAME_WIDTH, PRICE_WIDTH,
                         USERNAME_WIDTH, format_money, is_end_line, pad_text,
                         read_field, read_lines, read_money, write_lines)
from models import Game

FILE_NAME = "Available Games File"

# Line layout: NNNNNNNNNNNNNNNNNNNNNNNNN SSSSSSSSSSSSSSS PPPPPP
SELLER_START = GAME_NAME_WIDTH + 1
PRICE_START = SELLER_START + USERNAME_WIDTH + 1


class GameFile:
    """Loads, updates and saves every game currently for sale, keyed by name."""

    def __init__(self):
        """Start with no games for sale."""
        self.games = {}

    def load(self, path):
        """Read the games file at path, or raise FatalFileError if it is malformed."""
        self.games = {}
        for line in read_lines(path, FILE_NAME):
            if is_end_line(line, GAME_NAME_WIDTH):
                return
            game = self.parse_line(line)
            self.games[game.name] = game
        raise FatalFileError(f"{FILE_NAME}: missing END line")

    def parse_line(self, line):
        """Turn one fixed-width line into a Game."""
        name = read_field(line, 0, GAME_NAME_WIDTH)
        seller = read_field(line, SELLER_START, USERNAME_WIDTH)
        price = read_money(line, PRICE_START, PRICE_WIDTH, FILE_NAME)
        return Game(name, seller, price)

    def save(self, path):
        """Write every game, then the END line, to the file at path."""
        lines = [self.format_line(game) for game in self.games.values()]
        # The END line keeps the price column filled with zeros (no decimal point).
        lines.append(pad_text(END_MARKER, PRICE_START) + "0" * PRICE_WIDTH)
        write_lines(path, lines)

    def format_line(self, game):
        """Turn one Game into its fixed-width line."""
        return (pad_text(game.name, GAME_NAME_WIDTH) + " "
                + pad_text(game.seller, USERNAME_WIDTH) + " "
                + format_money(game.price, PRICE_WIDTH))

    def find(self, name):
        """Return the game with this name, or None."""
        return self.games.get(name)

    def add(self, game):
        """Put a new game up for sale."""
        self.games[game.name] = game

    def remove_by_seller(self, seller):
        """Take every game sold by this seller off the market."""
        self.games = {name: game for name, game in self.games.items()
                      if game.seller != seller}
