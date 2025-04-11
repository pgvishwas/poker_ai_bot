# ml_model/train_model.py

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from ucimlrepo import fetch_ucirepo

# fetch dataset
poker_hand = fetch_ucirepo(id=158)

# --------------- LOAD DATA ---------------
print("[INFO] Loading Poker Hand dataset from UCI repo...")
# data (as pandas dataframes)
X_raw = poker_hand.data.features
y_raw = poker_hand.data.targets

# Combine into a DataFrame
columns = [
    'S1', 'R1', 'S2', 'R2', 'S3', 'R3', 'S4', 'R4', 'S5', 'R5'
]
df = pd.DataFrame(X_raw, columns=columns)
df['Class'] = y_raw

# --------------- FEATURE ENGINEERING ---------------

def extract_features(df):
    ranks = df[['R1', 'R2', 'R3', 'R4', 'R5']]
    suits = df[['S1', 'S2', 'S3', 'S4', 'S5']]

    df['unique_ranks'] = ranks.nunique(axis=1)
    df['unique_suits'] = suits.nunique(axis=1)
    df['max_rank'] = ranks.max(axis=1)
    df['min_rank'] = ranks.min(axis=1)
    df['rank_std'] = ranks.std(axis=1)
    df['flush_possible'] = (df['unique_suits'] == 1).astype(int)
    df['straight_possible'] = ((df['max_rank'] - df['min_rank']) == 4).astype(int)

    return df[['unique_ranks', 'unique_suits', 'max_rank', 'min_rank', 'rank_std', 'flush_possible', 'straight_possible']]

X = extract_features(df)

# --------------- LABEL CREATION ---------------
# Convert original hand class to bot decision:
# 0 = Fold, 1 = Call, 2 = Raise

def convert_label(hand_class):
    if hand_class == 0:
        return 0  # Fold
    elif 1 <= hand_class <= 4:
        return 1  # Call
    else:
        return 2  # Raise

df['Action'] = df['Class'].apply(convert_label)
y = df['Action']

# --------------- TRAIN MODEL ---------------
print("[INFO] Training model...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --------------- EVALUATE ---------------
print("[INFO] Evaluating model...")
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=["Fold", "Call", "Raise"]))

# --------------- SAVE MODEL ---------------
MODEL_DIR = "ml_model"
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

# Create directory if it doesn't exist
os.makedirs(MODEL_DIR, exist_ok=True)

print(f"[INFO] Saving model to {MODEL_PATH}")
joblib.dump(model, MODEL_PATH)
print("[INFO] Done.")

