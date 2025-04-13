# bots/random_bot.py

import random
from bots.decision_ml import decide_action



class BotPlayer:
    def __init__(self, name):
        self.name = name

    def decide(self,hand,community_cards,min_bet):
        return decide_action(hand, community_cards,min_bet)
