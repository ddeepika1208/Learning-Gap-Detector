const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8080'

async function request(path, options) {
  const res = await fetch(`${BASE_URL}${path}`, options)
  if (!res.ok) {
    throw new Error(`Request failed with status ${res.status}`)
  }
  return res.json()
}

export const getConcepts = async () => {
  const response = await fetch(`${BASE_URL}/concepts`);

  if (!response.ok) {
    throw new Error("Failed to fetch concepts");
  }

  return response.json();
};

export const getNextQuestion = (studentId) =>
  request(`/questions/next?student_id=${encodeURIComponent(studentId)}`)

export const submitAnswer = (studentId, questionId, selected) =>
  request('/answers', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      student_id: studentId,
      question_id: questionId,
      selected,
    }),
  })

export const getMastery = (studentId) =>
  request(`/mastery?student_id=${encodeURIComponent(studentId)}`)
