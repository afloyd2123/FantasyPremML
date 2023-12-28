def get_predictions(preprocessed_data, opponent_model, valuation_model, ict_model):
    """
    Use the three models to get predictions for the current gameweek.
    """
    opponent_predictions = opponent_model.predict(preprocessed_data)
    valuation_predictions = valuation_model.predict(preprocessed_data)
    ict_predictions = ict_model.predict(preprocessed_data)

    predictions_df = pd.DataFrame({
        'player_id': preprocessed_data['id'],
        'opponent_predictions': opponent_predictions,
        'valuation_predictions': valuation_predictions,
        'ict_predictions': ict_predictions
    })

    return predictions_df
