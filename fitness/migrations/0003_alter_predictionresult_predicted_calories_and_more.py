# Generated by Django 5.2 on 2025-05-05 09:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0002_alter_meal_options_alter_workout_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predictionresult',
            name='predicted_calories',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='predictionresult',
            name='workout',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='predictionresult', to='fitness.workout'),
        ),
    ]
