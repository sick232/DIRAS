
import { useState } from 'react'
import '../styles/ResultsDisplay.css'

function ResultsDisplay({ results }) {
  const [debugOpen, setDebugOpen] = useState({
    query: true,
    retrievedChunks: false,
    retrievedContext: false,
    promptSent: false,
    geminiOutput: false,
    groqOutput: false,
    grokOutput: false,
    fallbackOutput: false,
    finalAnswer: true
  })

  if (!results) return null

  const getConfidenceClass = (confidence) => {
    if (confidence >= 0.8) return 'high'
    if (confidence >= 0.6) return 'medium'
    return 'low'
  }

  const formatConfidence = (confidence) => {
    return ((confidence || 0.85) * 100).toFixed(0)
  }

  const toggleSection = (key) => {
    setDebugOpen((prev) => ({
      ...prev,
      [key]: !prev[key]
    }))
  }

  const formatDebugValue = (value) => {
    if (value === undefined || value === null) return 'No data available.'
    if (typeof value === 'string') return value
    return JSON.stringify(value, null, 2)
  }

  const debugChunksText = results.debug_chunks
    ? results.debug_chunks
        .map((chunk, idx) =>
          `Document: ${chunk.document}\nSimilarity: ${chunk.similarity?.toFixed(4)}\nText:\n${chunk.text}`
        )
        .join('\n\n---\n')
    : ''

  const renderDebugSection = (key, title, value) => {
    if (!value) return null
    return (
      <div className={`debug-card ${debugOpen[key] ? 'open' : ''}`}>
        <button
          type="button"
          className="debug-header"
          onClick={() => toggleSection(key)}
        >
          <span>{debugOpen[key] ? '▼' : '▶'} {title}</span>
          <span className="debug-toggle">
            {debugOpen[key] ? 'Hide' : 'Show'}
          </span>
        </button>

        <div className="debug-content">
          <pre>{formatDebugValue(value)}</pre>
        </div>
      </div>
    )
  }

  return (
    <div className="results-display">

      {/* Intelligence Brief */}
      {results.answer && (
        <div className="answer-section">

          <div className="answer-header">
            <h2>🛡️ Intelligence Brief</h2>

            <span
              className={`confidence-badge confidence-${getConfidenceClass(
                results.confidence
              )}`}
            >
              {formatConfidence(results.confidence)}% Confidence
            </span>
          </div>

          <div className="intelligence-banner">
            <strong>Analysis Summary</strong>
            <p>
              Information retrieved from the Defence Knowledge Base using
              semantic search, vector retrieval and AI-assisted analysis.
            </p>
          </div>

          <div className="answer-content">
            <p className="answer-text">{results.answer}</p>
          </div>

          <div className="metadata">
            {results.processing_time && (
              <div className="meta-item">
                <span className="meta-icon">⏱️</span>
                <span>
                  Response Time
                  <br />
                  <strong>{results.processing_time.toFixed(2)}s</strong>
                </span>
              </div>
            )}

            {results.documents_searched && (
              <div className="meta-item">
                <span className="meta-icon">📚</span>
                <span>
                  Documents
                  <br />
                  <strong>{results.documents_searched}</strong>
                </span>
              </div>
            )}

            {results.results_count && (
              <div className="meta-item">
                <span className="meta-icon">🎯</span>
                <span>
                  Results Found
                  <br />
                  <strong>{results.results_count}</strong>
                </span>
              </div>
            )}

            {results.model_used && (
              <div className="meta-item">
                <span className="meta-icon">🤖</span>
                <span>
                  AI Model
                  <br />
                  <strong>{results.model_used}</strong>
                </span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Sources */}
      {results.sources && results.sources.length > 0 && (
        <div className="sources-section">
          <h3>📄 Intelligence Sources ({results.sources.length})</h3>

          <div className="sources-list">
            {results.sources.map((source, idx) => (
              <div key={idx} className="source-item">

                <div className="source-number">
                  {idx + 1}
                </div>

                <div className="source-content">
                  <p className="source-text">
                    {typeof source === 'string'
                      ? source
                      : source.title || JSON.stringify(source)}
                  </p>

                  <div
                    style={{
                      marginTop: '10px',
                      display: 'flex',
                      gap: '10px',
                      flexWrap: 'wrap'
                    }}
                  >
                    <span className="source-link">
                      Defence Document
                    </span>

                    {source.url && (
                      <a
                        href={source.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="source-link"
                      >
                        View Source
                      </a>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Debug Visibility */}
      <div className="debug-section-container">
        {renderDebugSection('query', 'User Query', results.query)}
        {renderDebugSection('retrievedChunks', 'Retrieved Chunks', debugChunksText)}
        {renderDebugSection('retrievedContext', 'Retrieved Context', results.retrieved_context)}
        {renderDebugSection('promptSent', 'Prompt Sent To LLM', results.prompt_sent)}
        {renderDebugSection('geminiOutput', 'Gemini Output', results.gemini_raw_response)}
        {renderDebugSection('groqOutput', 'Groq Output', results.groq_raw_response)}
        {renderDebugSection('grokOutput', 'Grok Output', results.grok_raw_response)}
        {renderDebugSection('fallbackOutput', 'Fallback Output', results.fallback_raw_response)}
        {renderDebugSection('finalAnswer', 'Final Intelligence Report', results.final_answer || results.answer)}
      </div>

      {/* Related Intelligence */}
      {results.related_documents &&
        results.related_documents.length > 0 && (
          <div className="related-section">

            <h3>🔍 Related Intelligence</h3>

            <div className="related-list">
              {results.related_documents.map((doc, idx) => (
                <div key={idx} className="related-item">
                  <p>{doc}</p>
                </div>
              ))}
            </div>

          </div>
        )}

      {/* Sections */}
      {results.sections &&
        Array.isArray(results.sections) && (
          <div className="sections-container">

            {results.sections.map((section, idx) => (
              <div key={idx} className="section">

                {section.title && (
                  <h3>{section.title}</h3>
                )}

                <p>{section.content}</p>

              </div>
            ))}

          </div>
        )}

      {!results.answer && !results.sources && (
        <div className="no-results">
          <p>
            No intelligence results found.
            Try rephrasing your query.
          </p>
        </div>
      )}

    </div>
  )
}

export default ResultsDisplay

