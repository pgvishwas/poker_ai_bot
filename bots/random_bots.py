# bots/random_bot.py

import random
from bots.decision_ml import decide_action



class BotPlayer:
    def __init__(self, name):
        self.name = name

    def decide(self, community_cards):
        return decide_action(self.hand, community_cards)
