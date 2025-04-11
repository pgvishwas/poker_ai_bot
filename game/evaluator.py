# game/evaluator.py

from treys import Card, Evaluator, Deck as TreysDeck

def convert_to_treys_card(card):
    rank_conversion = {
        '2': '2', '3': '3', '4': '4', '5': '5',
        '6': '6', '7': '7', '8': '8', '9': '9',
        '10': 'T', 'J': 'J', 'Q': 'Q', 'K': 'K', 'A': 'A'
    }
    suit_conversion = {
        'Hearts': 'h',
        'Diamonds': 'd',
        'Clubs': 'c',
        'Spades': 's'
    }

    treys_str = rank_conversion[card.rank] + suit_conversion[card.suit]
    return Card.new(treys_str)


def evaluate_winner(players, community_cards):
    evaluator = Evaluator()

    best_score = 9999
    winner = None

    treys_board = [convert_to_treys_card(c) for c in community_cards]

    for player in players:
        if player.folded:
            continue

        treys_hand = [convert_to_treys_card(c) for c in player.hand]
        score = evaluator.evaluate(treys_board, treys_hand)
        hand_rank = evaluator.class_to_string(evaluator.get_rank_class(score))

        print(f"{player.name} has {player.hand} → {hand_rank} (Score: {score})")

        if score < best_score:
            best_score = score
            winner = player

    return winner
