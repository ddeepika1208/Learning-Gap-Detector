import random
import json
from pathlib import Path
from fastapi import FastAPI

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

DATA_DIR = Path(__file__).parent / "data"

def load_json(filename):
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/concepts")
def get_concepts():
    return load_json("concepts.json")

@app.get("/questions/next")
def get_next_question(student_id: str):
    questions = load_json("questions.json")
    q = random.choice(questions)
    return {
        "id": q["id"],
        "concept_id": q["concept_id"],
        "text": q["text"],
        "options": q["options"],
        "difficulty": q["difficulty"],
    }

class AnswerIn(BaseModel):
    student_id: str
    question_id: str
    selected: int

@app.post("/answers")
def submit_answer(a: AnswerIn):
    questions = load_json("questions.json")
    q = next((x for x in questions if x["id"] == a.question_id), None)
    if q is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return {
        "correct": a.selected == q["answer"],
        "correct_answer": q["answer"],
    }