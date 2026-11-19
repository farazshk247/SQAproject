
from error_log import FatalFileError
from fixed_width import (END_MARKER, GAME_NAME_WIDTH, USERNAME_WIDTH,
                         is_end_line, pad_text, read_field, read_lines,
                         write_lines)
from models import CollectionEntry

FILE_NAME = "Game Collection File"

OWNER_START = GAME_NAME_WIDTH + 1
LINE_LENGTH = OWNER_START + USERNAME_WIDTH


class CollectionFile:

    def __init__(self):
        self.entries = []

    def load(self, path):
        self.entries = []
        for line in read_lines(path, FILE_NAME):
            if is_end_line(line, GAME_NAME_WIDTH):
                return
            self.entries.append(self.parse_line(line))
        raise FatalFileError(f"{FILE_NAME}: missing END line")

    def parse_line(self, line):
        game_name = read_field(line, 0, GAME_NAME_WIDTH)
        owner = read_field(line, OWNER_START, USERNAME_WIDTH)
        return CollectionEntry(game_name, owner)

    def save(self, path):
        lines = [self.format_line(entry) for entry in self.entries]
        lines.append(pad_text(END_MARKER, LINE_LENGTH))
        write_lines(path, lines)

    def format_line(self, entry):
        return (pad_text(entry.game_name, GAME_NAME_WIDTH) + " "
                + pad_text(entry.owner, USERNAME_WIDTH))

    def add(self, owner, game_name):
        self.entries.append(CollectionEntry(game_name, owner))
