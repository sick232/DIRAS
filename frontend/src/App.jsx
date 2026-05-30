import { useState, useEffect } from 'react'
import QueryInterface from './components/QueryInterface'
import ResultsDisplay from './components/ResultsDisplay'
import './styles/App.css'

function App() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [history, setHistory] = useState([])

  // Load history from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('diras_history')
    if (saved) {
      setHistory(JSON.parse(saved))
    }
  }, [])

  const handleSearch = async (query, topK, docType) => {
    setLoading(true)
    setError(null)

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      
      const payload = {
        question: query,
        top_k: parseInt(topK),
      }
      
      if (docType) {
        payload.document_type = docType
      }

      const response = await fetch(`${apiUrl}/api/v1/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`)
      }

      const data = await response.json()
      setResults(data)

      // Add to history
      const newHistoryItem = {
        query,
        timestamp: new Date().toLocaleString(),
        topK,
        docType,
      }
      const updatedHistory = [newHistoryItem, ...history].slice(0, 10)
      setHistory(updatedHistory)
      localStorage.setItem('diras_history', JSON.stringify(updatedHistory))
    } catch (err) {
      setError(err.message)
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleHistoryClick = (item) => {
    handleSearch(item.query, item.topK, item.docType)
  }

  const clearHistory = () => {
    setHistory([])
    localStorage.removeItem('diras_history')
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>🛡️ DIRAS</h1>
          <p>Defence Intelligence Retrieval & Analysis System</p>
          <p className="subtitle">Ask questions about defence documents with AI-powered answers</p>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          <div className="layout">
            <div className="main-content">
              <QueryInterface onSearch={handleSearch} loading={loading} />
              
              {error && (
                <div className="error-banner">
                  <strong>⚠️ Error:</strong> {error}
                  <div className="error-hint">
                    Make sure the backend is running: <code>docker compose up -d</code>
                  </div>
                </div>
              )}

              {loading && (
                <div className="loading-container">
                  <div className="spinner"></div>
                  <p>Searching documents and generating answer...</p>
                </div>
              )}

              {results && !loading && <ResultsDisplay results={results} />}

              {!results && !loading && !error && (
                <div className="welcome-message">
                  <h2>Welcome to DIRAS 🎯</h2>
                  <p>Enter your query above to get started</p>
                  <div className="example-queries">
                    <h3>Example Questions:</h3>
                    <ul>
                      <li>What is the latest defence procurement policy?</li>
                      <li>Tell me about recent military expenditure</li>
                      <li>What are the key defence strategies?</li>
                      <li>Explain the parliamentary defence committee's recommendations</li>
                    </ul>
                  </div>
                </div>
              )}
            </div>

            {history.length > 0 && (
              <aside className="sidebar">
                <div className="history-panel">
                  <div className="history-header">
                    <h3>📋 Search History</h3>
                    <button
                      className="clear-btn"
                      onClick={clearHistory}
                      title="Clear history"
                    >
                      ✕
                    </button>
                  </div>
                  <div className="history-list">
                    {history.map((item, idx) => (
                      <button
                        key={idx}
                        className="history-item"
                        onClick={() => handleHistoryClick(item)}
                        title={item.query}
                      >
                        <div className="history-query">{item.query}</div>
                        <div className="history-time">{item.timestamp}</div>
                      </button>
                    ))}
                  </div>
                </div>
              </aside>
            )}
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>DIRAS v1.0 | Defence Intelligence Retrieval & Analysis System</p>
        <p className="footer-tech">Powered by FastAPI, React, ChromaDB, and Llama 3</p>
      </footer>
    </div>
  )
}

export default App
