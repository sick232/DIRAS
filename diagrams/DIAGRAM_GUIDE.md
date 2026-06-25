# System Architecture Diagrams

## Mermaid Diagrams for DIRAS Architecture

---

## 1. High-Level System Architecture

```mermaid
graph TB
    subgraph Sources["Data Sources"]
        MOD["Ministry of Defence<br/>(mod.gov.in)"]
        DRDO["DRDO Public Reports<br/>(drdo.gov.in)"]
        Gazette["Gazette of India<br/>(egazette.gov.in)"]
        PIB["PIB Notices<br/>(pib.gov.in)"]
        Parliament["Parliamentary Reports<br/>(parliament.gov.in)"]
    end
    
    subgraph Ingestion["Data Ingestion Layer"]
        Scraper["Web Scrapers"]
        APIClient["API Clients"]
        DirectDL["Direct Download"]
        Validation["Validation & Dedup"]
    end
    
    subgraph Processing["Processing Pipeline"]
        OCR["OCR & Layout<br/>Analysis"]
        Preprocess["Text Preprocessing<br/>& Normalization"]
        Classification["Document<br/>Classification"]
        EntityExt["Entity Extraction<br/>(NER)"]
    end
    
    subgraph Analysis["Analysis & Storage"]
        Embeddings["Embedding<br/>Generation"]
        VectorDB["Vector Database<br/>(ChromaDB)"]
        BM25["BM25 Index<br/>(Sparse)"]
        DocStore["Document Store"]
    end
    
    subgraph Query["Query Processing"]
        QueryProc["Query<br/>Understanding"]
        DenseRet["Dense Retrieval<br/>(Vector Search)"]
        SparseRet["Sparse Retrieval<br/>(BM25)"]
        Fusion["Hybrid Fusion<br/>(RRF)"]
        Rerank["Cross-Encoder<br/>Reranking"]
    end
    
    subgraph Generation["Answer Generation"]
        Prompt["Prompt<br/>Construction"]
        LLM["LLM Inference"]
        FinAnalysis["Financial<br/>Analysis"]
        AuthID["Authority<br/>Identification"]
    end
    
    subgraph Output["Response"]
        Format["Response<br/>Formatting"]
        Citations["Citation<br/>Generation"]
        User["User Interface"]
    end
    
    MOD --> Scraper
    DRDO --> Scraper
    Gazette --> APIClient
    PIB --> APIClient
    Parliament --> DirectDL
    
    Scraper --> Validation
    APIClient --> Validation
    DirectDL --> Validation
    
    Validation --> OCR
    OCR --> Preprocess
    Preprocess --> Classification
    Classification --> EntityExt
    EntityExt --> Embeddings
    
    Embeddings --> VectorDB
    EntityExt --> BM25
    EntityExt --> DocStore
    
    QueryProc --> DenseRet
    QueryProc --> SparseRet
    
    DenseRet --> Fusion
    SparseRet --> Fusion
    Fusion --> Rerank
    
    Rerank --> Prompt
    Prompt --> LLM
    LLM --> FinAnalysis
    LLM --> AuthID
    
    FinAnalysis --> Format
    AuthID --> Format
    Format --> Citations
    Citations --> User
    
    style User fill:#90EE90
    style VectorDB fill:#FFB6C1
    style BM25 fill:#FFB6C1
    style DocStore fill:#FFB6C1
```

---

## 2. RAG Query Pipeline

```mermaid
sequenceDiagram
    actor User
    participant Query as Query<br/>Processing
    participant VecDB as Vector<br/>DB
    participant BM25 as BM25<br/>Index
    participant Rerank as Reranking
    participant LLM as LLM
    participant Response as Response<br/>Formatting
    
    User->>Query: Submit Query
    Query-->>Query: Normalize & Embed
    
    par Dense Retrieval
        Query->>VecDB: Query Embedding
        VecDB-->>Query: Top-50 Documents
    and Sparse Retrieval
        Query->>BM25: Tokenized Query
        BM25-->>Query: Top-50 Documents
    end
    
    Query->>Rerank: Combine Results (RRF)
    Rerank->>Rerank: Cross-Encoder Score
    Rerank-->>Rerank: Top-5 Documents
    
    Rerank->>LLM: Context + Query
    LLM->>LLM: Generate Answer
    LLM-->>Response: Answer + Citations
    
    Response->>Response: Format & Verify
    Response-->>User: Final Response
```

---

## 3. Document Processing Pipeline

```mermaid
graph LR
    A["Raw Document<br/>(PDF/Image/HTML)"]
    B["OCR & Layout<br/>Analysis"]
    C["Text Cleaning<br/>& Normalization"]
    D["Tokenization"]
    E["Lemmatization"]
    F["Entity Extraction"]
    G["Classification"]
    H["Chunking<br/>(384 tokens)"]
    I["Embedding<br/>Generation"]
    J["Vector Index"]
    K["BM25 Index"]
    L["Document Store"]
    
    A -->|scanned docs| B
    A -->|digital docs| C
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    H --> K
    I --> J
    F --> L
    G --> L
    
    style J fill:#FFB6C1
    style K fill:#FFB6C1
    style L fill:#E6E6FA
```

---

## 4. Entity Extraction & Authority Mapping

```mermaid
graph TB
    A["Document Text"]
    B["NER - Entity Recognition<br/>(spaCy/BERT)"]
    C["Authority Entities"]
    D["Financial Entities"]
    E["Other Entities"]
    F["Authority Linking<br/>(Canonical Mapping)"]
    G["Hierarchy Mapping"]
    H["Relationship Extraction"]
    I["Authority Report<br/>(Governance Mapping)"]
    
    A --> B
    B --> C
    B --> D
    B --> E
    C --> F
    F --> G
    G --> H
    H --> I
    
    style C fill:#FFB6C1
    style I fill:#90EE90
```

---

## 5. Financial Analysis Workflow

```mermaid
graph TB
    A["Financial Documents"]
    B["Financial Entity<br/>Extraction"]
    C["Amounts &<br/>Currencies"]
    D["Temporal<br/>Association"]
    E["Authority<br/>Association"]
    F["Amount<br/>Normalization"]
    G["Aggregation &<br/>Analysis"]
    H["Financial<br/>Intelligence Report"]
    
    A --> B
    B --> C
    B --> D
    B --> E
    C --> F
    F --> G
    D --> G
    E --> G
    G --> H
    
    style H fill:#90EE90
```

---

## 6. Embedding & Vector Search

```mermaid
graph TB
    subgraph Generation["Embedding Generation"]
        A["Document/Query Text"]
        B["Text Preparation<br/>(Cleaning & Chunking)"]
        C["Sentence Transformers<br/>(all-MiniLM-L6-v2)"]
        D["Vector Embedding<br/>(384 dimensions)"]
    end
    
    subgraph Storage["Vector Storage"]
        E["Vector Database<br/>(ChromaDB)"]
        F["Metadata Store<br/>(doc_id, chunk_id)"]
    end
    
    subgraph Retrieval["Similarity Search"]
        G["Query Embedding"]
        H["Cosine Similarity<br/>Calculation"]
        I["Top-K Selection<br/>(K=50)"]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    D --> F
    G --> H
    H --> I
    E -.->|search| I
    
    style E fill:#FFB6C1
    style F fill:#FFB6C1
```

---

## 7. Classification Hierarchy

```mermaid
graph TB
    A["Document Classification<br/>(10 Classes)"]
    
    A --> B["Financial<br/>(15%)"]
    A --> C["Procurement<br/>(20%)"]
    A --> D["Guidelines<br/>(15%)"]
    A --> E["Gazette<br/>(15%)"]
    A --> F["Memorandum<br/>(20%)"]
    A --> G["Technical<br/>(5%)"]
    A --> H["Administrative<br/>(5%)"]
    A --> I["Security<br/>(2%)"]
    A --> J["Budget<br/>(2%)"]
    A --> K["Tender<br/>(1%)"]
    
    style A fill:#87CEEB
    style B fill:#FFB6C1
    style C fill:#FFB6C1
    style E fill:#FFB6C1
    style F fill:#FFB6C1
```

---

## 8. Data Quality & Monitoring

```mermaid
graph TB
    A["Document Input"]
    B["Quality Checks"]
    C{Valid?}
    D["Processing Pipeline"]
    E["Quality Metrics"]
    F["Monitoring Dashboard"]
    G["Alert System"]
    
    H["Manual Review Queue<br/>(Low Confidence)"]
    
    A --> B
    B --> C
    C -->|Yes| D
    C -->|No| H
    D --> E
    E --> F
    F --> G
    G -->|Issue Detected| H
    
    style H fill:#FFD700
    style G fill:#FF6347
```

---

## 9. Scalability Architecture (Phase 4+)

```mermaid
graph TB
    subgraph Frontend["Load Balancer"]
        LB["API Gateway<br/>(Load Balanced)"]
    end
    
    subgraph Services["Microservices"]
        S1["Query Service<br/>(Replicated)"]
        S2["Retrieval Service<br/>(Replicated)"]
        S3["LLM Service<br/>(Replicated)"]
    end
    
    subgraph Storage["Distributed Storage"]
        VS["Vector DB<br/>(Distributed)"]
        BM["BM25 Shards<br/>(Multiple)"]
        DS["Document Store<br/>(Replicated)"]
    end
    
    subgraph Cache["Caching Layer"]
        QC["Query Cache"]
        RC["Response Cache"]
    end
    
    LB --> S1
    LB --> S2
    LB --> S3
    
    S1 --> QC
    S2 --> VS
    S2 --> BM
    S3 --> DS
    S2 --> RC
    
    style VS fill:#FFB6C1
    style BM fill:#FFB6C1
    style DS fill:#E6E6FA
```

---

## 10. Error Handling & Fallback Paths

```mermaid
graph TB
    A["Query Input"]
    B["Query Understanding"]
    C{Successful?}
    D["Dense Retrieval"]
    E{Success?}
    F["BM25 Fallback"]
    G["Reranking"]
    H{Top Results?}
    I["Return Best Effort<br/>+ Low Confidence"]
    J["LLM Inference"]
    K["Final Response"]
    
    A --> B
    B --> C
    C -->|No| I
    C -->|Yes| D
    D --> E
    E -->|No| F
    E -->|Yes| G
    F --> G
    G --> H
    H -->|No| I
    H -->|Yes| J
    J --> K
    I --> K
    
    style I fill:#FFD700
```

---

## Key Diagram Notes

1. **System Architecture**: Shows all major components and data flow
2. **RAG Pipeline**: Depicts query processing to response generation
3. **Processing Pipeline**: Document acquisition to indexing
4. **Entity Extraction**: Authority and relationship identification
5. **Financial Analysis**: Financial data extraction and analysis
6. **Embedding Pipeline**: Vector generation and storage
7. **Classification**: 10-class document categorization
8. **Monitoring**: Quality assurance and alerts
9. **Scalability**: Distributed architecture for Phase 4+
10. **Error Handling**: Fallback mechanisms for robustness

---

*Last Updated: May 26, 2026*
