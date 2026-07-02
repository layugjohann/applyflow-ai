from django.db import models
from django.contrib.auth.models import User


class JobApplication(models.Model):

    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Assessment', 'Assessment'),
        ('Rejected', 'Rejected'),
        ('Offer', 'Offer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    resume = models.ForeignKey(
    'Resume',
    on_delete=models.SET_NULL,
    null=True,
    blank=True
    
    )

    company_name = models.CharField(max_length=100)

    position = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    job_link = models.URLField(blank=True)

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    notes = models.TextField(blank=True)

    date_applied = models.DateTimeField(auto_now_add=True, db_index=True)

    match_score = models.IntegerField(null=True, blank=True)

    strengths = models.TextField(blank=True)

    missing_skills = models.TextField(blank=True)

    recommendation = models.TextField(blank=True)

    def __str__(self):
        return f"{self.company_name} - {self.position}"

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=False)