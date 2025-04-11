# game/table.py

from game.card import Deck
from game.player import Player

class Table:
    def __init__(self, players):
        self.players = players  # list of Player instances
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0

    def start_new_hand(self):
        self.deck.reset()
        self.community_cards = []
        self.pot = 0
        for player in self.players:
            player.reset_for_new_round()
            hole_cards = self.deck.deal(2)
            player.receive_cards(hole_cards)

    def deal_community_cards(self, stage):
        if stage == "flop":
            self.community_cards += self.deck.deal(3)
        elif stage == "turn":
            self.community_cards += self.deck.deal(1)
        elif stage == "river":
            self.community_cards += self.deck.deal(1)
        else:
            raise ValueError("Unknown stage")

    def show_table_state(self):
        print("\n--- TABLE STATE ---")
        print("Community Cards:", self.community_cards)
        print("Pot:", self.pot)
        for player in self.players:
            status = "Folded" if player.folded else f"Hand: {player.hand}"
            print(f"{player.name}: {status}, Bankroll: ${player.bankroll}")
        print("-------------------\n")

    def collect_bets(self, min_bet=10):
        for player in self.players:
            if player.folded:
                continue  # Skip folded players

            action, amount = player.make_decision(self, min_bet)

            if action == "fold":
                player.fold()
                print(f"{player.name} folds.")
            elif action == "call":
                try:
                    bet = player.bet(min_bet)
                    self.pot += bet
                    print(f"{player.name} calls ${bet}.")
                except ValueError:
                    player.fold()
                    print(f"{player.name} folds due to insufficient bankroll.")
            elif action == "raise":
                try:
                    bet = player.bet(amount)
                    self.pot += bet
                    print(f"{player.name} raises to ${bet}.")
                except ValueError:
                    player.fold()
                    print(f"{player.name} folds trying to raise with insufficient bankroll.")


    def remaining_players(self):
        return [p for p in self.players if not p.folded]

    def is_hand_over(self):
        return len(self.remaining_players()) <= 1
