import requests
from .models import WgerExercise

WGER_API_URL = "https://wger.de/api/v2/exercise/"

class WgerAPIClient:
    def __init__(self):
        self.session = requests.Session()

    def fetch_exercises(self, language=2, limit=100, offset=0):
        params = {
            'language': language,
            'limit': limit,
            'offset': offset,
            'status': 2
        }
        response = self.session.get(WGER_API_URL, params=params)
        response.raise_for_status()
        return response.json()

    def sync_exercises(self):
        offset = 0
        limit = 100
        while True:
            data = self.fetch_exercises(limit=limit, offset=offset)
            results = data.get('results', [])
            if not results:
                break
            for item in results:
                name = item.get('name', '')
                description = item.get('description', '')
                category = item.get('category', None)
                equipment = item.get('equipment', [])

                WgerExercise.objects.update_or_create(
                    wger_id=item.get('id'),
                    defaults={
                        'name': name,
                        'description': description,
                        'category': category,
                        'equipment': equipment,
                    }
                )
            offset += limit
            if not data.get('next'):
                break
