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