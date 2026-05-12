import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Sinhala Exam Paper Generator',
  description: 'Generate mock exam papers using AI and your study materials',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gradient-to-br from-slate-900 to-slate-800 text-white min-h-screen">
        <div className="max-w-7xl mx-auto px-4 py-8">
          <header className="mb-12 text-center">
            <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              Sinhala Exam Paper Generator
            </h1>
            <p className="text-slate-400">Upload your study materials and generate mock exam papers powered by AI</p>
          </header>
          {children}
        </div>
      </body>
    </html>
  )
}
