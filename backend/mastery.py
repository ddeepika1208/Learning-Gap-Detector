STORE = {}  # {student_id: {concept_id: mastery}}
START = 0.5

def get_mastery(student_id, concept_id):
    return STORE.get(student_id, {}).get(concept_id, START)

def update_mastery(student_id, concept_id, correct, difficulty):
    old = get_mastery(student_id, concept_id)
    rate = 0.1 + 0.05 * difficulty
    target = 1.0 if correct else 0.0
    new = old + rate * (target - old)
    STORE.setdefault(student_id, {})[concept_id] = round(new, 3)
    return round(new, 3)

def all_mastery(student_id, concepts):
    return [
        {"concept_id": c["id"], "mastery": get_mastery(student_id, c["id"])}
        for c in concepts
    ]