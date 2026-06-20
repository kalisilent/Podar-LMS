# Podar LMS

A production-ready, Coursera-style Learning Management System built with Django REST Framework and React.

---

## Features

**For Students**
- Browse course catalog with search, filtering, and pagination
- Enroll in courses (free or paid via Razorpay)
- Watch video lessons, read PDFs and text content
- Track progress per course with completion percentages
- Submit assignments with file upload
- Take timed quizzes (MCQ, True/False, Essay)
- View grades, GPA, and download PDF grade reports
- Participate in course discussion forums
- Receive real-time notifications (WebSocket)
- Generate and download course completion certificates with QR verification

**For Lecturers**
- Create and manage courses with sections and lessons
- Post assignments with due dates and grading rubrics
- Grade submissions with feedback
- Create quizzes with auto-grading for MCQ/True-False
- View gradebook with all student submissions
- Access course analytics and reports

**For Admins**
- Dashboard with user stats, revenue, and enrollment charts
- User management (search, filter by role, verify)
- Course management overview
- Payment and revenue tracking

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2, Django REST Framework, PostgreSQL |
| Auth | JWT (SimpleJWT) with token refresh and blacklisting |
| Frontend | React 18, Vite, Tailwind CSS, React Router v6 |
| State | Zustand, TanStack React Query |
| Real-time | Django Channels, Redis, WebSocket |
| Task Queue | Celery, Redis, django-celery-beat |
| File Storage | S3 / MinIO |
| Payments | Razorpay |
| Certificates | ReportLab PDF + QR codes |
| API Docs | drf-spectacular (Swagger/OpenAPI) |
| Testing | Pytest (backend), Vitest (frontend) |
| CI/CD | GitHub Actions |
| Deployment | Docker, Nginx, Gunicorn, Uvicorn |

---

## Prerequisites

- Docker & Docker Compose **or**
- Python 3.11+, Node.js 20+, PostgreSQL 15+, Redis 7+

---

## Quick Start (Docker)

```bash
# Clone the repo
git clone https://github.com/your-org/podar_lms.git
cd podar_lms

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start all services
docker compose up --build

# In another terminal — run migrations and seed data
docker compose exec django python manage.py migrate
docker compose exec django python manage.py seed
```

The app is now running:

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000/api/v1/ |
| Swagger Docs | http://localhost:8000/api/docs/ |
| Django Admin | http://localhost:8000/admin/ |
| MinIO Console | http://localhost:9001 |

---

## Login Credentials (after seeding)

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@podar-lms.io | admin123 |
| Lecturer | lecturer1@podar-lms.io | lecturer123 |
| Student | student1@podar-lms.io | student123 |

---

## Local Development (without Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up PostgreSQL and update .env
cp .env.example .env
# Edit DATABASE_URL in .env

python manage.py migrate
python manage.py seed
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | (required) |
| `DEBUG` | Debug mode | `True` |
| `DATABASE_URL` | PostgreSQL connection string | `sqlite:///db.sqlite3` |
| `REDIS_URL` | Redis URL for cache and channels | `redis://localhost:6379/0` |
| `CELERY_BROKER_URL` | Celery broker URL | `redis://localhost:6379/1` |
| `JWT_ACCESS_TOKEN_LIFETIME` | Access token lifetime (minutes) | `60` |
| `JWT_REFRESH_TOKEN_LIFETIME` | Refresh token lifetime (minutes) | `1440` |
| `AWS_S3_ENDPOINT_URL` | S3/MinIO endpoint | (optional) |
| `RAZORPAY_KEY_ID` | Razorpay API key | (optional) |
| `RAZORPAY_KEY_SECRET` | Razorpay secret | (optional) |
| `SENTRY_DSN` | Sentry error tracking | (optional) |

### Frontend (`frontend/.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API base URL | `http://localhost:8000/api/v1` |
| `VITE_WS_URL` | WebSocket URL | `ws://localhost:8000/ws` |
| `VITE_RAZORPAY_KEY_ID` | Razorpay publishable key | (optional) |

---

## API Documentation

Interactive Swagger docs available at `/api/docs/` when the server is running.

### Key endpoints

```
POST   /api/v1/auth/register/          # Register
POST   /api/v1/auth/login/             # Login (get JWT)
POST   /api/v1/auth/token/refresh/     # Refresh token
GET    /api/v1/auth/profile/           # User profile
GET    /api/v1/courses/                # Course catalog
POST   /api/v1/courses/<slug>/enroll/  # Enroll in course
GET    /api/v1/courses/<slug>/progress/ # Course progress
GET    /api/v1/assignments/            # List assignments
POST   /api/v1/assignments/<id>/submit/ # Submit assignment
GET    /api/v1/quizzes/                # List quizzes
POST   /api/v1/quizzes/<id>/start/     # Start quiz attempt
POST   /api/v1/payments/create-order/  # Create Razorpay order
GET    /api/v1/results/gpa/            # Student GPA
GET    /api/v1/notifications/          # Notifications
```

---

## Folder Structure

```
podar_lms/
├── backend/
│   ├── config/              # Django settings, URLs, ASGI/WSGI, Celery
│   ├── accounts/            # User model, auth, profiles, permissions
│   ├── course/              # Programs, courses, sections, lessons, enrollment
│   ├── assignments/         # Assignments and submissions
│   ├── quiz/                # Quizzes, questions, attempts
│   ├── forums/              # Discussion forums, threads, posts
│   ├── notifications/       # Notifications, WebSocket consumer, tasks
│   ├── certificates/        # Certificate generation and verification
│   ├── payments/            # Razorpay integration
│   ├── result/              # Grades, GPA, grade scale
│   ├── reports/             # PDF reports and analytics
│   ├── tests/               # Pytest test suite
│   └── manage.py
├── frontend/
│   └── src/
│       ├── components/      # Reusable UI components
│       │   ├── common/      # Spinner, Cards, StatCard, EmptyState
│       │   └── layout/      # Sidebar, Navbar, StudentLayout, AdminLayout
│       ├── pages/           # Route-level pages
│       │   ├── auth/        # Login, Register
│       │   ├── student/     # Dashboard, Catalog, CourseDetail, Assignments, Grades, Quizzes, Forums, Profile
│       │   ├── lecturer/    # Dashboard, Gradebook
│       │   └── admin/       # Dashboard, UserManagement, CourseManagement
│       ├── services/        # Axios API client
│       └── stores/          # Zustand auth store
├── deployment/
│   └── nginx/               # Nginx config
├── .github/workflows/       # CI/CD
├── docker-compose.yml
└── README.md
```

---

## Running Tests

### Backend
```bash
cd backend
pytest                          # Run all tests
pytest --cov=. --cov-report=html  # With coverage report
```

### Frontend
```bash
cd frontend
npm test
```

---

## Deployment Guide

### Docker (any VPS — AWS EC2, DigitalOcean, etc.)

```bash
# On the server
git clone <repo-url> && cd podar_lms
cp backend/.env.example backend/.env
# Edit backend/.env with production values:
#   DEBUG=False
#   SECRET_KEY=<generate-a-strong-key>
#   DATABASE_URL=postgres://...
#   ALLOWED_HOSTS=yourdomain.com

docker compose -f docker-compose.yml up -d --build
docker compose exec django python manage.py migrate
docker compose exec django python manage.py createsuperuser
```

### Railway / Render

Both support Docker deployments. Point to the repo and set environment variables in the dashboard. Use the `backend/Dockerfile` for the API service and `frontend/Dockerfile` for the frontend.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `CORS error` in browser | Check `CORS_ALLOWED_ORIGINS` in backend `.env` |
| `Connection refused` on API calls | Ensure backend is running on port 8000 |
| `relation does not exist` | Run `python manage.py migrate` |
| MinIO bucket not found | Create the bucket via MinIO console at `:9001` |
| Celery tasks not running | Check Redis is running and `CELERY_BROKER_URL` is correct |
| WebSocket not connecting | Ensure `daphne` is in `INSTALLED_APPS` and ASGI is configured |

---

## Future Roadmap

- [ ] Mobile app (React Native)
- [ ] Live video classes (WebRTC)
- [ ] AI-powered quiz generation
- [ ] Plagiarism detection for assignments
- [ ] Multi-language support (i18n)
- [ ] Course reviews and ratings
- [ ] Instructor earnings dashboard
- [ ] SCORM/xAPI content import
- [ ] SSO with Google/GitHub OAuth
- [ ] Dark mode (frontend toggle ready)

---

## License

MIT
