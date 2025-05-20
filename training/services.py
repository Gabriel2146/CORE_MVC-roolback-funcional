from datetime import datetime, timedelta

from datetime import datetime, timedelta
from .models import Exercise
from wger_integration.models import WgerExercise

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

        # Fetch exercises from both local and wger DB based on objective_type and other criteria
        local_exercises = list(Exercise.objects.filter(category__icontains=objective_type))
        wger_exercises = list(WgerExercise.objects.filter(category__icontains=objective_type))

        exercises = local_exercises + wger_exercises

        # If no exercises found, fallback to all exercises
        if not exercises:
            exercises = list(Exercise.objects.all()) + list(WgerExercise.objects.all())

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
        """
        Calculate a realistic effectiveness index considering:
        - Fatigue: estimated from recent sessions volume
        - Compatibility: match of exercises with objectives and restrictions
        - Variation: diversity of exercises and muscle groups
        - Progression: alignment with expected progression curve
        Returns a float between 0 and 1.
        """
        fatigue_score = 0.0
        compatibility_score = 0.0
        variation_score = 0.0
        progression_score = 0.0

        # Estimate fatigue from last 7 days sessions volume
        recent_sessions = [s for s in self.training_history if (datetime.now().date() - s['date']).days <= 7]
        total_volume = 0
        for session in recent_sessions:
            for ex in session.get('exercises', []):
                volume = ex.get('sets', 0) * ex.get('reps', 0)
                total_volume += volume
        fatigue_score = max(0, 1 - total_volume / 100)  # simplistic fatigue model

        # Compatibility: check exercises against restrictions and objectives
        restrictions = self.user_profile.restrictions if hasattr(self.user_profile, 'restrictions') else []
        objective_type = self.objectives.get('type', '').lower()
        compatible_exercises = 0
        total_exercises = 0
        for session in plan.get('sessions', []):
            for ex in session.get('exercises', []):
                total_exercises += 1
                # simplistic compatibility check: exclude exercises with restricted keywords
                if not any(r.lower() in ex['name'].lower() for r in restrictions):
                    if objective_type in ex['name'].lower() or objective_type == '':
                        compatible_exercises += 1
        compatibility_score = compatible_exercises / total_exercises if total_exercises > 0 else 0

        # Variation: count unique exercises and muscle groups (if available)
        unique_exercises = set()
        for session in plan.get('sessions', []):
            for ex in session.get('exercises', []):
                unique_exercises.add(ex['name'])
        variation_score = min(1.0, len(unique_exercises) / 10)  # target at least 10 unique exercises

        # Progression: simplistic check comparing planned volume increase over sessions
        volumes = []
        for session in plan.get('sessions', []):
            vol = 0
            for ex in session.get('exercises', []):
                vol += ex.get('sets', 0) * ex.get('reps', 0)
            volumes.append(vol)
        progression_score = 0.0
        if len(volumes) > 1:
            progression_score = sum(max(0, volumes[i+1] - volumes[i]) for i in range(len(volumes)-1)) / (len(volumes)-1) / max(volumes)

        # Weighted sum of factors
        effectiveness = (0.3 * fatigue_score +
                         0.3 * compatibility_score +
                         0.2 * variation_score +
                         0.2 * progression_score)
        return round(effectiveness, 3)

    def optimize_plan(self, plan):
        """
        Optimize the plan by adjusting exercises and session distribution to maximize effectiveness.
        For simplicity, this example will:
        - Replace exercises that conflict with restrictions.
        - Adjust sets/reps slightly to balance volume.
        """
        restrictions = self.user_profile.restrictions if hasattr(self.user_profile, 'restrictions') else []
        objective_type = self.objectives.get('type', '').lower()

        # Fetch all exercises matching objective type and not restricted
        candidate_exercises = list(Exercise.objects.filter(category__icontains=objective_type))
        if not candidate_exercises:
            candidate_exercises = list(Exercise.objects.all())

        for session in plan.get('sessions', []):
            new_exercises = []
            for ex in session.get('exercises', []):
                # Check restriction conflict
                if any(r.lower() in ex['name'].lower() for r in restrictions):
                    # Replace with a random compatible exercise
                    replacement = next((ce for ce in candidate_exercises if ce.name.lower() not in ex['name'].lower() and not any(r.lower() in ce.name.lower() for r in restrictions)), None)
                    if replacement:
                        new_exercises.append({
                            "name": replacement.name,
                            "sets": ex.get('sets', 4),
                            "reps": ex.get('reps', 8)
                        })
                    else:
                        new_exercises.append(ex)
                else:
                    # Slightly adjust sets/reps for variation
                    sets = ex.get('sets', 4)
                    reps = ex.get('reps', 8)
                    sets = max(3, min(5, sets + (1 if sets < 4 else -1)))
                    reps = max(6, min(10, reps + (1 if reps < 8 else -1)))
                    new_exercises.append({
                        "name": ex['name'],
                        "sets": sets,
                        "reps": reps
                    })
            session['exercises'] = new_exercises
        return plan

    def adjust_plan_dynamic(self, feedback):
        """
        Adjust the plan dynamically based on feedback and progress.
        Feedback is expected to be a dict with keys like:
        - 'missed_sessions': int
        - 'perceived_effort': float (0-1)
        - 'progress_metrics': dict with performance data
        This method modifies the plan accordingly.
        """
        missed_sessions = feedback.get('missed_sessions', 0)
        perceived_effort = feedback.get('perceived_effort', 0.5)
        progress_metrics = feedback.get('progress_metrics', {})

        # Example logic: reduce volume if perceived effort is high or missed sessions exceed threshold
        volume_adjustment_factor = 1.0
        if missed_sessions > 2:
            volume_adjustment_factor -= 0.2
        if perceived_effort > 0.8:
            volume_adjustment_factor -= 0.3

        # Adjust exercises in the current plan sessions
        for session in self.training_history:
            for ex in session.get('exercises', []):
                original_sets = ex.get('sets', 4)
                original_reps = ex.get('reps', 8)
                adjusted_sets = max(1, int(original_sets * volume_adjustment_factor))
                adjusted_reps = max(1, int(original_reps * volume_adjustment_factor))
                ex['sets'] = adjusted_sets
                ex['reps'] = adjusted_reps

        # Optionally, add logic to add/remove exercises based on progress_metrics

        # Return adjusted plan (assuming self.training_history is the plan representation)
        return self.training_history

    def create_plan(self):
        profile_data = self.collect_profile_data()
        objectives = self.define_objectives()
        preliminary_plan = self.generate_preliminary_plan()
        effectiveness = self.calculate_effectiveness_index(preliminary_plan)
        optimized_plan = self.optimize_plan(preliminary_plan)
        return optimized_plan
