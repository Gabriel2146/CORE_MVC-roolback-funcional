import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Exercise, TrainingPlan, TrainingSession, ExerciseEntry
from wger_integration.models import WgerExercise

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    user = User.objects.create_user(username='testuser', password='testpass', role='athlete')
    return user

@pytest.fixture
def trainer(db):
    user = User.objects.create_user(username='traineruser', password='trainerpass', role='trainer')
    return user

@pytest.fixture
def exercise(db):
    return Exercise.objects.create(name='Push Up', wger_id=1, category='strength')

@pytest.fixture
def wger_exercise(db):
    return WgerExercise.objects.create(wger_id=100, name='Squat', category='strength')

@pytest.mark.django_db
def test_generate_training_plan(api_client, trainer):
    api_client.force_authenticate(user=trainer)
    url = reverse('trainingplan-generate')
    data = {
        'user_profile': {'availability': ['Monday', 'Wednesday']},
        'training_history': [],
        'objectives': {'type': 'strength'}
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'plan' in response.data

@pytest.mark.django_db
def test_add_feedback_to_session(api_client, user, exercise):
    api_client.force_authenticate(user=user)
    plan = TrainingPlan.objects.create(user=user, name='Plan 1')
    session = TrainingSession.objects.create(training_plan=plan, date='2023-01-01')
    url = reverse('trainingsession-add-feedback', args=[session.id])
    data = {'perceived_effort': 0.7, 'total_duration': 3600, 'notes': 'Good session'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    session.refresh_from_db()
    assert session.perceived_effort == 0.7
    assert session.notes == 'Good session'

@pytest.mark.django_db
def test_progress_analysis(api_client, user):
    api_client.force_authenticate(user=user)
    plan = TrainingPlan.objects.create(user=user, name='Plan 1')
    session = TrainingSession.objects.create(training_plan=plan, date='2023-01-01')
    url = reverse('trainingsession-progress-analysis', args=[session.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'progress' in response.data

@pytest.mark.django_db
def test_add_metrics_to_exercise_entry(api_client, user, exercise):
    api_client.force_authenticate(user=user)
    plan = TrainingPlan.objects.create(user=user, name='Plan 1')
    session = TrainingSession.objects.create(training_plan=plan, date='2023-01-01')
    entry = ExerciseEntry.objects.create(session=session, exercise=exercise, sets=3, reps=10, weight=20)
    url = reverse('exerciseentry-add-metrics', args=[entry.id])
    data = {'rest_time': 60, 'perceived_effort': 0.8, 'sets': 4, 'reps': 12, 'weight': 25}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    entry.refresh_from_db()
    assert entry.rest_time.total_seconds() == 60
    assert entry.perceived_effort == 0.8
    assert entry.sets == 4
    assert entry.reps == 12
    assert entry.weight == 25

@pytest.mark.django_db
def test_training_plan_generator_adjust_plan_dynamic():
    from training.services import TrainingPlanGenerator
    user_profile = type('UserProfile', (), {'restrictions': [], 'availability': ['Monday', 'Wednesday']})()
    training_history = [
        {
            'date': datetime.now().date(),
            'exercises': [{'name': 'Push Up', 'sets': 4, 'reps': 8}]
        }
    ]
    objectives = {'type': 'strength'}
    generator = TrainingPlanGenerator(user_profile, training_history, objectives)
    feedback = {'missed_sessions': 3, 'perceived_effort': 0.9, 'progress_metrics': {}}
    adjusted_plan = generator.adjust_plan_dynamic(feedback)
    assert adjusted_plan is not None
    for session in adjusted_plan:
        for ex in session['exercises']:
            assert ex['sets'] <= 4
            assert ex['reps'] <= 8

@pytest.mark.django_db
def test_training_session_progress_analysis(api_client, user):
    api_client.force_authenticate(user=user)
    plan = TrainingPlan.objects.create(user=user, name='Plan 1')
    session = TrainingSession.objects.create(training_plan=plan, date='2023-01-01', perceived_effort=0.9, missed_sessions=3)
    url = reverse('trainingsession-progress-analysis', args=[session.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'progress' in response.data
    assert 'deviations' in response.data
    assert 'recommendations' in response.data
    assert 'High perceived effort' in response.data['deviations']
    assert 'Multiple missed sessions' in response.data['deviations']
