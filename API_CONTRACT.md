# API Contract

## GET /concepts
Returns all concepts.
Response: [{ "id": "pointers", "name": "Pointers", "prerequisites": ["variables", "arrays"] }]

## GET /questions/next?student_id=s1
Returns the next question for a student.
Response: { "id": "q2", "concept_id": "pointers", "text": "...", "options": ["A","B","C","D"], "difficulty": 2 }
Note: the answer is NOT sent, so students can't cheat from the browser.

## POST /answers
Student submits an answer.
Request: { "student_id": "s1", "question_id": "q2", "selected": 1 }
Response: { "correct": true, "correct_answer": 1, "weak_prerequisite": "variables" or null }

## GET /mastery?student_id=s1
Returns the student's mastery per concept.
Response: [{ "concept_id": "pointers", "mastery": 0.65 }]


## GET /students
Returns every student who has answered at least once.
```json
[
  {"student_id": "s1", "answers": 5, "avg_mastery": 0.46}
]
```

## GET /class/summary
```json
{
  "student_count": 3,
  "concepts": [
    {"concept_id": "pointers", "name": "Pointers", "avg_mastery": 0.52}
  ],
  "weakest_concepts": [
    {"concept_id": "recursion", "name": "Recursion", "avg_mastery": 0.31}
  ],
  "students_needing_help": [
    {"student_id": "s2", "avg_mastery": 0.33}
  ]
}
```
Rules:
- `concepts`: all 15 concepts, average over all students. A student with no score on a concept counts as 0.5.
- `weakest_concepts`: the 3 lowest `avg_mastery`.
- `students_needing_help`: students whose `avg_mastery` is below 0.4.
- `avg_mastery` is rounded to 3 decimals.
