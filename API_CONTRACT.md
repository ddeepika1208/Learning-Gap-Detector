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
