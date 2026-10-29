import json
from pathlib import Path

DATA = Path(__file__).parent / "data"

def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)

concepts = load("concepts.json")
questions = load("questions.json")
errors = []

concept_ids = {c["id"] for c in concepts}
if len(concept_ids) != len(concepts):
    errors.append("Duplicate concept ids")

for c in concepts:
    for p in c["prerequisites"]:
        if p not in concept_ids:
            errors.append(f"Concept {c['id']}: unknown prerequisite '{p}'")

seen = set()
counts = {cid: 0 for cid in concept_ids}

for q in questions:
    qid = q.get("id")
    if qid in seen:
        errors.append(f"{qid}: duplicate id")
    seen.add(qid)

    if q.get("concept_id") not in concept_ids:
        errors.append(f"{qid}: concept_id '{q.get('concept_id')}' not in concepts.json")
    else:
        counts[q["concept_id"]] += 1

    opts = q.get("options", [])
    if len(opts) != 4:
        errors.append(f"{qid}: needs exactly 4 options, has {len(opts)}")
    if len(set(opts)) != len(opts):
        errors.append(f"{qid}: duplicate options")
    if q.get("answer") not in (0, 1, 2, 3):
        errors.append(f"{qid}: answer must be 0 to 3")
    if q.get("difficulty") not in (1, 2, 3):
        errors.append(f"{qid}: difficulty must be 1, 2 or 3")
    if not q.get("text"):
        errors.append(f"{qid}: empty text")

print("Questions per concept:")
for cid, n in sorted(counts.items()):
    flag = "  <-- too few" if n < 6 else ""
    print(f"  {cid}: {n}{flag}")

print()
if errors:
    print(f"{len(errors)} problem(s):")
    for e in errors:
        print(" -", e)
else:
    print("All checks passed.")