import '../styles/ResultsDisplay.css'

function ResultsDisplay({ results }) {
  if (!results) return null

  const getConfidenceClass = (confidence) => {
    if (confidence >= 0.8) return 'high'
    if (confidence >= 0.6) return 'medium'
    return 'low'
  }

  const formatConfidence = (confidence) => {
    return ((confidence || 0.85) * 100).toFixed(0)
  }

  return (
    <div className="results-display">
      {/* Main Answer */}
      {results.answer && (
        <div className="answer-section">
          <div className="answer-header">
            <h2>📋 Answer</h2>
            <span className={`confidence-badge confidence-${getConfidenceClass(results.confidence)}`}>
              ✓ {formatConfidence(results.confidence)}% Confident
            </span>
          </div>
          <div className="answer-content">
            <p className="answer-text">{results.answer}</p>
          </div>

          {/* Metadata */}
          <div className="metadata">
            {results.processing_time && (
              <div className="meta-item">
                <span className="meta-icon">⏱️</span>
                <span>Response time: {results.processing_time.toFixed(2)}s</span>
              </div>
            )}
            {results.documents_searched && (
              <div className="meta-item">
                <span className="meta-icon">📚</span>
                <span>Documents searched: {results.documents_searched}</span>
              </div>
            )}
            {results.results_count && (
              <div className="meta-item">
                <span className="meta-icon">🎯</span>
                <span>Results found: {results.results_count}</span>
              </div>
            )}
            {results.model_used && (
              <div className="meta-item">
                <span className="meta-icon">🤖</span>
                <span>Model: {results.model_used}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Sources */}
      {results.sources && results.sources.length > 0 && (
        <div className="sources-section">
          <h3>📚 Source Documents ({results.sources.length})</h3>
          <div className="sources-list">
            {results.sources.map((source, idx) => (
              <div key={idx} className="source-item">
                <div className="source-number">{idx + 1}</div>
                <div className="source-content">
                  <p className="source-text">
                    {typeof source === 'string' ? source : source.title || JSON.stringify(source)}
                  </p>
                  {source.url && (
                    <a href={source.url} target="_blank" rel="noopener noreferrer" className="source-link">
                      View Document
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Related Information */}
      {results.related_documents && results.related_documents.length > 0 && (
        <div className="related-section">
          <h3>🔗 Related Documents</h3>
          <div className="related-list">
            {results.related_documents.map((doc, idx) => (
              <div key={idx} className="related-item">
                <p>{doc}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Sections for multi-part answers */}
      {results.sections && Array.isArray(results.sections) && (
        <div className="sections-container">
          {results.sections.map((section, idx) => (
            <div key={idx} className="section">
              {section.title && <h3>{section.title}</h3>}
              <p>{section.content}</p>
            </div>
          ))}
        </div>
      )}

      {/* Empty state */}
      {!results.answer && !results.sources && (
        <div className="no-results">
          <p>No results found. Try rephrasing your question.</p>
        </div>
      )}
    </div>
  )
}

export default ResultsDisplay
