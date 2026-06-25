# Phase 2 Implementation Planning

## Detailed Planning for Development Phase

---

## 1. Overview

Phase 2 (Development & Integration) runs for 6 months with a budget of ₹2-3 crores. This document details implementation planning.

---

## 2. Sprint Planning

### Sprint Structure
- 2-week sprints
- 8 total sprints over 16 weeks (Phase 2 = 14-16 weeks actual)
- Daily standups (15 min) + weekly planning (1 hour)
- Bi-weekly sprint reviews with stakeholders
- Sprint velocity target: 40-50 story points per sprint
- Planned buffer sprint: Sprint 7 for integration + testing

### Phase 2 Sprint Breakdown (16 weeks = 8 sprints)

#### Sprint 1 (Weeks 1-2): Project Initialization & Environment Setup
**Focus**: Team onboarding, infrastructure setup, development environment

**Deliverables**:
- 2-week DIRAS bootcamp completed (all 12 engineers)
- Development environment ready (laptops, VPN, Git access)
- CI/CD pipeline operational (GitHub Actions)
- Docker + container registry setup
- Initial repository structure created
- Architecture documentation reviewed + approved by team
- Technology stack confirmed (no changes to Phase 1 selection)

**Key Tasks**:
- Bootcamp curriculum finalized, delivered
- Git workflow training + first commits
- Docker image templates created
- CI/CD pipeline for automated testing
- Server setup + networking (on-prem)
- Monitoring tools basic setup (Grafana, basic metrics)

**Team**: All 12 engineers + DevOps (dedicated)
**Story Points**: 40
**Definition of Done**: Team can clone repo, run tests, deploy locally

**Sprint Gate**: All team members productive; infrastructure stable

---

#### Sprint 2 (Weeks 3-4): Data Pipeline Foundation
**Focus**: Set up document collection, OCR pipeline, basic preprocessing

**Deliverables**:
- Web scraping infrastructure operational (3-5 data sources)
- 5,000 documents collected + validated
- EasyOCR baseline established (88-90% accuracy)
- OCR preprocessing pipeline v1 (Regex + basic cleaning)
- Document storage setup (NAS, S3 backup)
- Data quality metrics dashboard (OCR accuracy per source)

**Key Tasks**:
- Scrapers for Ministry of Defence, Gazette of India, PIB (Weeks 1)
- Document validation + deduplication (Weeks 1-2)
- EasyOCR integration + accuracy testing (Weeks 1-2)
- Fallback Tesseract setup (Week 2)
- Storage setup, retention policies (Week 2)

**Team**: Data Engineer (1) + Backend (2) + DevOps (1)
**Story Points**: 50 (heavy data engineering)
**Definition of Done**: 5K docs in system, OCR baseline 88%+

**Sprint Gate**: OCR accuracy meets target; data pipeline stable

---

#### Sprint 3 (Weeks 5-6): Text Processing & Classification Foundation
**Focus**: Preprocessing, document classification training

**Deliverables**:
- Preprocessing pipeline v2 (NLTK + spaCy, lemmatization)
- Information loss measurement (<2%)
- Document classification training data prepared (3,000 docs, annotated)
- Classification model baselines (Logistic Regression, Random Forest)
- Classification accuracy ≥88% on test set
- Classification API endpoint operational

**Key Tasks**:
- Preprocessing design doc + tradeoffs (Week 1)
- Lemmatization + stemming experiments (Week 1-2)
- Duplicate detection improvement (Week 1)
- Classification data collection + annotation (Weeks 1-2)
- Random Forest baseline training (Week 2)
- Model evaluation on test set (Week 2)

**Team**: ML Engineers (3) + Data Engineer (1) + QA (1)
**Story Points**: 50
**Definition of Done**: Classification F1 ≥0.88; API operational

**Sprint Gate**: Classification baseline meets targets

---

#### Sprint 4 (Weeks 7-8): Entity Extraction (NER)
**Focus**: Named Entity Recognition system development

**Deliverables**:
- NER training dataset created (5,000+ entities annotated)
- spaCy NER baseline operational (F1 ≥0.80)
- BERT NER fine-tuning started
- Authority hierarchy knowledge base v1 (manual mapping)
- NER API endpoint operational
- Per-entity-type F1 metrics tracked

**Key Tasks**:
- NER annotation guidelines + tooling setup (Week 1)
- Crowdsource annotation (Week 1-2)
- spaCy NER training (Week 2)
- BERT NER fine-tuning begun (Week 2)
- Authority knowledge base setup (Week 2)

**Team**: ML Engineers (2) + NLP Specialist (if hired) + QA (1)
**Story Points**: 50
**Definition of Done**: NER F1 ≥0.82; spaCy + BERT both operational

**Sprint Gate**: NER accuracy targets met

---

#### Sprint 5 (Weeks 9-10): Embeddings & Vector Database
**Focus**: Embedding generation, vector DB setup, retrieval optimization

**Deliverables**:
- SentenceTransformers embedding model selected + loaded
- 10,000 documents embedded
- ChromaDB deployed + operational (1M vector capacity)
- BM25 index created (Elasticsearch or simple inverted index)
- Hybrid retrieval system v1 (dense + BM25 + RRF fusion)
- Retrieval latency <150ms p95 (100 QPS load)
- Precision@10 ≥0.75 (on benchmark queries)

**Key Tasks**:
- Embedding model selection + comparison (Week 1)
- Batch embedding generation (5K-10K docs) (Week 1)
- ChromaDB setup + configuration (Week 1-2)
- BM25 indexing (Week 1-2)
- Retrieval fusion (RRF) implementation (Week 2)
- Performance profiling + optimization (Week 2)

**Team**: Backend Engineers (2) + ML Engineer (1) + DevOps (1)
**Story Points**: 55
**Definition of Done**: Retrieval P@10 ≥0.75, <150ms latency

**Sprint Gate**: Retrieval quality + speed targets met

---

#### Sprint 6 (Weeks 11-12): RAG Pipeline & LLM Integration
**Focus**: RAG architecture, LLM integration, hallucination prevention

**Deliverables**:
- RAG pipeline v1 (retrieval → context → LLM)
- LLM integration (OpenAI API or Llama 3 self-hosted)
- Prompt templates created + tested
- Hallucination detection module (basic)
- Response generation + ranking
- 100 test queries with expected answers
- RAG answer quality baseline (faithfulness ≥0.90)

**Key Tasks**:
- RAG architecture design doc (Week 1)
- LangChain RAG setup (Week 1-2)
- LLM API integration (Week 1-2)
- Prompt engineering + testing (Week 2)
- Hallucination detection (Week 2)
- Evaluation on 100 queries (Week 2)

**Team**: ML Engineers (2) + Backend (1) + NLP Specialist (1)
**Story Points**: 60 (high complexity)
**Definition of Done**: RAG operational; faithfulness ≥0.90

**Sprint Gate**: RAG quality meets targets; no critical hallucinations

---

#### Sprint 7 (Weeks 13-14): Financial Analysis & Authority Identification
**Focus**: Specialized modules, system integration

**Deliverables**:
- Financial entity extraction (rules + BERT NER)
- Monetary amount normalization + aggregation
- Authority identification system operational
- Approval chain mapping (80%+ accuracy)
- Financial query answering working
- Authority queries answering working
- Integration testing (all modules together)

**Key Tasks**:
- Financial entity definition + rules (Week 1)
- Rule-based extraction + BERT backup (Week 1-2)
- Amount normalization (currency, format) (Week 1)
- Authority hierarchy engine (Week 1-2)
- Approval chain extraction (Week 2)
- End-to-end integration testing (Week 2)

**Team**: ML Engineers (2) + Backend (2) + QA (1)
**Story Points**: 55
**Definition of Done**: Financial + Authority queries working; integration tests passing

**Sprint Gate**: Specialized modules meet accuracy targets

---

#### Sprint 8 (Weeks 15-16): Testing, Evaluation & UAT Preparation
**Focus**: Comprehensive testing, performance optimization, UAT setup

**Deliverables**:
- Golden dataset (960 docs) finalized + annotated
- Benchmark query set (200 queries) finalized + validated
- Evaluation framework operational (Ragas, custom metrics)
- Performance profiling + optimization (latency <2s)
- UAT environment setup + user training materials
- Phase 2 comprehensive test suite passing (95%+ pass rate)
- Regression test suite automated
- UAT scheduled + stakeholders notified

**Key Tasks**:
- Golden dataset annotation completion (Week 1)
- Benchmark query creation + verification (Week 1)
- Evaluation framework implementation (Week 1-2)
- Performance profiling (all modules) (Week 1-2)
- Optimization (target: 20% latency improvement) (Week 2)
- UAT environment preparation (Week 2)
- End-to-end system test (Week 2)

**Team**: QA (2) + ML Engineers (2) + Backend (1)
**Story Points**: 50
**Definition of Done**: UAT ready; all tests passing; baseline metrics established

**Sprint Gate**: UAT environment operational; team trained; stakeholders ready

---

### Phase 2 Success Criteria (End of Sprint 8)

**Mandatory (MVP)**:
- ✅ OCR accuracy ≥88%
- ✅ Classification F1 ≥0.88
- ✅ NER F1 ≥0.82
- ✅ Retrieval P@10 ≥0.75
- ✅ RAG faithfulness ≥0.90
- ✅ System latency <2s per query
- ✅ Hallucination rate ≤8%
- ✅ 5,000+ documents indexed

**Nice-to-Have**:
- BERT fine-tuning > Random Forest
- Authority mapping accuracy ≥80%
- Financial queries working reliably
- Multi-query handling

**UAT Requirements**:
- 5 real-world scenarios tested
- 80%+ user satisfaction (Phase 2 MVP)
- Zero critical blockers
- All infrastructure stable

---

### Risk Management in Sprints

**Critical Path**:
1. Data pipeline (Sprints 1-2) → affects downstream tasks
2. Classification + NER (Sprints 3-4) → required for routing
3. Retrieval (Sprint 5) → required for RAG
4. RAG (Sprint 6) → final integration

**Buffer Allocation**:
- Sprint 7 includes integration buffer (1 week)
- Sprint 8 includes testing buffer + UAT prep
- If slippage detected in Sprint 1-4, activate 2-week extension plan

---

---

## 3. Core Development Tasks

### Task 1: Data Pipeline (Weeks 1-6)

**Objectives**:
- Set up data collection infrastructure
- Implement OCR pipeline
- Create preprocessing pipeline
- Validate data quality

**Deliverables**:
- 10,000 documents collected
- OCR accuracy >88%
- Processing speed >5000 docs/hour

**Team**: 3-4 engineers
**Tools**: Python, Scrapy, EasyOCR, spaCy

---

### Task 2: Classification & NER (Weeks 3-10)

**Objectives**:
- Train document classifier
- Deploy NER system
- Create entity linking
- Implement hierarchy mapping

**Deliverables**:
- Classifier accuracy >90%
- NER F1-score >85%
- Authority mapping system

**Team**: 2-3 ML engineers
**Tools**: scikit-learn, BERT, spaCy

---

### Task 3: Embeddings & Vector DB (Weeks 5-12)

**Objectives**:
- Choose embedding model
- Set up vector database
- Create BM25 index
- Optimize retrieval latency

**Deliverables**:
- 10,000 documents embedded
- ChromaDB deployment
- BM25 index created
- Retrieval latency <200ms

**Team**: 2 engineers
**Tools**: SentenceTransformers, ChromaDB, Elasticsearch

---

### Task 4: RAG & LLM Integration (Weeks 8-24)

**Objectives**:
- Implement RAG pipeline
- Integrate LLM API
- Create prompt templates
- Implement hallucination detection

**Deliverables**:
- RAG system operational
- 100 test queries with answers
- Evaluation framework
- Hallucination rate <2%

**Team**: 2-3 engineers
**Tools**: LangChain, OpenAI API, Llama

---

### Task 5: Financial Analysis (Weeks 10-20)

**Objectives**:
- Define financial entities
- Implement extraction rules
- Train NER model
- Create aggregation logic

**Deliverables**:
- Financial entity extraction
- Amount normalization
- Authority association
- Aggregation reports

**Team**: 2 engineers
**Tools**: BERT, regex, custom scripts

---

### Task 6: Authority Identification (Weeks 12-22)

**Objectives**:
- Build knowledge base
- Implement NER for authorities
- Create hierarchy engine
- Extract relationships

**Deliverables**:
- Authority knowledge base
- Mapping system operational
- Governance reports
- 95%+ accuracy

**Team**: 2-3 engineers
**Tools**: Neo4j, spaCy, custom code

---

### Task 7: Evaluation & Testing (Weeks 14-26)

**Objectives**:
- Create test datasets
- Run evaluation benchmarks
- User acceptance testing
- Performance profiling

**Deliverables**:
- 500+ test queries
- Evaluation reports
- Performance benchmarks
- UAT sign-off

**Team**: 2-3 QA engineers
**Tools**: Custom evaluation scripts

---

## 4. Technology Stack Decision

### OCR & Layout
- **Primary**: EasyOCR (Hindi support, accuracy >88%)
- **Fallback**: Tesseract
- **Complex layouts**: LayoutParser

### Text Processing
- **Tokenization**: NLTK + spaCy
- **Lemmatization**: spaCy (neural)
- **Advanced**: Transformers for specific tasks

### Classification
- **Model**: Random Forest (production-ready)
- **Baseline**: Logistic Regression
- **Ensemble**: BERT for confidence

### Entity Extraction
- **Primary**: spaCy (speed)
- **Secondary**: BERT NER (accuracy)
- **Specialized**: CRF for specific entity types

### Embeddings
- **Model**: SentenceTransformers (all-MiniLM-L6-v2)
- **Alternative**: BGE (if performance needed)
- **Future**: Upgrade to all-mpnet-base-v2 (Phase 4)

### Vector Database
- **Chosen**: ChromaDB
- **Rationale**: Easy setup, 1M document scale, dynamic indexing
- **Future migration**: Weaviate (Phase 4)

### Search Strategy
- **Dense**: Cosine similarity on embeddings
- **Sparse**: BM25 on tokenized text
- **Fusion**: Reciprocal Rank Fusion (RRF)
- **Reranking**: Cross-Encoder (ms-marco-MiniLM-L6-v2)

### RAG Architecture
- **Chosen**: Traditional/Hybrid RAG
- **Framework**: LangChain for orchestration
- **LLM**: OpenAI GPT-3.5 or Llama 3 (if self-hosted)

### Infrastructure
- **Framework**: Python 3.10+
- **Web**: FastAPI for API endpoints
- **Storage**: PostgreSQL for metadata
- **Deployment**: Docker containers on VM/Kubernetes
- **Cloud**: Optional AWS/GCP (or on-premise)

---

## 5. Development Milestones

| Milestone | Timeline | Deliverable |
|-----------|----------|-----------|
| Data Pipeline v1 | Week 6 | 10K documents, OCR working |
| Classification v1 | Week 10 | >90% accuracy |
| Embeddings Ready | Week 12 | All documents embedded |
| RAG System v1 | Week 16 | Basic Q&A working |
| Financial Analysis v1 | Week 20 | Amount extraction >95% |
| Authority System v1 | Week 22 | Authority mapping >90% |
| Evaluation Complete | Week 24 | All metrics passing |
| Production Ready | Week 26 | UAT approved, deployed |

---

## 6. Risk Management

### Technical Risks

**Risk**: OCR accuracy below 85%
- Mitigation: Multi-model ensemble, fallback to manual
- Contingency: Budget 2 weeks extra for fine-tuning

**Risk**: LLM hallucination rate >5%
- Mitigation: Confidence scoring, validation layer
- Contingency: Implement stronger validation mechanisms

**Risk**: Retrieval recall <75%
- Mitigation: Test different embedding models
- Contingency: Upgrade to paid embedding API

### Resource Risks

**Risk**: Team attrition
- Mitigation: Clear documentation, knowledge sharing
- Contingency: Cross-training on critical modules

**Risk**: Scope creep
- Mitigation: Strict sprint planning, feature prioritization
- Contingency: Defer to Phase 3 if needed

---

## 7. Quality Assurance Strategy

### Testing Levels

1. **Unit Testing**: Each module (>80% coverage)
2. **Integration Testing**: Component interactions
3. **End-to-End Testing**: Full pipeline
4. **Performance Testing**: Latency & throughput
5. **User Acceptance Testing**: Stakeholder validation

### Benchmarking

- Create 500-1000 test queries
- Multi-annotator evaluation (Kappa >0.85)
- Weekly progress reporting
- Monthly performance review

---

## 8. Documentation Requirements

### During Development
- Code documentation (docstrings)
- API documentation (OpenAPI)
- Architecture decisions (ADRs)
- Operational procedures

### For Handoff
- User manual
- Administrator guide
- API reference
- Troubleshooting guide

---

## 9. Budget Allocation

| Item | Budget |
|------|--------|
| Engineering (12-15 people) | ₹1.2-1.8 crores |
| Infrastructure & Tools | ₹20-30 lakhs |
| Training & Documentation | ₹10-15 lakhs |
| Contingency (10%) | ₹20-25 lakhs |
| **Total** | **₹1.7-2.5 crores** |

---

## 10. Success Criteria

### Technical Metrics
- ✅ Retrieval Precision@5 >0.75
- ✅ Classification Accuracy >90%
- ✅ NER F1-score >85%
- ✅ RAG Hallucination <2%
- ✅ End-to-end latency <5s

### Business Metrics
- ✅ 10,000+ documents indexed
- ✅ 100+ test queries passing
- ✅ Stakeholder sign-off
- ✅ UAT completed
- ✅ Documentation complete

### Team Metrics
- ✅ Zero critical security issues
- ✅ <5% code defect rate
- ✅ Team knowledge transfer complete
- ✅ Deployment procedures validated

---

## 11. Handoff to Phase 3

**Deliverables for QA Team**:
- Complete system documentation
- Test suite (500+ test cases)
- Known issues and workarounds
- Performance baseline
- Recommendations for improvements

**Success Definition**:
- System meets all Phase 2 success criteria
- Full operational documentation
- Team trained on operations
- Ready for comprehensive testing phase

---

*Last Updated: May 26, 2026*
