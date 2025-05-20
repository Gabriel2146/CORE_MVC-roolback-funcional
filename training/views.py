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

    def create(self, request, *args, **kwargs):
        # Override create to set user automatically
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_feedback(self, request, pk=None):
        """
        Endpoint to add feedback and metrics to a training session.
        """
        session = self.get_object()
        perceived_effort = request.data.get('perceived_effort')
        total_duration = request.data.get('total_duration')
        notes = request.data.get('notes')
        missed_sessions = request.data.get('missed_sessions')
        deviation_detected = request.data.get('deviation_detected')
        recommendations = request.data.get('recommendations')

        if perceived_effort is not None:
            session.perceived_effort = perceived_effort
        if total_duration is not None:
            # Expecting total_duration in seconds
            from datetime import timedelta
            session.total_duration = timedelta(seconds=int(total_duration))
        if notes is not None:
            session.notes = notes
        if missed_sessions is not None:
            session.missed_sessions = missed_sessions
        if deviation_detected is not None:
            session.deviation_detected = deviation_detected
        if recommendations is not None:
            session.recommendations = recommendations

        session.save()
        serializer = self.get_serializer(session)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def progress_analysis(self, request, pk=None):
        """
        Endpoint to analyze progress and detect deviations for a session.
        """
        session = self.get_object()
        # Implement real analysis logic based on session data
        progress_status = "on track"
        deviations = []
        recommendations = "Keep following the plan."

        # Example logic: detect deviation if perceived effort is too high or missed sessions > threshold
        if session.perceived_effort and session.perceived_effort > 0.8:
            deviations.append("High perceived effort")
            progress_status = "needs attention"
            recommendations = "Consider reducing intensity."
        if session.missed_sessions and session.missed_sessions > 2:
            deviations.append("Multiple missed sessions")
            progress_status = "needs attention"
            recommendations = "Increase adherence to the plan."

        analysis_result = {
            "progress": progress_status,
            "deviations": deviations,
            "recommendations": recommendations
        }
        return Response(analysis_result, status=status.HTTP_200_OK)

class ExerciseEntryViewSet(viewsets.ModelViewSet):
    queryset = ExerciseEntry.objects.all()
    serializer_class = ExerciseEntrySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_metrics(self, request, pk=None):
        """
        Endpoint to add metrics and feedback to an exercise entry.
        """
        entry = self.get_object()
        rest_time = request.data.get('rest_time')
        perceived_effort = request.data.get('perceived_effort')
        sets = request.data.get('sets')
        reps = request.data.get('reps')
        weight = request.data.get('weight')

        from datetime import timedelta
        if rest_time is not None:
            entry.rest_time = timedelta(seconds=int(rest_time))
        if perceived_effort is not None:
            entry.perceived_effort = perceived_effort
        if sets is not None:
            entry.sets = sets
        if reps is not None:
            entry.reps = reps
        if weight is not None:
            entry.weight = weight

        entry.save()
        serializer = self.get_serializer(entry)
        return Response(serializer.data, status=status.HTTP_200_OK)
