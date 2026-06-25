import { useState } from 'react'
import '../styles/QueryInterface.css'

function QueryInterface({ onSearch, loading }) {
  const [query, setQuery] = useState('')
  const [topK, setTopK] = useState('15')
  const [docType, setDocType] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim()) {
      onSearch(query, topK, docType)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div className="query-interface">
      <form onSubmit={handleSubmit} className="query-form">
        <div className="input-group">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask your question... (Press Enter to search, Shift+Enter for new line)"
            className="query-input"
            disabled={loading}
            rows="3"
          />
          <button
            type="submit"
            className="search-button"
            disabled={loading || !query.trim()}
          >
            {loading ? '⟳ Searching...' : '🔍 Search'}
          </button>
        </div>

        <div className="filters">
          <div className="filter-group">
            <label htmlFor="topK">Results to retrieve:</label>
            <select
              id="topK"
              value={topK}
              onChange={(e) => setTopK(e.target.value)}
              className="filter-select"
              disabled={loading}
            >
              <option value="3">Top 3</option>
              <option value="5">Top 5</option>
              <option value="10">Top 10</option>
              <option value="15">Top 15</option>
              <option value="20">Top 20</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="docType">Document type (optional):</label>
            <select
              id="docType"
              value={docType}
              onChange={(e) => setDocType(e.target.value)}
              className="filter-select"
              disabled={loading}
            >
              <option value="">All Types</option>
              <option value="press_release">Press Release</option>
              <option value="policy_document">Policy Document</option>
              <option value="procurement">Procurement</option>
              <option value="financial_report">Financial Report</option>
              <option value="parliamentary_report">Parliamentary Report</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="topK" style={{ visibility: 'hidden' }}>Placeholder</label>
            <button
              type="reset"
              className="reset-button"
              onClick={() => {
                setQuery('')
                setTopK('15')
                setDocType('')
              }}
              disabled={loading}
            >
              🔄 Clear
            </button>
          </div>
        </div>
      </form>
    </div>
  )
}

export default QueryInterface
