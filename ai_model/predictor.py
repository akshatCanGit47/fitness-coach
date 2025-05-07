import joblib
import pandas as pd
import numpy as np
from django.conf import settings

# Load model and encoder
model = joblib.load('ai_model/trained_model.h5')
encoder = joblib.load('ai_model/encoder.h5')

def predict_calories(workout_type, duration):
    try:
        # Create input DataFrame
        input_data = pd.DataFrame([[workout_type, duration]],
                                columns=['workout_type', 'duration'])
        
        # Encode categorical feature (returns dense array)
        encoded = encoder.transform(input_data[['workout_type']])
        
        # Combine features
        features = np.concatenate(
            [encoded, input_data[['duration']].values],
            axis=1
        )
        
        # Make prediction
        prediction = model.predict(features)
        return round(float(prediction[0]), 2)
        
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        raise