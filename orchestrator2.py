import pandas as pd
from data_preprocessing import fetch_current_gw_data, process_gw_data
from feature_engineering import create_features_for_current_gw
from user_team import get_user_team_for_gw
from ICT_model import predict_using_ict_model
from opponent_modl import predict_using_opponent_model
from valuation_model2 import predict_using_valuation_model
from decision_engine import make_transfer_decisions, make_chip_decisions

DATA_PATH = "C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023/"
MERGED_GW_PATH = DATA_PATH + ""

# Fetch and preprocess the latest data
fetch_current_gw_data()
process_gw_data()

# Load merged_gw.csv to determine the current game week
merged_gw_data = pd.read_csv(MERGED_GW_PATH)
current_gw = merged_gw_data['gw'].max()

# Feature Engineering
players_data = create_features_for_current_gw(current_gw)

# Incorporate user team
user_team = get_user_team_for_gw(current_gw)
players_data = pd.concat([players_data, user_team], axis=0, ignore_index=True)

# Model Predictions
ict_predictions = predict_using_ict_model(players_data)
opponent_predictions = predict_using_opponent_model(players_data)
valuation_predictions = predict_using_valuation_model(players_data)

# Transfer Decisions
transfer_in, transfer_out = make_transfer_decisions(
    ict_predictions, 
    opponent_predictions, 
    valuation_predictions
)

# Chip Decisions
chip_to_play = make_chip_decisions(
    ict_predictions, 
    opponent_predictions, 
    valuation_predictions
)

# Define N and threshold
N = 50  # for example, top 50 players
threshold = 0.8  # for starts-based star players

# Points-Based Star Players
top_points_players = df_players.nlargest(N, 'total_points')['name'].tolist()

# Starts-Based Star Players
starters = df_players[df_players['starts'] / df_players['games_played'] > threshold]['name'].tolist()

# Valuation-Based Star Players
top_valuation_players = df_players.nlargest(N, 'valuation')['name'].tolist()

# Union of star players
star_players = set(top_points_players + starters + top_valuation_players)



# Check for Injuries and Plan Transfers

# Assuming 'status' column indicates a player's injury status, and 'element' is the player's ID
injured_players = user_team_data[user_team_data['status'] == 'injured']['element'].tolist()

# Placeholder for potential transfers
transfers_out = []

for player in injured_players:
    # Check the expected return date or severity of injury (if data available)
    # If the injury is long-term or no return date is provided, plan a transfer
    transfers_out.append(player)

    # Find a replacement based on the valuation model or other criteria
    # This can be a cheap player expected to rise in value or a bench player
    # Placeholder logic: (Actual logic would involve querying the valuation model and other datasets)
    replacement = get_cheap_rising_player(player_position=player['position'])
    user_team_data = user_team_data.replace(player, replacement)

# After this, the models and decision engine would run, taking into account the planned transfers


print(f"Transfers: OUT - {transfer_out}, IN - {transfer_in}")
print(f"Play Chip: {chip_to_play}")


# Print Transfer Suggestions
if players_to_transfer_in:
    print("Consider transferring in: ", ', '.join(players_to_transfer_in))
if players_to_transfer_out:
    print("Consider transferring out: ", ', '.join(players_to_transfer_out))

# Model Evaluation

# Fetch actual points for the players in the user team for the current game week
actual_points = merged_gw[(merged_gw['gw'] == current_gw) & (merged_gw['element'].isin(user_team))]['total_points'].values

# Assuming predictions from models are stored in the following format:
# predicted_points_ict, predicted_points_valuation, predicted_points_opponent

# Calculate error metrics
mae_ict = np.mean(np.abs(predicted_points_ict - actual_points))
mae_valuation = np.mean(np.abs(predicted_points_valuation - actual_points))
mae_opponent = np.mean(np.abs(predicted_points_opponent - actual_points))

rmse_ict = np.sqrt(np.mean((predicted_points_ict - actual_points)**2))
rmse_valuation = np.sqrt(np.mean((predicted_points_valuation - actual_points)**2))
rmse_opponent = np.sqrt(np.mean((predicted_points_opponent - actual_points)**2))

# Store the error metrics for further analysis (optional)
error_data = {
    'game_week': current_gw,
    'mae_ict': mae_ict,
    'mae_valuation': mae_valuation,
    'mae_opponent': mae_opponent,
    'rmse_ict': rmse_ict,
    'rmse_valuation': rmse_valuation,
    'rmse_opponent': rmse_opponent
}

error_df = pd.DataFrame([error_data])
error_output_path = "C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023/error_metrics.csv"
if os.path.exists(error_output_path):
    error_df.to_csv(error_output_path, mode='a', header=False, index=False)
else:
    error_df.to_csv(error_output_path, mode='w', index=False)


import csv

def log_recommendations(gw, in_players, out_players, chips, predicted_scores):
    with open('history.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([gw, ', '.join(in_players), ', '.join(out_players), ', '.join(chips), predicted_scores])

# Sample usage
gw = "GW2"
in_players = ["Player A", "Player B"]
out_players = ["Player C"]
chips = ["Bench Boost"]
predicted_scores = "Player A: 6, Player B: 7"
log_recommendations(gw, in_players, out_players, chips, predicted_scores)
