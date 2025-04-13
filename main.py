# main.py

from game.card import Deck
from game.player import Player
from game.table import Table
from game.evaluator import evaluate_winner


def play_hand(num_players=6):  # You can change num_players to simulate more players
    # Create a list of players
    players = []

    # Add bots and humans (for now, add bots randomly)
    for i in range(num_players):
        if i % 2 == 0:  # Simulate alternating bot and human players for example
            players.append(Player(f"Bot_{i + 1}", is_bot=True, strategy="random"))
        else:
            players.append(Player(f"Player_{i + 1}"))

    # Set up table
    table = Table(players)

    # Start new hand
    table.start_new_hand()
    table.show_table_state()

    # Pre-flop betting
    print("Pre-Flop Betting:")
    table.collect_bets(min_bet=10)
    table.show_table_state()

    if table.is_hand_over():
        print("Hand ends after pre-flop.")
        return

    # Flop
    print("Flop:")
    table.deal_community_cards("flop")
    table.collect_bets(min_bet=10)
    table.show_table_state()

    if table.is_hand_over():
        print("Hand ends after flop.")
        return

    # Turn
    print("Turn:")
    table.deal_community_cards("turn")
    table.collect_bets(min_bet=10)
    table.show_table_state()

    if table.is_hand_over():
        print("Hand ends after turn.")
        return

    # River
    print("River:")
    table.deal_community_cards("river")
    table.collect_bets(min_bet=10)
    table.show_table_state()

    if table.is_hand_over():
        print("Hand ends after river.")
        return

    # Showdown
    print("Showdown:")
    winner = evaluate_winner(table.remaining_players(), table.community_cards)

    if winner:
        print(f"🏆 {winner.name} wins the pot of ${table.pot}!")
        winner.bankroll += table.pot
    else:
        print("No winner. Everyone folded.")


if __name__ == "__main__":
    play_hand(num_players=6)  # Test with 6 players (can change this number)
