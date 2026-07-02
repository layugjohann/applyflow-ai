from django import forms
from .models import JobApplication


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication

        fields = [
            "company_name",
            "position",
            "status",
            "job_link",
            "salary",
            "notes",
        ]

        widgets = {
            "company_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Google"
            }),

            "position": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Software Engineer"
            }),

            "status": forms.Select(attrs={
                "class": "form-select"
            }),

            "job_link": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://company.com/jobs/123"
            }),

            "salary": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Optional"
            }),

            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Add notes about the role, recruiter, interview schedule..."
            }),
        }