from django.db import models
from django.conf import settings

class Exercise(models.Model):
    wger_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=255, blank=True)
    muscle_group = models.CharField(max_length=255, blank=True)
    difficulty = models.CharField(max_length=50, blank=True)
    equipment = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class TrainingPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='training_plans')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    goals = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} for {self.user.username}"

class TrainingSession(models.Model):
    training_plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Session on {self.date} for {self.training_plan.name}"

class ExerciseEntry(models.Model):
    session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE, related_name='exercise_entries')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(default=0)
    reps = models.IntegerField(default=0)
    weight = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.exercise.name} in session {self.session.id}"
