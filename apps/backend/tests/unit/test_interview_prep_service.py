from unittest.mock import AsyncMock, patch

import pytest
from pydantic import ValidationError

from app.services.interview_prep import generate_interview_prep


SAMPLE_RESUME = {
    "personalInfo": {"name": "Jane Doe"},
    "summary": "Backend engineer",
    "workExperience": [],
    "education": [],
    "personalProjects": [],
    "additional": {"technicalSkills": ["Python", "FastAPI"]},
}


def _valid_payload():
    return {
        "role_fit_analysis": ["Python API experience is relevant."],
        "resume_questions": [
            {
                "question": "How did you build the API?",
                "focus_area": "Backend APIs",
                "suggested_answer_points": ["Use resume-grounded API details."],
            }
        ],
        "project_follow_ups": [],
        "skill_gaps": [
            {
                "skill": "Kubernetes",
                "why_it_matters": "The JD mentions deployment.",
                "preparation_suggestion": "Review basics without claiming experience.",
            }
        ],
        "talking_points": ["Connect FastAPI work to the role."],
    }


@pytest.mark.asyncio
async def test_generate_interview_prep_validates_successful_json():
    with patch(
        "app.services.interview_prep.complete_json",
        new_callable=AsyncMock,
    ) as mock_complete:
        mock_complete.return_value = _valid_payload()

        result = await generate_interview_prep(SAMPLE_RESUME, "Need FastAPI", "en")

    assert result.role_fit_analysis == ["Python API experience is relevant."]
    mock_complete.assert_awaited_once()
    assert mock_complete.await_args.kwargs["schema_type"] == "interview_prep"


@pytest.mark.asyncio
async def test_generate_interview_prep_rejects_malformed_llm_json():
    with patch(
        "app.services.interview_prep.complete_json",
        new_callable=AsyncMock,
    ) as mock_complete:
        mock_complete.return_value = {
            "role_fit_analysis": ["Only one required key is present."]
        }

        with pytest.raises(ValidationError):
            await generate_interview_prep(SAMPLE_RESUME, "Need FastAPI", "en")
