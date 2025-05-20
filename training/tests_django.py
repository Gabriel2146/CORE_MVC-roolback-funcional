from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from training.services import TrainingPlanGenerator
from wger_integration.models import WgerExercise
from training.models import Exercise

class TrainingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_profile = type('UserProfile', (), {'availability': ['Monday'], 'restrictions': [], 'physical_info': None, 'condition_level': None})()
        self.training_history = []
        self.objectives = {'type': 'strength'}

    def test_wger_exercise_model(self):
        exercise = WgerExercise.objects.create(
            wger_id=9999,
            name="Test Wger Exercise",
            category="strength",
            muscle_group="arms",
            difficulty="medium",
            equipment="dumbbell"
        )
        self.assertTrue(WgerExercise.objects.filter(wger_id=9999).exists())

    def test_training_plan_generator_includes_wger_exercises(self):
        local_ex = Exercise.objects.create(wger_id=-1, name="Local Exercise", category="strength")
        wger_ex = WgerExercise.objects.create(wger_id=1, name="Wger Exercise", category="strength")
        generator = TrainingPlanGenerator(self.user_profile, self.training_history, self.objectives)
        plan = generator.generate_preliminary_plan()
        exercise_names = [ex['name'] for session in plan['sessions'] for ex in session['exercises']]
        self.assertTrue("Local Exercise" in exercise_names or "Wger Exercise" in exercise_names)

    def test_api_generate_training_plan(self):
        # Crear usuario y autenticar
        from users.models import User
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)

        # Asignar permisos o roles necesarios al usuario para acceder al endpoint
        # Esto depende de la implementación de permisos en el proyecto
        # Por ejemplo, si usa Django Guardian o grupos:
        # from django.contrib.auth.models import Group
        # group = Group.objects.get(name='Trainer')
        # user.groups.add(group)
        # user.save()

        url = reverse('trainingplan-generate')  # Ajustar según el nombre real del endpoint
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
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('plan', response.data)

    def test_api_sync_wger_exercises_command(self):
        from django.core.management import call_command
        call_command('sync_wger_exercises')
        count = WgerExercise.objects.count()
        self.assertGreater(count, 0)
