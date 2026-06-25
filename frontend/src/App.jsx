
import { useState, useEffect } from 'react'
import QueryInterface from './components/QueryInterface'
import ResultsDisplay from './components/ResultsDisplay'
import './styles/App.css'

function App() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [history, setHistory] = useState([])

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
      const apiUrl = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

      const payload = {
        question: query,
        top_k: parseInt(topK),
      }

      if (docType) {
        payload.document_type = docType
      }

      const requestUrl = `${apiUrl}/api/v1/query`
      console.log('Request URL:', requestUrl)
      const response = await fetch(requestUrl, {
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

      const newHistoryItem = {
        query,
        timestamp: new Date().toLocaleString(),
        topK,
        docType,
      }

      const updatedHistory = [
        newHistoryItem,
        ...history,
      ].slice(0, 10)

      setHistory(updatedHistory)

      localStorage.setItem(
        'diras_history',
        JSON.stringify(updatedHistory)
      )
    } catch (err) {
      const msg = err && err.message ? `${err.message}` : String(err)
      setError(msg)
      console.error('Search request failed', err)
    } finally {
      setLoading(false)
    }
  }

  const handleHistoryClick = (item) => {
    handleSearch(
      item.query,
      item.topK,
      item.docType
    )
  }

  const clearHistory = () => {
    setHistory([])
    localStorage.removeItem('diras_history')
  }

  return (
    <div className="app">

      <header className="app-header">

        <div className="header-content">

          <h1>
            🛡️ DAPS
          </h1>

          <p>
            Defence Acquisition & Procurement System
          </p>

          <p className="subtitle">
            AI-Powered Defence Knowledge &
            Analysis Platform
          </p>

          <div
            style={{
              display: 'flex',
              gap: '12px',
              flexWrap: 'wrap',
              marginTop: '16px'
            }}
          >
            <span className="status-pill">
              🟢 Vector DB Online
            </span>

            <span className="status-pill">
              🟢 AI Ready
            </span>

            <span className="status-pill">
              📄 Defence Knowledge Base
            </span>
          </div>

        </div>

      </header>

      <main className="app-main">

        <div className="container">

          {/* DASHBOARD CARDS */}

          <div className="stats-grid">

            <div className="stat-card">
              <h3>Knowledge Base</h3>
              <span>Active</span>
            </div>

            <div className="stat-card">
              <h3>Search History</h3>
              <span>{history.length}</span>
            </div>

            <div className="stat-card">
              <h3>AI Status</h3>
              <span>Online</span>
            </div>

            <div className="stat-card">
              <h3>Platform</h3>
              <span>DIRAS</span>
            </div>

          </div>

          <div className="layout">

            <div className="main-content">

              <QueryInterface
                onSearch={handleSearch}
                loading={loading}
              />

              {error && (
                <div className="error-banner">

                  <strong>
                    ⚠️ Connection Error
                  </strong>

                  <div className="error-hint">
                    {error}
                  </div>

                </div>
              )}

              {loading && (
                <div className="loading-container">

                  <div className="spinner"></div>

                  <p>
                    Analyzing Defence
                    Knowledge Base...
                  </p>

                </div>
              )}

              {results && !loading && (
                <ResultsDisplay
                  results={results}
                />
              )}

              {!results &&
                !loading &&
                !error && (
                  <div className="welcome-message">

                    <h2>
                      Defence
                      Procurement Analytics Platform
                    </h2>

                    <p>
                      Search defence
                      procurement,
                      expenditure,
                      parliamentary reports,
                      DRDO research,
                      gazette notifications
                      and official
                      memorandums.
                    </p>

                    <div className="example-queries">

                      <h3>
                        Popular Queries
                      </h3>

                      <ul>
                        <li>
                          What is the latest
                          defence procurement
                          policy?
                        </li>

                        <li>
                          Explain defence
                          budget allocations.
                        </li>

                        <li>
                          What are DRDO's
                          latest initiatives?
                        </li>

                        <li>
                          Show recent
                          parliamentary
                          defence committee
                          recommendations.
                        </li>

                        <li>
                          Which authority
                          approves major
                          defence acquisitions?
                        </li>

                      </ul>

                    </div>

                  </div>
                )}

            </div>

            {history.length > 0 && (
              <aside className="sidebar">

                <div className="history-panel">

                  <div className="history-header">

                    <h3>
                      📋 Search History
                    </h3>

                    <button
                      className="clear-btn"
                      onClick={clearHistory}
                    >
                      ✕
                    </button>

                  </div>

                  <div className="history-list">

                    {history.map(
                      (item, idx) => (
                        <button
                          key={idx}
                          className="history-item"
                          onClick={() =>
                            handleHistoryClick(
                              item
                            )
                          }
                        >
                          <div className="history-query">
                            {item.query}
                          </div>

                          <div className="history-time">
                            {item.timestamp}
                          </div>
                        </button>
                      )
                    )}

                  </div>

                </div>

              </aside>
            )}

          </div>

        </div>

      </main>

    </div>
  )
}

export default App
