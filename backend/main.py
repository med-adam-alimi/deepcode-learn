from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm import call_deepseek
from evaluator import evaluate_code

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Submission(BaseModel):
    problem_id: int
    student_code: str

@app.post("/submit/")
def submit_code(sub: Submission):
    result = evaluate_code(sub.problem_id, sub.student_code)
    
    if result["score"] < 100:
        # Student code failed → get model suggestion
        prompt = f"Write a correct Python solution for the following task:\n{result['description']}"
        correction = call_deepseek(prompt)
        result["correction"] = correction
    else:
        result["correction"] = None

    return result
