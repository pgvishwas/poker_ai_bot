# bot/decision_ml.py

import joblib
import os
import numpy as np

# Load model
MODEL_PATH = os.path.join("ml_model","ml_model","model.pkl")
model = joblib.load(MODEL_PATH)

def extract_features(cards):
    """Takes 5 cards, returns 7 feature values for ML model."""
    suits = [card.suit for card in cards]
    ranks = [card.rank for card in cards]

    unique_ranks = len(set(ranks))
    unique_suits = len(set(suits))
    max_rank = max(ranks)
    min_rank = min(ranks)
    rank_std = np.std(ranks)
    flush_possible = 1 if unique_suits == 1 else 0
    straight_possible = 1 if max_rank - min_rank == 4 and unique_ranks == 5 else 0

    return [[unique_ranks, unique_suits, max_rank, min_rank, rank_std, flush_possible, straight_possible]]

def decide_action(hand, community_cards):
    """
    Returns: "fold", "call", or "raise"
    """
    if len(community_cards) < 3:
        return "call"  # too early for ML logic

    # Take 5 cards for evaluation (2 hole + 3 flop or best 5)
    all_cards = hand + community_cards
    if len(all_cards) >= 5:
        # Pick best 5 (you can improve this later using hand ranking)
        cards = all_cards[:5]
    else:
        cards = all_cards

    features = extract_features(cards)
    prediction = model.predict(features)[0]

    return {0: "fold", 1: "call", 2: "raise"}[prediction]
