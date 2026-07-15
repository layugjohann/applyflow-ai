# 🚀 ApplyFlow

> **An AI-powered job application tracker that helps job seekers organize applications, analyze resume compatibility, and generate tailored cover letters.**

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-4.2-success)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Docker](https://img.shields.io/badge/Container-Docker-blue)
![OpenRouter](https://img.shields.io/badge/AI-OpenRouter-green)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-blue)

---

## 📖 Overview

ApplyFlow is a full-stack, AI-powered job application tracking platform built with Django.

Instead of managing job applications through spreadsheets or scattered notes, ApplyFlow provides a centralized dashboard where users can track their application pipeline, manage resumes, analyze resume-to-job compatibility with AI, and generate tailored cover letters.

The project was built to explore production-style full-stack development, including AI integration, PostgreSQL, Docker, cloud deployment, automated CI workflows, and responsive SaaS-inspired UI design.

---

## ✨ Features

### 📊 Analytics Dashboard

- Application pipeline overview
- Key application metrics
- Monthly application trends
- Application status breakdown
- Monthly application goal tracking
- Success rate monitoring
- Recent application activity
- Interactive charts powered by Chart.js

### 💼 Job Application Tracker

- Add, edit, and delete job applications
- Track applications through multiple stages:
  - Applied
  - Interview
  - Assessment
  - Offer
  - Rejected
- Store job links
- Store salary information
- Add application notes
- View detailed information for individual applications

### 🤖 AI Resume Matching

- AI-powered resume-to-job analysis
- Compatibility match scoring
- Resume strengths detection
- Missing skills identification
- Personalized recommendations
- Cached analysis results to reduce repeated AI requests

### ✍️ AI Cover Letter Generator

- Generate tailored cover letters for individual job applications
- Uses information from the user's resume and saved job details
- Designed to avoid inventing experience or qualifications
- Regenerate cover letters when needed
- Copy generated letters directly to the clipboard

### 📄 Resume Manager

- Upload multiple resumes
- Select an active resume
- Associate resumes with job applications
- Preview uploaded resumes
- Delete outdated resumes
- Extract resume text from PDF files for AI analysis

### 🔐 Authentication

- User registration and login
- Django password validation
- User-specific job applications and resumes
- Protected application views

### 🎨 UI / UX

- Dark SaaS-inspired interface
- Responsive Bootstrap layout
- Modern analytics dashboard
- Animated charts and progress indicators
- Interactive AI analysis interface
- Status-based visual system

---

## 🛠 Tech Stack

### Backend

- Python 3.13
- Django 4.2
- Gunicorn

### Database

- PostgreSQL
- Supabase

### Frontend

- HTML
- CSS
- Bootstrap 5
- JavaScript
- Chart.js
- Bootstrap Icons

### AI & Document Processing

- OpenRouter API
- OpenAI Python SDK
- PyMuPDF

### Infrastructure & DevOps

- Docker
- Docker Compose
- Git
- GitHub
- GitHub Actions
- Render

---

## 🏗 Architecture

```text
                        ┌─────────────────────┐
                        │       Browser       │
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │   Django / Gunicorn │
                        └──────────┬──────────┘
                                   │
                  ┌────────────────┼────────────────┐
                  │                │                │
                  ▼                ▼                ▼
         ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
         │  PostgreSQL  │  │   Resume     │  │  OpenRouter  │
         │  (Supabase)  │  │   Storage    │  │    AI API    │
         └──────────────┘  └──────────────┘  └──────────────┘
```

Django acts as the primary application layer and handles authentication, business logic, database access, resume processing, and communication with the AI service.

---

## 🐳 Running Locally with Docker

### Prerequisites

Make sure you have installed:

- Docker Desktop
- Docker Compose
- Git

You will also need:

- A PostgreSQL database
- An OpenRouter API key

### 1. Clone the repository

```bash
git clone https://github.com/layugjohann/applyflow-ai.git
cd applyflow-ai
```

### 2. Create your environment file

Create a `.env` file in the project root.

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_URL=your-postgresql-database-url
DB_SSL_REQUIRE=True

OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_MODEL=your-selected-openrouter-model
```

Never commit your real `.env` file or credentials to version control.

### 3. Build and start the application

```bash
docker compose up -d --build
```

### 4. Apply database migrations

```bash
docker compose exec web python manage.py migrate
```

### 5. Open the application

Visit:

```text
http://127.0.0.1:8000
```

---

## ⚙️ Useful Development Commands

Start the containers:

```bash
docker compose up -d
```

Stop the containers:

```bash
docker compose down
```

Restart the Django container:

```bash
docker compose restart web
```

View application logs:

```bash
docker compose logs -f web
```

Run Django system checks:

```bash
docker compose exec web python manage.py check
```

Check for missing migrations:

```bash
docker compose exec web python manage.py makemigrations --check --dry-run
```

Apply migrations:

```bash
docker compose exec web python manage.py migrate
```

Run automated tests:

```bash
docker compose exec web python manage.py test
```

---

## 🔑 Environment Variables

| Variable | Description |
| --- | --- |
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Enables or disables Django debug mode |
| `ALLOWED_HOSTS` | Hosts allowed to serve the Django application |
| `DATABASE_URL` | PostgreSQL database connection URL |
| `DB_SSL_REQUIRE` | Controls whether the database connection requires SSL |
| `OPENROUTER_API_KEY` | API key used for AI requests |
| `OPENROUTER_MODEL` | OpenRouter model used by the AI service |

Production secrets should always be configured through environment variables and never committed to the repository.

---

## 🔄 Continuous Integration

ApplyFlow uses GitHub Actions for continuous integration.

The CI workflow automatically runs when code is pushed to the `main` branch or when a pull request targets `main`.

The pipeline:

1. Checks out the latest source code
2. Sets up Python
3. Starts an isolated PostgreSQL service
4. Installs project dependencies
5. Runs Django system checks
6. Checks for missing migrations
7. Applies migrations to the temporary PostgreSQL database
8. Runs the Django test suite

```text
Push / Pull Request
        │
        ▼
   GitHub Actions
        │
        ▼
Temporary PostgreSQL
        │
        ▼
   Django Checks
        │
        ▼
 Migration Validation
        │
        ▼
     Tests
        │
        ▼
   Pass / Fail
```

The CI environment uses its own temporary PostgreSQL database and does not run migrations against the production Supabase database.

---

## 🔒 Security

ApplyFlow follows several practices to reduce exposure of sensitive information:

- Application secrets are stored using environment variables
- `.env` files are excluded from version control
- Django's built-in authentication and password validation are used
- Application data is accessed through the Django backend
- Supabase Data API access is disabled because the application connects directly to PostgreSQL
- Production database connections use SSL
- CI runs against an isolated PostgreSQL database instead of production

---

## 🗺 Future Improvements

Potential future improvements include:

- AI Resume Optimizer
- Interview Preparation Assistant
- Email synchronization
- Calendar integration
- Interview reminder notifications
- Resume version comparison
- Expanded automated test coverage
- Chrome extension integration

ApplyFlow v1.0 is considered feature-complete. Future development will focus on improvements rather than core functionality.

---

## 📚 What I Learned

Building ApplyFlow gave me practical experience with:

- Django application architecture
- PostgreSQL database integration
- Docker and containerized development
- AI-powered application workflows
- Prompt engineering
- Third-party API integration
- PDF document processing
- Environment variable and secret management
- Database migrations
- Cloud deployment
- GitHub Actions and continuous integration
- Debugging environment-specific issues
- Responsive SaaS-style UI development
- Performance optimization through cached AI results

One of the most valuable parts of the project was learning how the different layers of a production-style application work together—from the user interface and Django backend to PostgreSQL, external AI services, Docker, and automated CI workflows.

---

## 📌 Project Status

**ApplyFlow v1.0 — Feature Complete**

Core application development is complete. The project is stable and the GitHub Actions CI pipeline is operational.

---

## 👨‍💻 Author

**Johann Layug**

GitHub: https://github.com/layugjohann

LinkedIn: https://www.linkedin.com/in/johannlayug/