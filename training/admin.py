from django.contrib import admin
from .models import Exercise, TrainingPlan, TrainingSession, ExerciseEntry

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'muscle_group', 'difficulty', 'equipment')
    search_fields = ('name', 'category', 'muscle_group')

@admin.register(TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at')
    search_fields = ('name', 'user__username')
    list_filter = ('created_at',)

@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ('training_plan', 'date')
    list_filter = ('date',)

@admin.register(ExerciseEntry)
class ExerciseEntryAdmin(admin.ModelAdmin):
    list_display = ('session', 'exercise', 'sets', 'reps', 'weight')
    search_fields = ('exercise__name',)
