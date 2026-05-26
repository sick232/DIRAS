# Defence Intelligence Retrieval and Analysis System (DIRAS)

**AI-Powered RAG-Based Defence Document Intelligence Platform**

> **Phase 1: Research, Planning & System Design**  
> This repository contains the complete research, architectural design, and algorithmic analysis for an enterprise-grade defence intelligence system. **NO implementation code is included at this phase.**

---

## 🎯 Project Overview

### Mission
Build an AI-powered intelligence retrieval platform capable of extracting, analysing, and intelligently retrieving information from defence-related public documents to support decision-making at the Ministry of Defence India.

### Vision
Transform unstructured defence documents into structured, semantically searchable intelligence assets using state-of-the-art retrieval-augmented generation (RAG) technology.

### Strategic Importance
- **Policy Intelligence**: Rapid retrieval of applicable policies and guidelines
- **Procurement Analysis**: Understanding defence procurement patterns and authorities
- **Budget Intelligence**: Tracking defence expenditure and resource allocation
- **Authority Mapping**: Identifying responsible departments and officers
- **Compliance Verification**: Ensuring adherence to defence regulations
- **Trend Analysis**: Identifying patterns in defence operations and investments

---

## 📋 Project Objectives

The system aims to:

✅ Extract public defence-related documents from authoritative sources  
✅ Analyse financial expenditure and procurement information  
✅ Retrieve relevant policy documents and guidelines  
✅ Identify responsible authorities and departments  
✅ Process official notices, memorandums, and circulars  
✅ Answer semantic questions using RAG architecture  
✅ Build searchable defence knowledge base  
✅ Support Hindi-English bilingual retrieval (future)  
✅ Enable speech-based intelligence queries (future)  

---

## 📚 Document Types Handled

The system is designed to process:

| Category | Document Types |
|----------|---|
| **Policy & Governance** | Defence Guidelines, Circulars, Memorandums, Official Notices |
| **Financial** | Defence Budget Documents, Financial Expenditure Reports, Audit Reports |
| **Procurement** | Tender Documents, Procurement Notices, Contract Notices |
| **Publications** | Gazette Publications, Parliamentary Defence Reports, Public Policies |
| **Technical** | Defence Technical Reports, DRDO Publications, Research Papers |
| **Administrative** | Administrative Orders, Organizational Directives, Implementation Notices |

---

## 🌐 Data Sources

All data sources are **public, open-access, and unclassified**:

| Source | Description |
|--------|---|
| **Ministry of Defence India** | Official MOD website, publications, orders |
| **Gazette of India** | Official government gazette publications |
| **PIB (Press Information Bureau)** | Defence-related press releases and notices |
| **DRDO Public Reports** | Published research and technical reports |
| **Parliamentary Reports** | Defence-related parliamentary discussions and reports |
| **Open Government Data** | Data.gov.in, open public government datasets |
| **Defence Procurement Portal** | Public procurement notices and documents |
| **Audit Reports** | CAG (Comptroller & Auditor General) defence audit reports |

---

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE                             │
│                      (Query Entry Points)                            │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                    QUERY UNDERSTANDING LAYER                         │
│   Intent Detection │ Query Expansion │ Semantic Processing           │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                     HYBRID RETRIEVAL LAYER                           │
│  ┌──────────────────┬──────────────────┬──────────────────┐         │
│  │ Similarity Match │ Vector Search    │ BM25 Retrieval   │         │
│  │ (Dense)          │ (FAISS/Vector DB)│ (Sparse)         │         │
│  └──────────────────┴──────────────────┴──────────────────┘         │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                      RERANKING LAYER                                 │
│   Cross-Encoder Reranking │ MMR │ Reciprocal Rank Fusion            │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                   CONTEXT RETRIEVAL & RAG                            │
│  Document Context Assembly │ Prompt Engineering │ Citation Linking   │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                     LLM REASONING LAYER                              │
│         Authority Identification │ Financial Extraction              │
│                    Answer Generation                                │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────────┐
│                      RESPONSE GENERATION                             │
│            Formatted Answer │ Source Citations │ Confidence          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
DIRAS/
│
├── README.md                          # Main project overview
├── ARCHITECTURE.md                    # Complete system architecture
├── RESEARCH_ROADMAP.md               # 5-phase implementation roadmap
├── SECURITY_ETHICS.md                # Compliance & ethical guidelines
│
├── research/                         # Research overview & methodology
│   ├── RESEARCH_OVERVIEW.md
│   └── METHODOLOGY.md
│
├── architecture/                     # System design & pipelines
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── DATA_PIPELINE.md
│   ├── QUERY_FLOW.md
│   ├── RETRIEVAL_ARCHITECTURE.md
│   └── RAG_ARCHITECTURE.md
│
├── modules/                          # 12 research modules
│   ├── 01-dataset-collection/
│   ├── 02-ocr-document-understanding/
│   ├── 03-preprocessing-pipeline/
│   ├── 04-document-classification/
│   ├── 05-entity-extraction/
│   ├── 06-embeddings/
│   ├── 07-vector-database/
│   ├── 08-retrieval-algorithms/
│   ├── 09-rag-architecture/
│   ├── 10-llm-research/
│   ├── 11-financial-analysis/
│   └── 12-authority-identification/
│
├── algorithms/                       # Algorithm research & comparisons
│   ├── QUERY_UNDERSTANDING.md
│   ├── SEMANTIC_SIMILARITY.md
│   ├── RANKING_ALGORITHMS.md
│   ├── RETRIEVAL_RANKING.md
│   └── HALLUCINATION_DETECTION.md
│
├── workflows/                        # Detailed workflow documentation
│   ├── 01-data-collection-workflow.md
│   ├── 02-preprocessing-workflow.md
│   ├── 03-indexing-workflow.md
│   ├── 04-query-workflow.md
│   ├── 05-retrieval-workflow.md
│   ├── 06-rag-workflow.md
│   ├── 07-financial-analysis-workflow.md
│   ├── 08-authority-identification-workflow.md
│   └── WORKFLOW_ORCHESTRATION.md
│
├── diagrams/                         # Mermaid workflow diagrams
│   ├── 01-system-architecture.mmd
│   ├── 02-rag-pipeline.mmd
│   ├── 03-data-pipeline.mmd
│   ├── 04-query-flow.mmd
│   ├── 05-embedding-pipeline.mmd
│   ├── 06-vector-search.mmd
│   ├── 07-financial-analysis.mmd
│   ├── 08-authority-identification.mmd
│   ├── 09-document-classification.mmd
│   ├── 10-preprocessing.mmd
│   ├── 11-entity-extraction.mmd
│   └── DIAGRAM_GUIDE.md
│
├── evaluation/                       # Evaluation framework
│   ├── EVALUATION_FRAMEWORK.md
│   ├── RETRIEVAL_METRICS.md
│   ├── RAG_METRICS.md
│   ├── CLASSIFICATION_METRICS.md
│   ├── OCR_METRICS.md
│   ├── ENTITY_EXTRACTION_METRICS.md
│   ├── FINANCIAL_EXTRACTION_METRICS.md
│   ├── BENCHMARK_DATASETS.md
│   └── HUMAN_EVALUATION_PROTOCOL.md
│
├── benchmarking/                     # Benchmarking strategy
│   ├── BENCHMARKING_STRATEGY.md
│   ├── BASELINE_ESTABLISHMENT.md
│   ├── REGRESSION_TESTING.md
│   ├── SCALABILITY_BENCHMARKS.md
│   ├── LATENCY_ANALYSIS.md
│   ├── THROUGHPUT_ANALYSIS.md
│   ├── MEMORY_PROFILING.md
│   └── COST_ANALYSIS.md
│
├── use-cases/                        # Defence applications
│   ├── DEFENCE_USE_CASES.md
│   ├── PROCUREMENT_ANALYSIS.md
│   ├── BUDGET_INTELLIGENCE.md
│   ├── POLICY_RETRIEVAL.md
│   ├── AUTHORITY_MAPPING.md
│   └── CASE_STUDY_TEMPLATE.md
│
├── comparisons/                      # Technique comparisons
│   ├── TECHNIQUES_COMPARISON_MATRIX.md
│   ├── FRAMEWORK_COMPARISON.md
│   ├── DATABASE_COMPARISON.md
│   ├── LLM_COMPARISON.md
│   └── COST_EFFECTIVENESS_ANALYSIS.md
│
├── future-scope/                     # Future capabilities
│   ├── MULTILINGUAL_RETRIEVAL.md
│   ├── SPEECH_QUERYING.md
│   ├── KNOWLEDGE_GRAPHS.md
│   ├── MULTIMODAL_RAG.md
│   ├── AUTONOMOUS_AGENTS.md
│   ├── POLICY_ASSISTANTS.md
│   └── EMERGING_TECHNOLOGIES.md
│
├── implementation-roadmap/           # Implementation phases
│   ├── PHASE_1_RESEARCH.md
│   ├── PHASE_2_DEVELOPMENT.md
│   ├── PHASE_3_TESTING.md
│   ├── PHASE_4_DEPLOYMENT.md
│   ├── PHASE_5_OPERATIONS.md
│   └── MILESTONE_TRACKER.md
│
├── documentation/                    # Implementation planning
│   ├── API_PLANNING.md
│   ├── DATA_SCHEMA_PLANNING.md
│   ├── CONFIGURATION_GUIDE.md
│   ├── DEPLOYMENT_PLANNING.md
│   ├── MAINTENANCE_PLANNING.md
│   └── GLOSSARY.md
│
└── references/                       # Resources & references
    ├── ACADEMIC_PAPERS.md
    ├── INDUSTRY_STANDARDS.md
    ├── TOOLS_AND_LIBRARIES.md
    └── EXTERNAL_RESOURCES.md
```

---

## 🔍 Quick Navigation

### **Getting Started**
- 📖 [System Architecture](architecture/SYSTEM_ARCHITECTURE.md) — Complete system design
- 🗺️ [Implementation Roadmap](implementation-roadmap/PHASE_1_RESEARCH.md) — Path to implementation
- 🎯 [Use Cases](use-cases/DEFENCE_USE_CASES.md) — Defence applications

### **Research Areas**
- 📊 [All 12 Research Modules](modules/) — Technique comparisons and research
- 🔄 [Workflows](workflows/) — Step-by-step process flows
- 📈 [Algorithms](algorithms/) — Algorithm research and analysis
- 📊 [Comparisons](comparisons/) — Technique comparison matrices

### **Technical Planning**
- 📋 [Evaluation Framework](evaluation/EVALUATION_FRAMEWORK.md) — Metrics and benchmarks
- 🧪 [Benchmarking Strategy](benchmarking/BENCHMARKING_STRATEGY.md) — Performance testing
- 🔐 [Security & Ethics](SECURITY_ETHICS.md) — Compliance and safety

### **Future Capabilities**
- 🚀 [Future Scope](future-scope/) — Emerging technologies
- 🌍 [Multilingual Support](future-scope/MULTILINGUAL_RETRIEVAL.md)
- 🤖 [Autonomous Agents](future-scope/AUTONOMOUS_AGENTS.md)

---

## 📊 Research Modules at a Glance

| # | Module | Focus | Key Comparisons |
|---|--------|-------|---|
| 1 | Dataset Collection | Data acquisition strategy | Web scraping, APIs, OCR extraction, automated crawling |
| 2 | OCR & Document Understanding | Text extraction from scans | Tesseract, EasyOCR, PaddleOCR, LayoutParser |
| 3 | Preprocessing Pipeline | Text cleaning and normalization | Regex, NLTK, SpaCy, Transformer-based |
| 4 | Document Classification | 10-class document taxonomy | SVM, Random Forest, Logistic Regression, BERT |
| 5 | Entity Extraction | NER for defence entities | SpaCy, BERT, CRF, BiLSTM-CRF |
| 6 | Embeddings | Text to vector conversion | OpenAI, SentenceTransformers, BGE, E5 |
| 7 | Vector Database | Semantic similarity search | FAISS, ChromaDB, Pinecone, Weaviate |
| 8 | Retrieval Algorithms | Finding relevant documents | Cosine, BM25, DPR, Hybrid + reranking |
| 9 | RAG Architecture | Question answering pipeline | Traditional, Hybrid, Graph, Multi-query, Agentic |
| 10 | LLM Research | Large language models | GPT, Llama, Mistral, Gemini |
| 11 | Financial Analysis | Monetary data extraction | Rule-based, Transformer-based |
| 12 | Authority Identification | Department/officer mapping | NER, Semantic mapping, Graph extraction |

---

## 🎓 Key Research Questions

### Architecture & Design
- How do we build a RAG system that handles defence document complexity?
- What is the optimal pipeline for retrieval + LLM reasoning?
- How do we minimize hallucination in defence-critical contexts?

### Technical Choices
- Which embedding model best captures defence terminology?
- What retrieval strategy (dense, sparse, hybrid) performs best?
- Should we use local or API-based LLMs?

### Evaluation & Quality
- How do we benchmark retrieval quality on defence documents?
- What metrics ensure factual correctness?
- How do we implement human evaluation at scale?

### Scalability & Operations
- How do we scale from thousands to millions of documents?
- What infrastructure supports production deployment?
- How do we maintain quality as the knowledge base grows?

---

## 🔐 Security & Ethical Commitments

✅ **Public Documents Only** — No classified or sensitive defence information  
✅ **Transparent Data Sources** — All sources are open-access and documented  
✅ **Hallucination Mitigation** — Multi-layer safeguards against factual errors  
✅ **Audit Logging** — Complete audit trails for accountability  
✅ **Ethical AI** — Bias detection and mitigation strategies  
✅ **Regulatory Compliance** — Adherence to MOD/DRDO guidelines  

See [SECURITY_ETHICS.md](SECURITY_ETHICS.md) for detailed policies.

---

## 📈 Evaluation Strategy

The system will be evaluated across multiple dimensions:

### Component-Level Metrics
- **Retrieval**: Precision@K, Recall@K, MAP, MRR, NDCG
- **Classification**: Accuracy, Precision, Recall, F1-Score
- **Entity Extraction**: Precision, Recall, F1 per entity type
- **OCR**: Character Error Rate, Word Error Rate

### System-Level Metrics
- **Faithfulness**: Answers grounded in retrieved documents
- **Answer Relevance**: Responses address the query
- **Hallucination Rate**: Percentage of unfaithful claims
- **Context Precision**: Relevant documents ranked highly

### Performance Metrics
- **Latency**: Response time per query
- **Throughput**: Queries per second capacity
- **Scalability**: Performance with 10K to 100M documents
- **Cost**: Infrastructure and operational expenses

See [EVALUATION_FRAMEWORK.md](evaluation/EVALUATION_FRAMEWORK.md) for comprehensive methodology.

---

## 🚀 Implementation Roadmap

### Phase 1: Research & Planning (Current - Ongoing)
- ✅ Complete architectural design
- ✅ Algorithm evaluation planning
- ✅ Technology selection framework
- ✅ Performance baseline definition

### Phase 2: Development & Integration
- Build core system components
- Implement data pipeline
- Integrate all 12 modules
- Create working prototype

### Phase 3: Testing & Evaluation
- Comprehensive testing suite
- Benchmark evaluation
- Performance optimization
- Refinement based on results

### Phase 4: Production Deployment
- Security hardening
- Scalability verification
- Operational procedures
- Production deployment

### Phase 5: Operations & Maintenance
- Continuous monitoring
- Regular updates
- Performance optimization
- Sustained operations

See [RESEARCH_ROADMAP.md](RESEARCH_ROADMAP.md) for detailed phase breakdown.

---

## 🌟 Future Scope

### Short-term (Phase 2-3)
- Multilingual retrieval (Hindi-English)
- Enhanced financial data extraction
- Improved authority identification

### Medium-term (Phase 4-5)
- Speech-based intelligence queries
- Knowledge graph integration
- Autonomous agent systems

### Long-term (Beyond Phase 5)
- Multimodal RAG (images, tables, diagrams)
- Real-time intelligence updates
- AI-powered policy assistance

See [FUTURE_SCOPE](future-scope/) directory for detailed analysis.

---

## 👥 Project Governance

**Stakeholders**
- Ministry of Defence (MOD) India
- Defence Research & Development Organisation (DRDO)
- Defence Policy Think Tanks
- Parliamentary Defence Committee

**Repository Standards**
- All documentation follows professional academic style
- Comparisons include multiple perspectives
- Security and compliance are paramount
- Ethical AI principles guide all decisions

---

## 📚 Key Documents by Purpose

### For Decision Makers
- [System Architecture](architecture/SYSTEM_ARCHITECTURE.md) — Understand the system design
- [Use Cases](use-cases/DEFENCE_USE_CASES.md) — See practical applications
- [Implementation Roadmap](implementation-roadmap/) — Understand timeline and phases

### For Technical Teams
- [12 Research Modules](modules/) — Detailed algorithm research
- [Workflows](workflows/) — Understand each process step
- [Evaluation Framework](evaluation/) — Know how to measure success

### For AI/ML Engineers
- [Algorithm Comparisons](comparisons/) — Technical deep dives
- [Benchmarking Strategy](benchmarking/) — Performance testing approach
- [Architecture Planning](architecture/) — System design details

### For Project Managers
- [Research Roadmap](RESEARCH_ROADMAP.md) — Phases and deliverables
- [Milestone Tracker](implementation-roadmap/MILESTONE_TRACKER.md) — Key metrics
- [Cost Analysis](benchmarking/COST_ANALYSIS.md) — Resource requirements

---

## 📝 Repository Status

| Aspect | Status |
|--------|--------|
| Phase 1: Research & Planning | 🟢 In Progress |
| Architecture Documentation | 🟢 In Progress |
| 12 Research Modules | 🟢 In Progress |
| Evaluation Framework | 🟢 In Progress |
| Implementation Code | 🔴 Not Started (Phase 2) |
| Deployment | 🔴 Not Started (Phase 4) |

---

## 🔗 Related Resources

### Official Sources
- [Ministry of Defence India](https://mod.gov.in/)
- [DRDO Official Portal](https://www.drdo.gov.in/)
- [Gazette of India](https://egazette.gov.in/)
- [PIB News Archive](https://pib.gov.in/)

### Research Standards
- [RAG Survey Papers](references/ACADEMIC_PAPERS.md)
- [LLM Benchmarks](references/EXTERNAL_RESOURCES.md)
- [Industry Standards](references/INDUSTRY_STANDARDS.md)

---

## 📞 Repository Information

- **Project Title**: Defence Intelligence Retrieval and Analysis System (DIRAS)
- **Phase**: Phase 1 - Research, Planning & System Design
- **Status**: Active Development
- **Last Updated**: May 26, 2026
- **Repository Type**: Research & Planning Repository
- **Code Status**: No implementation code (planning phase)

---

## ⚖️ License & Attribution

This research repository is designed for the Ministry of Defence India and follows strict security and ethical guidelines. See [SECURITY_ETHICS.md](SECURITY_ETHICS.md) for compliance information.

---

## 📖 How to Navigate This Repository

1. **Start Here**: [ARCHITECTURE.md](architecture/SYSTEM_ARCHITECTURE.md) — Understand the system design
2. **Deep Dive**: Select any [Research Module](modules/) for detailed algorithm comparison
3. **Understand Workflows**: Browse [Workflows](workflows/) directory for process flows
4. **See Implementation Plan**: Review [RESEARCH_ROADMAP.md](RESEARCH_ROADMAP.md) for next steps
5. **Check Evaluation**: Read [EVALUATION_FRAMEWORK.md](evaluation/EVALUATION_FRAMEWORK.md) for metrics

---

**Repository maintained for the Defence Research & Development Organisation (DRDO)**

*This is a professional research proposal for an enterprise-grade AI system. No implementation code is included in Phase 1.*
