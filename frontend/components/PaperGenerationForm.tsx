'use client'

import { useState, useEffect } from 'react'
import toast from 'react-hot-toast'
import { apiClient } from '@/lib/api'

interface PaperGenerationFormProps {
  materials: any[]
  onPaperGenerated: (paper: any) => void
}

export function PaperGenerationForm({ materials, onPaperGenerated }: PaperGenerationFormProps) {
  const [subject, setSubject] = useState('Mathematics')
  const [grade, setGrade] = useState(10)
  const [numQuestions, setNumQuestions] = useState(10)
  const [totalMarks, setTotalMarks] = useState(100)
  const [loading, setLoading] = useState(false)
  const [subjects, setSubjects] = useState<string[]>([])

  useEffect(() => {
    // Load available subjects
    const loadSubjects = async () => {
      try {
        const response = await apiClient.listSubjects()
        setSubjects(response.subjects || [])
      } catch (error) {
        console.error('Failed to load subjects:', error)
      }
    }
    loadSubjects()
  }, [])

  const handleGeneratePaper = async (e: React.FormEvent) => {
    e.preventDefault()

    if (materials.length === 0) {
      toast.error('Please upload materials first')
      return
    }

    setLoading(true)
    try {
      const paper = await apiClient.generatePaper({
        subject,
        grade,
        num_questions: numQuestions,
        total_marks: totalMarks,
      })
      toast.success('Paper generated successfully!')
      onPaperGenerated(paper)
    } catch (error: any) {
      console.error('Generation error:', error)
      toast.error(error.response?.data?.detail || 'Failed to generate paper')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Generate Mock Paper</h2>

      {materials.length === 0 && (
        <div className="bg-amber-900 bg-opacity-30 border border-amber-600 rounded-lg p-4 text-amber-200">
          ⚠️ Please upload study materials first to generate a paper.
        </div>
      )}

      <form onSubmit={handleGeneratePaper} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-semibold mb-2 text-slate-300">
              Subject
            </label>
            <select
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              className="w-full bg-slate-700 rounded-lg px-4 py-2 border border-slate-600 focus:border-blue-400 outline-none"
            >
              {subjects.length > 0 ? (
                subjects.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))
              ) : (
                <option>Loading subjects...</option>
              )}
            </select>
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2 text-slate-300">
              Grade
            </label>
            <input
              type="number"
              value={grade}
              onChange={(e) => setGrade(parseInt(e.target.value))}
              min="1"
              max="13"
              className="w-full bg-slate-700 rounded-lg px-4 py-2 border border-slate-600 focus:border-blue-400 outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2 text-slate-300">
              Number of Questions
            </label>
            <input
              type="number"
              value={numQuestions}
              onChange={(e) => setNumQuestions(parseInt(e.target.value))}
              min="5"
              max="50"
              className="w-full bg-slate-700 rounded-lg px-4 py-2 border border-slate-600 focus:border-blue-400 outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2 text-slate-300">
              Total Marks
            </label>
            <input
              type="number"
              value={totalMarks}
              onChange={(e) => setTotalMarks(parseInt(e.target.value))}
              min="50"
              max="500"
              step="10"
              className="w-full bg-slate-700 rounded-lg px-4 py-2 border border-slate-600 focus:border-blue-400 outline-none"
            />
          </div>
        </div>

        <div className="bg-slate-700 bg-opacity-50 rounded-lg p-4 border border-slate-600">
          <h3 className="font-semibold text-slate-300 mb-2">Uploaded Materials:</h3>
          <p className="text-slate-400">
            {materials.length} material{materials.length !== 1 ? 's' : ''} ready to use
          </p>
        </div>

        <button
          type="submit"
          disabled={loading || materials.length === 0}
          className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold py-3 rounded-lg transition-all text-lg"
        >
          {loading ? 'Generating Paper...' : 'Generate Exam Paper'}
        </button>
      </form>

      <div className="bg-blue-900 bg-opacity-20 border border-blue-600 rounded-lg p-4 text-blue-200 text-sm">
        <p>💡 The paper will be generated based on your uploaded study materials using AI-powered RAG (Retrieval Augmented Generation) technology.</p>
      </div>
    </div>
  )
}
