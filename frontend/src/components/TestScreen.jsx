import { useEffect, useState } from 'react'
import { getNextQuestion, submitAnswer, getConcepts } from '../api'

export default function TestScreen({ studentId }) {
  const [question, setQuestion] = useState(null)
  const [selected, setSelected] = useState(null)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [concepts, setConcepts] = useState([])

  function loadQuestion() {
    setQuestion(null)
    setSelected(null)
    setResult(null)
    setError('')
    getNextQuestion(studentId)
      .then(setQuestion)
      .catch((err) => setError(err.message))
  }

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(loadQuestion, [studentId])
  useEffect(() => {
    getConcepts()
     .then(setConcepts)
     .catch((err) => setError(err.message))
    }, [])

  async function handleSubmit() {
    try {
      const data = await submitAnswer(studentId, question.id, selected)
      console.log(data)
      setResult(data)
    } catch (err) {
      setError(err.message)
    }
  }

  if (error) return <p className="p-4 text-red-700">Error: {error}</p>
  if (!question) return <p className="p-4">Loading question...</p>

  const answered = result !== null

  function optionStyle(i) {
    if (answered && i === result.correct_answer)
      return 'border-green-600 bg-green-50'
    if (answered && selected === i) return 'border-red-600 bg-red-50'
    if (selected === i) return 'border-blue-600 bg-blue-50'
    return 'border-gray-300 bg-white'
  }

  return (
    <div className="mx-auto max-w-xl p-4">
      <h2 className="mb-4 text-lg font-semibold">{question.text}</h2>
      <div className="space-y-2">
        {question.options.map((option, i) => (
          <button
            key={i}
            disabled={answered}
            onClick={() => setSelected(i)}
            className={`w-full rounded-md border p-3 text-left ${optionStyle(i)}`}
          >
            {option}
          </button>
        ))}
      </div>

      {!answered && (
        <button
          onClick={handleSubmit}
          disabled={selected === null}
          className="mt-4 rounded-md bg-blue-600 px-4 py-2 text-white disabled:opacity-50"
        >
          Submit
        </button>
      )}

      {answered && (
        <div className="mt-4">
          <p className="font-semibold">
            {result.correct ? 'Correct' : 'Wrong'}
          </p>
          {result.weak_prerequisite && (
            <p className="mt-2 font-medium text-orange-700">
            Revise{' '}
            {concepts.find((concept) => concept.id === result.weak_prerequisite)?.name ?? result.weak_prerequisite}{' '}
            first.
            </p>
          )}
          <button
            onClick={loadQuestion}
            className="mt-2 rounded-md bg-blue-600 px-4 py-2 text-white"
          >
            Next
          </button>
        </div>
      )}
    </div>
  )
}