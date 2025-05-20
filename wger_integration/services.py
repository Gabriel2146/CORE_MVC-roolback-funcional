import requests
from .models import WgerExercise

WGER_API_URL = 'https://wger.de/api/v2/exercise/'

def fetch_wger_exercises():
    """
    Fetch exercises from the wger API and save/update them in the local database.
    """
    url = WGER_API_URL
    exercises_fetched = 0
    while url:
        response = requests.get(url)
        if response.status_code != 200:
            break
        data = response.json()
        for item in data.get('results', []):
            wger_id = item.get('id')
            name = item.get('name') or 'Unnamed Exercise'
            category = item.get('category', {}).get('name', '') if isinstance(item.get('category'), dict) else ''
            muscle_group = item.get('muscles', [])
            difficulty = item.get('difficulty_level', '')
            equipment = item.get('equipment', [])
            # Simplify muscle_group and equipment to comma separated strings if needed
            muscle_group_str = ','.join(str(m) for m in muscle_group) if muscle_group else ''
            equipment_str = ','.join(str(e) for e in equipment) if equipment else ''

            obj, created = WgerExercise.objects.update_or_create(
                wger_id=wger_id,
                defaults={
                    'name': name,
                    'category': category,
                    'muscle_group': muscle_group_str,
                    'difficulty': difficulty,
                    'equipment': equipment_str
                }
            )
            exercises_fetched += 1
        url = data.get('next')
    return exercises_fetched
