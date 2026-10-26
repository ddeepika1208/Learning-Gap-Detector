from mastery import update_mastery, all_mastery, get_mastery
from graph import build_graph, find_weak_root
import random
import json
from pathlib import Path
from fastapi import FastAPI

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

DATA_DIR = Path(__file__).parent / "data"
LAST = {}  # remembers the last question each student got
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
    graph = build_graph(load_json("concepts.json"))

    with_questions = {q["concept_id"] for q in questions}
    target = min(with_questions, key=lambda c: get_mastery(student_id, c))

    weak = find_weak_root(student_id, target, graph, get_mastery)
    if weak in with_questions:
        target = weak

    m = get_mastery(student_id, target)
    wanted = 1 if m < 0.4 else 2 if m < 0.7 else 3

    pool = [q for q in questions if q["concept_id"] == target]
    fresh = [q for q in pool if q["id"] != LAST.get(student_id)] or pool
    q = min(fresh, key=lambda x: abs(x["difficulty"] - wanted))
    LAST[student_id] = q["id"]

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
    correct = a.selected == q["answer"]
    update_mastery(a.student_id, q["concept_id"], correct, q["difficulty"])
    weak = None
    if not correct:
        graph = build_graph(load_json("concepts.json"))
        weak = find_weak_root(a.student_id, q["concept_id"], graph, get_mastery)
    return {
        "correct": correct,
        "correct_answer": q["answer"],
        "weak_prerequisite": weak,
    }
@app.get("/mastery")
def get_mastery_all(student_id: str):
    return all_mastery(student_id, load_json("concepts.json"))