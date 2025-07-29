# backend/correction.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
from llm import call_deepseek  # Assuming you have this LLM integration module

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CorrectionRequest(BaseModel):
    problem_id: int
    student_code: str
    language: str = "python"
    problem_context: Optional[str] = None  # Additional context about the problem

@router.post("/correction/")
async def generate_correction(req: CorrectionRequest):
    """
    Generate a code correction using DeepSeek LLM.
    
    Args:
        req: CorrectionRequest containing:
            - problem_id: Identifier for the problem
            - student_code: Code submitted by student
            - language: Programming language (default: python)
            - problem_context: Optional description of the problem
    
    Returns:
        JSON response with either:
            - correction: The corrected code
            - OR error message if correction fails
    """
    # Validate input code isn't empty
    if not req.student_code.strip():
        raise HTTPException(
            status_code=400,
            detail="Empty code submission"
        )

    # Construct the prompt with problem context if available
    prompt = f"""
    Analyze this {req.language} code submission for problem {req.problem_id}:
    
    ```{req.language}
    {req.student_code}
    ```
    
    {f"Problem context: {req.problem_context}" if req.problem_context else ""}
    
    Provide a corrected version that would pass all tests for this problem.
    Return ONLY the corrected code with no additional explanation or formatting.
    The response must be valid {req.language} code that can be directly executed.
    """

    try:
        logger.info(f"Generating correction for problem {req.problem_id}")
        correction_code = call_deepseek(
            prompt=prompt,
            max_tokens=512,
            temperature=0.2  # Lower temperature for more deterministic corrections
        )
        
        # Clean up the response (remove markdown code blocks if present)
        if correction_code.startswith("```") and correction_code.endswith("```"):
            correction_code = correction_code[3:-3].strip()
            if correction_code.startswith(req.language):
                correction_code = correction_code[len(req.language):].strip()
        
        return {
            "correction": correction_code,
            "language": req.language,
            "problem_id": req.problem_id
        }
        
    except Exception as e:
        logger.error(f"Correction generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate correction: {str(e)}"
        )