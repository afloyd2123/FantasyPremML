import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# # Load datasets
# data = pd.read_csv("C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023/Fantasy-Premier-League/data/2021-22/gws/data.csv")
# cleaned_players = pd.read_csv("C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023/Fantasy-Premier-League/data/2021-22/cleaned_players.csv")

# # Create a unique identifier for players
# cleaned_players['name'] = cleaned_players['first_name'] + "_" + cleaned_players['second_name']
# data['name'] = data['name']

data = pd.read_csv("feature_engineering.csv")

# Calculate the valuation change for each player for each gameweek
data['valuation_change'] = data.groupby('name')['value'].diff().fillna(0)

# Prepare data for the model
features = ['minutes', 'goals_scored', 'assists', 'clean_sheets', 'goals_conceded', 'bonus', 'bps', 'influence', 'creativity', 'threat', 'ict_index', 'yellow_cards', 'red_cards']
X = data[features]
y = data['valuation_change']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Predict on test data
y_pred = rf.predict(X_test)

# Calculate RMSE
rmse = mean_squared_error(y_test, y_pred, squared=False)
print(f"RMSE for Valuation Model: {rmse}")


# Predict the valuation change for the entire dataset
data['predicted_valuation_change'] = rf.predict(X)

# Save the predictions to a CSV file
data[['name', 'GW', 'predicted_valuation_change']].to_csv("valuation_predictions.csv", index=False)

# Display the first few rows of the predictions
data[['name', 'GW', 'predicted_valuation_change']].head()

# # Save the trained model
# with open('C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023/valuation_model.pkl', 'wb') as f:
#     pickle.dump(model, f)
import os
dir_path = 'C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023'
if not os.path.exists(dir_path):
    os.makedirs(dir_path)