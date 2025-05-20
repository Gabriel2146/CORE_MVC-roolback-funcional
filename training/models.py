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

    # New fields for adaptive optimization metrics
    fatigue_index = models.FloatField(null=True, blank=True, help_text="Fatigue index for the plan (0-1 scale)")
    compatibility_index = models.FloatField(null=True, blank=True, help_text="Compatibility index for the plan (0-1 scale)")
    variation_index = models.FloatField(null=True, blank=True, help_text="Variation index for the plan (0-1 scale)")
    progression_index = models.FloatField(null=True, blank=True, help_text="Progression index for the plan (0-1 scale)")

    def __str__(self):
        return f"{self.name} for {self.user.get_username()}"

class TrainingSession(models.Model):
    training_plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    notes = models.TextField(blank=True)
    total_duration = models.DurationField(null=True, blank=True)
    perceived_effort = models.FloatField(null=True, blank=True, help_text="Perceived effort for the session (0-1 scale)")

    # New fields for session metrics and feedback
    missed_sessions = models.IntegerField(default=0, help_text="Number of missed sessions")
    deviation_detected = models.BooleanField(default=False, help_text="Flag for detected deviation in progress")
    recommendations = models.TextField(blank=True, help_text="Recommendations based on progress analysis")

    def __str__(self):
        return f"Session on {self.date} for {self.training_plan.name}"

class ExerciseEntry(models.Model):
    session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE, related_name='exercise_entries')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(default=0)
    reps = models.IntegerField(default=0)
    weight = models.FloatField(default=0.0)
    rest_time = models.DurationField(null=True, blank=True, help_text="Rest time after exercise")
    perceived_effort = models.FloatField(null=True, blank=True, help_text="Perceived effort for the exercise (0-1 scale)")

    # New fields for detailed exercise metrics
    tempo = models.CharField(max_length=50, blank=True, help_text="Tempo of the exercise")
    time_under_tension = models.DurationField(null=True, blank=True, help_text="Time under tension for the exercise")

    def __str__(self):
        return f"{self.exercise.name} in session {self.session.pk}"
