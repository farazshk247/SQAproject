"""Plain data classes for the three kinds of records the system stores."""

# User types: AA admin, FS full-standard, BS buy-standard,
# SS sell-standard, AM account manager.


class UserAccount:
    """One user from the Current User Accounts File: name, type and credit."""

    def __init__(self, username, user_type, credit):
        """Store the account's username, two-letter type and credit balance."""
        self.username = username
        self.user_type = user_type
        self.credit = credit

    def add_credit(self, amount):
        """Increase the balance by amount."""
        self.credit += amount

    def remove_credit(self, amount):
        """Decrease the balance by amount."""
        self.credit -= amount


class Game:
    """One game for sale from the Available Games File."""

    def __init__(self, name, seller, price):
        """Store the game's name, the seller's username and its price."""
        self.name = name
        self.seller = seller
        self.price = price


class CollectionEntry:
    """One line of the Game Collection File: a game owned by a user."""

    def __init__(self, game_name, owner):
        """Store the owned game's name and the owner's username."""
        self.game_name = game_name
        self.owner = owner
