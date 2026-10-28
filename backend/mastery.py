from sqlalchemy import func
from db import SessionLocal, Student, Answer, Mastery

START = 0.5


def _ensure_student(s, student_id):
    if s.get(Student, student_id) is None:
        s.add(Student(id=student_id))
        s.flush()


def get_mastery(student_id, concept_id):
    with SessionLocal() as s:
        row = s.get(Mastery, (student_id, concept_id))
        return row.value if row else START


def update_mastery(student_id, concept_id, correct, difficulty):
    rate = 0.1 + 0.05 * difficulty
    target = 1.0 if correct else 0.0
    with SessionLocal() as s:
        _ensure_student(s, student_id)
        row = s.get(Mastery, (student_id, concept_id))
        old = row.value if row else START
        new = round(old + rate * (target - old), 3)
        if row:
            row.value = new
        else:
            s.add(Mastery(student_id=student_id,
                          concept_id=concept_id, value=new))
        s.commit()
    return new


def record_answer(student_id, question_id, concept_id, selected, correct):
    with SessionLocal() as s:
        _ensure_student(s, student_id)
        s.add(Answer(student_id=student_id, question_id=question_id,
                     concept_id=concept_id, selected=selected,
                     correct=correct))
        s.commit()


def all_mastery(student_id, concepts):
    with SessionLocal() as s:
        rows = s.query(Mastery).filter_by(student_id=student_id).all()
        saved = {r.concept_id: r.value for r in rows}
    return [
        {"concept_id": c["id"], "mastery": saved.get(c["id"], START)}
        for c in concepts
    ]

def list_students(concepts):
    n = len(concepts)
    with SessionLocal() as s:
        counts = dict(
            s.query(Answer.student_id, func.count(Answer.id))
            .group_by(Answer.student_id).all()
        )
        sums = dict(
            s.query(Mastery.student_id, func.sum(Mastery.value))
            .group_by(Mastery.student_id).all()
        )
        saved = dict(
            s.query(Mastery.student_id, func.count(Mastery.concept_id))
            .group_by(Mastery.student_id).all()
        )
    result = []
    for sid, cnt in counts.items():
        total = (sums.get(sid) or 0) + START * (n - saved.get(sid, 0))
        result.append({
            "student_id": sid,
            "answers": cnt,
            "avg_mastery": round(total / n, 3),
        })
    return result

def class_summary(concepts):
    students = list_students(concepts)
    with SessionLocal() as s:
        rows = s.query(Mastery).all()
    by_concept = {}
    for r in rows:
        by_concept.setdefault(r.concept_id, {})[r.student_id] = r.value
    n_students = len(students)

    items = []
    for c in concepts:
        scores = by_concept.get(c["id"], {})
        total = sum(scores.values()) + START * (n_students - len(scores))
        avg = round(total / n_students, 3) if n_students else START
        items.append({"concept_id": c["id"], "name": c["name"],
                      "avg_mastery": avg})

    weakest = sorted(items, key=lambda x: x["avg_mastery"])[:3]
    needing_help = [
        {"student_id": st["student_id"], "avg_mastery": st["avg_mastery"]}
        for st in students if st["avg_mastery"] < 0.4
    ]
    return {
        "student_count": n_students,
        "concepts": items,
        "weakest_concepts": weakest,
        "students_needing_help": needing_help,
    }