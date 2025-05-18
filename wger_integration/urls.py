from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WgerExerciseViewSet

router = DefaultRouter()
router.register(r'exercises', WgerExerciseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
