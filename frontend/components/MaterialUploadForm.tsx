'use client'

import { useState, useEffect } from 'react'
import toast from 'react-hot-toast'
import { apiClient } from '@/lib/api'

export function MaterialUploadForm({ onMaterialUploaded }: { onMaterialUploaded: (material: any) => void }) {
  const [file, setFile] = useState<File | null>(null)
  const [title, setTitle] = useState('')
  const [subject, setSubject] = useState('Mathematics')
  const [grade, setGrade] = useState(10)
  const [loading, setLoading] = useState(false)
  const [uploadType, setUploadType] = useState<'file' | 'text'>('file')
  const [textContent, setTextContent] = useState('')

  const subjects = [
    'Mathematics',
    'Science',
    'History',
    'Geography',
    'Literature',
    'English',
    'Sinhala',
  ]

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      setFile(e.target.files[0])
      setTitle(e.target.files[0].name.replace(/\.[^/.]+$/, ''))
    }
  }

  const handleFileUpload = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!file) {
      toast.error('Please select a file')
      return
    }

    if (!title) {
      toast.error('Please enter a title')
      return
    }

    setLoading(true)
    try {
      const result = await apiClient.uploadMaterial(file)
      toast.success(`Material uploaded: ${result.filename}`)
      onMaterialUploaded(result)
      setFile(null)
      setTitle('')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  const handleTextUpload = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!title.trim()) {
      toast.error('Please enter a title')
      return
    }

    if (!textContent.trim()) {
      toast.error('Please enter content')
      return
    }

    setLoading(true)
    try {
      const result = await apiClient.addTextMaterial({
        title,
        content: textContent,
        subject,
        grade,
      })
      toast.success(`Material added: ${result.title}`)
      onMaterialUploaded(result)
      setTitle('')
      setTextContent('')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Upload Study Materials</h2>
      
      {/* Upload Type Selector */}
      <div className="flex gap-4 border-b border-slate-600">
        <button
          onClick={() => setUploadType('file')}
          className={`px-4 py-2 font-semibold transition-colors ${
            uploadType === 'file'
              ? 'text-blue-400 border-b-2 border-blue-400'
              : 'text-slate-400 hover:text-slate-300'
          }`}
        >
          Upload File
        </button>
        <button
          onClick={() => setUploadType('text')}
          className={`px-4 py-2 font-semibold transition-colors ${
            uploadType === 'text'
              ? 'text-blue-400 border-b-2 border-blue-400'
              : 'text-slate-400 hover:text-slate-300'
          }`}
        >
          Add Text
        </button>
      </div>

      {/* File Upload */}
      {uploadType === 'file' && (
        <form onSubmit={handleFileUpload} className="space-y-4">
          <div className="border-2 border-dashed border-slate-600 rounded-lg p-8 text-center hover:border-blue-400 transition-colors cursor-pointer">
            <input
              type="file"
              onChange={handleFileChange}
              accept=".pdf,.txt,.docx,.doc"
              className="hidden"
              id="file-input"
            />
            <label htmlFor="file-input" className="cursor-pointer">
              <div className="text-4xl mb-2">📄</div>
              <p className="text-slate-300">
                {file ? file.name : 'Drop your file here or click to select'}
              </p>
              <p className="text-xs text-slate-500 mt-2">Supported: PDF, TXT, DOCX</p>
            </label>
          </div>

          <input
            type="text"
            placeholder="Material Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full bg-slate-700 rounded-lg px-4 py-2 border border-slate-600 focus:border-blue-400 outline-none"
          />

          <select
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            className="w-full bg-slate-700 rounded-lg px-4 py-2 border border-slate-600 focus:border-blue-400 outline-none"
          >
            {subjects.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>

          <input
            type="number"
            placeholder="Grade"
            value={grade}
            onChange={(e) => setGrade(parseInt(e.target.value))}
            min="1"
            max="13"
            className="w-full bg-slate-700 rounded-lg px-4 py-2 border border-slate-600 focus:border-blue-400 outline-none"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 font-semibold py-3 rounded-lg transition-all"
          >
            {loading ? 'Uploading...' : 'Upload Material'}
          </button>
        </form>
      )}

      {/* Text Upload */}
      {uploadType === 'text' && (
        <form onSubmit={handleTextUpload} className="space-y-4">
          <input
            type="text"
            placeholder="Material Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full bg-slate-700 rounded-lg px-4 py-2 border border-slate-600 focus:border-blue-400 outline-none"
          />

          <select
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            className="w-full bg-slate-700 rounded-lg px-4 py-2 border border-slate-600 focus:border-blue-400 outline-none"
          >
            {subjects.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>

          <input
            type="number"
            placeholder="Grade"
            value={grade}
            onChange={(e) => setGrade(parseInt(e.target.value))}
            min="1"
            max="13"
            className="w-full bg-slate-700 rounded-lg px-4 py-2 border border-slate-600 focus:border-blue-400 outline-none"
          />

          <textarea
            placeholder="Paste your study material content here..."
            value={textContent}
            onChange={(e) => setTextContent(e.target.value)}
            rows={8}
            className="w-full bg-slate-700 rounded-lg px-4 py-2 border border-slate-600 focus:border-blue-400 outline-none font-mono text-sm"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 font-semibold py-3 rounded-lg transition-all"
          >
            {loading ? 'Adding...' : 'Add Material'}
          </button>
        </form>
      )}
    </div>
  )
}
