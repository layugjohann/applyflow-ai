from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils.pdf_utils import extract_text_from_pdf
from django.contrib import messages

from .services.ai_service import AIService

from .models import JobApplication, Resume
from .forms import JobApplicationForm 

def normalize_list(field):
    if isinstance(field, list):
        return field

    if isinstance(field, str):
        return [item.strip() for item in field.splitlines() if item.strip()]

    return []

@login_required
def job_list(request):

    jobs = JobApplication.objects.filter(user=request.user)

    # GET parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    # Search by company name
    if search_query:
        jobs = jobs.filter(company_name__icontains=search_query)

    # Filter by status
    if status_filter:
        jobs = jobs.filter(status=status_filter)

    context = {
        'jobs': jobs,
        'search_query': search_query,
        'status_filter': status_filter,
    }

    return render(request, "applications/job_list.html", context)

@login_required
def add_job(request):

    if request.method == "POST":

        form = JobApplicationForm(request.POST, request.FILES)

        if form.is_valid():

            job = form.save(commit=False)
            job.user = request.user
            job.save()

            job_link = form.cleaned_data.get("job_link")

            latest_resume = Resume.objects.filter(
                user=request.user
            ).order_by("-uploaded_at").first()

            if latest_resume:

                try:
                    resume_text = extract_text_from_pdf(
                        latest_resume.file
                    )

                    job.resume = latest_resume
                    job.save()

                    if resume_text and job_link:

                        try:
                            print("CALLING AI NOW...")

                            ai_data = AIService.match_resume_to_job(
                                resume_text,
                                job_link
                            )

                            print("AI RESPONSE:", ai_data)

                            job.match_score = ai_data.get("match_score", 0)

                            job.strengths = "\n".join(
                                ai_data.get("strengths", [])
                            )

                            job.missing_skills = "\n".join(
                                ai_data.get("missing_skills", [])
                            )

                            job.recommendation = ai_data.get(
                                "recommendation",
                                ""
                            )

                            job.save()

                            print("AI DONE AND SAVED")

                        except Exception as e:
                            import traceback

                            print("========== ADD JOB AI ERROR ==========")
                            print("ERROR TYPE:", type(e).__name__)
                            print("ERROR MESSAGE:", repr(e))
                            print("FULL TRACEBACK:")
                            print(traceback.format_exc())
                            print("======================================")

                except Exception as e:
                    import traceback

                    print("========== RESUME EXTRACTION ERROR ==========")
                    print("ERROR TYPE:", type(e).__name__)
                    print("ERROR MESSAGE:", repr(e))
                    print("FULL TRACEBACK:")
                    print(traceback.format_exc())
                    print("=============================================")

            return redirect("job_list")

    else:
        form = JobApplicationForm()

    return render(
        request,
        "applications/add_job.html",
        {
            "form": form
        }
    )

@login_required
def edit_job(request, id):

    job = get_object_or_404(
        JobApplication,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        form = JobApplicationForm(request.POST, instance=job)

        if form.is_valid():

            form.save()
            return redirect("job_list")

    else:

        form = JobApplicationForm(instance=job)

    return render(request, "applications/edit_job.html", {
        "form": form,
        "job": job
    })

@login_required
def delete_job(request, id):

    job = get_object_or_404(
        JobApplication,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        job.delete()
        return redirect("job_list")

    return render(request, "applications/delete_job.html", {
        "job": job
    })

@login_required
def dashboard(request):

    jobs = JobApplication.objects.filter(user=request.user)

    total_jobs = jobs.count()

    applied_count = jobs.filter(status='Applied').count()
    interview_count = jobs.filter(status='Interview').count()
    assessment_count = jobs.filter(status='Assessment').count()
    offer_count = jobs.filter(status='Offer').count()
    rejected_count = jobs.filter(status='Rejected').count()

    recent_jobs = jobs.order_by('-date_applied')[:5]

    success_rate = 0
    if total_jobs > 0:
        success_rate = round((offer_count / total_jobs) * 100)

    # MONTHLY DATA
    monthly_data = (
        jobs
        .annotate(month=TruncMonth('date_applied'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )

    monthly_goal = 20  # you can change this later or make it user-defined

    current_month_apps = jobs.filter(
        date_applied__month=timezone.now().month,
        date_applied__year=timezone.now().year
    ).count()

    goal_progress = int((current_month_apps / monthly_goal) * 100) if monthly_goal else 0

    month_labels = []
    month_counts = []

    for item in monthly_data:
        month_labels.append(item['month'].strftime('%b %Y'))
        month_counts.append(item['total'])

    context = {
        'total_jobs': total_jobs,
        'applied_count': applied_count,
        'interview_count': interview_count,
        'assessment_count': assessment_count,
        'offer_count': offer_count,
        'rejected_count': rejected_count,
        'success_rate': success_rate,
        'recent_jobs': recent_jobs,
        'month_labels': month_labels,
        'month_counts': month_counts,
        'monthly_goal': monthly_goal,
        'current_month_apps': current_month_apps,
        'goal_progress': goal_progress,
    }

    return render(
        request,
        'applications/dashboard.html',
        context
    )

@login_required
def job_detail(request, id):
    job = get_object_or_404(JobApplication, id=id, user=request.user)

    return render(request, "applications/job_detail.html", {
        "job": job
    })

@csrf_exempt
def analyze_job(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            job_description = data.get("description")

            result = AIService.analyze_job(job_description)

            return JsonResponse({
                "success": True,
                "result": result
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            })

@csrf_exempt
def match_resume(request):

    if request.method == "POST":

        resume = request.POST.get("resume")
        job_description = request.POST.get("job_description")

        result = AIService.match_resume_to_job(
            resume,
            job_description
        )

        return JsonResponse({
            "success": True,
            "data": result
        })

@login_required
def resume_manager(request):

    resumes = Resume.objects.filter(user=request.user).order_by("-uploaded_at")
    latest_resume = resumes.first()

    # -------------------------
    # UPLOAD NEW RESUME
    # -------------------------
    if request.method == "POST" and "upload_resume" in request.POST:

        try:
            resume_file = request.FILES.get("resume_file")

            if not resume_file:
                print("No file uploaded.")
                return redirect("resume_manager")

            # Deactivate current active resume
            Resume.objects.filter(user=request.user).update(is_active=False)

            print("Resume file received:", resume_file.name)
            print("Resume file size:", resume_file.size)

            # Save new resume
            Resume.objects.create(
                user=request.user,
                file=resume_file,
                is_active=True
            )

            print("Resume uploaded successfully.")

        except Exception as e:
            import traceback

            print("========== RESUME UPLOAD ERROR ==========")
            print("ERROR TYPE:", type(e).__name__)
            print("ERROR MESSAGE:", repr(e))
            print("FULL TRACEBACK:")
            print(traceback.format_exc())
            print("=========================================")

    # -------------------------
    # SET ACTIVE RESUME
    # -------------------------
    if request.method == "POST" and "set_active" in request.POST:

        resume_id = request.POST.get("resume_id")

        Resume.objects.filter(user=request.user).update(is_active=False)

        Resume.objects.filter(
            id=resume_id,
            user=request.user
        ).update(is_active=True)

        return redirect("resume_manager")

    # -------------------------
    # DELETE RESUME
    # -------------------------
    if request.method == "POST" and "delete_resume" in request.POST:

        resume_id = request.POST.get("resume_id")

        Resume.objects.filter(
            id=resume_id,
            user=request.user
        ).delete()

        return redirect("resume_manager")

    try:
        return render(
            request,
            "applications/resume_manager.html",
            {
                "resumes": resumes,
                "latest_resume": latest_resume,
            },
        )

    except Exception as e:
        import traceback

        print("========== RESUME MANAGER RENDER ERROR ==========", flush=True)
        print("ERROR TYPE:", type(e).__name__, flush=True)
        print("ERROR MESSAGE:", repr(e), flush=True)
        print("FULL TRACEBACK:", flush=True)
        print(traceback.format_exc(), flush=True)
        print("=================================================", flush=True)

        return HttpResponse("Resume Manager temporarily unavailable.", status=500)

@login_required
def job_ai_analysis(request, job_id):

    job = get_object_or_404(JobApplication, id=job_id, user=request.user)

    # ✅ RETURN CACHED RESULT FIRST
    if job.match_score is not None and job.recommendation:
        return JsonResponse({
            "cached": True,
            "match_score": job.match_score,
            "strengths": normalize_list(job.strengths),
            "missing_skills": normalize_list(job.missing_skills),
            "recommendation": job.recommendation
        })

    resume = Resume.objects.filter(
        user=request.user,
        is_active=True
    ).first()

    if not resume:
        return JsonResponse({
            "error": "No active resume",
            "match_score": 0,
            "strengths": [],
            "missing_skills": [],
            "recommendation": "Upload or select an active resume first."
        }, status=400)

    try:
        print("STEP 1: Resume extracted")
        resume_text = extract_text_from_pdf(resume.file)

        print("STEP 2: About to call AI")
        ai_data = AIService.match_resume_to_job(
            resume_text,
            job.job_link
        )

        print("STEP 3: AI returned")
        print(ai_data)

        safe_data = {
            "cached": False,
            "match_score": ai_data.get("match_score", 0),
            "strengths": normalize_list(ai_data.get("strengths")),
            "missing_skills": normalize_list(ai_data.get("missing_skills")),
            "recommendation": ai_data.get("recommendation", "") or ""
        }

        job.match_score = safe_data["match_score"]
        job.strengths = "\n".join(safe_data["strengths"])
        job.missing_skills = "\n".join(safe_data["missing_skills"])
        job.recommendation = safe_data["recommendation"]
        job.save()

        return JsonResponse(safe_data)

    except Exception as e:
        print("AI ERROR:", str(e))

        return JsonResponse({
            "error": str(e),
            "match_score": 0,
            "strengths": [],
            "missing_skills": [],
            "recommendation": "AI service failed."
        }, status=500)

@login_required
def generate_cover_letter(request, job_id):
    job = get_object_or_404(
        JobApplication,
        id=job_id,
        user=request.user,
    )

    if request.method != "POST":
        return redirect("job_detail", id=job.id)

    # Prefer a resume explicitly assigned to this job.
    resume = job.resume

    # Otherwise, use the user's active resume.
    if not resume:
        resume = Resume.objects.filter(
            user=request.user,
            is_active=True,
        ).first()

    if not resume:
        messages.error(
            request,
            "Please upload or select an active resume first."
        )
        return redirect("job_detail", id=job.id)

    try:
        resume_text = extract_text_from_pdf(resume.file)

        if not resume_text:
            raise ValueError(
                "No readable text could be extracted from the resume."
            )

        cover_letter = AIService.generate_cover_letter(
            resume_text=resume_text,
            company_name=job.company_name,
            position=job.position,
            job_description=job.notes,
            job_link=job.job_link,
        )

        return render(
            request,
            "applications/cover_letter.html",
            {
                "job": job,
                "cover_letter": cover_letter,
            },
        )

    except Exception as error:
        print("COVER LETTER ERROR:", str(error))

        messages.error(
            request,
            "The cover letter could not be generated. Please try again."
        )

        return redirect("job_detail", id=job.id)