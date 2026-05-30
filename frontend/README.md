# DIRAS Frontend

Defence Intelligence Retrieval & Analysis System - React-based user interface for querying defence documents.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm/yarn
- Backend API running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📦 Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # React components
│   │   ├── QueryInterface.jsx    # Search form
│   │   └── ResultsDisplay.jsx    # Results view
│   ├── styles/          # CSS files
│   │   ├── index.css            # Global styles
│   │   ├── App.css              # App layout
│   │   ├── QueryInterface.css   # Search form styles
│   │   └── ResultsDisplay.css   # Results styles
│   ├── api/             # API integration
│   ├── App.jsx          # Main app component
│   └── main.jsx         # React entry point
├── index.html           # HTML entry point
├── vite.config.js       # Vite configuration
├── package.json         # Dependencies
└── README.md           # This file
```

## 🛠️ Available Scripts

### Development
```bash
# Start development server with hot reload
npm run dev
```

### Production
```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Code Quality
```bash
# Lint code
npm run lint
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
VITE_DEV_SERVER_PORT=3000
```

### Backend CORS

Make sure your FastAPI backend has CORS enabled:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📋 Features

✅ **Search Interface**
- Multi-line query input
- Document type filtering
- Results count selection
- Clear button to reset form

✅ **Results Display**
- Main answer with confidence score
- Response time metrics
- Source documents with references
- Related documents
- Search history

✅ **User Experience**
- Responsive design (desktop, tablet, mobile)
- Loading states with spinner
- Error handling with helpful messages
- Search history in localStorage
- Keyboard shortcuts (Enter to search, Shift+Enter for new line)

✅ **Performance**
- Fast development server
- Optimized production builds
- Lazy loading support
- Smooth animations

## 🔌 API Integration

### Query Endpoint

```
POST /api/v1/query
```

**Request:**
```json
{
  "question": "What is the latest defence procurement policy?",
  "top_k": 5,
  "document_type": "policy_document"
}
```

**Response:**
```json
{
  "answer": "The latest defence procurement policy...",
  "sources": ["Document 1", "Document 2"],
  "confidence": 0.92,
  "processing_time": 0.8,
  "documents_searched": 5000,
  "results_count": 5,
  "model_used": "Llama 3"
}
```

## 📱 Responsive Design

The frontend is fully responsive and works on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## 🎨 Styling

### Color Scheme
- Primary: `#667eea` (Purple)
- Secondary: `#764ba2` (Dark Purple)
- Success: `#28a745` (Green)
- Warning: `#ffc107` (Yellow)
- Error: `#dc3545` (Red)

### Fonts
- Primary: System fonts (Segoe UI, Roboto, etc.)
- Monospace: Courier New (for code)

## 🚀 Deployment

### Build

```bash
npm run build
```

This creates an optimized production build in the `dist/` directory.

### Serve

```bash
# Using a simple HTTP server
python -m http.server 3000

# Or using Node.js
npx serve -s dist -p 3000
```

### Docker

```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=build /app/dist ./dist
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
```

Build and run:
```bash
docker build -t diras-frontend .
docker run -p 3000:3000 diras-frontend
```

## 🐛 Troubleshooting

### Backend Connection Issues
- Ensure backend is running: `docker compose up -d`
- Check `VITE_API_URL` in `.env` matches backend URL
- Verify CORS is enabled on backend

### Module Not Found
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Port Already in Use
```bash
# Use different port
npm run dev -- --port 3001
```

## 📚 Technology Stack

- **Framework**: React 18
- **Build Tool**: Vite 5
- **HTTP Client**: Axios
- **Styling**: CSS3
- **State Management**: React Hooks

## 📖 Development Guide

### Component Structure

Each component follows this pattern:
```jsx
import { useState, useEffect } from 'react'
import '../styles/Component.css'

function Component({ prop1, prop2 }) {
  const [state, setState] = useState(null)

  useEffect(() => {
    // Setup
  }, [])

  return (
    <div className="component">
      {/* JSX */}
    </div>
  )
}

export default Component
```

### Adding New Features

1. Create component in `src/components/`
2. Add styles in `src/styles/`
3. Import in `App.jsx`
4. Update API integration if needed

## 📝 License

Part of DIRAS project - Defence Intelligence Retrieval & Analysis System

## 🤝 Contributing

Please follow the existing code style and component structure.

## 📞 Support

For issues or questions, refer to the main DIRAS documentation.
