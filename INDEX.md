# DIRAS Repository Index

## Defence Intelligence Retrieval and Analysis System - Complete Documentation Index

---

## 📋 Quick Navigation

### Start Here
- [README.md](README.md) - Project overview, vision, and quick start
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design and components
- [SECURITY_ETHICS.md](SECURITY_ETHICS.md) - Security framework and guidelines

### Research & Planning
- [RESEARCH_ROADMAP.md](RESEARCH_ROADMAP.md) - 5-phase implementation timeline
- [Techniques Comparison Matrix](comparisons/TECHNIQUES_COMPARISON_MATRIX.md) - All technique comparisons
- [Real-World Use Cases](use-cases/REAL_WORLD_SCENARIOS.md) - 10 key applications
- [Advanced Capabilities](future-scope/ADVANCED_CAPABILITIES.md) - Features for Phase 4+

---

## 📚 12 Core Research Modules

Each module contains detailed research on specific system components with 4+ technique comparisons.

### Module 1: Dataset Collection
- **Research**: [modules/01-dataset-collection/RESEARCH.md](modules/01-dataset-collection/RESEARCH.md)
- **Focus**: 5 data collection techniques (web scraping, APIs, direct download, email feeds, OCR)
- **Recommendation**: Combined approach - APIs + Web Scraping + Direct Download
- **Volume**: 50-100 documents/day

### Module 2: OCR & Document Understanding
- **Research**: [modules/02-ocr-document-understanding/RESEARCH.md](modules/02-ocr-document-understanding/RESEARCH.md)
- **Focus**: 4 OCR approaches (Tesseract, EasyOCR, PaddleOCR, LayoutParser)
- **Recommendation**: EasyOCR primary (88-94% accuracy), LayoutParser for complex layouts
- **Key Metrics**: Character Error Rate <8%, Word Error Rate <5%

### Module 3: Preprocessing Pipeline
- **Research**: [modules/03-preprocessing-pipeline/RESEARCH.md](modules/03-preprocessing-pipeline/RESEARCH.md)
- **Focus**: 4 text processing techniques (Regex, NLTK, spaCy, Transformers)
- **Recommendation**: Hybrid - Regex (fast) + spaCy (neural-based)
- **Speed**: 5000+ documents/hour

### Module 4: Document Classification
- **Research**: [modules/04-document-classification/RESEARCH.md](modules/04-document-classification/RESEARCH.md)
- **Focus**: 4 classification algorithms (SVM, Random Forest, Logistic Regression, BERT)
- **Recommendation**: Random Forest baseline + BERT ensemble
- **Accuracy Target**: >90% overall, >85% per-class F1-score

### Module 5: Entity Extraction (NER)
- **Research**: [modules/05-entity-extraction/RESEARCH.md](modules/05-entity-extraction/RESEARCH.md)
- **Focus**: 4 NER methods (spaCy, BERT NER, CRF, BiLSTM-CRF)
- **Recommendation**: Hybrid - spaCy (fast) + BERT (accurate) for critical entities
- **Entities**: 9 types (Authority, Officer, Date, Monetary, Equipment, etc.)
- **Performance**: F1-score >85% target

### Module 6: Embeddings
- **Research**: [modules/06-embeddings/RESEARCH.md](modules/06-embeddings/RESEARCH.md)
- **Focus**: 4 embedding models (OpenAI, SentenceTransformers, BGE, E5)
- **Recommendation**: SentenceTransformers (all-MiniLM-L6-v2) - free, 2000-5000 embeds/hr CPU
- **Alternative**: BGE or E5 for better quality
- **Cost**: Free (vs OpenAI $20K/1B tokens)

### Module 7: Vector Database
- **Research**: [modules/07-vector-database/RESEARCH.md](modules/07-vector-database/RESEARCH.md)
- **Focus**: 4 vector DB solutions (FAISS, ChromaDB, Pinecone, Weaviate)
- **Recommendation**: ChromaDB (Phase 2-3), migrate to Weaviate (Phase 4+)
- **Scale**: 1M document capacity
- **Rationale**: Easy setup, dynamic indexing, no privacy concerns

### Module 8: Retrieval Algorithms
- **Research**: [modules/08-retrieval-algorithms/RESEARCH.md](modules/08-retrieval-algorithms/RESEARCH.md)
- **Focus**: 4 retrieval algorithms (Cosine Similarity, BM25, DPR, Hybrid)
- **Recommendation**: Hybrid (Dense + Sparse) with RRF fusion
- **Performance**: Recall@10 >0.80, Precision@5 >0.75
- **Reranking**: Cross-Encoder for quality improvement

### Module 9: RAG Architecture
- **Research**: [modules/09-rag-architecture/RESEARCH.md](modules/09-rag-architecture/RESEARCH.md)
- **Focus**: 5 RAG approaches (Traditional, Hybrid, Graph, Multi-query, Agentic)
- **Recommendation**: Hybrid RAG (Phase 2-3), Graph/Agentic (Phase 4+)
- **Hallucination**: 5-layer mitigation strategy, target <2%

### Module 10: Large Language Models
- **Research**: [modules/10-llm-research/RESEARCH.md](modules/10-llm-research/RESEARCH.md)
- **Focus**: 4 LLM options (GPT-4, Llama 3 70B, Mistral, Gemini)
- **Recommendation**: Llama 3 70B (long-term value) or GPT-4 (max quality)
- **Cost**: $300-500/1M tokens vs free infrastructure
- **Context**: 8K-128K token windows

### Module 11: Financial Analysis
- **Research**: [modules/11-financial-analysis/RESEARCH.md](modules/11-financial-analysis/RESEARCH.md)
- **Focus**: Financial entity extraction and analysis
- **Features**: Amount extraction, temporal association, authority linking
- **Accuracy Target**: >95% for amounts, >90% for authority association
- **Output**: Financial intelligence reports, aggregation analysis

### Module 12: Authority Identification
- **Research**: [modules/12-authority-identification/RESEARCH.md](modules/12-authority-identification/RESEARCH.md)
- **Focus**: Authority extraction and governance mapping
- **Methods**: NER + semantic mapping + hierarchy-based linking
- **Output**: Authority responsibility matrix, approval chain tracking
- **Accuracy Target**: >90% for authority recognition

---

## 🏗️ System Architecture

### Main Documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - Complete system design (1100+ lines)
  - 12 modular components
  - Data flow architecture
  - 9-stage query processing pipeline
  - Scalability considerations
  - Failure modes and monitoring

### Diagrams & Visualizations
- [Diagram Guide](diagrams/DIAGRAM_GUIDE.md) - 10 Mermaid diagrams explaining:
  1. High-level system architecture
  2. RAG query pipeline (sequence diagram)
  3. Document processing pipeline
  4. Entity extraction & authority mapping
  5. Financial analysis workflow
  6. Embedding & vector search
  7. Document classification hierarchy
  8. Data quality & monitoring
  9. Scalability architecture (Phase 4+)
  10. Error handling & fallbacks

---

## 🔄 Workflows

- [Workflow Orchestration](workflows/WORKFLOW_ORCHESTRATION.md) - Complete workflow documentation
  - 12 major workflows documented
  - Data collection & ingestion
  - Preprocessing & classification
  - Entity extraction & embedding
  - Query processing & retrieval
  - RAG & answer generation
  - Financial analysis (specialized)
  - Authority identification (specialized)
  - Monitoring & QA
  - System maintenance

---

## 📊 Evaluation & Benchmarking

### Evaluation Framework
- [Evaluation Framework](evaluation/EVALUATION_FRAMEWORK.md) - Comprehensive metrics system
  - Retrieval metrics (Precision@K, Recall@K, MAP, MRR, NDCG)
  - RAG/Answer quality (Faithfulness, Relevance, Hallucination, Context Precision)
  - Component-level metrics (OCR, Classification, NER accuracy)
  - Performance metrics (Latency, Throughput, Resource Utilization)
  - Benchmark datasets (500-1000 query-document pairs)
  - Human evaluation protocols
  - Quality assurance checklist
  - Continuous improvement process

---

## 📈 Planning & Implementation

### Research Roadmap
- [Research Roadmap](RESEARCH_ROADMAP.md) - 5-phase timeline
  - **Phase 1 (0-6 months)**: Research & Planning (current) - ₹50-75L
  - **Phase 2 (6-12 months)**: Development & Integration - ₹2-3 crores
  - **Phase 3 (12-18 months)**: Testing & Evaluation - ₹1.5-2 crores
  - **Phase 4 (18-24 months)**: Production Deployment - ₹3-4 crores
  - **Phase 5 (24+ months)**: Operations & Maintenance - ₹1.5-2 crores/year
  - **Total Project Cost**: ₹7-10 crores

### Phase 2 Development Plan
- [Phase 2 Implementation](implementation-roadmap/PHASE_2_DEVELOPMENT.md)
  - Sprint planning structure
  - 7 core development tasks (Data, Classification, Embeddings, RAG, etc.)
  - Technology stack decisions
  - Development milestones
  - Risk management strategy
  - Budget allocation (₹2-3 crores)
  - Success criteria

---

## 🎯 Use Cases & Applications

- [Real-World Scenarios](use-cases/REAL_WORLD_SCENARIOS.md) - 10 key use cases
  1. Strategic Defence Planning - 95% time reduction
  2. Budget Allocation Optimization - Data-driven planning
  3. Policy Compliance & Governance - Automated audit trails
  4. Intelligence & Capability Assessment - Comprehensive analysis
  5. Researcher Query Support - Academic research assistance
  6. Financial Transparency & RTI - Citizen engagement
  7. Risk & Vulnerability Assessment - Proactive management
  8. Administrative Efficiency - Succession planning
  9. Technology Transfer & Commercialization - Innovation pipeline
  10. Training & Education - Teaching materials

---

## 🔐 Security & Ethics

- [Security & Ethics](SECURITY_ETHICS.md) - Comprehensive framework (1000+ lines)
  - **Data Policy**: Public documents only, no classified information
  - **Hallucination Mitigation**: 5-layer defense strategy
  - **Security Architecture**: Access control, encryption, audit trails
  - **Bias & Fairness**: Monitoring and mitigation strategies
  - **Regulatory Compliance**: Public Data Act, RTI, GDPR-like principles
  - **Incident Response**: Procedures and escalation paths

---

## 🚀 Future Scope

- [Advanced Capabilities](future-scope/ADVANCED_CAPABILITIES.md) - Features for Phase 4-5
  - Graph-based retrieval
  - Agentic RAG systems
  - Multilingual support (Hindi/regional languages)
  - Advanced analytics (predictive, comparative, anomaly detection)
  - Visualization dashboards
  - Integration capabilities (government systems, mobile apps)
  - Enterprise features (multi-tenancy, RBAC, APIs)
  - LLM enhancements (multimodal, specialized models)
  - Security & privacy advancements
  - Operational maturity

---

## 📚 Comparison Matrices

- [Techniques Comparison Matrix](comparisons/TECHNIQUES_COMPARISON_MATRIX.md)
  - All 12 modules' techniques in one master table
  - Side-by-side comparisons for quick reference
  - Cost-effectiveness analysis
  - Integration complexity matrix
  - Recommendation summary for Phase 2 and Phase 4+

---

## 📖 Project Overview

- [README.md](README.md) - Main entry point (2800+ lines)
  - Project vision and mission
  - Objectives and scope
  - Data sources (10 public sources listed)
  - System architecture overview
  - Research modules summary
  - Evaluation strategy
  - Future scope preview
  - Navigation by user type (Technical, Business, Strategic)

---

## 🔍 Key Decisions Summary

### Technology Stack (Phase 2-3)
| Component | Choice | Rationale |
|-----------|--------|-----------|
| **OCR** | EasyOCR | Hindi support, accuracy >88%, free |
| **Text Processing** | spaCy + Regex | Fast, neural-based, contextual |
| **Classification** | Random Forest | >90% accuracy, interpretable, fast |
| **NER** | spaCy + BERT | Speed + accuracy hybrid |
| **Embeddings** | SentenceTransformers | Free, 2000-5000 embeds/hr, no privacy concerns |
| **Vector DB** | ChromaDB | 1M scale, dynamic indexing, easy setup |
| **Retrieval** | Hybrid (Dense+Sparse) | Recall >0.80, Precision >0.75 |
| **RAG** | Hybrid RAG | Good balance of speed and quality |
| **LLM** | Llama 3 or GPT-3.5 | Cost-effective with good quality |

### Key Performance Targets
- ✅ Retrieval Precision@5: >0.75
- ✅ Classification Accuracy: >90%
- ✅ NER F1-Score: >85%
- ✅ Answer Faithfulness: >95%
- ✅ Hallucination Rate: <2%
- ✅ End-to-End Latency: <5 seconds
- ✅ Processing Speed: 5000+ docs/hour

---

## 📋 File Organization

```
e:\projects\drdo\
├── README.md (Main overview)
├── ARCHITECTURE.md (System design)
├── SECURITY_ETHICS.md (Security & policies)
├── RESEARCH_ROADMAP.md (5-phase plan)
│
├── modules/ (12 research modules)
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
├── workflows/ (System workflows)
│   └── WORKFLOW_ORCHESTRATION.md
│
├── diagrams/ (Architecture diagrams)
│   └── DIAGRAM_GUIDE.md
│
├── evaluation/ (Quality assessment)
│   └── EVALUATION_FRAMEWORK.md
│
├── comparisons/ (Technique comparisons)
│   └── TECHNIQUES_COMPARISON_MATRIX.md
│
├── use-cases/ (Real-world applications)
│   └── REAL_WORLD_SCENARIOS.md
│
├── future-scope/ (Phase 4+ features)
│   └── ADVANCED_CAPABILITIES.md
│
├── implementation-roadmap/ (Development plans)
│   └── PHASE_2_DEVELOPMENT.md
│
├── algorithms/ (To be completed)
├── benchmarking/ (To be completed)
├── references/ (To be completed)
└── documentation/ (To be completed)
```

---

## 🎓 How to Use This Repository

### For Business Leaders
1. Start with [README.md](README.md) - Project vision
2. Review [RESEARCH_ROADMAP.md](RESEARCH_ROADMAP.md) - Timeline & budget
3. Check [Real-World Use Cases](use-cases/REAL_WORLD_SCENARIOS.md) - Applications
4. See [Phase 2 Plan](implementation-roadmap/PHASE_2_DEVELOPMENT.md) - Development roadmap

### For Technical Teams
1. Start with [ARCHITECTURE.md](ARCHITECTURE.md) - System design
2. Review individual [Modules](modules/) - Research & comparisons
3. Check [Diagrams](diagrams/DIAGRAM_GUIDE.md) - Visual architecture
4. Review [Workflows](workflows/WORKFLOW_ORCHESTRATION.md) - System processes
5. Study [Evaluation Framework](evaluation/EVALUATION_FRAMEWORK.md) - Quality metrics

### For Researchers
1. Review [Techniques Comparison](comparisons/TECHNIQUES_COMPARISON_MATRIX.md) - All techniques
2. Check individual [Modules](modules/) - Detailed comparisons
3. Review [Future Scope](future-scope/ADVANCED_CAPABILITIES.md) - Advanced topics

### For Project Managers
1. Review [RESEARCH_ROADMAP.md](RESEARCH_ROADMAP.md) - Phase structure
2. Check [Phase 2 Plan](implementation-roadmap/PHASE_2_DEVELOPMENT.md) - Development tasks
3. Review [Evaluation Framework](evaluation/EVALUATION_FRAMEWORK.md) - Success criteria

---

## 📊 Repository Statistics

- **Total Documents**: 20+ (with 70+ files in complete Phase 1)
- **Total Lines**: 12,000+ lines of research documentation
- **Modules**: 12 comprehensive research modules
- **Techniques Compared**: 4+ per module
- **Use Cases**: 10 real-world scenarios
- **Diagrams**: 10 architectural diagrams
- **Workflows**: 12 system workflows

---

## 🎯 Phase 1 Completion Status

✅ **Completed**:
- [x] Core documentation (README, ARCHITECTURE, SECURITY, ROADMAP)
- [x] All 12 research modules with technique comparisons
- [x] System architecture and design
- [x] Workflow documentation
- [x] Evaluation framework
- [x] Comparison matrices
- [x] Use cases and applications
- [x] Future scope planning
- [x] Phase 2 implementation plan

⏳ **Ready for Phase 2**:
- All research and planning complete
- Technology stack selected
- Success metrics defined
- Development roadmap established
- Team requirements documented
- Budget allocated (₹2-3 crores)

---

## 📞 Questions & Support

**For Questions About**:
- **System Design**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Specific Techniques**: Check individual module RESEARCH.md files
- **Implementation**: Review [Phase 2 Plan](implementation-roadmap/PHASE_2_DEVELOPMENT.md)
- **Evaluation**: See [Evaluation Framework](evaluation/EVALUATION_FRAMEWORK.md)
- **Use Cases**: Review [Real-World Scenarios](use-cases/REAL_WORLD_SCENARIOS.md)

---

**Last Updated**: May 26, 2026  
**Version**: 1.0 (Phase 1 Complete)  
**Status**: Ready for Phase 2 Implementation

---

*This repository represents a comprehensive defence-grade AI research proposal for the Defence Intelligence Retrieval and Analysis System (DIRAS), prepared for the Ministry of Defence and DRDO.*
