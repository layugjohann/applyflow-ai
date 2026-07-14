import os
import json
from openai import OpenAI


class AIService:

    @staticmethod
    def get_client():
        api_key = os.getenv("OPENROUTER_API_KEY", "").strip()

        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is missing")

        return OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "http://127.0.0.1:8000",
                "X-Title": "ApplyFlow",
            },
        )

    @staticmethod
    def match_resume_to_job(resume_text, job_description):

        prompt = f"""
You are a senior technical recruiter.

Analyze the resume against the job.

Return ONLY valid JSON in this exact format:

{{
    "match_score": 0,
    "strengths": ["item"],
    "missing_skills": ["item"],
    "recommendation": "short advice"
}}

Rules:
- match_score must be a number from 0 to 100
- strengths must be a short list
- missing_skills must be a short list
- recommendation must be 1-2 sentences
- no markdown
- no extra explanation

RESUME:
{resume_text}

JOB:
{job_description}
"""

        client = AIService.get_client()

        response = client.chat.completions.create(
            model=os.getenv(
                "OPENROUTER_MODEL",
                "deepseek/deepseek-chat-v3-0324:free"
            ).strip(),
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                "match_score": 0,
                "strengths": [],
                "missing_skills": ["AI returned invalid JSON"],
                "recommendation": "Please try regenerating the analysis.",
            }

    @staticmethod
    def generate_cover_letter(
        resume_text,
        company_name,
        position,
        job_description="",
        job_link="",
    ):
        prompt = f"""
You are an expert career coach and professional cover letter writer.

Write a tailored cover letter using the candidate's resume and the job details.

Requirements:
- Keep it professional, confident, and natural.
- Use approximately 300 to 400 words.
- Do not invent experience, skills, achievements, or credentials.
- Highlight only relevant information found in the resume.
- Connect the candidate's experience to the target role.
- Avoid generic phrases and excessive enthusiasm.
- Do not use markdown.
- Do not add headings such as "Cover Letter".
- Do not include placeholders such as [Hiring Manager Name].
- Start with "Dear Hiring Manager,"
- End with "Sincerely,"
- Leave a blank line after "Sincerely," so the user can add their name.

COMPANY:
{company_name}

POSITION:
{position}

JOB DESCRIPTION OR NOTES:
{job_description or "No detailed job description was provided."}

JOB LINK:
{job_link or "No job link was provided."}

RESUME:
{resume_text}
"""

        client = AIService.get_client()

        response = client.chat.completions.create(
            model=os.getenv(
                "OPENROUTER_MODEL",
                "deepseek/deepseek-chat-v3-0324:free"
            ).strip(),
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.5,
        )

        cover_letter = response.choices[0].message.content

        if not cover_letter:
            raise ValueError("AI returned an empty cover letter")

        return cover_letter.strip()