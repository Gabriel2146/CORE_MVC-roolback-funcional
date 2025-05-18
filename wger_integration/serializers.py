from rest_framework import serializers
from .models import WgerExercise

class WgerExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WgerExercise
        fields = '__all__'
