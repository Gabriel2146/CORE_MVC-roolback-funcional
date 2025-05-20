import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from training.services import TrainingPlanGenerator
from wger_integration.models import WgerExercise
from training.models import Exercise

@pytest.mark.django_db
def test_fetch_wger_exercises_model():
    # Test that WgerExercise model can be created and queried
    exercise = WgerExercise.objects.create(
        wger_id=9999,
        name="Test Wger Exercise",
        category="strength",
        muscle_group="arms",
        difficulty="medium",
        equipment="dumbbell"
    )
    assert WgerExercise.objects.filter(wger_id=9999).exists()

@pytest.mark.django_db
def test_training_plan_generator_includes_wger_exercises():
    user_profile = type('UserProfile', (), {'availability': ['Monday'], 'restrictions': [], 'physical_info': None, 'condition_level': None})()
    training_history = []
    objectives = {'type': 'strength'}
    # Create local and wger exercises
    local_ex = Exercise.objects.create(name="Local Exercise", category="strength")
    wger_ex = WgerExercise.objects.create(wger_id=1, name="Wger Exercise", category="strength")
    generator = TrainingPlanGenerator(user_profile, training_history, objectives)
    plan = generator.generate_preliminary_plan()
    exercise_names = [ex['name'] for session in plan['sessions'] for ex in session['exercises']]
    assert "Local Exercise" in exercise_names or "Wger Exercise" in exercise_names

@pytest.mark.django_db
def test_api_generate_training_plan():
    client = APIClient()
    url = reverse('trainingplan-generate')  # Assuming this is the name of the endpoint
    data = {
        "user_profile": {
            "physical_info": "average",
            "condition_level": "intermediate",
            "restrictions": [],
            "availability": ["Monday", "Wednesday"]
        },
        "training_history": [],
        "objectives": {
            "type": "strength"
        }
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 200
    assert 'plan' in response.data

@pytest.mark.django_db
def test_api_sync_wger_exercises_command():
    from django.core.management import call_command
    call_command('sync_wger_exercises')
    count = WgerExercise.objects.count()
    assert count > 0
