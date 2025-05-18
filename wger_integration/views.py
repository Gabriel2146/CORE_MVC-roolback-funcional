from rest_framework import viewsets
from .models import WgerExercise
from .serializers import WgerExerciseSerializer

class WgerExerciseViewSet(viewsets.ModelViewSet):
    queryset = WgerExercise.objects.all()
    serializer_class = WgerExerciseSerializer
