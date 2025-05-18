from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExerciseViewSet, TrainingPlanViewSet, TrainingSessionViewSet, ExerciseEntryViewSet

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet)
router.register(r'training-plans', TrainingPlanViewSet, basename='trainingplan')
router.register(r'training-sessions', TrainingSessionViewSet)
router.register(r'exercise-entries', ExerciseEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
