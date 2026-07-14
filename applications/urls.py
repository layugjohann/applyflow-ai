from django.urls import path
from . import views
from .models import JobApplication

urlpatterns = [
    path('add/', views.add_job, name='add_job'),
    path('', views.job_list, name='job_list'),
    path('<int:id>/edit/', views.edit_job, name='edit_job'),
    path('<int:id>/delete/', views.delete_job, name='delete_job'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('jobs/<int:id>/', views.job_detail, name='job_detail'),
    path("ai/analyze-job/", views.analyze_job, name="analyze_job"),
    path('ai/match-resume/', views.match_resume, name='match_resume'),
    path("resume/", views.resume_manager, name="resume_manager"),
    path("<int:job_id>/ai/", views.job_ai_analysis, name="job_ai_analysis"),
    path("<int:job_id>/cover-letter/", views.generate_cover_letter, name="generate_cover_letter",),

]