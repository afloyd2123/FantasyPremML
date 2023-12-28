import pandas as pd
from fetch_current_data import fetch_latest_data
from feature_engineering import preprocess_data
from ICT_model import predict_ict_performance
from opponent_modl import predict_opponent_difficulty
from valuation_model2 import predict_valuation_changes
from decision_framework import make_decisions, save_decisions

def run_workflow(current_gameweek):
    # 1. Data Collection
    fetch_latest_data()

    # 2. Data Preprocessing & Feature Engineering
    player_data, fixtures_data = preprocess_data()

    # 3. Model Predictions
    ict_predictions = predict_ict_performance(player_data)
    opponent_predictions = predict_opponent_difficulty(player_data, fixtures_data)
    valuation_predictions = predict_valuation_changes(player_data)

    # 4. Decision Making
    decisions = make_decisions(ict_predictions, opponent_predictions, valuation_predictions, current_gameweek)

    # 5. Output & User Review
    print("Recommended Decisions for Gameweek", current_gameweek)
    print(decisions)  # This is a simple print, but we can expand this to a more detailed output or dashboard

    # 6. Save State & Progress
    save_decisions(decisions, current_gameweek)

    return decisions

if __name__ == "__main__":
    current_gameweek = input("Enter the current gameweek: ")
    run_workflow(current_gameweek)
