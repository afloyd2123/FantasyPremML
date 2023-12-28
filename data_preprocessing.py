import pandas as pd

# Load last season's playerset, then comment out.
# players = pd.read_csv("C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023/Fantasy-Premier-League/data/2022-23/cleaned_players.csv")
#Load this season's playerset
players = pd.read_csv("C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023/Fantasy-Premier-League/data/2022-23/cleaned_players.csv")


# Generate the name column
players['name'] = players['first_name'] + ' ' + players['second_name']


def compute_form(player_data, window=5):
    """
    Calculate the average points a player has obtained in the last few matches.
    """
    player_data['form'] = player_data.groupby('name')['total_points'].rolling(window=window).mean().reset_index(level=0, drop=True)
    return player_data

def compute_home_away_advantage(player_data):
    """
    Derive the average points difference between home and away games for each player.
    """
    home_avg = player_data[player_data['was_home'] == True].groupby('name')['total_points'].mean()
    away_avg = player_data[player_data['was_home'] == False].groupby('name')['total_points'].mean()
    advantage = home_avg - away_avg
    player_data['home_advantage'] = player_data['name'].map(advantage)
    return player_data

def compute_team_strength(player_data, team_data):
    """
    Use team standings as a feature.
    """
    team_strength = team_data.set_index('id')['strength_overall_home'].to_dict()
    player_data['team_strength'] = player_data['team'].map(team_strength)
    return player_data

def compute_opponent_strength(player_data, team_data):
    """
    Factor in the strength of the opponent the player is facing.
    """
    opponent_strength = team_data.set_index('id')['strength_defence_away'].to_dict()
    player_data['opponent_strength'] = player_data['opponent_team'].map(opponent_strength)
    return player_data

def compute_position_based_features(player_data):
    """
    Extract position-based features.
    """
    positions = pd.get_dummies(player_data['element_type'], prefix='position')
    player_data = pd.concat([player_data, positions], axis=1)
    return player_data

def compute_value_efficiency(player_data):
    """
    Player value (cost) efficiency.
    """
    player_data['value_efficiency'] = player_data['total_points'] / player_data['value']
    return player_data

def compute_rolling_averages(player_data, windows=[2, 3, 4]):
    """
    Average performance over the last n game weeks.
    """
    for window in windows:
        col_name = f"avg_last_{window}_gws"
        player_data[col_name] = player_data.groupby('name')['total_points'].rolling(window=window).mean().reset_index(level=0, drop=True)
    return player_data

def preprocess_data(player_data, team_data):
    player_data = compute_form(player_data)
    player_data = compute_home_away_advantage(player_data)
    player_data = compute_team_strength(player_data, team_data)
    player_data = compute_opponent_strength(player_data, team_data)
    player_data = compute_position_based_features(player_data)
    player_data = compute_value_efficiency(player_data)
    player_data = compute_rolling_averages(player_data)
    return player_data

players.to_csv('data_preprocessing.csv', index=False)
