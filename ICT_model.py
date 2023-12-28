import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pickle
import os

# Load data
players = pd.read_csv('feature_engineering.csv')

# Extract ICT metrics and shift total_points to predict next gameweek's points
ict_data = players[['name', 'GW', 'influence', 'creativity', 'threat', 'ict_index', 'total_points']].copy()

# Convert columns to numeric
ict_data['influence'] = pd.to_numeric(ict_data['influence'], errors='coerce')
ict_data['creativity'] = pd.to_numeric(ict_data['creativity'], errors='coerce')
ict_data['threat'] = pd.to_numeric(ict_data['threat'], errors='coerce')
ict_data['ict_index'] = pd.to_numeric(ict_data['ict_index'], errors='coerce')

# Shift total_points to create 'next_gw_points'
ict_data['next_gw_points'] = ict_data.groupby('name')['total_points'].shift(-1)

# Instead of dropping NaNs, we fill them with a default value of 0
ict_data.fillna(0, inplace=True)

# Define features and target variable
features_ict = ['influence', 'creativity', 'threat', 'ict_index']
target_ict = 'next_gw_points'

# Split data into training and validation sets
X_ict = ict_data[features_ict]
y_ict = ict_data[target_ict]
X_train_ict, X_val_ict, y_train_ict, y_val_ict = train_test_split(X_ict, y_ict, test_size=0.2, random_state=42)

# Train RandomForestRegressor model
model_ict = RandomForestRegressor(n_estimators=100, random_state=42)
model_ict.fit(X_train_ict, y_train_ict)

# Predict next gameweek's points for the validation set and calculate RMSE
y_pred_ict = model_ict.predict(X_val_ict)
rmse_ict = mean_squared_error(y_val_ict, y_pred_ict, squared=False)

# Train the RandomForestRegressor model on the entire data
model_ict.fit(X_ict, y_ict)

# Predict next gameweek's points for the entire dataset
ict_data['predicted_points'] = model_ict.predict(X_ict)

# Save the predictions to a CSV file
ict_data[['name', 'GW', 'predicted_points']].to_csv("ict_predictions.csv", index=False)


if ict_data[['influence', 'creativity', 'threat', 'ict_index']].isnull().sum().any():
    print("Some values failed to convert to numbers in the ICT metrics.")
print(ict_data['next_gw_points'].describe())
unique_target_values = ict_data['next_gw_points'].nunique()
if unique_target_values == 1:
    print(f"There is only 1 unique value in 'next_gw_points': {ict_data['next_gw_points'].iloc[0]}")
else:
    print(f"There are {unique_target_values} unique values in 'next_gw_points'.")
print(f"Training data size: {X_train_ict.shape[0]} rows")
print(f"Validation data size: {X_val_ict.shape[0]} rows")
print("First 10 Predicted values:", y_pred_ict[:10])
print("First 10 Actual values:", y_val_ict.iloc[:10].values)
unique_predictions = pd.Series(y_pred_ict).nunique()
if unique_predictions == 1:
    print(f"All predictions are the same: {y_pred_ict[0]}")
else:
    print(f"There are {unique_predictions} unique predicted values.")
print(ict_data['total_points'].describe())
sample_player = ict_data['name'].iloc[0]
print(ict_data[ict_data['name'] == sample_player][['GW', 'total_points', 'next_gw_points']])


print("RMSE for ICT model:", rmse_ict)

# Save the trained model
dir_path = 'C:/Users/afloy/OneDrive/Desktop/Data Science/Fantasy Prem/Fantasy Prem 2023'
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

with open(os.path.join(dir_path, 'ICT_model.pkl'), 'wb') as f:
    pickle.dump(model_ict, f)
