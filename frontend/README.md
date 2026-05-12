# Sinhala Exam Paper Generator - Frontend

A modern Next.js frontend for the Sinhala Exam Paper Generator API. Users can upload study materials and generate mock exam papers powered by AI.

## Features

- 📄 **Material Upload** - Upload PDF, DOCX, TXT files or paste text directly
- ✍️ **Paper Generation** - Generate customized mock exam papers based on uploaded materials
- 🎯 **Flexible Configuration** - Choose subject, grade, number of questions, and total marks
- 👁️ **Paper Preview** - View, expand, and review generated questions
- 🖨️ **Print & Download** - Print papers or download as text files

## Quick Start

### Prerequisites
- Node.js 18+
- Backend API running on `http://localhost:8000`

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

## Environment Configuration

Create a `.env.local` file to configure the API URL:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production, update this to your deployed API URL:

```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## Project Structure

```
frontend/
├── app/                      # Next.js app directory
│   ├── layout.tsx           # Root layout with header
│   ├── page.tsx             # Main page with tabs
│   └── globals.css          # Global styles
├── components/              # React components
│   ├── MaterialUploadForm.tsx    # File/text upload
│   ├── PaperGenerationForm.tsx   # Paper generation
│   └── PaperDisplay.tsx          # Paper preview
├── lib/                     # Utilities
│   └── api.ts              # API client
├── package.json            # Dependencies
└── tailwind.config.ts      # Tailwind configuration
```

## Component Overview

### MaterialUploadForm
- File upload (PDF, DOCX, TXT)
- Direct text paste
- Subject and grade selection
- Material metadata management

### PaperGenerationForm
- Subject selection from backend
- Grade level input
- Question count configuration
- Total marks setting
- Validation and error handling

### PaperDisplay
- Expandable question cards
- Answer and explanation display
- Print functionality
- Download as text file
- Paper metadata (ID, timestamp)

## API Integration

The frontend communicates with these endpoints:

**Materials:**
- `POST /api/v1/materials/upload` - Upload file
- `POST /api/v1/materials/add-text` - Add text material
- `GET /api/v1/materials/materials` - List materials

**Papers:**
- `POST /api/v1/papers/generate` - Generate paper
- `GET /api/v1/papers/subjects` - List available subjects

## Styling

- **Tailwind CSS** - Utility-first CSS framework
- **Dark theme** - Professional dark UI with blue/purple gradients
- **Responsive** - Mobile, tablet, and desktop optimized
- **Accessibility** - Semantic HTML and ARIA attributes

## Technologies

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **React Hot Toast** - Notifications

## Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Docker

Create a `Dockerfile`:

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

Build and run:

```bash
docker build -t sinhala-exam-frontend .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://api:8000 sinhala-exam-frontend
```

## Development Tips

- Check browser console for API errors
- Use React DevTools for component debugging
- Tailwind CSS class completion with VS Code extension
- Hot reload enabled for faster development

## Troubleshooting

**API Connection Issues:**
- Ensure backend is running on correct port
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify CORS settings in backend

**File Upload Not Working:**
- Check file size (large files may timeout)
- Verify supported formats: PDF, TXT, DOCX
- Check browser console for errors

**Paper Generation Fails:**
- Ensure materials are uploaded first
- Check backend logs for generation errors
- Verify grade level is within valid range

## License

MIT
