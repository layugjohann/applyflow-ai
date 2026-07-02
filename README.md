# 🚀 ApplyFlow

> **AI-powered job application tracker that helps job seekers organize applications, analyze resume compatibility, and gain actionable insights with AI.**

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-4.2-success)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)
![OpenRouter](https://img.shields.io/badge/AI-OpenRouter-green)

---

## 📖 Overview

ApplyFlow is a full-stack web application built to simplify the job application process.

Instead of managing applications with spreadsheets, ApplyFlow provides an organized dashboard where users can:

* Track job applications
* Upload and manage resumes
* Analyze resume-to-job compatibility using AI
* Receive personalized recommendations
* Visualize application progress through interactive analytics

The goal of the project was to build a production-style SaaS application while learning modern backend development, AI integration, caching, and responsive UI design.

---

## ✨ Features

### 📊 Dashboard

* Interactive analytics dashboard
* Monthly application trends
* Application status breakdown
* Responsive charts powered by Chart.js

### 💼 Job Tracker

* Add, edit, and delete job applications
* Track application status
* Store notes and salary information
* Manage application history

### 🤖 AI Resume Matching

* AI-powered resume analysis
* Resume-to-job compatibility scoring
* Resume strengths detection
* Missing skills identification
* Personalized recommendations

### 📄 Resume Manager

* Upload multiple resumes
* Set an active resume
* Preview uploaded resumes
* Delete old resumes

### ⚡ Performance

* Cached AI analysis
* Faster repeated requests
* Reduced API usage

### 🎨 UI / UX

* Dark SaaS-inspired interface
* Responsive layout
* Animated charts
* Interactive AI drawer
* Modern dashboard cards
* Status-based color system

---

## 🛠 Tech Stack

### Backend

* Python
* Django
* MySQL (Development)
* PostgreSQL (Production)

### Frontend

* HTML
* CSS
* Bootstrap 5
* JavaScript
* Chart.js

### AI

* OpenRouter API
* PDF Resume Parsing

### Deployment

* Render

---

## 📸 Screenshots

### Dashboard

> *(Add screenshot here)*

---

### AI Resume Analysis

> *(Add screenshot here)*

---

### Resume Manager

> *(Add screenshot here)*

---

### Job Details

> *(Add screenshot here)*

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/applyflow.git
cd applyflow
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

Windows

```bash
venv\Scripts\activate
```

macOS / Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file using `.env.example`.

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

---

## 🔑 Environment Variables

Example:

```env
SECRET_KEY=your-secret-key

DEBUG=True

OPENROUTER_API_KEY=your-openrouter-key

OPENROUTER_MODEL=openrouter/free
```

---

## 🗺 Roadmap

Future improvements include:

* Chrome Extension
* AI Resume Optimizer
* AI Cover Letter Generator
* Interview Preparation Assistant
* Email Synchronization
* Calendar Integration
* Interview Reminder Notifications
* Resume Version Comparison

---

## 📚 What I Learned

Building ApplyFlow helped me gain practical experience with:

* Django application architecture
* REST API integration
* AI-powered workflows
* Environment variable management
* Production deployment
* Responsive UI design
* Performance optimization through caching
* Building maintainable full-stack applications

---

## 👨‍💻 Author

**Johann Layug**

GitHub: https://github.com/layugjohann

LinkedIn: https://www.linkedin.com/in/johannlayug/
