
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

  const getPromptTemplate = (query) => {
    const actualQuery = query || ''
    return `You are a Senior Defence Procurement and Acquisition Specialist.

You are an expert in:

• Defence Acquisition Procedure (DAP 2020)
• Defence Procurement Procedure (DPP)
• General Financial Rules (GFR)
• Delegation of Financial Powers
• Government Procurement
• Defence Budget
• Capital Acquisition
• Revenue Procurement
• Tendering
• Contract Management
• Indian Ministry of Defence Policies
• Public Procurement
• Financial Regulations

Answer the following question using your own knowledge.

Question:
${actualQuery}

Instructions:

1. Give a complete answer.

2. Answer in professional defence language.

3. Explain concepts clearly.

4. If applicable mention:
   - Relevant Rules
   - DAP Chapters
   - GFR Rules
   - Procurement Categories
   - Financial Authorities
   - Budget implications
   - Tender Process

5. Never hallucinate.
If uncertain, explicitly state it.

6. Use headings.

7. Use bullet points.

8. Include examples whenever helpful.

9. Never use "Based on the provided context."

10. Never mention you are an AI.

Return only the answer.`
  }

  const formatDebugValue = (value, key) => {
    if (value === undefined || value === null) return 'No data available.'
    if (key === 'promptSent') {
      return getPromptTemplate(results?.query || '')
    }
    if (typeof value === 'string') return value
    return JSON.stringify(value, null, 2)
  }

  const renderReportText = (text) => {
    if (!text) return null

    const lines = text.split(/\r?\n/)
    const result = []
    let bullets = []

    const flushBullets = (key) => {
      if (bullets.length === 0) return null
      const list = (
        <ul key={key} className="report-bullets">
          {bullets.map((item, idx) => (
            <li key={`${key}-${idx}`}>{item}</li>
          ))}
        </ul>
      )
      bullets = []
      return list
    }

    lines.forEach((line, index) => {
      const trimmed = line.trim()
      if (!trimmed) {
        const list = flushBullets(`flush-${index}`)
        if (list) result.push(list)
        return
      }

      const headingIcons = ['🏁', '🔑', '📅', '📚', '📊']
      const isHeading = headingIcons.some((icon) => trimmed.startsWith(icon))
      const markdownHeading = trimmed.match(/^(#{1,6})\s+(.*)$/)

      if (markdownHeading) {
        const list = flushBullets(`heading-${index}`)
        if (list) result.push(list)
        result.push(
          <h3 key={`heading-${index}`} className="report-heading">
            {markdownHeading[2]}
          </h3>
        )
        return
      }

      if (isHeading) {
        const list = flushBullets(`heading-${index}`)
        if (list) result.push(list)
        result.push(
          <h3 key={`heading-${index}`} className="report-heading">
            {trimmed}
          </h3>
        )
        return
      }

      const bulletMatch = trimmed.match(/^[•\-*\d\.]+\s+(.*)$/)
      if (bulletMatch) {
        bullets.push(bulletMatch[1])
        return
      }

      const list = flushBullets(`text-${index}`)
      if (list) result.push(list)
      result.push(
        <p key={`p-${index}`} className="report-paragraph">
          {trimmed}
        </p>
      )
    })

    const finalList = flushBullets('final')
    if (finalList) result.push(finalList)

    return result
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
          <pre>{formatDebugValue(value, key)}</pre>
        </div>
      </div>
    )
  }

  return (
    <div className="results-display">

      {/* Analysis Brief */}
      {results.answer && (
        <div className="answer-section">

          <div className="answer-header">
            <h2>🛡️ Analysis Brief</h2>

            <span
              className={`confidence-badge confidence-${getConfidenceClass(
                results.confidence
              )}`}
            >
              {formatConfidence(results.confidence)}% Confidence
            </span>
          </div>

          <div className="Analysis-banner">
            <strong>Analysis Summary</strong>
            <p>
              Information retrieved from the Defence Knowledge Base using
              semantic search, vector retrieval and AI-assisted analysis.
            </p>
          </div>

          <div className="answer-content">
            <div className="answer-text">{renderReportText(results.answer)}</div>
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
          <h3>📄 Analysis Sources ({results.sources.length})</h3>

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
        {renderDebugSection('finalAnswer', 'Final Analysis Report', results.final_answer || results.answer)}
      </div>

      {/* Related Analysis */}
      {results.related_documents &&
        results.related_documents.length > 0 && (
          <div className="related-section">

            <h3>🔍 Related Analysis </h3>

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
            No results found.
            Try rephrasing your query.
          </p>
        </div>
      )}

    </div>
  )
}

export default ResultsDisplay

