# Workflows Overview

## DIRAS System Workflows

This document provides an overview of all major workflows in the system.

---

## 1. Data Collection & Ingestion Workflow

**Purpose**: Acquire documents from external sources

**Steps**:
1. Source monitoring (daily)
2. Document download
3. Duplicate detection
4. Validation checks
5. Metadata extraction
6. Storage

**Frequency**: Continuous (daily)
**Latency**: 1-7 days from publication to system
**Volume**: 50-100 documents/day

---

## 2. Preprocessing Workflow

**Purpose**: Clean and normalize text from OCR

**Steps**:
1. Text cleaning (regex-based)
2. Tokenization (sentence and word level)
3. Normalization (lowercase, standardization)
4. Lemmatization/stemming
5. Quality validation

**Frequency**: For each new document
**Processing Speed**: 5000+ documents/hour
**Output**: Normalized, tokenized text ready for analysis

---

## 3. Document Classification Workflow

**Purpose**: Categorize documents into 10 classes

**Steps**:
1. Feature extraction (TF-IDF or embeddings)
2. Primary classifier (Random Forest)
3. Confidence thresholding
4. Secondary classifier if needed (BERT)
5. Manual review for edge cases

**Accuracy Target**: >90%
**Processing Speed**: 2000+ documents/hour

---

## 4. Entity Extraction Workflow

**Purpose**: Extract structured information (authorities, dates, amounts)

**Steps**:
1. Named entity recognition (spaCy/BERT)
2. Entity linking (canonical forms)
3. Relationship extraction
4. Validation against knowledge base
5. Confidence scoring

**Coverage**: 8+ entity types
**F1-Score Target**: >85% overall

---

## 5. Embedding & Indexing Workflow

**Purpose**: Generate vectors and build searchable index

**Steps**:
1. Document chunking (384 tokens, 64-token overlap)
2. Embedding generation (SentenceTransformers)
3. Vector index storage (ChromaDB/FAISS)
4. Metadata storage
5. BM25 sparse index creation

**Throughput**: 3000+ documents/hour (CPU)
**Storage**: ~2-4 bytes per document

---

## 6. Query Processing Workflow

**Purpose**: Process user query and prepare for retrieval

**Steps**:
1. Query cleaning and normalization
2. Intent classification
3. Query expansion (synonyms)
4. Authority/financial query detection
5. Embedding generation
6. Prepared for retrieval

**Latency**: <100ms
**Output**: Query embedding + metadata

---

## 7. Retrieval & Ranking Workflow

**Purpose**: Find relevant documents for query

**Steps**:
1. Parallel retrieval:
   - Dense retrieval (vector similarity)
   - Sparse retrieval (BM25)
2. Hybrid fusion (Reciprocal Rank Fusion)
3. Cross-encoder reranking
4. Maximal marginal relevance (diversity)
5. Top-5 document selection

**Latency**: <200ms
**Quality Target**: Precision@5 >0.75

---

## 8. RAG & Answer Generation Workflow

**Purpose**: Generate answer grounded in retrieved documents

**Steps**:
1. Context assembly (top-5 documents)
2. Prompt construction (system + context + query)
3. LLM inference
4. Answer generation
5. Citation extraction
6. Confidence scoring
7. Hallucination detection

**Latency**: 1-5 seconds
**Faithfulness Target**: >95%

---

## 9. Financial Analysis Workflow

**Purpose**: Extract and analyse financial information

**Steps**:
1. Document filtering (financial documents)
2. Financial entity extraction (amounts, categories)
3. Temporal association (fiscal year)
4. Authority association
5. Amount normalization
6. Aggregation and analysis
7. Report generation

**Accuracy Target**: >95% for amounts

---

## 10. Authority Identification Workflow

**Purpose**: Map responsible departments and officers

**Steps**:
1. Authority name extraction (NER)
2. Canonical mapping
3. Hierarchy resolution
4. Relationship extraction
5. Responsibility mapping
6. Validation
7. Authority report generation

**Accuracy Target**: >90%

---

## 11. Monitoring & Quality Assurance Workflow

**Purpose**: Ensure system quality and detect issues

**Activities**:
- Daily: Monitor retrieval quality, LLM outputs
- Weekly: Analyze error logs, user feedback
- Monthly: Full quality assessment, benchmarking
- Quarterly: Performance review, optimization planning
- Annually: Comprehensive audit, strategic planning

---

## 12. System Maintenance Workflow

**Purpose**: Keep system running reliably

**Activities**:
- Daily: Backups, log analysis, security checks
- Weekly: Performance optimization, dependency updates
- Monthly: Model retraining if needed, infrastructure review
- Quarterly: Major updates, feature deployments
- Annually: Full system audit, infrastructure upgrade planning

---

## Workflow Orchestration

**How Workflows Connect**:

```
Incoming Documents
    ↓
[Collection] ← Daily trigger
    ↓
[Preprocessing] ← Auto-triggered
    ↓
[Classification] ← Auto-triggered
    ↓
[Entity Extraction] ← Auto-triggered
    ↓
[Embedding & Indexing] ← Auto-triggered
    ↓
Ready for Queries
    ↓
[Query Processing] ← User triggered
    ↓
[Retrieval & Ranking] ← Auto-triggered
    ↓
[RAG & Answer Generation] ← Auto-triggered
    ↓
├─[Financial Analysis] ← If financial query
├─[Authority Identification] ← If governance query
└─[Regular Response] ← Otherwise
    ↓
Answer to User
    ↓
[Monitoring & QA] ← Continuous
    ↓
[Maintenance] ← Scheduled
```

---

## Key Characteristics

**Automation**: 95% of workflows are fully automated
**Monitoring**: All workflows have metrics and alerts
**Error Handling**: Graceful degradation at each stage
**Scalability**: Workflows designed to scale to 1M+ documents
**Auditability**: Complete audit trail of all operations

---

*Last Updated: May 26, 2026*
