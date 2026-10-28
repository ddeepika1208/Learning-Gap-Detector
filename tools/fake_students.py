import json, random
from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

CONCEPTS = ["variables", "operators", "control_flow", "loops",
    "functions", "arrays", "strings", "pointers", "recursion",
    "structs", "dynamic_memory", "linked_list", "stack_queue",
    "sorting", "trees"]

PENALTY = {"pointers": -0.20, "linked_list": -0.25,
           "recursion": -0.10, "dynamic_memory": -0.15}

students = []
for i in range(1, 31):
    skill = random.uniform(0.35, 0.85)
    mastery = []
    for c in CONCEPTS:
        score = skill + PENALTY.get(c, 0) + random.uniform(-0.1, 0.1)
        score = max(0, min(1, score))
        mastery.append({"concept_id": c, "mastery": round(score, 2)})
    students.append({"student_id": f"s{i}", "name": fake.name(), "mastery": mastery})

with open("tools/fake_students.json", "w") as f:
    json.dump(students, f, indent=2)
print("Saved", len(students), "students")