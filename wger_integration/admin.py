from django.contrib import admin
from .models import WgerExercise

@admin.register(WgerExercise)
class WgerExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'muscle_group', 'difficulty', 'equipment')
    search_fields = ('name', 'category', 'muscle_group')
