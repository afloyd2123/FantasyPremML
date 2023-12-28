import pandas as pd
import numpy as np
import os

base_dir = "C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023/"
###################Please Read Below############################
#Initializing Last Seasons Model: Load datasets 
teams_path = os.path.join(base_dir, "Fantasy-Premier-League/data/2022-23/teams.csv")
fixtures_path = os.path.join(base_dir, "Fantasy-Premier-League/data/2022-23/fixtures.csv")
gws_path = os.path.join(base_dir, "Fantasy-Premier-League/data/2022-23/gws/merged_gw.csv")
players_path = os.path.join(base_dir, 'data_preprocessing.csv')

# #Initializing This Season's Model: Load Datasets
# teams_path = os.path.join(base_dir, "Fantasy-Premier-League/data/2023-24/teams.csv")
# fixtures_path = os.path.join(base_dir, "Fantasy-Premier-League/data/2023-24/fixtures.csv")
# gws_path = os.path.join(base_dir, "Fantasy-Premier-League/data/2023-24/gws/merged_gw.csv")
# players_path = os.path.join(base_dir, 'data_preprocessing.csv')


teams = pd.read_csv(teams_path)
fixtures = pd.read_csv(fixtures_path)
gws = pd.read_csv(gws_path)
players = pd.read_csv(players_path)

# if __name__ == "__main__":
#     # Load necessary datasets
#     player_data = pd.read_csv("C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023/current_data/cleaned_players.csv")
#     teams_data = pd.read_csv("C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023/current_data/teams.csv")
#     gws_data = pd.read_csv("C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023/current_data/merged_gw.csv")
    
# Fill missing values
players.fillna(0, inplace=True)
teams.fillna(0, inplace=True)
gws.fillna(0, inplace=True)

# Concatenate the names
# players['name'] = players['first_name'] + ' ' + players['second_name']

# Identify duplicate names
duplicate_names = players['name'].value_counts()
duplicate_names = duplicate_names[duplicate_names > 1].index.tolist()

# Drop rows with duplicate names
players = players[~players['name'].isin(duplicate_names)]


def generate_features(players, teams, gws):
    """
    Generate features for the dataset.
    """

    # # Generate features
    # enhanced_player_data = generate_features(players, teams, gws)
    # # Save the enhanced data for further processing
    # enhanced_player_data.to_csv("C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023/", index=False)

    # Map team names to team IDs
    team_map = teams.set_index('id').name.to_dict()
    gws['team_name'] = gws['team'].map(team_map)

    # Create a mapping for home and away teams in fixtures
    fixtures['home_team'] = fixtures['team_a'].map(team_map)
    fixtures['away_team'] = fixtures['team_h'].map(team_map)

    # Merge gws and fixtures on game week and team
    gws = gws.merge(fixtures, left_on=['gw', 'team_name'], right_on=['gw', 'home_team'], how='left')

    # If the player's team matches home_team after merging, then they played at home; otherwise, they played away
    gws['match_location'] = np.where(gws['team_name'] == gws['home_team'], 'home', 'away')

    # Convert match_location to a binary flag for ease of use in modeling
    gws['home'] = (gws['match_location'] == 'home').astype(int)

    return gws

# # Drop unnecessary columns
# gws.drop(columns=['team_name'], inplace=True)

####################### remove form column
gws['form']=0


# Calculate rolling average for total points, form, and value over the last 5 game weeks
gws['rolling_avg_points'] = gws.groupby('name')['total_points'].transform(lambda x: x.rolling(5, 1).mean())

if 'form' in gws.columns:
    gws['rolling_avg_form'] = gws.groupby('name')['form'].transform(lambda x: x.rolling(5, 1).mean())

gws['rolling_avg_value'] = gws.groupby('name')['value'].transform(lambda x: x.rolling(5, 1).mean())

# Assuming you have already created the 'full_name' column in both DataFrames as discussed

# Merge gws and players on full_name to get element_type
gws = pd.merge(gws, players[['name', 'element_type']], left_on='name', right_on='name', how='left')

# # Rename the element_type column to position
# gws.rename(columns={'element_type': 'position'}, inplace=True)


def home_away_factor(gws_data, fixtures):
    # Merge gws_data and fixtures on game week and team to get match location
    gws_data = gws_data.merge(fixtures, left_on=['gw', 'team'], right_on=['gw', 'team_h'], how='left')
    
    # If the merge on team_h was successful, it means the match was at home. Else, it was away.
    gws_data['home_away'] = gws_data['team_h'].apply(lambda x: 1 if pd.notnull(x) else 0)
    
    return gws_data


# def add_ict_index(players, gws_data):
#     # Logic to add ICT index for each player
#     pass

def valuation_change_trend(players, gws_data):
    # Calculate the valuation change for each game week
    gws_data['valuation_change'] = gws_data.groupby('name')['value'].diff().fillna(0)
    
    # Compute the valuation change trend over the last 5 game weeks
    gws_data['valuation_trend_last_5'] = gws_data.groupby('name')['valuation_change'].transform(lambda x: x.rolling(5, 1).sum())
    
    return gws_data


import pandas as pd

def calculate_team_avg_points(data, is_home):
    """
    Calculate average points scored by a team at home/away.
    """
    if is_home:
        team_points = data.groupby('team')['total_points'].mean().reset_index()
        team_points.columns = ['team', 'avg_home_points']
    else:
        team_points = data.groupby('opponent_team')['total_points'].mean().reset_index()
        team_points.columns = ['team', 'avg_away_points']

    return team_points

def calculate_team_form(data, team_id, recent_games=5):
    """
    Calculate the form of a team based on recent performances.
    """
    team_data = data[data['team'] == team_id]
    team_data = team_data.sort_values(by='round', ascending=False).head(recent_games)
    total_points = team_data['total_points'].sum()
    avg_points_last_5 = total_points / recent_games
    return avg_points_last_5

def calculate_player_form(data, name, recent_games=3):
    """
    Calculate the average performance of a player over the last few matches.
    """
    players = data[data['name'] == name]
    players = players.sort_values(by='round', ascending=False).head(recent_games)
    total_points = players['total_points'].sum()
    avg_points_last_3 = total_points / recent_games
    return avg_points_last_3

# Placeholder for Injury Status
def is_player_injured(player_name, user_team_file="user_team.xlsx"):
    df = pd.read_excel(user_team_file)
    player_data = df[df['name'] == player_name]
    if player_data.empty:
        return "Player not found in user team"
    injury_status = "Injured" if player_data['Injury Status'].iloc[0] == 1 else "Not Injured"
    injury_notes = player_data['Injury Notes'].iloc[0]
    return injury_status, injury_notes


# More feature functions can be added...


    # Team average points
    home_points = calculate_team_avg_points(data, True)
    away_points = calculate_team_avg_points(data, False)
    data = data.merge(home_points, on='team', how='left')
    data = data.merge(away_points, on='opponent_team', how='left')

    # Team form
    data['team_form'] = data.apply(lambda x: calculate_team_form(data, x['team']), axis=1)
    data['opponent_team_form'] = data.apply(lambda x: calculate_team_form(data, x['opponent_team']), axis=1)

    # Player form
    data['player_form'] = data.apply(lambda x: calculate_player_form(data, x['name']), axis=1)

    # Injury status
    data['is_injured'] = data.apply(lambda x: is_player_injured(x['name']), axis=1)

    # Other features...
    
    return data

# Sample usage:
# df = pd.read_csv("your_data_file.csv")
# enhanced_df = generate_features(df)


# def generate_features(player_data, teams_data, gws_data):
#     player_data = calculate_form(player_data, gws_data)
#     player_data = calculate_team_strength(teams_data, gws_data)
#     player_data = calculate_opponent_strength(teams_data, gws_data)
#     player_data = home_away_factor(gws_data)
#     player_data = add_ict_index(player_data, gws_data)
#     player_data = valuation_change_trend(player_data, gws_data)
#     return player_data


# Encode categorical features
players = pd.get_dummies(players, columns=['element_type'])
# fixture = pd.get_dummies(fixtures, columns=['team_h_difficulty', 'team_a_difficulty'])

# 1. Player's performance metrics relative to team average
team_avg = gws.groupby('team')['total_points'].mean().reset_index()
team_avg.columns = ['team', 'team_avg_points']
gws = gws.merge(team_avg, on='team', how='left')
gws['relative_performance'] = gws['total_points'] - gws['team_avg_points']

# 2. Player's form - average points in the last 3 games
gws['form_last_3'] = gws.groupby('name')['total_points'].rolling(window=3).mean().reset_index(0, drop=True)

# 3. Team's form - average points in the last 3 games
team_form_last_3 = gws.groupby(['team', 'round'])['total_points'].sum().rolling(window=3).mean().reset_index()
team_form_last_3.columns = ['team', 'round', 'team_form_last_3']
gws = gws.merge(team_form_last_3, on=['team', 'round'], how='left')

# 4. Opponent's strength - use 'team_h_difficulty' and 'team_a_difficulty' from teams dataset
# Assuming 'opponent_team' in gws corresponds to 'id' in teams
gws = gws.merge(fixtures[['id', 'team_h_difficulty', 'team_a_difficulty']], left_on='opponent_team', right_on='id', how='left')
gws['opponent_strength'] = np.where(gws['was_home'], gws['team_a_difficulty'], gws['team_h_difficulty'])

strength_columns = ['id', 'strength_overall_home', 'strength_overall_away', 
                    'strength_attack_home', 'strength_attack_away', 
                    'strength_defence_home', 'strength_defence_away']

gws = gws.merge(teams[strength_columns], left_on='opponent_team', right_on='id', how='left')


# Drop intermediate columns
# gws.drop(columns=['team_avg_points', 'id', 'team_h_difficulty', 'team_a_difficulty'], inplace=True)
columns_to_drop = ['team_avg_points', 'id', 'team_h_difficulty', 'team_a_difficulty']
existing_columns = [col for col in columns_to_drop if col in gws.columns]
gws.drop(columns=existing_columns, inplace=True)



# Save the preprocessed data
#gws.to_csv("C:\Users\afloy\OneDrive\Desktop\Data Science\Fantasy Prem\Fantasy Prem 2023/data_preprocessing.csv", index=False)
gws.to_csv("C:\\Users\\afloy\\OneDrive\\Desktop\\Data Science\\Fantasy Prem\\Fantasy Prem 2023\\feature_engineering.csv", index=False)


