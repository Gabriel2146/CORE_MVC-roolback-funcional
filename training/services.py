from datetime import datetime, timedelta

from datetime import datetime, timedelta
from .models import Exercise

class TrainingPlanGenerator:
    def __init__(self, user_profile, training_history, objectives):
        self.user_profile = user_profile
        self.training_history = training_history
        self.objectives = objectives

    def collect_profile_data(self):
        profile_data = {
            'physical_info': getattr(self.user_profile, 'physical_info', None),
            'condition_level': getattr(self.user_profile, 'condition_level', None),
            'restrictions': getattr(self.user_profile, 'restrictions', None),
            'availability': getattr(self.user_profile, 'availability', ['Monday', 'Wednesday', 'Friday']),
        }
        return profile_data

    def define_objectives(self):
        return self.objectives

    def generate_preliminary_plan(self):
        days_available = self.user_profile.availability if hasattr(self.user_profile, 'availability') else ['Monday', 'Wednesday', 'Friday']
        objective_type = self.objectives.get('type', 'strength')

        # Fetch exercises from DB based on objective_type and other criteria
        exercises = Exercise.objects.filter(category__icontains=objective_type)

        # If no exercises found, fallback to all exercises
        if not exercises.exists():
            exercises = Exercise.objects.all()

        selected_exercises = []
        for exercise in exercises[:3]:  # select first 3 exercises for simplicity
            selected_exercises.append({
                "name": exercise.name,
                "sets": 4,
                "reps": 8
            })

        sessions = []
        start_date = datetime.now().date()
        for i, day in enumerate(days_available):
            session_date = start_date + timedelta(days=i*2)
            sessions.append({
                "date": session_date,
                "exercises": selected_exercises
            })

        plan = {
            "sessions": sessions
        }
        return plan

    def calculate_effectiveness_index(self, plan):
        return 0.9

    def optimize_plan(self, plan):
        return plan

    def adjust_plan_dynamic(self, feedback):
        pass

    def create_plan(self):
        profile_data = self.collect_profile_data()
        objectives = self.define_objectives()
        preliminary_plan = self.generate_preliminary_plan()
        effectiveness = self.calculate_effectiveness_index(preliminary_plan)
        optimized_plan = self.optimize_plan(preliminary_plan)
        return optimized_plan
