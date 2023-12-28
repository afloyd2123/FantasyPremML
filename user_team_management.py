import pandas as pd

# Function to Read Your Current Team
def read_current_team():
    user_team_path = "user_team.xlsx"
    user_team = pd.read_excel(user_team_path)
    return user_team

# Function to Update Your Team with Trades
def update_user_team_with_trades(trade_in, trade_out):
    user_team = read_current_team()
    # Remove the traded-out player
    user_team = user_team[user_team["Player"] != trade_out]
    # Add the traded-in player's details
    new_player_data = {"Player": trade_in, "Position": "TBD", "Team": "TBD", "Status": "Starting", "Trade Notes": "Traded In GWX"}
    user_team = user_team.append(new_player_data, ignore_index=True)
    user_team.to_excel("user_team.xlsx", index=False)

# Function to Update Your Performance After Each Game Week
def update_user_performance(merged_gw_data, game_week):
    user_performance_path = "user_performance.xlsx"
    user_performance = pd.read_excel(user_performance_path)

    user_team = read_current_team()
    players = user_team["Player"].tolist()

    for player in players:
        player_data = merged_gw_data[(merged_gw_data["name"] == player) & (merged_gw_data["round"] == game_week)]
        points = player_data["total_points"].values[0] if not player_data.empty else 0
        position = player_data["element_type"].values[0] if not player_data.empty else "N/A"
        status = user_team[user_team["Player"] == player]["Status"].values[0]

        new_performance_data = {"Game Week": game_week, "Player": player, "Position": position, "Points": points, "Status": status}
        user_performance = user_performance.append(new_performance_data, ignore_index=True)

    user_performance.to_excel(user_performance_path, index=False)
