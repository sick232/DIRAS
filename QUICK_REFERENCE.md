# Quick Reference Guide

## DIRAS - Quick Lookup for Key Information

---

## 🎯 System Overview (30 seconds)

**What**: Defence Intelligence Retrieval and Analysis System  
**Purpose**: AI-powered search & analysis of public defence documents  
**Architecture**: RAG (Retrieval-Augmented Generation) pipeline  
**Tech Stack**: Python, SentenceTransformers, ChromaDB, LangChain, GPT/Llama  
**Cost**: ₹7-10 crores (5 years), ₹2-3 crores (Phase 2)

---

## 🔑 Key Numbers

| Metric | Target |
|--------|--------|
| Documents to index | 10,000 (Phase 2), 1M+ (Phase 4) |
| Answer speed | <5 seconds (p95) |
| Hallucination rate | <2% |
| Classification accuracy | >90% |
| Entity extraction F1 | >85% |
| Answer faithfulness | >95% |
| Processing speed | 5000+ docs/hour |
| Team size (Phase 2) | 12-15 engineers |

---

## 📂 Where to Find What

### For Business/Leadership
- **Budget & Timeline**: [RESEARCH_ROADMAP.md](RESEARCH_ROADMAP.md)
- **ROI & Use Cases**: [REAL_WORLD_SCENARIOS.md](use-cases/REAL_WORLD_SCENARIOS.md)
- **Phase 2 Plan**: [PHASE_2_DEVELOPMENT.md](implementation-roadmap/PHASE_2_DEVELOPMENT.md)

### For Technical Teams
- **System Design**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Technology Stack**: [TECHNIQUES_COMPARISON_MATRIX.md](comparisons/TECHNIQUES_COMPARISON_MATRIX.md)
- **Workflows**: [WORKFLOW_ORCHESTRATION.md](workflows/WORKFLOW_ORCHESTRATION.md)

### For Researchers
- **Detailed Comparisons**: Individual [Module files](modules/)
- **Master Comparison**: [TECHNIQUES_COMPARISON_MATRIX.md](comparisons/TECHNIQUES_COMPARISON_MATRIX.md)
- **Future Capabilities**: [ADVANCED_CAPABILITIES.md](future-scope/ADVANCED_CAPABILITIES.md)

### For Project Managers
- **Timeline**: [RESEARCH_ROADMAP.md](RESEARCH_ROADMAP.md)
- **Success Criteria**: [EVALUATION_FRAMEWORK.md](evaluation/EVALUATION_FRAMEWORK.md)
- **Development Tasks**: [PHASE_2_DEVELOPMENT.md](implementation-roadmap/PHASE_2_DEVELOPMENT.md)

---

## 📊 12 Modules At A Glance

| # | Module | Recommendation | Key Metric |
|----|--------|---|---|
| 1 | Dataset Collection | APIs + Web Scraping | 50-100 docs/day |
| 2 | OCR | EasyOCR | 88-94% accuracy |
| 3 | Preprocessing | spaCy + Regex | 5000+ docs/hour |
| 4 | Classification | Random Forest | >90% accuracy |
| 5 | Entity Extraction | spaCy + BERT | F1 >85% |
| 6 | Embeddings | SentenceTransformers | Free, 2000-5000 embeds/hr |
| 7 | Vector DB | ChromaDB | 1M document scale |
| 8 | Retrieval | Hybrid Dense+Sparse | Recall@10 >0.80 |
| 9 | RAG | Hybrid RAG | Quality >4.0/5.0 |
| 10 | LLM | Llama 3 or GPT-3.5 | Cost-effective quality |
| 11 | Financial Analysis | Hybrid Rule+Transformer | >95% accuracy |
| 12 | Authority ID | Hierarchy-based | >90% accuracy |

---

## 🏗️ System Architecture (1-page)

```
Data Sources (MOD, DRDO, Gazette, PIB...)
         ↓
    Ingestion (Scraping, APIs, Download)
         ↓
    Processing (OCR → Clean → Classify → Extract)
         ↓
    Embedding (SentenceTransformers)
         ↓
    Storage (ChromaDB + BM25)
         ↓
    User Query
         ↓
    Retrieval (Dense + Sparse + Rerank)
         ↓
    RAG (LLM generates answer)
         ↓
    Output (With citations)
```

---

## 📈 5-Phase Timeline

| Phase | Duration | Cost | Focus | Team |
|-------|----------|------|-------|------|
| 1 | 6 mo | ₹75L | Research | 5-8 |
| 2 | 6 mo | ₹2.5Cr | Development | 12-15 |
| 3 | 6 mo | ₹1.75Cr | Testing | 8-12 |
| 4 | 6 mo | ₹3.5Cr | Production | 10-12 |
| 5 | Ongoing | ₹1.75Cr/yr | Operations | 5-8 |

**Total**: ₹7-10 crores (first 2 years)

---

## 🎯 Top 3 Use Cases

1. **Strategic Planning** - Find all ₹100+ crore procurements (95% time saved)
2. **Budget Analysis** - Track spending patterns (80% time saved)
3. **Compliance Audit** - Verify policy adherence (70% time saved)

---

## 💡 Key Technology Decisions

**Self-Hosted > Cloud APIs**:
- ChromaDB (not Pinecone) - privacy & cost
- SentenceTransformers (not OpenAI) - free & fast
- Llama 3 (not GPT-4 only) - cost-effective

**Hybrid Approaches**:
- Regex + spaCy (fast + smart preprocessing)
- Dense + Sparse retrieval (recall optimization)
- Rule-based + ML (financial analysis)

**Graceful Degradation**:
- Multiple retrieval fallbacks
- Confidence scoring at each stage
- Manual review queue for uncertain results

---

## ✅ Phase 1 Deliverables

- [x] 12 research modules (7,000+ lines)
- [x] System architecture (1,100+ lines)
- [x] Security framework (1,000+ lines)
- [x] Implementation roadmap (1,200+ lines)
- [x] 10 architecture diagrams
- [x] 12 system workflows
- [x] 40+ evaluation metrics
- [x] Comparison matrices
- [x] 10 use case scenarios
- [x] Phase 2 development plan

**Total**: 20+ documents, 12,000+ lines

---

## 🚀 Ready for Phase 2?

### Checklist
- [x] Research complete
- [x] Technology stack selected
- [x] Architecture validated
- [x] Team requirements defined
- [x] Budget allocated
- [x] Success metrics defined
- [x] Risk mitigation planned

### Start Phase 2 By
1. Review [INDEX.md](INDEX.md) - Get oriented
2. Approve technology stack
3. Recruit Phase 2 team
4. Plan sprint schedule
5. Set up development environment

---

## 📞 Quick Questions

**Q: What's the total cost?**  
A: ₹7-10 crores (5 years), ₹2-3 crores for Phase 2 development

**Q: How long to get answers?**  
A: <5 seconds end-to-end, from question to answer

**Q: What documents are supported?**  
A: 10 public government sources - MOD, DRDO, Gazette, PIB, Parliament, CAG, etc. (public only)

**Q: Can it hallucinate?**  
A: Yes, but <2% target with 5-layer mitigation strategy

**Q: What about Hindi documents?**  
A: Supported via EasyOCR and SentenceTransformers (future upgrade planned)

**Q: When is Phase 2 starting?**  
A: After approval of Phase 1 + team recruitment (ready to start immediately)

---

## 📚 Essential Reading (in order)

1. **5 min**: [README.md](README.md) - Project overview
2. **10 min**: [RESEARCH_ROADMAP.md](RESEARCH_ROADMAP.md) - Budget & timeline
3. **15 min**: [ARCHITECTURE.md](ARCHITECTURE.md) - System design
4. **10 min**: [TECHNIQUES_COMPARISON_MATRIX.md](comparisons/TECHNIQUES_COMPARISON_MATRIX.md) - Tech decisions
5. **5 min**: [REAL_WORLD_SCENARIOS.md](use-cases/REAL_WORLD_SCENARIOS.md) - Use cases

**Total**: 45 minutes to understand entire system

---

## 🎓 Complete Learning Path

**For Business Leaders** (1 hour):
- README.md → RESEARCH_ROADMAP.md → REAL_WORLD_SCENARIOS.md

**For Technical Leads** (2 hours):
- ARCHITECTURE.md → TECHNIQUES_COMPARISON_MATRIX.md → PHASE_2_DEVELOPMENT.md

**For Full Understanding** (4 hours):
- All core docs + Select modules by interest

---

## Repository Structure (Quick)

```
drdo/
├── README.md ⭐ START HERE
├── ARCHITECTURE.md
├── SECURITY_ETHICS.md
├── RESEARCH_ROADMAP.md
├── INDEX.md (Full navigation)
│
├── modules/ (12 research modules)
├── workflows/ (System workflows)
├── diagrams/ (Architecture diagrams)
├── evaluation/ (Metrics)
├── comparisons/ (Tech comparison)
├── use-cases/ (Real scenarios)
├── future-scope/ (Phase 4+)
└── implementation-roadmap/ (Phase 2 plan)
```

---

## Last Updated

**Date**: May 26, 2026  
**Version**: 1.0 - Phase 1 Complete  
**Status**: ✅ Ready for Phase 2 Implementation

---

*For more information, start with INDEX.md or README.md*
