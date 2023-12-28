import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# # Load datasets with the specified paths
# data = pd.read_csv("C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023/Fantasy-Premier-League/data/2021-22/gws/data.csv")
# data = pd.read_csv("C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023/Fantasy-Premier-League/data/2021-22/data.csv")
# teams = pd.read_csv("C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023/current_data/teams.csv")
# fixtures = pd.read_csv("C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023/current_data/fixtures.csv")

data = pd.read_csv("feature_engineering.csv")
# 1. Data Integrity Checks:
print("Checking for missing values...")
print(data.isnull().sum())

# Check distribution of key columns
print("\nDistribution of 'total_points':")
print(data['total_points'].describe())

# 2. Data Distribution Checks:
# Assuming 'home' is a binary column indicating if the match is home (1) or away (0)
if 'home' in data.columns:
    print("\nBalance of home and away matches:")
    print(data['home'].value_counts())
# List of necessary columns
data_columns = ['team', 'name', 'opponent_team', 'total_points', 'round', 'strength_overall_home', 'strength_attack_home', 'strength_defence_home', 
            'strength_overall_away', 'strength_attack_away', 'strength_defence_away', 'was_home', 'GW']
# teams_columns = ['name', 'id']
# fixture_columns = ['event', 'team_a', 'team_h']
# Drop columns that are not in the list of necessary columns
data = data[data_columns]
# teams = teams[teams_columns]
# fixtures = fixtures[fixture_columns]


# # Merge the relevant columns from fixtures into data based on a common column (assuming it's 'round')
# data = pd.merge(data, fixtures[['event', 'team_a', 'team_h']], left_on='round', right_on='event', how='left')

# Mapping team IDs to team names
# Create a mapping from team IDs to team names
# team_id_name_map = dict(zip(teams['id'], teams['name']))

# # Using the mapping to get team names for team_a and team_h in fixtures data
# data['Home Team'] = data['team_h'].map(team_id_name_map)
# data['Away Team'] = data['team_a'].map(team_id_name_map)


# # Mapping to get opponent name in data
# data['opponent_name'] = data['opponent_team'].map(teams.set_index('id')['name'])

# # Calculate average points for home and away
# avg_points_home = data.groupby('team')['total_points'].mean().reset_index()
# avg_points_home.columns = ['Home Team', 'avg_points_home']
# avg_points_away = data.groupby('opponent_name')['total_points'].mean().reset_index()
# avg_points_away.columns = ['Away Team', 'avg_points_away']

# # Merge average points with data
# data = data.merge(avg_points_home, on='Home Team', how='left')
# data = data.merge(avg_points_away, on='Away Team', how='left')

# # Prepare data for model
# data_for_model = data.merge(data[['Home Team', 'Away Team', 'avg_points_home', 'avg_points_away']], left_on=['team', 'opponent_name'], right_on=['Home Team', 'Away Team'], how='left')
# data_for_model = data_for_model[['total_points', 'avg_points_home', 'avg_points_away']].dropna()

# X = data_for_model[['avg_points_home', 'avg_points_away']]
# y = data_for_model['total_points']

# # Split data, train model, and predict
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
# rf_model.fit(X_train, y_train)
# y_pred = rf_model.predict(X_test)

# # Calculate RMSE
# rmse = mean_squared_error(y_test, y_pred, squared=False)
# print(f"RMSE for Opponent-based model: {rmse}")

# # # Save the trained model
# # with open('C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023/opponent_model.pkl', 'wb') as f:
# #     pickle.dump(rf_model, f)
# import os
# dir_path = 'C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023'
# if not os.path.exists(dir_path):
#     os.makedirs(dir_path)

data['opposition_overall_strength'] = np.where(data['was_home'], data['strength_overall_away'], data['strength_overall_home'])
data['opposition_attack_strength'] = np.where(data['was_home'], data['strength_attack_away'], data['strength_attack_home'])
data['opposition_defence_strength'] = np.where(data['was_home'], data['strength_defence_away'], data['strength_defence_home'])

# Selecting relevant columns
features = ['strength_overall_home', 'strength_attack_home', 'strength_defence_home', 
            'strength_overall_away', 'strength_attack_away', 'strength_defence_away']
X = data[features]
y = data['total_points']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predict
y_pred = rf_model.predict(X_test)


# Predict the points for the entire dataset
data['predicted_points_opponent'] = rf_model.predict(X)

# Save the predictions to a CSV file
data[['name', 'GW', 'predicted_points_opponent']].to_csv("opponent_predictions.csv", index=False)

# Display the first few rows of the predictions
data[['name', 'GW', 'predicted_points_opponent']].head()

# 3. Model Performance Checks:
y_train_pred = rf_model.predict(X_train)
y_val_pred = rf_model.predict(X)
print("\nTraining RMSE:", mean_squared_error(y_train, y_train_pred, squared=False))
print("Validation RMSE:", mean_squared_error(y, y_val_pred, squared=False))

# 4. Prediction Sanity Checks:
print("\nPredicted values range:")
print("Min:", y_val_pred.min(), "Max:", y_val_pred.max())

# Comparing to a simple baseline
baseline_pred = [y_train.mean()] * len(y)
print("\nBaseline RMSE:", mean_squared_error(y, baseline_pred, squared=False))

# Calculate RMSE
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f"RMSE: {rmse}")

import os
dir_path = 'C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023'
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

with open(os.path.join(dir_path, 'opponent_model.pkl'), 'wb') as f:
    pickle.dump(rf_model, f)