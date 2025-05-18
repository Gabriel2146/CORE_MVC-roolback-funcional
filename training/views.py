from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Exercise, TrainingPlan, TrainingSession, ExerciseEntry
from .serializers import ExerciseSerializer, TrainingPlanSerializer, TrainingSessionSerializer, ExerciseEntrySerializer
from .services import TrainingPlanGenerator
from users.permissions import IsAdmin, IsTrainer, IsAthlete, IsGuest
from rest_framework.permissions import IsAuthenticated

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

class TrainingPlanViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingPlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return TrainingPlan.objects.all()
        return TrainingPlan.objects.filter(user=user)

    @action(detail=False, methods=['post'], permission_classes=[IsTrainer])
    def generate(self, request):
        user_profile = request.data.get('user_profile')
        training_history = request.data.get('training_history')
        objectives = request.data.get('objectives')

        # For demonstration, we pass the raw data; in real app, fetch user profile and history from DB
        generator = TrainingPlanGenerator(user_profile, training_history, objectives)
        plan = generator.create_plan()

        return Response({'plan': plan}, status=status.HTTP_201_CREATED)

class TrainingSessionViewSet(viewsets.ModelViewSet):
    queryset = TrainingSession.objects.all()
    serializer_class = TrainingSessionSerializer
    permission_classes = [IsAuthenticated]

class ExerciseEntryViewSet(viewsets.ModelViewSet):
    queryset = ExerciseEntry.objects.all()
    serializer_class = ExerciseEntrySerializer
    permission_classes = [IsAuthenticated]
