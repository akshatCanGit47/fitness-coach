from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import joblib
import pandas as pd
import os
from django.conf import settings
from .models import Workout, Meal, PredictionResult

# Load AI model
model = joblib.load(os.path.join(settings.BASE_DIR, 'ai_model/trained_model.h5'))
encoder = joblib.load(os.path.join(settings.BASE_DIR, 'ai_model/encoder.h5'))

@login_required
def dashboard(request):
    if request.method == 'POST':
        # Handle workout prediction
        if 'predict_workout' in request.POST:
            try:
                workout_type = request.POST['workout_type'].strip()
                duration = int(request.POST['duration'])
                
                # Create workout with prediction
                workout = Workout.objects.create(
                    user=request.user,
                    workout_type=workout_type,
                    duration=duration,
                    calories_burned=0  # Temporary value
                )
                
                # Make prediction
                calories = predict_calories(workout_type, duration)
                workout.calories_burned = calories
                workout.save()
                
                # Create prediction record
                prediction = PredictionResult.objects.create(
                    user=request.user,
                    workout=workout,
                    predicted_calories=calories
                )
                
                return redirect('fitness:result', prediction_id=prediction.id)
            
            except Exception as e:
                messages.error(request, f"Workout error: {str(e)}")
        
        # Handle meal logging
        elif 'log_meal' in request.POST:
            try:
                Meal.objects.create(
                    user=request.user,
                    meal_type=request.POST['meal_type'].strip(),
                    calories=float(request.POST['meal_calories'])
                )
                messages.success(request, "Meal logged successfully!")
                return redirect('dashboard')
            
            except Exception as e:
                messages.error(request, f"Meal error: {str(e)}")
    
    # Get data
    workouts = Workout.objects.filter(user=request.user)
    meals = Meal.objects.filter(user=request.user)
    
    return render(request, 'fitness/dashboard.html', {
        'workouts': workouts,
        'meals': meals
    })

@login_required
def result_view(request, prediction_id):
    prediction = get_object_or_404(PredictionResult, id=prediction_id, user=request.user)
    return render(request, 'fitness/result.html', {'prediction': prediction})

def predict_calories(workout_type, duration):
    input_df = pd.DataFrame([[workout_type, duration]], columns=['workout_type', 'duration'])
    encoded = encoder.transform(input_df[['workout_type']])
    features = pd.concat([
        pd.DataFrame(encoded, columns=encoder.get_feature_names_out()),
        input_df[['duration']]
    ], axis=1)
    return round(float(model.predict(features)[0]), 2)