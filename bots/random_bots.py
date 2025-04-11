# bots/random_bot.py

import random

class RandomBot:
    def __init__(self, name="RandomBot"):
        self.name = name

    def decide(self, player, table, min_bet):
        if player.folded:
            return "fold", 0

        actions = ["fold", "call", "raise"]
        action = random.choice(actions)

        if action == "fold":
            return "fold", 0
        elif action == "call":
            return "call", min_bet
        elif action == "raise":
            raise_amount = random.randint(min_bet, min_bet + 50)
            return "raise", raise_amount
