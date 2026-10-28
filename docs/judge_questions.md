\# Judge Questions and Answers



\## Q1. Why is this better than a normal quiz app?

A normal quiz gives the same questions to everyone and only shows a score. Ours knows that concepts depend on each other. If a student fails linked lists, we check whether the real gap is pointers and practise that first.



\## Q2. How is mastery calculated?

Each student has a score from 0 to 1 for each of the 15 concepts. A correct answer raises that concept's score and a wrong answer lowers it. \[CONFIRM EXACT FORMULA WITH PERSON 1]



\## Q3. How does the app pick the next question?

It looks for the student's weakest concepts, checks their prerequisites first, and picks a question from the 30 reviewed questions on that concept. So students practise where they are weak, not what they already know.



\## Q4. Did AI write your questions? How do you know they are correct?

AI helped us draft them. Every one of the 30 questions was reviewed by a human before use. Nothing unreviewed reaches a student. We see this validation layer as a feature, not a shortcut.



\## Q5. What does the prerequisite graph actually do?

It is a map of 15 concepts with arrows from what you must know first to what comes next. It lets the app trace a weak topic back to its root cause, and it shows teachers where learning chains break.

\## Q6. Why not just ask ChatGPT to teach students?

A chat tool does not remember each student's mastery or know our prerequisite map. Ours tracks progress over time, picks questions on purpose, and gives teachers a class-level view. It is a structured system, not a one-off chat.



\## Q7. What happens when a new student has no data?

They start with a default score on every concept, and the first few questions adjust it quickly. \[CONFIRM STARTING SCORE WITH PERSON 1]



\## Q8. Is the dashboard showing real data?

We used fake students to build and test the dashboard before the backend was ready. The final dashboard reads real data from our backend. The pilot uses real students.



\## Q9. Only 30 questions. Is that enough?

For a prototype, yes. It is a small, carefully reviewed bank covering all 15 concepts. The design lets us add more questions without changing the system. We chose quality over quantity.



\## Q10. Does your pilot prove students learn better?

No, and we say so. With 10-20 students, the pilot measures usability and student feedback, not long-term learning gains. Proving learning gains needs a larger, longer study, which is our future work.

