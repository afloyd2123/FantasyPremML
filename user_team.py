# initial_team_config.py

# List of your initial players, you can specify either their names or unique IDs.
# Here, I'm using names as placeholders, but IDs might be more precise.
INITIAL_TEAM = [
    "Matt Turner",
    "Alphonse Areola",
    "Reece James",
    "Gabriel dos Santos Magalhaes",
    "Pervis Estupinan",
    "Tyrone Mings",
    "Divin Mubama",
    "Kevin De Bruyne",
    "Bruno Borges Fernandes",
    "Martin Odegaard",
    "Bukayo Saka",
    "Jack Grealish",
    "Joao Pedro Junqueira de Jesus",
    "Erling Haaland",
    "Sven Botman"
]

# Your initial budget. This is optional, but can be useful for tracking purposes.
INITIAL_BUDGET = 100.0  # This is just an example value; adjust as needed.

# Any other initial configurations or parameters you'd like to include.
import pandas as pd

def update_user_performance(user_team_path, merged_gw_path, user_performance_path, gw):
    # Load necessary data
    user_team = pd.read_excel(user_team_path, sheet_name='Team')
    merged_gw_data = pd.read_csv(merged_gw_path)
    user_performance = pd.read_excel(user_performance_path)

    # Compute points for the game week
    gw_data = merged_gw_data[merged_gw_data['gw'] == gw]
    user_gw_data = gw_data[gw_data['player'].isin(user_team['Player'])]
    total_points = user_gw_data['total_points'].sum()
    
    # Double the captain's points
    captain_points = user_gw_data[user_gw_data['player'] == user_team['Captain'].iloc[0]]['total_points'].values[0]
    total_points += captain_points

    # Subtract points for transfers if they exceed the free transfer (assuming -4 points for each extra transfer)
    transfers = user_team['Transfer In'].notna().sum()
    if transfers > 1:
        total_points -= (transfers - 1) * 4

    # Append data to user_performance
    new_data = {
        'Game Week': gw,
        'Points': total_points,
        'Transfers Made': transfers,
        'Captain': user_team['Captain'].iloc[0],
        'Vice Captain': user_team['Vice Captain'].iloc[0]
    }
    user_performance = user_performance.append(new_data, ignore_index=True)
    user_performance.to_excel(user_performance_path, index=False)
