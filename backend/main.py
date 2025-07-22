# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm import call_deepseek
from evaluator import evaluate_code
from auth import router as auth_router
from fastapi import Request, Depends, HTTPException
import firebase_admin
from firebase_admin import auth, credentials

cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

app = FastAPI()
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="No auth token")
    token = auth_header.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid token")

class Submission(BaseModel):
    problem_id: int
    student_code: str

class CorrectionRequest(BaseModel):
    problem_id: int
    student_code: str

@app.post("/submit/")
def submit_code(sub: Submission):
    result = evaluate_code(sub.problem_id, sub.student_code)

    feedback = ""
    if result["score"] < 100:
        feedback += "❌ Your code did not pass all tests.\n"
        for r in result["results"]:
            if not r["passed"]:
                feedback += f"- Test with input `{r['input']}` failed. Expected `{r['expected']}` but got `{r['actual']}`.\n"
    else:
        feedback = "✅ Great job! Your solution passed all the tests."

    return {
        "score": result["score"],
        "feedback": feedback
    }

@app.post("/correction/")
def correction(sub: CorrectionRequest):
    result = evaluate_code(sub.problem_id, sub.student_code)

    if result["score"] == 100:
        return {"correction": "✅ No correction needed. Your code is perfect!"}

    prompt = f"Correct the following Python function task:\n\n{result['description']}"
    correction = call_deepseek(prompt)
    return {"correction": correction}
