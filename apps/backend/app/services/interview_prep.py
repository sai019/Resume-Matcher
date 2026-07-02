"""Interview preparation generation service."""

import json
from typing import Any

from app.llm import complete_json
from app.prompts import INTERVIEW_PREP_PROMPT, get_language_name
from app.schemas import InterviewPrepData


async def generate_interview_prep(
    resume_data: dict[str, Any],
    job_description: str,
    language: str = "en",
) -> InterviewPrepData:
    """Generate structured interview preparation for a tailored resume."""
    prompt = INTERVIEW_PREP_PROMPT.format(
        job_description=job_description,
        resume_data=json.dumps(resume_data, ensure_ascii=False),
        output_language=get_language_name(language),
    )

    result = await complete_json(
        prompt=prompt,
        system_prompt=(
            "You are a career interview coach. Output truthful, resume-grounded "
            "interview preparation as JSON only."
        ),
        max_tokens=4096,
        schema_type="interview_prep",
    )

    return InterviewPrepData.model_validate(result)
