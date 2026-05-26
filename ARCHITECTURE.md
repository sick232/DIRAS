# Complete System Architecture

## Defence Intelligence Retrieval and Analysis System (DIRAS)

**A comprehensive AI-powered RAG system for defence document intelligence**

---

## 1. Architecture Overview

### System Objectives
The DIRAS system transforms unstructured defence documents into intelligent, queryable knowledge assets through a multi-stage pipeline combining:
- **Document acquisition** from public defence sources
- **Advanced OCR and preprocessing** for text extraction
- **Semantic understanding** using embeddings and transformers
- **Intelligent retrieval** using hybrid search methods
- **Context-aware generation** using fine-tuned LLMs
- **Authority and financial intelligence** extraction

---

## 2. High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      INPUT SOURCES                                   │
│  MOD | DRDO | Gazette | PIB | Parliamentary | Procurement Portals   │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│               DATA COLLECTION & INGESTION LAYER                      │
│  • Web crawling and API integration                                 │
│  • Automated document discovery                                      │
│  • Metadata extraction (date, source, classification)                │
│  • Duplicate detection and deduplication                             │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│              OCR & DOCUMENT UNDERSTANDING LAYER                      │
│  • Scanned PDF processing                                           │
│  • Table and layout extraction                                       │
│  • Multi-language OCR (English, Hindi)                              │
│  • Confidence scoring and quality assessment                         │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│              PREPROCESSING & NORMALIZATION LAYER                     │
│  • Text cleaning (remove artifacts, normalize whitespace)            │
│  • Tokenization (word, sentence, paragraph-level)                   │
│  • Stopword removal and stemming/lemmatization                       │
│  • Duplicate detection at document level                             │
│  • Language identification and handling                              │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│            DOCUMENT CLASSIFICATION & ANNOTATION LAYER                │
│  • Classify documents into 10 categories                            │
│  • Named entity recognition (authorities, dates, amounts)            │
│  • Extract financial data and amounts                                │
│  • Identify responsible departments and officers                     │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│              SEMANTIC ENCODING & EMBEDDING LAYER                     │
│  • Generate dense embeddings for all documents                       │
│  • Chunk documents for granular retrieval                           │
│  • Create BM25 sparse indices for lexical search                    │
│  • Store metadata with vectors (authority, date, classification)    │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│           VECTOR DATABASE & INDEXING LAYER                           │
│  • Index embeddings in vector database                              │
│  • Maintain parallel sparse indices (BM25)                          │
│  • Configure for efficient similarity search                         │
│  • Enable metadata filtering for fine-grained retrieval              │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │ USER QUERY  │
                    └──────┬──────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│              QUERY UNDERSTANDING & PROCESSING LAYER                  │
│  • Intent detection (what type of query is this?)                   │
│  • Query expansion (find alternative phrasings)                      │
│  • Semantic rewriting (normalize to canonical form)                  │
│  • Multi-hop reasoning detection                                     │
│  • Financial/authority-specific query handling                       │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│            HYBRID RETRIEVAL & SEARCH LAYER                           │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ DENSE RETRIEVAL (Vector Search)                             │   │
│  │  - Convert query to embedding                               │   │
│  │  - Search vector database (FAISS/ChromaDB/Pinecone)         │   │
│  │  - Return top-K candidates (K=50)                           │   │
│  └──────────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ SPARSE RETRIEVAL (BM25)                                      │   │
│  │  - Tokenize query                                            │   │
│  │  - BM25 similarity scoring                                   │   │
│  │  - Return top-K candidates (K=50)                            │   │
│  │  - Complement dense retrieval with keyword matches           │   │
│  └──────────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ HYBRID FUSION                                                │   │
│  │  - Normalize scores from both retrievers                     │   │
│  │  - Reciprocal Rank Fusion (RRF)                              │   │
│  │  - Weighted combination based on query type                  │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│              RERANKING & CONTEXT SELECTION LAYER                     │
│  • Cross-encoder reranking (top-K candidates to top-5)              │
│  • Maximal Marginal Relevance (reduce redundancy)                   │
│  • Diversity scoring (ensure varied perspectives)                    │
│  • Semantic coherence checking                                       │
│  • Retrieve full document context                                    │
│  • Maximum context window assembly (e.g., 8K-16K tokens)            │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│              FINANCIAL INTELLIGENCE MODULE (Optional)                 │
│  • Extract monetary values, amounts, budget figures                  │
│  • Identify fund sources and allocation patterns                     │
│  • Link to responsible authorities                                   │
│  • Calculate aggregate statistics                                    │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│            AUTHORITY IDENTIFICATION MODULE (Optional)                 │
│  • Extract responsible departments and divisions                     │
│  • Identify approving and implementing authorities                    │
│  • Map to organizational hierarchy                                   │
│  • Associate with specific officials when mentioned                  │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│              RAG PROMPT & LLM REASONING LAYER                        │
│  • Construct RAG prompt with:                                       │
│    - System prompt (define role and constraints)                     │
│    - Retrieved context (most relevant documents)                     │
│    - User query (original question)                                  │
│    - Few-shot examples (if needed)                                   │
│  • Call LLM with assembled context                                   │
│  • LLM reasoning on defence-specific questions                       │
│  • Hallucination detection and mitigation                            │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│              RESPONSE GENERATION & FORMATTING LAYER                  │
│  • Generate natural language response                                │
│  • Format for readability                                            │
│  • Highlight key findings                                            │
│  • Generate source citations                                         │
│  • Confidence scoring                                                │
│  • Structured output (JSON for automated systems)                    │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                      OUTPUT GENERATION                               │
│  • Natural language answer with source attribution                   │
│  • Document references and excerpts                                  │
│  • Authority and responsibility mapping (if relevant)                │
│  • Financial data summaries (if applicable)                          │
│  • Confidence level indicator                                        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Modular Components Overview

### Component 1: Data Acquisition Layer
**Responsibility**: Collect documents from authoritative sources
- **Input**: URLs, APIs, search parameters
- **Output**: Raw documents with metadata
- **Key Technologies**:
  - Web crawlers (Scrapy, Selenium)
  - API clients (REST, GraphQL)
  - Scheduling (APScheduler, Celery)
  - Duplicate detection (SimHash, MinHash)

### Component 2: OCR & Text Extraction
**Responsibility**: Extract text from scanned PDFs and images
- **Input**: PDF files, image files
- **Output**: Clean text with layout preservation
- **Key Technologies**:
  - Tesseract, EasyOCR, PaddleOCR, LayoutParser
  - Table extraction (Camelot, Tabula)
  - Layout analysis

### Component 3: Preprocessing Pipeline
**Responsibility**: Clean and normalize extracted text
- **Input**: Raw text from OCR
- **Output**: Normalized, tokenized text
- **Operations**:
  - Text cleaning (special characters, artifacts)
  - Tokenization (sentence and word-level)
  - Normalization (lowercase, expand contractions)
  - Lemmatization/stemming
  - Stopword removal

### Component 4: Classification Engine
**Responsibility**: Categorize documents into 10 predefined classes
- **Output**: Document class + confidence score
- **Classes**: Financial, Procurement, Guidelines, Gazette, Memorandum, Technical, Administrative, Security, Budget, Tender
- **Algorithms**: SVM, Random Forest, BERT

### Component 5: Entity Extraction (NER)
**Responsibility**: Extract structured information from documents
- **Entity Types**:
  - Authority names and departments
  - Officer names
  - Dates and temporal expressions
  - Monetary values and amounts
  - Defence equipment and platforms
  - Organizations and locations
- **Methods**: SpaCy, BERT-NER, CRF, BiLSTM-CRF

### Component 6: Embedding Generation
**Responsibility**: Convert text to semantic vectors
- **Input**: Preprocessed text chunks
- **Output**: Dense vector embeddings
- **Models**: OpenAI, SentenceTransformers, BGE, E5
- **Chunk Strategy**: Sliding window with overlap for context preservation

### Component 7: Vector Database
**Responsibility**: Store and index embeddings for fast retrieval
- **Options**: FAISS, ChromaDB, Pinecone, Weaviate
- **Features**: 
  - Fast similarity search
  - Metadata filtering
  - Scalability to millions of vectors
  - Distributed search capability

### Component 8: Retrieval Engine
**Responsibility**: Find relevant documents for a given query
- **Methods**:
  - Dense retrieval (semantic similarity)
  - Sparse retrieval (BM25 keyword matching)
  - Hybrid fusion (combine both)
  - Reranking (cross-encoders, MMR)

### Component 9: RAG Pipeline
**Responsibility**: Combine retrieval with LLM reasoning
- **Flow**:
  1. Retrieve relevant documents
  2. Construct prompt with context
  3. Call LLM
  4. Post-process and format response

### Component 10: LLM Reasoning Engine
**Responsibility**: Generate answers using large language models
- **Capabilities**:
  - Semantic question understanding
  - Multi-hop reasoning
  - Factual grounding in retrieved context
  - Hallucination mitigation
- **Options**: GPT, Llama, Mistral, Gemini

### Component 11: Financial Analysis Module
**Responsibility**: Extract and analyze financial information
- **Capabilities**:
  - Monetary value extraction
  - Budget allocation tracking
  - Procurement cost analysis
  - Fund source identification

### Component 12: Authority Identification Module
**Responsibility**: Identify responsible departments and officials
- **Capabilities**:
  - NER for authorities
  - Organizational hierarchy mapping
  - Responsibility assignment
  - Relation extraction

---

## 4. Data Flow Architecture

### Document Ingestion Flow
```
Raw Document 
    ↓
OCR Extraction (if scanned)
    ↓
Text Cleaning & Normalization
    ↓
Tokenization
    ↓
Duplicate Detection
    ↓
Classification
    ↓
Entity Extraction
    ↓
Chunking & Embedding
    ↓
Vector Index Storage
    ↓
BM25 Index Storage
    ↓
Document Store (Full text + metadata)
```

### Query Processing Flow
```
User Query
    ↓
Intent Detection
    ↓
Query Expansion
    ↓
Dense Embedding Generation
    ↓
Parallel Search:
  ├─ Vector Search (FAISS)
  └─ BM25 Search (Sparse Index)
    ↓
Score Fusion (Reciprocal Rank Fusion)
    ↓
Cross-Encoder Reranking
    ↓
Context Assembly (Top-5 documents)
    ↓
Prompt Construction
    ↓
LLM Inference
    ↓
Response Generation & Formatting
    ↓
Output (with citations)
```

---

## 5. Query Processing Pipeline

### Stage 1: Query Understanding
**Input**: User query in natural language
**Operations**:
- Intent classification (search vs analysis vs comparison)
- Named entity recognition in query
- Authority/financial query detection
- Query expansion (synonyms, related terms)

**Output**: Structured query representation

### Stage 2: Semantic Embedding
**Operations**:
- Convert query to embedding using same model as documents
- Normalize embedding
- Add query metadata (intent, entities)

**Output**: Query vector + metadata

### Stage 3: Retrieval (Dual-Path)
**Path A - Dense Retrieval**:
- Search vector index with query embedding
- Return top-50 similar documents
- Compute cosine similarity scores

**Path B - Sparse Retrieval**:
- Tokenize query
- BM25 scoring against document index
- Return top-50 matching documents
- Compute BM25 scores

**Output**: Two ranked lists of candidates

### Stage 4: Hybrid Fusion
**Operations**:
- Normalize scores from both paths (0-1 range)
- Apply weighting based on query type
- Use Reciprocal Rank Fusion (RRF) to combine rankings
- Produce unified ranking of candidates

**Output**: Top-100 fused ranked documents

### Stage 5: Reranking
**Operations**:
- Load cross-encoder model
- Score top-100 documents with query
- Rank by cross-encoder score
- Apply Maximal Marginal Relevance (MMR) for diversity
- Select top-5 documents

**Output**: Top-5 most relevant documents with scores

### Stage 6: Context Assembly
**Operations**:
- Retrieve full document text for top-5
- Extract relevant passages
- Assemble into context window (e.g., 8K tokens)
- Add metadata (source, date, authority)
- Handle case where retrieved documents don't fit in context

**Output**: Assembled context + document metadata

### Stage 7: RAG Prompt Construction
**Components**:
```
SYSTEM PROMPT:
- Role definition (you are a defence intelligence assistant)
- Constraints (only use provided documents, flag uncertainty)
- Output format (natural language with citations)

RETRIEVED CONTEXT:
- Top-5 documents with full text
- Metadata (source, date, authority)
- Document boundaries clearly marked

USER QUERY:
- Original question
- Clarifications if needed

FEW-SHOT EXAMPLES (optional):
- Example Q&A pairs for complex queries
```

**Output**: Complete prompt ready for LLM

### Stage 8: LLM Reasoning
**Operations**:
- Send prompt to LLM (local or API)
- LLM reasons over retrieved context
- Generate answer grounded in documents
- Identify relevant sections
- Extract authority/financial info if applicable

**Output**: LLM-generated answer

### Stage 9: Response Formatting
**Operations**:
- Parse LLM response
- Extract citations and references
- Format for readability
- Add confidence indicators
- Structure JSON output (if needed)
- Highlight key findings

**Output**: Formatted response with citations

---

## 6. Component Interactions

### Embedding & Indexing Workflow
```
Documents → Preprocessing → Chunking → Embedding Model
                                              ↓
                                    Dense Vectors + Metadata
                                              ↓
                                  ┌─────────────────────┐
                                  │  Vector Database    │
                                  │  (FAISS/ChromaDB)   │
                                  └─────────────────────┘
                                              ↓
                                    Indexed for Fast Search
                                    
Parallel:
Documents → Tokenization → BM25 Index
                                ↓
                          Sparse Index Storage
```

### Retrieval Workflow
```
Query → Embedding → Vector Search (→ Top-50)
           ↓
        Tokenization → BM25 Search (→ Top-50)
           ↓
    Hybrid Fusion (RRF) → Top-100
           ↓
    Cross-Encoder Reranking → Top-5
           ↓
    Context Assembly → Full Documents
           ↓
    Prompt Construction → LLM Ready
```

### Authority Extraction Flow
```
Document Text
    ↓
Named Entity Recognition
    ↓
Authority Entity Detection
    ↓
Organizational Hierarchy Lookup
    ↓
Relationship Extraction
    ↓
Structured Authority Information
```

### Financial Analysis Flow
```
Document Text
    ↓
Financial NER (amounts, currencies)
    ↓
Pattern Matching (budget lines, allocations)
    ↓
Amount Extraction & Normalization
    ↓
Temporal Association (fiscal year, quarter)
    ↓
Authority Association
    ↓
Aggregation & Analysis
    ↓
Financial Intelligence Report
```

---

## 7. Scalability Considerations

### Scaling Dimensions

#### 1. Document Volume
- **Current**: 10K documents (planning stage)
- **Phase 2**: 100K documents
- **Phase 3**: 1M documents
- **Phase 4+**: 10M+ documents

**Scaling Strategy**:
- Vector DB sharding across multiple nodes
- Distributed embedding computation
- Batch processing pipelines
- Multi-partition BM25 indices

#### 2. Query Throughput
- **Target**: 100-1000 QPS (Queries Per Second)
- **Architecture**: Load balancing across query processors
- **Caching**: Cache popular queries and their results
- **Optimization**: Optimize embedding and retrieval latency

#### 3. Latency Requirements
- **Query embedding**: <100ms
- **Retrieval (dense + sparse)**: <200ms
- **Reranking**: <150ms
- **LLM inference**: 1-5s
- **Total system latency**: <6-7 seconds

#### 4. Storage Requirements
- **Document storage**: 100GB-500GB (with replicas)
- **Vector index**: 50GB-200GB (4TB for 100M docs)
- **BM25 index**: 10GB-50GB
- **Metadata storage**: 5GB-20GB

### Performance Optimization Strategies

**Retrieval Acceleration**:
- FAISS with GPU acceleration
- Quantized vectors (8-bit, binarized)
- Approximate nearest neighbor search
- Caching frequently accessed vectors

**LLM Optimization**:
- Model quantization (4-bit, 8-bit)
- Batch processing of queries
- Prompt caching
- Token-level sampling for faster generation

**Pipeline Optimization**:
- Asynchronous processing (embedding, classification)
- Batch processing where possible
- Lazy loading of documents
- Connection pooling for databases

---

## 8. Failure Modes & Resilience

### Potential Failure Points

#### 1. OCR Errors
- **Risk**: Incorrect text extraction from scanned PDFs
- **Mitigation**: Multiple OCR engines with voting, confidence thresholding, manual review queue

#### 2. Embedding Model Limitations
- **Risk**: Poor semantic representation of defence terminology
- **Mitigation**: Domain-specific fine-tuning, custom vocabulary, periodic retraining

#### 3. Hallucination in LLM Responses
- **Risk**: LLM generates plausible but false information
- **Mitigation**: Grounding in retrieved context, fact verification against sources, confidence scoring

#### 4. Retrieval Failure
- **Risk**: Relevant documents not retrieved
- **Mitigation**: Hybrid search (dense + sparse), query expansion, fallback methods

#### 5. Vector DB Outage
- **Risk**: Loss of semantic search capability
- **Mitigation**: Replicated indices, backup indices, fallback to sparse search

#### 6. LLM Service Unavailability
- **Risk**: Cannot generate responses
- **Mitigation**: Multiple LLM options, local model fallbacks, response caching

### Resilience Features

- **Redundancy**: Backup systems for critical components
- **Graceful Degradation**: Fall back to BM25 if vector search fails
- **Circuit Breakers**: Stop calling failing services
- **Monitoring**: Real-time health checks
- **Audit Logging**: Complete trace of all operations

---

## 9. Security Architecture

### Data Security
- **Encryption at Rest**: AES-256 for document storage
- **Encryption in Transit**: TLS 1.3 for all communications
- **Access Control**: Role-based access to documents and queries
- **Audit Logging**: Complete audit trail of all data access

### Model Security
- **Model Versioning**: Track all model versions and updates
- **Prompt Injection Prevention**: Validate user inputs
- **Model Monitoring**: Detect anomalous outputs
- **Bias Detection**: Regular fairness audits

### Infrastructure Security
- **Network Isolation**: Private networks for sensitive components
- **Authentication**: Multi-factor authentication for access
- **Intrusion Detection**: Monitor for suspicious activities
- **Compliance**: Adherence to MOD/DRDO security standards

---

## 10. Monitoring & Observability

### Metrics to Monitor

**System Health**:
- Query latency (p50, p95, p99)
- Throughput (queries per second)
- Error rates (retrieval failures, LLM errors)
- Service availability (uptime percentage)

**Retrieval Quality**:
- Precision@K, Recall@K
- MRR, NDCG scores
- CTR (Click-through rate on returned documents)
- User satisfaction ratings

**LLM Quality**:
- Hallucination rate
- Factual correctness score
- Citation accuracy
- User feedback ratings

**Resource Utilization**:
- CPU and memory usage
- Disk I/O and network bandwidth
- Vector DB query latency
- LLM API costs

### Logging & Tracing
- **Structured Logging**: JSON format for all logs
- **Distributed Tracing**: Track queries across components
- **Performance Profiling**: Identify bottlenecks
- **Error Tracking**: Capture and analyze exceptions

---

## 11. Testing Strategy

### Unit Testing
- Test individual components in isolation
- Mock external services
- Test edge cases and error conditions

### Integration Testing
- Test component interactions
- Test end-to-end workflows
- Test with real data (sanitized)

### Performance Testing
- Latency benchmarks
- Throughput testing
- Scalability under load
- Memory profiling

### Quality Testing
- Retrieval quality evaluation
- RAG answer quality assessment
- Hallucination detection
- Entity extraction accuracy

---

## 12. Deployment Architecture

### Staging Environments
- **Development**: Single-machine setup for development
- **Staging**: Production-like environment for testing
- **Production**: Scaled, hardened, monitored system

### Containerization
- Docker containers for all services
- Docker Compose for local development
- Kubernetes for production orchestration

### Infrastructure
- **Compute**: CPU for embeddings, GPU for optional LLM acceleration
- **Storage**: Object storage for documents, databases for indices
- **Networking**: Load balancing, service mesh for microservices

---

## Next Steps

1. **Deep Dive into Modules**: Read individual research modules for detailed algorithm comparisons
2. **Explore Workflows**: Review workflow documentation for process flows
3. **Check Evaluation Framework**: Understand metrics and benchmarking strategies
4. **Review Implementation Roadmap**: See planned development phases
5. **Study Use Cases**: Understand specific defence applications

See [RESEARCH_ROADMAP.md](../RESEARCH_ROADMAP.md) for implementation phases and timeline.
