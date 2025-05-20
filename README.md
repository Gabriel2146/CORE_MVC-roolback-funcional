# Core MVC Training Project

## Overview
This project is a web application for managing adaptive training plans, exercise tracking, and athlete progress analysis. It includes a Django REST backend and a Vue.js frontend.

## Features
- Adaptive training plan generation and optimization
- Detailed session and exercise tracking
- Integration with external exercise database (wger)
- Progress analysis with graphical dashboards
- User roles: athlete, trainer, admin
- Administrative interfaces for managing exercises, users, and plans
- JWT-based authentication and authorization

## Setup

### Backend
1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Configure PostgreSQL database and update `core_mvc_backend/settings.py` with your credentials.
3. Run migrations:
   ```
   python manage.py migrate
   ```
4. Create a superuser for admin access:
   ```
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```
   python manage.py runserver
   ```

### Frontend
1. Navigate to the `frontend` directory.
2. Install dependencies:
   ```
   npm install
   ```
3. Run the development server:
   ```
   npm run dev
   ```

## Deployment Recommendations
- Set `DEBUG = False` in `core_mvc_backend/settings.py`.
- Configure `ALLOWED_HOSTS` with your domain names.
- Use HTTPS with proper SSL certificates.
- Configure caching (e.g., Redis) for performance.
- Harden security headers and permissions.
- Monitor logs and set up alerts.

## Testing
- Backend tests use `pytest`.
- Frontend tests use Jest and Vue Test Utils.
- Run backend tests:
  ```
  python -m pytest
  ```
- Run frontend tests:
  ```
  npm run test:unit
  ```

## Contributing
Please follow coding standards and write tests for new features.

## License
[Specify your license here]
