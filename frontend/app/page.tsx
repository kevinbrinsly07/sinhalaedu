'use client'

import { useState, useRef } from 'react'
import { MaterialUploadForm } from '@/components/MaterialUploadForm'
import { PaperGenerationForm } from '@/components/PaperGenerationForm'
import { PaperDisplay } from '@/components/PaperDisplay'
import { Toaster } from 'react-hot-toast'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'upload' | 'generate'>('upload')
  const [materials, setMaterials] = useState<any[]>([])
  const [generatedPaper, setGeneratedPaper] = useState<any | null>(null)
  const [loading, setLoading] = useState(false)

  const handleMaterialUploaded = (material: any) => {
    setMaterials([...materials, material])
  }

  const handlePaperGenerated = (paper: any) => {
    setGeneratedPaper(paper)
    setActiveTab('preview')
  }

  return (
    <>
      <Toaster position="top-right" />
      
      <main className="space-y-8">
        {/* Tabs */}
        <div className="flex gap-4 border-b border-slate-700">
          <button
            onClick={() => setActiveTab('upload')}
            className={`px-6 py-3 font-semibold transition-colors ${
              activeTab === 'upload'
                ? 'text-blue-400 border-b-2 border-blue-400'
                : 'text-slate-400 hover:text-slate-300'
            }`}
          >
            Upload Materials
          </button>
          <button
            onClick={() => setActiveTab('generate')}
            className={`px-6 py-3 font-semibold transition-colors ${
              activeTab === 'generate'
                ? 'text-blue-400 border-b-2 border-blue-400'
                : 'text-slate-400 hover:text-slate-300'
            }`}
          >
            Generate Paper
          </button>
          {generatedPaper && (
            <button
              onClick={() => setActiveTab('preview')}
              className={`px-6 py-3 font-semibold transition-colors ${
                activeTab === 'preview'
                  ? 'text-blue-400 border-b-2 border-blue-400'
                  : 'text-slate-400 hover:text-slate-300'
              }`}
            >
              Paper Preview
            </button>
          )}
        </div>

        {/* Content */}
        <div className="glass-effect rounded-2xl p-8 fade-in">
          {activeTab === 'upload' && (
            <MaterialUploadForm onMaterialUploaded={handleMaterialUploaded} />
          )}
          
          {activeTab === 'generate' && (
            <PaperGenerationForm
              materials={materials}
              onPaperGenerated={handlePaperGenerated}
            />
          )}
          
          {activeTab === 'preview' && generatedPaper && (
            <PaperDisplay paper={generatedPaper} />
          )}
        </div>

        {/* Materials List */}
        {materials.length > 0 && (
          <div className="glass-effect rounded-2xl p-8">
            <h2 className="text-2xl font-bold mb-6">Uploaded Materials</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {materials.map((material, idx) => (
                <div key={idx} className="bg-slate-700 rounded-lg p-4 border border-slate-600">
                  <h3 className="font-semibold text-blue-300">{material.filename}</h3>
                  <p className="text-sm text-slate-400">ID: {material.material_id.slice(0, 12)}...</p>
                  <p className="text-xs text-slate-500 mt-2">Status: {material.status}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </>
  )
}
