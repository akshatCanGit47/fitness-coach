# ai_model/model_trainer.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
import joblib
import os

def train_and_save_model():
    # Create sample training data (replace with real data)
    data = pd.DataFrame([
        ['Running', 30, 300],
        ['Cycling', 45, 400],
        ['Swimming', 60, 500],
        ['Yoga', 45, 250],
        ['Weightlifting', 60, 350],
        ['Pilates', 30, 200],
        ['Boxing', 60, 600]
    ], columns=['workout_type', 'duration', 'calories'])

    try:
        # Create output directory if not exists
        os.makedirs('ai_model', exist_ok=True)

        # Initialize and fit encoder
        encoder = OneHotEncoder(
            handle_unknown='ignore',
            sparse_output=False  # Set to False for dense arrays
        )
        encoder.fit(data[['workout_type']])

        # Transform workout types
        encoded_types = encoder.transform(data[['workout_type']])

        # Combine features
        X = np.concatenate(
            [encoded_types, data[['duration']].values],
            axis=1
        )
        y = data['calories']

        # Train model
        model = LinearRegression()
        model.fit(X, y)

        # Test prediction
        test_input = encoder.transform([['Running']])
        test_features = np.concatenate(
            [test_input, np.array([[30]])],
            axis=1
        )
        test_pred = model.predict(test_features)
        print(f"Test prediction (Running, 30min): {test_pred[0]:.1f} calories")

        # Save artifacts
        joblib.dump(model, 'ai_model/trained_model.h5')
        joblib.dump(encoder, 'ai_model/encoder.h5')
        print("Model training successful! Files saved to ai_model/")

    except Exception as e:
        print(f"Model training failed: {str(e)}")
        raise

if __name__ == "__main__":
    train_and_save_model()