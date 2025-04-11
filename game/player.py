# game/player.py
from bots.random_bots import RandomBot

class Player:
    def __init__(self, name, is_bot=False, strategy=None, bankroll=1000):
        self.name = name
        self.is_bot = is_bot
        self.strategy = strategy or ("random" if is_bot else None)
        self.bankroll = bankroll
        self.hand = []
        self.current_bet = 0
        self.folded = False

        if self.is_bot and self.strategy == "random":
            self.bot = RandomBot(name)
        else:
            self.bot = None

    def make_decision(self, table, min_bet):
        if self.bot:
            action, amount = self.bot.decide(self, table, min_bet)
            return action, amount
        else:
            # placeholder for human input later
            return "call", min_bet

    def receive_cards(self, cards):
        self.hand = cards

    def bet(self, amount):
        if amount > self.bankroll:
            raise ValueError(f"{self.name} doesn't have enough bankroll.")
        self.bankroll -= amount
        self.current_bet += amount
        return amount

    def fold(self):
        self.folded = True

    def reset_for_new_round(self):
        self.hand = []
        self.current_bet = 0
        self.folded = False

    def __repr__(self):
        return f"{self.name} ({'Bot' if self.is_bot else 'Human'}) - Bankroll: ${self.bankroll}"
