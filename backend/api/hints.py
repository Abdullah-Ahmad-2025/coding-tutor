from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.hint_generator import HintGenerator

router = APIRouter(prefix="/api/hints", tags=["hints"])


class HintRequest(BaseModel):
    problem_description: str
    user_code: str
    test_results: list
    mistakes: list


class ExplainRequest(BaseModel):
    problem_description: str
    user_code: str
    test_results: list
    mistake_type: str


@router.post("/generate")
async def get_hint(req: HintRequest):
    """Generate a hint for the student."""
    try:
        generator = HintGenerator()
        hint = generator.generate_hint(
            req.problem_description,
            req.user_code,
            req.test_results,
            req.mistakes,
        )
        return {"hint": hint}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hint generation failed: {e}")


@router.post("/explain")
async def explain_mistake(req: ExplainRequest):
    """Explain a specific mistake."""
    try:
        generator = HintGenerator()
        explanation = generator.explain_mistake(
            req.problem_description,
            req.user_code,
            req.test_results,
            req.mistake_type,
        )
        return {"explanation": explanation}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation failed: {e}")
