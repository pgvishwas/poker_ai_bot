# bot/decision_ml.py

import joblib
import os
import numpy as np
import pandas as pd

# Load model
MODEL_PATH = os.path.join("ml_model", "ml_model", "model.pkl")
model = joblib.load(MODEL_PATH)


rank_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
            '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
suit_map = {
    'Spades': 0, 'Hearts': 1, 'Diamonds': 2, 'Clubs': 3
}
feature_names = ['unique_ranks', 'unique_suits', 'max_rank', 'min_rank', 'rank_std', 'flush_possible', 'straight_possible']

def extract_features(cards):
    """Takes 5 cards, returns 7 feature values for ML model.
    #suits = [card.suit for card in cards]
    #ranks = [card.rank for card in cards]
    #print(cards)
    features = []
    for card in cards:
        # card is something like: "7 of Hearts"
        parts = str(card).split(" of ")
        rank_str, suit_str = parts[0], parts[1]

        ranks = rank_map.get(rank_str, 0)
        suits = suit_map.get(suit_str, 0)
    unique_ranks = len(set(ranks))
    unique_suits = len(set(suits))
    max_rank = max(ranks)
    min_rank = min(ranks)
    rank_std = np.std(ranks)
    flush_possible = 1 if unique_suits == 1 else 0
    straight_possible = 1 if max_rank - min_rank == 4 and unique_ranks == 5 else 0
    print("Extract Features O/P:\n",[unique_ranks, unique_suits, max_rank, min_rank, rank_std, flush_possible, straight_possible])
    return [[unique_ranks, unique_suits, max_rank, min_rank, rank_std, flush_possible, straight_possible]]"""
    ranks = [rank_map.get(str(card.rank), 0) for card in cards]
    suits = [suit_map.get(str(card.suit), 0) for card in cards]
    unique_ranks = len(set(ranks))
    unique_suits = len(set(suits))
    max_rank = max(ranks)
    min_rank = min(ranks)
    rank_std = np.std(ranks)
    flush_possible = 1 if unique_suits == 1 else 0
    straight_possible = 1 if max_rank - min_rank == 4 and unique_ranks == 5 else 0

    features = [unique_ranks, unique_suits, max_rank, min_rank, rank_std, flush_possible, straight_possible]
    df_features = pd.DataFrame([features], columns=feature_names)

    return df_features


def decide_action(hand, community_cards,min_bet):
    """
    Returns: "fold", "call", or "raise"
    """
    if len(community_cards) < 3:
        return "call" ,min_bet # too early for ML logic

    # Take 5 cards for evaluation (2 hole + 3 flop or best 5)
    all_cards = hand + community_cards
    if len(all_cards) >= 5:
        # Pick best 5 (you can improve this later using hand ranking)
        cards = all_cards[:5]
    else:
        cards = all_cards

    features = extract_features(cards)
    prediction = model.predict(features)[0]

    action =  {0: "fold", 1: "call", 2: "raise"}[prediction]
    if action == "fold":
        return action, 0
    elif action == "call":
        return action, min_bet
    else:  # raise
        return action, min_bet * 2
