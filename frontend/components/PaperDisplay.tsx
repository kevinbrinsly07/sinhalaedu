'use client'

import { useState } from 'react'

interface Question {
  id: string
  question_text: string
  question_type: string
  marks: number
  options?: string[]
  correct_answer?: string
  explanation?: string
}

interface Paper {
  paper_id: string
  title: string
  subject: string
  grade: number
  total_marks: number
  duration_minutes: number
  questions: Question[]
  instructions: string
  generated_at: string
}

export function PaperDisplay({ paper }: { paper: Paper }) {
  const [expandedQuestions, setExpandedQuestions] = useState<Set<string>>(new Set())

  const toggleQuestion = (questionId: string) => {
    const newExpanded = new Set(expandedQuestions)
    if (newExpanded.has(questionId)) {
      newExpanded.delete(questionId)
    } else {
      newExpanded.add(questionId)
    }
    setExpandedQuestions(newExpanded)
  }

  const handlePrint = () => {
    window.print()
  }

  const handleDownload = () => {
    const text = generatePaperText()
    const element = document.createElement('a')
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text))
    element.setAttribute('download', `exam_paper_${paper.paper_id}.txt`)
    element.style.display = 'none'
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
  }

  const generatePaperText = () => {
    let text = `EXAM PAPER\n`
    text += `Title: ${paper.title}\n`
    text += `Subject: ${paper.subject}\n`
    text += `Grade: ${paper.grade}\n`
    text += `Total Marks: ${paper.total_marks}\n`
    text += `Duration: ${paper.duration_minutes} minutes\n`
    text += `\n---\n\n`

    if (paper.instructions) {
      text += `INSTRUCTIONS:\n${paper.instructions}\n\n`
    }

    paper.questions.forEach((q, idx) => {
      text += `Q${idx + 1}. ${q.question_text} (${q.marks} marks)\n`
      if (q.options) {
        q.options.forEach((opt, i) => {
          text += `   ${String.fromCharCode(65 + i)}) ${opt}\n`
        })
      }
      text += `\n`
    })

    return text
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h2 className="text-3xl font-bold text-blue-300 mb-2">{paper.title}</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <p className="text-slate-400">Subject</p>
              <p className="font-semibold text-white">{paper.subject}</p>
            </div>
            <div>
              <p className="text-slate-400">Grade</p>
              <p className="font-semibold text-white">{paper.grade}</p>
            </div>
            <div>
              <p className="text-slate-400">Total Marks</p>
              <p className="font-semibold text-white">{paper.total_marks}</p>
            </div>
            <div>
              <p className="text-slate-400">Duration</p>
              <p className="font-semibold text-white">{paper.duration_minutes} min</p>
            </div>
          </div>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handlePrint}
            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg font-semibold transition-colors"
          >
            🖨️ Print
          </button>
          <button
            onClick={handleDownload}
            className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg font-semibold transition-colors"
          >
            ⬇️ Download
          </button>
        </div>
      </div>

      {paper.instructions && (
        <div className="bg-slate-700 bg-opacity-50 rounded-lg p-4 border border-slate-600">
          <h3 className="font-semibold mb-2 text-blue-300">Instructions</h3>
          <p className="text-slate-300 whitespace-pre-wrap">{paper.instructions}</p>
        </div>
      )}

      <div className="space-y-3">
        <h3 className="text-xl font-semibold text-blue-300">
          Questions ({paper.questions.length})
        </h3>

        {paper.questions.map((question, idx) => (
          <div key={question.id} className="border border-slate-600 rounded-lg overflow-hidden">
            <button
              onClick={() => toggleQuestion(question.id)}
              className="w-full p-4 hover:bg-slate-700 bg-slate-800 transition-colors text-left flex justify-between items-start"
            >
              <div className="flex-1">
                <div className="flex items-start gap-3">
                  <span className="font-bold text-blue-400 mt-1">Q{idx + 1}</span>
                  <div>
                    <p className="text-white font-semibold">{question.question_text}</p>
                    <div className="flex gap-4 mt-2 text-xs text-slate-400">
                      <span>📌 {question.question_type}</span>
                      <span>⭐ {question.marks} marks</span>
                    </div>
                  </div>
                </div>
              </div>
              <span className="text-slate-400 ml-4">
                {expandedQuestions.has(question.id) ? '▼' : '▶'}
              </span>
            </button>

            {expandedQuestions.has(question.id) && (
              <div className="p-4 bg-slate-900 border-t border-slate-600 space-y-3">
                {question.options && (
                  <div>
                    <p className="text-slate-300 font-semibold mb-2">Options:</p>
                    <div className="space-y-1">
                      {question.options.map((opt, i) => (
                        <div key={i} className="text-slate-300">
                          <span className="font-semibold text-blue-400">
                            {String.fromCharCode(65 + i)})
                          </span>{' '}
                          {opt}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {question.correct_answer && (
                  <div className="bg-green-900 bg-opacity-30 border border-green-600 rounded p-3">
                    <p className="text-green-300 font-semibold">✓ Answer: {question.correct_answer}</p>
                  </div>
                )}

                {question.explanation && (
                  <div className="bg-blue-900 bg-opacity-30 border border-blue-600 rounded p-3">
                    <p className="text-blue-300 font-semibold mb-1">💡 Explanation:</p>
                    <p className="text-blue-200 text-sm">{question.explanation}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="text-sm text-slate-500">
        <p>Generated: {new Date(paper.generated_at).toLocaleString()}</p>
        <p>Paper ID: {paper.paper_id}</p>
      </div>
    </div>
  )
}
