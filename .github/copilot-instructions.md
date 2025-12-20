# Portfolio Project Instructions

## 🏗 Project Architecture
- **Full Stack**: Django REST Framework (Backend) + Vanilla TypeScript (Frontend).
- **Backend**: `portfolio_backend/` (Django 4.2, Python 3.11+).
  - Uses `api/` app for all endpoints.
  - `media/` for user uploads, `staticfiles/` for collected static assets.
  - **Database**: PostgreSQL (prod), SQLite (dev).
  - **Caching**: Redis.
- **Frontend**: `frontend/` (HTML5, CSS3, TypeScript).
  - **No Framework**: Pure DOM manipulation via TypeScript.
  - **Entry Point**: `src/main.ts` compiles to `dist/main.js`.
  - **Styling**: `style.css` with CSS variables for theming.

## 🚀 Development Workflows
- **Backend**:
  - Run server: `python manage.py runserver` (in `portfolio_backend/`).
  - Migrations: `python manage.py makemigrations` -> `python manage.py migrate`.
  - Tests: `pytest` or `python manage.py test`.
  - Linting: `black .`, `isort .`, `flake8 .`.
- **Frontend**:
  - Build: `npm run build` (runs `tsc`).
  - Watch: `npm run watch` (for auto-recompile).
  - Serve: `npx serve .` or `python -m http.server`.

## 📝 Code Conventions
- **TypeScript**:
  - Define interfaces for all API responses (e.g., `Profile`, `Project`).
  - Use `async/await` for API calls.
  - Handle API failures gracefully with mock data fallbacks (see `main.ts`).
  - **Strict Mode**: Ensure type safety, avoid `any`.
- **Django/Python**:
  - **Views**: Use `ViewSet` for CRUD, `APIView` for single resources.
  - **Serializers**: ModelSerializers in `api/serializers.py`.
  - **URLs**: Register ViewSets in `api/urls.py` via `DefaultRouter`.
  - **Env Vars**: Use `python-dotenv` pattern (refer to `.env.example`).

## 🔌 Integration & API
- **Base URL**: `http://localhost:8000/api/`.
- **Endpoints**:
  - `projects/`, `blog/`, `contact/` (ViewSets).
  - `portfolio/`, `profile/`, `skills/` (Specialized Views).
- **Frontend Config**: Update `API_BASE_URL` in `src/main.ts`.
- **Images**: Backend serves media URLs; Frontend must handle full paths.

## 🐳 Docker & Deployment
- **Docker**: `docker-compose.yml` orchestrates Web (Django), DB (Postgres), Redis, Nginx.
- **Static Files**: Run `collectstatic` before deployment.
- **Production**: Set `DEBUG=False`, configure `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`.
