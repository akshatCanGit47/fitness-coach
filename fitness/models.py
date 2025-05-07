from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_type = models.CharField(max_length=100)
    duration = models.IntegerField()
    calories_burned = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)  # Correct field name

    class Meta:
        ordering = ['-created_at']  # Default ordering

    def __str__(self):
        return f"{self.workout_type} ({self.duration} mins)"
    
class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=100)
    calories = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)  # Correct field name

    class Meta:
        ordering = ['-created_at']  # Default ordering

    def __str__(self):
        return f"{self.meal_type} ({self.calories} kcal)"

class PredictionResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.OneToOneField(  # Changed to OneToOneField
        Workout, 
        on_delete=models.CASCADE,
        related_name='predictionresult' ,
         null=True # This enables workout.predictionresult
    )
    predicted_calories = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.workout.workout_type} - {self.predicted_calories}kcal"