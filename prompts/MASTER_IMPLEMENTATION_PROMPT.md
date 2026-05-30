# DIRAS Phase 2 Master Implementation Prompt

**For: GitHub Copilot Chat in VS Code**  
**Duration**: 16 weeks (8 sprints × 2 weeks)  
**Team**: 12 engineers  
**Approach**: Copy-paste into Copilot Chat; follow step-by-step guidance  
**Date**: June 1 - September 30, 2026

---

## 🎯 Mission Statement

You are building **DIRAS (Defence Intelligence Retrieval and Analysis System)** - an AI-powered Retrieval-Augmented Generation (RAG) system for the Ministry of Defence India.

This document provides a **comprehensive Phase 2 implementation roadmap** to transform research (Phase 1, 78% complete) into production-ready code.

**Success Definition**: By end of Phase 2 (Oct 2026):
- 5,000+ documents indexed with OCR accuracy ≥88%
- Document classification F1 ≥0.88 (10 document types)
- Entity extraction F1 ≥0.82 (authorities, amounts, dates)
- Hybrid retrieval precision ≥0.75 with latency <150ms
- RAG pipeline generating factually accurate answers (hallucination ≤8%)
- 5 real-world scenarios validated in UAT (80%+ pass rate)

---

## 📋 Phase 2 Architecture Overview

### System Components

```
User Query
    ↓
Query Understanding → Intent classification + expansion
    ↓
Retrieval (Dual Path)
├─ Dense: Embeddings (SentenceTransformers) → ChromaDB
└─ Sparse: BM25 tokenized search → Elasticsearch
    ↓
Fusion Layer (Reciprocal Rank Fusion)
    ↓
Reranking (Cross-Encoder)
    ↓
RAG Pipeline
├─ Context compression
├─ Prompt construction
└─ LLM inference (OpenAI/Llama)
    ↓
Post-Processing
├─ Hallucination detection
├─ Citation extraction
└─ Financial/Authority annotation
    ↓
API Response / Web UI
```

### Tech Stack (Validated from Phase 1 Research)

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Data Ingestion** | Scrapy, Selenium | Scrape 5 MoD sources (Gazette, PIB, DRDO) |
| **OCR** | EasyOCR + LayoutParser | 88-94% accuracy, Hindi support |
| **Preprocessing** | NLTK + spaCy | Fast, accurate lemmatization |
| **Classification** | Random Forest + BERT | Production-ready + confidence-aware |
| **NER** | spaCy + BERT fine-tune | Dual models for speed + accuracy |
| **Embeddings** | SentenceTransformers (all-MiniLM) | Free, 2-5K embeds/hr, 384 dimensions |
| **Vector DB** | ChromaDB | 1M capacity, dynamic indexing, Phase 2-3 |
| **Sparse Search** | BM25 (Elasticsearch) | Fast keyword search + term matching |
| **Reranking** | Cross-Encoder (ms-marco-MiniLM) | Rank top-50 → top-5 accurately |
| **RAG** | LangChain | Orchestrate retrieval → prompt → LLM |
| **LLM** | OpenAI GPT-3.5 or Llama 3 70B | Speed vs. Cost (trade-off decision) |
| **Backend** | FastAPI + Python 3.10 | REST API, async, OpenAPI docs |
| **Orchestration** | Docker + Docker-Compose | Local Phase 2, Kubernetes Phase 4 |
| **CI/CD** | GitHub Actions | Auto-test, auto-deploy to staging |
| **Monitoring** | Prometheus + Grafana | Metrics: OCR%, F1 scores, latency |

---

## 📂 Repository Structure

```
/diras
├── /data
│   ├── /raw                    # Downloaded documents
│   ├── /processed              # OCR'd, preprocessed docs
│   ├── /golden-dataset         # 960 docs for evaluation
│   ├── /embeddings             # Document vectors
│   └── /backup                 # S3 backups
│
├── /src
│   ├── /01-data-pipeline       # Scrapers + OCR
│   ├── /02-preprocessing       # Tokenization + cleaning
│   ├── /03-classification      # Doc classifier + training
│   ├── /04-ner                 # NER extraction + linking
│   ├── /05-embeddings          # Vector generation
│   ├── /06-retrieval           # BM25 + dense + fusion
│   ├── /07-rag                 # LangChain + prompt
│   ├── /08-financial           # Financial extraction
│   ├── /09-authority           # Authority hierarchy
│   ├── /10-api                 # FastAPI server
│   ├── /11-cli                 # Command-line tools
│   ├── /12-evaluation          # Test framework
│   └── /shared                 # Utils, config, constants
│
├── /docs
│   ├── /architecture           # Design decisions
│   ├── /api                    # API documentation
│   └── /deployment             # DevOps guides
│
├── /tests
│   ├── /unit                   # Module-level tests
│   ├── /integration            # End-to-end tests
│   └── /uat                    # User acceptance tests
│
├── /models
│   ├── /classification         # Trained classifiers
│   ├── /ner                    # NER models
│   └── /embeddings             # Embedding weights (cache)
│
├── /notebooks
│   ├── 01-data-exploration.ipynb
│   ├── 02-ocr-accuracy.ipynb
│   ├── 03-classification-training.ipynb
│   ├── 04-retrieval-metrics.ipynb
│   └── 05-evaluation-dashboard.ipynb
│
├── docker-compose.yml          # Local dev environment
├── Dockerfile                  # Application container
├── requirements.txt            # Python dependencies
├── .github/workflows/          # CI/CD pipelines
├── README.md                   # Quick start guide
└── PHASE_2_IMPLEMENTATION_CHECKLIST.md
```

---

## 🔄 Development Workflow

### How to Use This Prompt

1. **Read entire prompt** (5 min)
2. **Clone repository** + setup environment (see Setup section)
3. **Start with Sprint 1** (follow sprint prompts below)
4. **Daily standup**: What did I do? What will I do? Blockers?
5. **Each task**: Write test first → implement → merge
6. **Sprint end**: Demo to team + retrospective

### Copilot Usage Pattern

**Ideal Workflow**:
```
1. Open Copilot Chat (Cmd+Shift+I on Mac, Ctrl+Shift+I on Windows)
2. Paste task description from appropriate section below
3. Follow Copilot's step-by-step guidance
4. For each code suggestion:
   - Understand before copying
   - Ask clarifying questions
   - Test immediately
5. When stuck: Re-read research module (referenced below)
```

**Anti-Pattern** (Avoid):
❌ Copy-pasting entire code files without understanding  
❌ Building entire features without tests  
❌ Skipping documentation/comments  
❌ Ignoring Phase 1 research (context matters!)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+ (check: `python --version`)
- Git (check: `git --version`)
- Docker + Docker-Compose (check: `docker --version`)
- Conda or venv (for Python environment)

### Setup (30 min)

```bash
# Clone repo (or create from scratch)
git clone https://github.com/your-org/diras.git
cd diras

# Create Python environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p data/{raw,processed,golden-dataset,embeddings,backup}
mkdir -p models/{classification,ner,embeddings}

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys (OpenAI, HuggingFace, etc.)

# Start development services
docker-compose up -d  # ChromaDB, Elasticsearch, Grafana

# Run sanity checks
python -m pytest tests/unit/test_imports.py -v

# If all green: ✅ Ready to code!
```

---

## 📅 Sprint-by-Sprint Breakdown

### Sprint 1 (Weeks 1-2): Project Initialization & Environment

**Goal**: Team onboarded, dev environment operational, first code merged

**What to Do**:
1. **Team Onboarding** (Day 1-2)
   - Run DIRAS 2-week bootcamp curriculum (see TEAM_STRUCTURE.md)
   - Topics: Architecture, technology stack, code standards
   - Outcome: Team understands system design + why Phase 1 choices made

2. **CI/CD Setup** (Day 2-3)
   - Create GitHub Actions workflow: `.github/workflows/test.yml`
   - Auto-run tests on every push
   - Deploy staging on merge to `develop` branch
   - Outcome: Any code can be auto-tested + auto-deployed

3. **Repository Structure** (Day 3)
   - Create `/src/01-data-pipeline`, `/src/02-preprocessing`, etc.
   - Create `/tests/unit` and `/tests/integration` directories
   - Add README.md + CONTRIBUTING.md
   - Outcome: Clear folder structure, team coordination

4. **Docker Environment** (Day 4-5)
   - Write Dockerfile for Python app
   - Write docker-compose.yml with ChromaDB, Elasticsearch, Grafana
   - All team members can `docker-compose up` and run system
   - Outcome: Reproducible dev environment (no "works on my machine")

5. **First Merge** (Day 5)
   - Everyone creates a branch + commits dummy code
   - Code review + merge to main
   - Verify CI/CD runs automatically
   - Outcome: Git workflow proven, no fear of breaking main

**Deliverables**:
- ✅ All 12 engineers onboarded, notebooks ready
- ✅ CI/CD pipeline green (auto-run tests)
- ✅ Docker environment reproducible (all can run locally)
- ✅ First PR merged to main
- ✅ Team documentation (standards, deployment guide)

**Copilot Prompt for Sprint 1**:
> "Create a GitHub Actions CI/CD workflow for a Python FastAPI + ML project. Requirements: (1) Auto-run pytest on push, (2) Build Docker image on merge to develop, (3) Deploy to staging server. Here's my current repo structure: [paste structure from above]. How should I set up GitHub Actions?"

---

### Sprint 2 (Weeks 3-4): Data Pipeline Foundation

**Goal**: 5,000 documents collected + OCR baseline established

**What to Do**:
1. **Document Collection Setup** (Week 1)
   - Write Scrapy spider for Ministry of Defence website
   - Write Scrapy spider for Gazette of India
   - Write Scrapy spider for PIB (Press Information Bureau)
   - Add duplicate detection (URL + content hash)
   - Outcome: 3-5 sources, 2,000-3,000 documents

2. **OCR Pipeline** (Week 1-2)
   - Implement EasyOCR integration (handles images + PDFs)
   - Add LayoutParser for complex layouts (multi-column, tables)
   - Create preprocessing: remove noise, normalize text
   - Log OCR accuracy metrics (character accuracy, word accuracy)
   - Outcome: 5,000 documents OCR'd, accuracy ≥88%

3. **Quality Validation** (Week 2)
   - Test OCR on different document types (financial, gazette, etc.)
   - Measure accuracy per source (identify problem sources)
   - Create data quality dashboard (Grafana visualization)
   - Outcome: Confidence in data quality before downstream processing

**Phase 1 Research Reference**: See `/modules/01-dataset-collection/RESEARCH.md` + `/modules/02-ocr-document-understanding/RESEARCH.md` for technology choices

**Deliverables**:
- ✅ 5,000 documents collected + stored
- ✅ EasyOCR + LayoutParser operational
- ✅ OCR accuracy ≥88% (character + word level)
- ✅ Data quality dashboard (Grafana)
- ✅ Automated data pipeline (can run daily)

**Copilot Prompt for Sprint 2**:
> "I need to build a Scrapy spider to scrape PDF documents from [URL]. Each document has: title, publication date, content (text + tables). I need to: (1) Extract PDF links, (2) Download PDFs to /data/raw/, (3) Handle duplicates, (4) Log errors. Here's the site structure: [describe site]. What's the step-by-step approach?"

---

### Sprint 3 (Weeks 5-6): Text Processing & Classification

**Goal**: Document classifier F1 ≥0.88, preprocessing pipeline operational

**What to Do**:
1. **Preprocessing Pipeline** (Week 1)
   - Tokenization (spaCy)
   - Lemmatization (spaCy neural models)
   - Remove stopwords + normalize
   - Measure information loss (<2% target)
   - Outcome: Clean text ready for ML

2. **Classification Training Data** (Week 1-2)
   - Annotate 3,000 documents across 10 types:
     - Financial (500 docs)
     - Memorandum (500 docs)
     - Gazette (400 docs)
     - Guidelines (400 docs)
     - Procurement (300 docs)
     - Technical (300 docs)
     - Administrative (200 docs)
     - Security (200 docs)
     - Tender (100 docs)
     - Other (100 docs)
   - Use Label Studio (open-source annotation tool)
   - Outcome: Balanced dataset with 3K annotations

3. **Classification Baseline** (Week 2)
   - Train Logistic Regression (baseline)
   - Train Random Forest (production candidate)
   - Evaluate on test set (stratified split, 80/20)
   - Target: Accuracy ≥90%, F1 ≥0.88
   - Outcome: Production-ready classifier

**Phase 1 Reference**: `/modules/04-document-classification/RESEARCH.md`

**Deliverables**:
- ✅ Preprocessing pipeline v1 (<2% info loss)
- ✅ Classification training data (3,000 annotated)
- ✅ Random Forest classifier (F1 ≥0.88)
- ✅ Classification API endpoint

**Copilot Prompt for Sprint 3**:
> "Build a document classification pipeline in Python. Steps: (1) Load 3000 annotated documents from CSV, (2) Preprocess (tokenize, lemmatize, remove stopwords), (3) Vectorize (TF-IDF), (4) Train Random Forest, (5) Evaluate (accuracy, F1, per-class metrics), (6) Save model to disk. Libraries: spaCy, scikit-learn. What's the implementation?"

---

### Sprint 4 (Weeks 7-8): Named Entity Recognition

**Goal**: NER F1 ≥0.82, Authority knowledge base created

**What to Do**:
1. **NER Training Data** (Week 1)
   - Annotate 5,000+ entities across types:
     - Authority (1,500 entities: ministry names, departments)
     - Monetary (1,500 entities: amounts in ₹, USD, etc.)
     - Dates (1,000 entities: various formats)
     - Location (500 entities: place names)
     - Equipment (300 entities: military equipment)
     - Officer/Rank (600 entities: positions)
     - Policy/Law (500 entities: act names, rules)
   - Use BIO tagging format (Beginning, Inside, Outside)
   - Outcome: Quality NER training set

2. **spaCy NER Training** (Week 1-2)
   - Train spaCy NER on annotated data
   - Target: F1 ≥0.80
   - Evaluate per entity type (see BASELINE_METRICS.md)
   - Outcome: Fast production-ready NER

3. **BERT NER Fine-tuning** (Week 2)
   - Fine-tune BERT on same dataset
   - Target: F1 ≥0.82+ (better than spaCy)
   - Create ensemble: spaCy (fast) + BERT (accurate, use if confident >0.85)
   - Outcome: High-accuracy NER with fallback

4. **Authority Knowledge Base** (Week 2)
   - Extract all authorities mentioned in documents
   - Build manual mapping: Authority Name → Official Designation → Parent Organization
   - Create knowledge graph (or simple JSON)
   - Outcome: Authority hierarchy for queries

**Phase 1 Reference**: `/modules/05-entity-extraction/RESEARCH.md`

**Deliverables**:
- ✅ NER training dataset (5K+ entities)
- ✅ spaCy NER model (F1 ≥0.80)
- ✅ BERT NER fine-tuning (F1 ≥0.82)
- ✅ Authority knowledge base v1
- ✅ NER API endpoint

---

### Sprint 5 (Weeks 9-10): Embeddings & Vector Database

**Goal**: Retrieval P@10 ≥0.75, latency <150ms

**What to Do**:
1. **Embedding Model Selection** (Week 1)
   - Test SentenceTransformers (all-MiniLM-L6-v2) on 500 document pairs
   - Measure semantic correlation with manual similarity scores
   - Target: Pearson correlation ≥0.75
   - Outcome: Validated embedding model

2. **Batch Embedding Generation** (Week 1-2)
   - Embed all 5,000+ documents
   - Generate 384-dim vectors (SentenceTransformers)
   - Store in ChromaDB with metadata (doc_id, title, source)
   - Outcome: All docs searchable by semantic similarity

3. **BM25 Index** (Week 1-2)
   - Create inverted index (Elasticsearch or simple Python implementation)
   - Index tokenized text for keyword search
   - Outcome: Fast keyword-based retrieval

4. **Hybrid Retrieval** (Week 2)
   - Implement Reciprocal Rank Fusion (RRF)
   - Retrieve top-50 from dense (ChromaDB)
   - Retrieve top-50 from sparse (BM25)
   - Fuse rankings: combined_score = dense_score * 0.6 + sparse_score * 0.4
   - Return top-10 merged results
   - Outcome: Better precision than either alone

5. **Retrieval Evaluation** (Week 2)
   - Test on benchmark queries (100-200 from Phase 1)
   - Measure: Precision@10, Recall@50, MRR, latency p95
   - Target: P@10 ≥0.75, <150ms latency
   - Outcome: Quality metrics meet UAT requirements

**Phase 1 Reference**: `/modules/06-embeddings/RESEARCH.md`, `/modules/07-vector-database/RESEARCH.md`, `/modules/08-retrieval-algorithms/RESEARCH.md`

**Deliverables**:
- ✅ SentenceTransformers embedding model
- ✅ 5,000+ docs embedded in ChromaDB
- ✅ BM25 index operational
- ✅ Hybrid retrieval (dense + sparse + RRF)
- ✅ Retrieval metrics dashboard
- ✅ <150ms p95 latency

**Copilot Prompt for Sprint 5**:
> "Build a hybrid retrieval system combining dense (embeddings) + sparse (BM25) search. Steps: (1) Load SentenceTransformers embedding model, (2) Embed 5000 documents, store in ChromaDB, (3) Create BM25 inverted index, (4) Implement Reciprocal Rank Fusion to fuse top-50 from each, (5) Return merged top-10. Libraries: sentence-transformers, chromadb, elasticsearch (or simple BM25). Show the implementation."

---

### Sprint 6 (Weeks 11-12): RAG Pipeline & LLM Integration

**Goal**: RAG operational, hallucination ≤8%, faithfulness ≥0.90

**What to Do**:
1. **RAG Architecture** (Week 1)
   - Design: Query → Retrieval → Context Compression → Prompt → LLM → Response
   - Implement using LangChain (orchestration library)
   - Outcome: Modular, testable RAG

2. **LLM Integration** (Week 1-2)
   - Decision: OpenAI GPT-3.5-turbo (cost ≈ ₹2-3 per query) OR Llama 3 70B self-hosted
   - Option A (OpenAI): Use OpenAI API, track tokens
   - Option B (Llama): Deploy Llama 3 70B locally (requires GPU)
   - Start with OpenAI for simplicity, decide by Sprint 6 end
   - Outcome: LLM calling working

3. **Prompt Engineering** (Week 1-2)
   - Design system prompt + user template
   - Example template:
     ```
     System: You are a Defence Intelligence Analyst...
     User: [Question]
     Context: [Top-5 retrieved documents]
     Answer the question using ONLY the provided context.
     If context doesn't answer, say "I don't have information."
     ```
   - Test on 50 queries, measure hallucination rate
   - Outcome: Low-hallucination responses

4. **Response Post-Processing** (Week 2)
   - Extract citations (which documents were cited)
   - Detect hallucinations (fact-check against context using LLM)
   - Add confidence scores to responses
   - Outcome: Trustworthy, cited answers

5. **Evaluation** (Week 2)
   - Test on 100 benchmark queries
   - Measure: Hallucination rate, faithfulness (Ragas), relevance
   - Target: Hallucination ≤8%, Faithfulness ≥0.90
   - Outcome: Baseline established

**Phase 1 Reference**: `/modules/09-rag-architecture/RESEARCH.md`, `/modules/10-llm-research/RESEARCH.md`

**Deliverables**:
- ✅ RAG pipeline operational (retrieval → LLM → response)
- ✅ LLM integrated (OpenAI or Llama)
- ✅ Prompt templates engineered + tested
- ✅ Response post-processing (citations, hallucination detection)
- ✅ Evaluation framework (Ragas metrics)
- ✅ Baseline: Hallucination ≤8%, Faithfulness ≥0.90

---

### Sprint 7 (Weeks 13-14): Specialized Modules & Integration

**Goal**: Financial + Authority modules working, full system integrated

**What to Do**:
1. **Financial Analysis Module** (Week 1-2)
   - Extract monetary values + units (₹ vs USD)
   - Normalize amounts (₹5000 = 5000, not 5,00,0)
   - Identify spending categories (salary, equipment, misc.)
   - Map to approving authorities
   - Create financial summary reports
   - Outcome: Financial queries answerable

2. **Authority Identification Module** (Week 1-2)
   - Extract authority relationships (reports-to, approves, etc.)
   - Build approval chain lookup (can authority X approve amount Y?)
   - Implement delegation rules
   - Outcome: Authority queries answerable

3. **End-to-End Integration** (Week 2)
   - All modules (OCR, classification, NER, embeddings, retrieval, RAG, financial, authority) work together
   - Query → Route to correct module → Answer
   - Outcome: Full system working

4. **Integration Testing** (Week 2)
   - Write integration tests covering all modules
   - Test end-to-end: Query in → Answer out
   - Measure overall latency, accuracy
   - Outcome: High confidence in system

**Phase 1 Reference**: `/modules/11-financial-analysis/RESEARCH.md`, `/modules/12-authority-identification/RESEARCH.md`

**Deliverables**:
- ✅ Financial extraction + analysis working
- ✅ Authority identification + hierarchy working
- ✅ All modules integrated
- ✅ Integration test suite passing
- ✅ End-to-end system latency <2s

---

### Sprint 8 (Weeks 15-16): Testing & UAT Preparation

**Goal**: Ready for User Acceptance Testing, all baseline metrics established

**What to Do**:
1. **Golden Dataset Finalization** (Week 1)
   - Collect 960 hand-curated test documents
   - Annotate with ground truth (correct answers for evaluation)
   - Achieve inter-annotator agreement κ ≥0.80
   - Outcome: Gold-standard evaluation set

2. **Benchmark Query Set** (Week 1)
   - Create 200 queries across all use cases
   - Verify expected answers against golden dataset
   - Difficulty distribution: 30% easy, 50% medium, 20% hard
   - Outcome: Reproducible retrieval + RAG evaluation

3. **Evaluation Framework** (Week 1-2)
   - Implement Ragas metrics (hallucination, faithfulness, relevance)
   - Create metric dashboards (Grafana)
   - Automate weekly metric runs
   - Outcome: Weekly metric tracking

4. **Performance Profiling** (Week 2)
   - Measure latency: Query → Answer (p50, p95, p99)
   - Measure resource usage (CPU, memory, GPU)
   - Identify bottlenecks
   - Optimize: Target 20% latency improvement
   - Outcome: <2s p95 latency

5. **UAT Environment Setup** (Week 2)
   - Clone production environment (separate from dev)
   - Prepare for 5-10 real users
   - Create user training materials
   - Schedule UAT: 2-3 weeks (see UAT_STRATEGY.md)
   - Outcome: Ready for stakeholder testing

6. **System Test Suite** (Week 2)
   - Unit tests: Each module (classification, NER, retrieval, etc.)
   - Integration tests: End-to-end workflows
   - UAT tests: Real-world scenarios from 5 stakeholders
   - Target: 95%+ pass rate
   - Outcome: High confidence in system

**Phase 1 Reference**: `/evaluation/TEST_DATASET_STRATEGY.md`, `/benchmarking/BASELINE_METRICS.md`

**Deliverables**:
- ✅ 960-doc golden dataset annotated + validated
- ✅ 200-query benchmark set with expected answers
- ✅ Evaluation framework operational (Ragas + custom metrics)
- ✅ Weekly metric dashboards (Grafana)
- ✅ System test suite 95%+ passing
- ✅ UAT environment ready
- ✅ Phase 2 complete, ready for Phase 3

---

## 🎓 Key Learning References (From Phase 1 Research)

| Task | Research Module | Key Insight |
|------|-----------------|------------|
| Document collection | `/modules/01-dataset-collection/RESEARCH.md` | Public sources only (ethical compliance) |
| OCR accuracy | `/modules/02-ocr-document-understanding/RESEARCH.md` | EasyOCR (88-94%) beats alternatives |
| Preprocessing | `/modules/03-preprocessing-pipeline/RESEARCH.md` | Lemmatization >stemming; <2% info loss |
| Classification | `/modules/04-document-classification/RESEARCH.md` | Random Forest practical, BERT for ensemble |
| NER | `/modules/05-entity-extraction/RESEARCH.md` | spaCy (speed) + BERT (accuracy) dual-model |
| Embeddings | `/modules/06-embeddings/RESEARCH.md` | SentenceTransformers (free, 2-5K embeds/hr) |
| Vector DB | `/modules/07-vector-database/RESEARCH.md` | ChromaDB Phase 2-3, Weaviate Phase 4+ |
| Retrieval | `/modules/08-retrieval-algorithms/RESEARCH.md` | Hybrid (dense+sparse+RRF) > single approach |
| RAG | `/modules/09-rag-architecture/RESEARCH.md` | Traditional RAG sufficient; avoid complexity |
| LLM | `/modules/10-llm-research/RESEARCH.md` | Llama 3 (cost) vs. GPT-4 (quality); decide by Sprint 6 |
| Financial | `/modules/11-financial-analysis/RESEARCH.md` | Amount normalization critical (₹5000 vs 5,00,0) |
| Authority | `/modules/12-authority-identification/RESEARCH.md` | Org chart + NER + rules engine approach |

---

## ⚠️ Common Pitfalls to Avoid

1. **Skipping testing**: Write tests BEFORE implementing features
2. **Ignoring latency**: Measure latency at every step, not just end-to-end
3. **Hallucination blindness**: ALWAYS evaluate hallucination rates; users won't trust otherwise
4. **Over-engineering**: Use simplest solution that meets requirements (e.g., Random Forest > XGBoost, unless XGBoost needed)
5. **No monitoring**: Set up metrics early; don't wait for failures
6. **Communication gaps**: Daily standups; escalate blockers immediately
7. **No documentation**: Document design decisions as you go (not at end)

---

## 🚨 Critical Success Factors

**MUST-HAVES** (Non-negotiable):
- ✅ OCR accuracy ≥88% (else retrieval broken)
- ✅ Classification F1 ≥0.88 (else document routing wrong)
- ✅ Hallucination rate ≤8% (else users won't trust)
- ✅ Latency <2s (else UX terrible)
- ✅ All tests passing (else Phase 3 blocked)

**RED FLAGS** (Escalate immediately):
- 🚨 OCR accuracy <85% in Sprint 2
- 🚨 Classification F1 <0.85 in Sprint 3
- 🚨 Retrieval P@10 <0.70 in Sprint 5
- 🚨 Hallucination rate >10% in Sprint 6
- 🚨 System latency >3s end-to-end

---

## 📞 Questions to Ask Your Tech Lead

- "Which LLM should we use: OpenAI or self-hosted Llama?" (Sprint 6 decision point)
- "Should we invest in BERT fine-tuning or stick with spaCy?" (Depends on F1 gap)
- "When should we migrate from ChromaDB to Weaviate?" (Phase 3, not Phase 2)
- "How do we prevent hallucinations?" (Context pruning + LLM selection + post-processing)

---

## 📊 Success Metrics Dashboard

**Weekly Tracking** (Every Friday):
```
Sprint 1-2: OCR Accuracy %
Sprint 3: Classification F1
Sprint 4: NER F1 per entity type
Sprint 5: Retrieval P@10, Latency p95
Sprint 6: Hallucination Rate %, Faithfulness %
Sprint 7: Financial/Authority module accuracy
Sprint 8: Overall system readiness (% UAT ready)
```

---

## 🎯 Phase 2 → Phase 3 Handoff

**If Phase 2 succeeds** (all metrics met, UAT passed):
- 🟢 Start Phase 3 (October 1, 2026)
- Expand to 15-20 users
- Add advanced features (authority hierarchy, temporal analysis, etc.)

**If Phase 2 partially succeeds** (some gaps):
- 🟡 2-week stabilization sprint
- Fix blockers, improve metrics
- Re-run UAT if needed

**If Phase 2 fails** (critical metrics missed):
- 🔴 Escalate to executive sponsor
- Analyze root causes
- Plan 3-4 week remediation sprint

---

## 📚 Additional Resources

- **Architecture decisions**: See `/ARCHITECTURE.md` (1,100+ lines)
- **Risk management**: See `/documentation/RISK_MANAGEMENT.md` (30 risks identified)
- **Cost tracking**: See `/documentation/COST_BREAKDOWN.md` (phase-by-phase budget)
- **Team structure**: See `/documentation/TEAM_STRUCTURE.md` (roles + hiring)
- **Infrastructure**: See `/architecture/INFRASTRUCTURE_DESIGN.md` (Phase 2-5 scaling)

---

## ✅ Next Steps

1. **Copy this prompt** into Copilot Chat
2. **Start with Sprint 1 section** ("Project Initialization")
3. **Follow prompts chronologically** (Sprints 1-8 in order)
4. **Reference research modules** when stuck (linked above)
5. **Track metrics weekly** (dashboard above)
6. **Escalate blockers** immediately to Tech Lead

---

**Good luck! 🚀 You're building intelligence systems for the Ministry of Defence India.**

*Document Version: 1.0*  
*Last Updated: May 28, 2026*  
*For: Phase 2 Implementation (June-September 2026)*
