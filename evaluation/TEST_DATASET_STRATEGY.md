# Test Dataset Strategy & Benchmark Methodology - DIRAS Phase 2-5

**Document Version**: 1.0  
**Last Updated**: May 28, 2026  
**Focus**: Golden dataset creation, benchmark queries, edge case validation  
**Timeline**: Creation during Phase 2, Refinement during Phases 3-4

---

## Executive Summary

This document defines strategy for creating test datasets that measure DIRAS performance across all modules. Includes golden datasets (hand-curated), benchmark queries, edge cases, and annotation guidelines to ensure fair, reproducible evaluation.

---

## Test Dataset Architecture

```
DIRAS Evaluation Suite
│
├─ Golden Dataset (500-1000 documents)
│  ├─ Hand-curated test documents
│  ├─ Ground truth annotations
│  └─ Per-module relevance labels
│
├─ Benchmark Query Set (100-200 queries)
│  ├─ Financial queries (20)
│  ├─ Procurement queries (20)
│  ├─ Authority queries (20)
│  ├─ Guideline queries (20)
│  ├─ General queries (20)
│  └─ Edge case queries (20)
│
├─ Edge Case Dataset (100-200 documents)
│  ├─ OCR-heavy PDFs
│  ├─ Multilingual documents
│  ├─ Complex layouts (tables, charts)
│  ├─ Small font sizes
│  └─ Damaged/scanned documents
│
├─ NER Annotation Dataset (5000-10000 entities)
│  ├─ Authority names (1000)
│  ├─ Departments (500)
│  ├─ Monetary values (1000)
│  ├─ Dates (500)
│  └─ Projects/Equipment (500)
│
└─ Classification Training Data (3000-5000 documents)
   ├─ Financial (600)
   ├─ Procurement (400)
   ├─ Guidelines (500)
   ├─ Gazette (500)
   ├─ Memorandum (600)
   ├─ Technical (400)
   ├─ Administrative (300)
   ├─ Security (200)
   └─ Tender (500)
```

---

## 1. Golden Dataset (500-1000 Documents)

### 1.1 Golden Dataset Purpose
- **Goal**: Comprehensive benchmark for all downstream modules
- **Use case**: Baseline metrics + regression testing
- **Maintenance**: Fixed throughout project (not changed after Phase 2)
- **Quality**: Hand-curated by domain experts (not automated)

### 1.2 Composition

| Document Type | Count | Source | Annotation |
|----------------|-------|--------|-----------|
| **Financial Reports** | 100 | Ministry, DRDO | Expenditure amounts, approving authority |
| **Gazette Publications** | 150 | Gazette of India | Document type, date, authority |
| **Procurement Notices** | 80 | Defence ministry | Tender ID, amount, authority |
| **Guidelines/Circulars** | 100 | Ministry, DRDO | Effective date, target audience |
| **Memorandums** | 150 | Ministry | Date, approving authority, key decisions |
| **Parliamentary Reports** | 100 | Parliament website | Parliament references, key findings |
| **Press Releases** | 100 | PIB | Date, ministry, key facts |
| **Audit Reports** | 80 | CAG, Ministry | Audit findings, entities involved |
| **Technical Papers** | 50 | DRDO | Research area, key findings |
| **Other** | 50 | Mixed sources | - |
| **Total** | **960** | - | **100% annotated** |

### 1.3 Annotation Schema (Golden Dataset)

**Metadata per document**
```json
{
  "doc_id": "GD-001",
  "filename": "Ministry_Defence_2024_Budget_Report.pdf",
  "source": "Ministry of Defence",
  "document_type": "financial_report",
  "publication_date": "2024-03-15",
  "language": "English",
  "page_count": 45,
  "ocr_quality": "high",  // high/medium/low
  "contains_tables": true,
  "contains_images": false,
  
  "annotations": {
    "authorities": [
      {"name": "Ministry of Defence", "type": "ministry"},
      {"name": "Department of Defence Finance", "type": "department"}
    ],
    "monetary_values": [
      {"amount": "5000000000", "currency": "INR", "context": "defence allocation"}
    ],
    "dates": [
      {"date": "2024-03-15", "context": "publication date"}
    ],
    "key_topics": ["defence spending", "budget allocation", "military equipment"],
    "relevance_to_modules": {
      "ocr": 1.0,  // How relevant (0-1)
      "classification": 0.95,
      "ner": 0.85,
      "financial_analysis": 0.95
    }
  }
}
```

### 1.4 Golden Dataset Creation Process

**Phase 2 Timeline (3-4 weeks)**

| Week | Activity | Owner | Deliverable |
|------|----------|-------|-------------|
| 1 | Select 100 representative documents per type | Data Eng | Document list + sources |
| 2 | OCR all documents, manual inspection | Data Eng + QA | OCR output + quality assessment |
| 3-4 | Annotation + quality checks | QA Eng + Domain Expert | Annotated dataset, inter-annotator agreement κ |

**Annotation Process**
1. 2-3 domain experts independently annotate each document
2. Calculate inter-annotator agreement (Cohen's κ)
3. Resolve disagreements in consensus meeting
4. Final review by QA engineer
5. Version control (git-track all annotations)

**Quality Gates**
- Inter-annotator agreement κ ≥ 0.80 (substantial agreement)
- 100% documents reviewed + approved
- Annotation completeness: all fields filled (no missing data)

---

## 2. Benchmark Query Set (100-200 Queries)

### 2.1 Query Categories

**Category 1: Financial Queries (20 queries)**
```
Q1: "What was the total defence expenditure in 2023?"
Q2: "Which ministry approved the ₹5000 crore defence budget?"
Q3: "Find all budget allocations for the Navy."
Q4: "What was the expenditure on military procurement last year?"
Q5: "How much was allocated to DRDO research?"
... (15 more financial queries)
```

**Expected answers**:
- Exact numbers from documents
- Time periods
- Approving authorities
- Department-wise breakdown

**Retrieval Targets**:
- Precision@5: ≥0.80 (retrieve financial documents in top 5)
- Recall@50: ≥0.90 (capture all relevant financial documents)

---

**Category 2: Procurement Queries (20 queries)**
```
Q1: "What were the tender details for defence equipment procurement?"
Q2: "Find all procurement notices issued by the Air Force."
Q3: "What was the estimated cost of the Rafale aircraft procurement?"
Q4: "Which authority approved the defence procurement policy?"
Q5: "List all ammunition procurement projects."
... (15 more procurement queries)
```

**Expected answers**:
- Tender documents
- Procurement amounts
- Equipment specifications
- Timeline / authority
- Procurement authority

**Retrieval Targets**:
- Precision@5: ≥0.75 (some procurement noise acceptable)
- Recall@50: ≥0.85

---

**Category 3: Authority Identification Queries (20 queries)**
```
Q1: "Who is responsible for defence budget approval?"
Q2: "Which department handles military procurement?"
Q3: "What is the hierarchy of defence decision-making?"
Q4: "Who approves new defence policies?"
Q5: "Which authority can override defence procurement decisions?"
... (15 more authority queries)
```

**Expected answers**:
- Department names
- Ministry names
- Officer titles / roles
- Approval chains
- Authority relationships

**Entity Extraction Targets**:
- Authority NER F1: ≥0.85
- Hierarchy mapping accuracy: ≥0.80

---

**Category 4: Guideline Queries (20 queries)**
```
Q1: "What are the guidelines for defence procurement?"
Q2: "What is the procedure for defence budget allocation?"
Q3: "What are the security requirements for defence documents?"
Q4: "What guidelines govern defence equipment export?"
Q5: "What are the criteria for defence facility authorization?"
... (15 more guideline queries)
```

**Expected answers**:
- Circular/guideline documents
- Procedure steps
- Approval criteria
- Timeline requirements

**Classification Targets**:
- Guideline document classification F1: ≥0.85

---

**Category 5: General Knowledge Queries (20 queries)**
```
Q1: "What is the mandate of the Ministry of Defence?"
Q2: "What are the main defence organizations in India?"
Q3: "What is the scope of DRDO research?"
Q4: "What are the types of defence documents?"
Q5: "How are defence documents classified?"
... (15 more general queries)
```

**Expected answers**:
- Institutional information
- Organizational structure
- Scope / definitions
- Classification schemes

**Retrieval Targets**:
- Precision@10: ≥0.70
- Recall@50: ≥0.75

---

**Category 6: Edge Case / Adversarial Queries (20 queries)**
```
Q1: "Find documents with conflicting budget amounts." (test: conflicting info handling)
Q2: "What was allocated vs. actually spent on defence?" (test: comparing different doc types)
Q3: "Find policy updates that supersede previous policies." (test: version handling)
Q4: "Which procurement tenders were cancelled?" (test: handling negative info)
Q5: "Retrieve documents with incomplete authority information." (test: handling incomplete data)
Q6: "Find documents where OCR failed for key terms." (test: OCR robustness)
Q7: "Retrieve multilingual documents (Hindi + English)." (test: language handling)
Q8: "Find documents with table-based financial data." (test: table extraction)
Q9: "What was allocated to non-existent departments?" (test: catching errors)
Q10: "Find outdated documents vs. current policy." (test: temporal understanding)
... (10 more edge cases)
```

**Expected answers**: Varied (system should handle gracefully)

---

### 2.2 Query Annotation Schema

```json
{
  "query_id": "Q-FIN-001",
  "query_text": "What was the total defence expenditure in 2023?",
  "category": "financial",
  "difficulty": "medium",  // easy/medium/hard
  "relevant_documents": [
    {"doc_id": "GD-001", "relevance_score": 0.95},
    {"doc_id": "GD-045", "relevance_score": 0.80},
    {"doc_id": "GD-102", "relevance_score": 0.60}
  ],
  "expected_answer": "₹5.8 trillion (approx)",
  "expected_answer_source": "GD-001 (pages 12-15)",
  "intent": "retrieval",  // retrieval/calculation/summarization
  "entities_required": ["amount", "year"],
  "complexity": 1,  // 1=simple, 3=complex multi-hop
}
```

### 2.3 Benchmark Query Creation Timeline

**Phase 2 (2-3 weeks)**
- Week 1: Define query categories + write 100 queries (3-4 queries per category)
- Week 2: Test queries against golden dataset (verify expected answers exist)
- Week 3: Refine + finalize 200-query benchmark set

**Quality Gates**
- All queries have ground truth answers verified
- Difficulty distribution: 30% easy, 50% medium, 20% hard
- Clear expected answers documented

---

## 3. Edge Case Dataset (100-200 Documents)

### 3.1 Edge Case Types

**OCR-Heavy PDFs** (20 documents)
- Scanned documents (1980-2000s era)
- Poor image quality
- Skewed pages
- Mixed fonts / handwriting
- Expected OCR accuracy: 70-85% (lower than golden set)

**Multilingual Documents** (15)
- Hindi + English code-switching
- English official text, Hindi summary
- Legal jargon in both languages
- Expected retrieval accuracy: 70% (harder than pure English)

**Complex Layouts** (15)
- Documents with tables (financial tables, expense lists)
- Documents with charts/images
- Multi-column layouts
- Embedded lists + bullet points
- Expected table extraction accuracy: 60-75% (challenging)

**Small Font / Low Resolution** (10)
- Documents with <8pt font
- Compressed scans
- Microfilm quality
- Expected OCR: 60-70% accuracy

**Damaged/Degraded** (10)
- Water-damaged documents
- Ink smudges, stamps overlaid on text
- Fading text
- Expected OCR: 50-65% accuracy

**Very Long Documents** (10)
- 100+ page government reports
- Test chunking strategy + retrieval
- Test handling of long context windows
- Expected latency: 2-5 seconds (higher than normal)

**Duplicate/Near-Duplicate** (10)
- Same document in multiple formats (PDF, scanned image)
- Updated versions of same document
- Test deduplication strategy
- Expected dedup accuracy: ≥95%

**Temporal/Version Variations** (8)
- Policy documents with multiple versions
- Amendment notices attached to original
- Superseded policies
- Test version handling, temporal queries
- Expected accuracy: 80% (identify correct version)

---

### 3.2 Edge Case Evaluation Process

**Phase 3 (During module optimization)**

For each edge case, measure:
```
Edge Case Metric = 
  (Accuracy on Edge Case) / (Accuracy on Golden Set)
  
Target: Edge Case Metric ≥ 0.70
  (i.e., accuracy drops by max 30% on edge cases)
```

**If Edge Case Metric < 0.70**:
1. Investigate root cause (OCR? chunking? embeddings?)
2. Add preprocessing rule or special handling
3. Retrain model if needed
4. Retest until metric ≥ 0.70

---

## 4. NER Annotation Dataset (5000-10000 Entities)

### 4.1 Entity Types

| Entity Type | Expected Count | Examples |
|-------------|----------------|----------|
| **Authority** | 1,500 | Ministry of Defence, Department of Finance |
| **Department** | 800 | Air Force, Navy, Defence Research |
| **Organization** | 800 | DRDO, BDL, HAL |
| **Officer/Rank** | 600 | Secretary of Defence, Wing Commander |
| **Monetary Amount** | 1,500 | ₹5000 crores, $10 million, 100,000 USD |
| **Date** | 1,000 | 15-03-2024, March 15, 2024, Q3 FY2024 |
| **Equipment/Project** | 500 | Rafale fighter, INS Vikrant, Agni missile |
| **Location** | 300 | Bangalore, New Delhi, Hyderabad |
| **Policy/Law** | 400 | Defence Procurement Policy 2020, DPM 2013 |
| **Other** | 100 | - |
| **Total** | **≥7,000** | - |

### 4.2 NER Annotation Schema

**Format: CoNLL BIO Tagging**
```
Ministry B-ORG
of O
Defence I-ORG
approved O
a O
budget B-MONETARY
of O
₹5000 I-MONETARY
crores I-MONETARY
on O
15 B-DATE
March I-DATE
2024 I-DATE
```

**Per-token fields**:
- Token: word/subword
- Label: B-ENT (Begin), I-ENT (Inside), O (Outside)
- Confidence: human annotator confidence (0-1)
- Source doc: which document

### 4.3 NER Dataset Creation

**Phase 2-3 (6-8 weeks)**

**Week 1-2**: Annotation guidelines creation
- Define entity boundaries (does "Ministry of Defence" include "of Defence"?)
- Example annotations for each type
- Consensus rules for ambiguous cases

**Week 3-6**: Annotation
- 5-10 annotators (domain experts)
- Collaborative annotation tool (Prodigy, Label Studio)
- Inter-annotator agreement tracking (κ ≥ 0.80 target)

**Week 7-8**: Review + finalization
- Conflict resolution (majority vote or expert decision)
- Quality checks (no missing annotations)

**Quality Gates**
- Inter-annotator agreement κ ≥ 0.80
- 100% entity coverage (all entities found)
- Boundary accuracy ≥0.95 (correct start/end tokens)

---

## 5. Classification Training Dataset (3000-5000 Documents)

### 5.1 Document Type Distribution

| Type | Target Count | Source | Balance |
|------|----------|--------|---------|
| Financial | 600 | Ministry, Budget docs | Balanced |
| Procurement | 400 | Procurement portal | Imbalanced (rare) |
| Guidelines | 500 | Circulars, DPM | Balanced |
| Gazette | 500 | Gazette of India | Balanced |
| Memorandum | 600 | Ministry memos | Balanced |
| Technical | 400 | DRDO reports | Balanced |
| Administrative | 300 | Admin circulars | Balanced |
| Security | 200 | Security-related | Imbalanced (rare) |
| Tender | 500 | Procurement notices | Balanced |
| **Total** | **≥3,900** | - | **Balanced across types** |

### 5.2 Handling Class Imbalance

**Strategy**:
1. Oversample rare classes (procurement, security) to match majority
2. Use weighted loss during training (penalize rare class errors more)
3. Separate eval metrics per class (not just overall accuracy)
4. Set per-class minimum F1 target (not just macro-average)

**Target F1 per class**:
- High-frequency classes (Financial, Memorandum, Gazette): ≥0.90
- Medium-frequency (Guidelines, Technical): ≥0.88
- Low-frequency (Procurement, Security): ≥0.85 (lower bar, but still strict)

---

## 6. Test Dataset Maintenance & Versioning

### 6.1 Version Control

**Git-tracked test datasets**
```
/test-data/
├─ golden-dataset/
│  ├─ v1.0/ (Phase 2 initial)
│  │  ├─ documents/
│  │  ├─ annotations.json
│  │  └─ README.md
│  └─ v1.1/ (Phase 3 refinements)
│
├─ benchmark-queries/
│  ├─ v1.0/
│  │  └─ queries.json
│  └─ v1.1/
│
├─ edge-cases/
│  └─ v1.0/
│
└─ training-data/
   ├─ classification/
   │  ├─ v1.0/
   │  └─ v1.1/
   └─ ner/
      ├─ v1.0/
      └─ v1.1/
```

### 6.2 Frozen vs. Evolving Datasets

**Frozen** (no changes after Phase 2):
- Golden dataset (baseline for regression testing)
- Benchmark queries (ensure comparable metrics over time)

**Evolving** (updated as project progresses):
- Edge case dataset (add new edge cases discovered in production)
- Training datasets (add annotated data for fine-tuning)

### 6.3 Changelog

```
v1.0 (End of Phase 2):
- Initial golden dataset: 960 documents, all annotated
- Benchmark queries: 200 queries, all verified
- NER training: 7,000 entities annotated
- Classification training: 3,900 documents labeled

v1.1 (Phase 3):
- Golden dataset + 50 edge cases discovered in production
- Benchmark queries + 10 new adversarial queries (stress testing)
- NER training + 1,000 new entities from Phase 3 corrections
- Classification training + 500 misclassified documents re-annotated
```

---

## 7. Annotation Tool & Infrastructure

### 7.1 Recommended Tools

**Option 1: Prodigy** (Commercial, ₹3-5 L/year)
- Advantages: Custom workflows, active learning support
- Disadvantages: Paid, requires technical setup
- Use case: Complex annotations (NER, entity relations)

**Option 2: Label Studio** (Open-source, self-hosted)
- Advantages: Free, flexible, good UI
- Disadvantages: Manual setup required, active learning limited
- Use case: All annotation types

**Option 3: Doccano** (Open-source, self-hosted)
- Advantages: Free, simple setup
- Disadvantages: Limited for complex annotations
- Use case: Document classification, simple labeling

**Recommendation**: Use Label Studio (free, sufficient capabilities)

### 7.2 Annotation Interface Setup

```
Label Studio Instance
│
├─ Project 1: Golden Dataset Annotation
│  ├─ Task: Entity extraction (authorities, dates, amounts)
│  ├─ Annotators: 3 domain experts
│  ├─ Consensus: Majority vote
│  └─ Agreement threshold: κ ≥ 0.80
│
├─ Project 2: Classification Annotation
│  ├─ Task: Document type classification
│  ├─ Annotators: 2 annotators
│  ├─ Consensus: Majority vote
│  └─ Agreement threshold: κ ≥ 0.80
│
└─ Project 3: Benchmark Query Validation
   ├─ Task: Verify query answers in golden dataset
   ├─ Annotators: QA team
   └─ Consensus: All must agree
```

---

## 8. Evaluation Metrics Definition

### 8.1 Metrics by Module

**OCR Module**
```
Character Accuracy = (Correctly recognized chars) / (Total chars in ground truth)
Word Accuracy = (Correctly recognized words) / (Total words in ground truth)
Target: Char Acc ≥90%, Word Acc ≥88%
Measured on: Golden dataset + edge cases
```

**Classification Module**
```
Per-class F1 = 2 * (Precision * Recall) / (Precision + Recall)
Macro F1 = Average F1 across all classes
Weighted F1 = F1 weighted by class frequency
Target: Macro F1 ≥0.88
Minimum per-class: Financial/Memorandum ≥0.90, Procurement/Security ≥0.85
```

**NER Module**
```
Token F1 = F1 at token level (BIO tagging)
Entity F1 = F1 at entity level (exact boundary match)
Per-entity-type F1 = F1 for each entity type
Target: Entity F1 ≥0.85 for authorities, ≥0.80 for monetary/dates
```

**Retrieval Module**
```
Precision@K = (Relevant docs in top K) / K
Recall@K = (Relevant docs retrieved) / (Total relevant docs)
MAP = Mean Average Precision (ranking quality)
MRR = Mean Reciprocal Rank (1st relevant position)
NDCG = Normalized Discounted Cumulative Gain (ranking with relevance scores)
Target: P@10 ≥0.80, Recall@100 ≥0.85, MRR ≥0.75
```

**RAG Module**
```
Faithfulness = (Facts in answer that are in retrieved docs) / (Total facts)
Answer Relevance = Semantic similarity(query, answer)
Hallucination Rate = (Hallucinated statements) / (Total statements)
Context Precision = (Relevant context in top K) / K
Target: Faithfulness ≥0.90, Hallucination Rate ≤5%
```

---

## 9. Benchmark Execution Schedule

### Phase 2 (Test Data Creation)
- **Week 1-2**: Finalize dataset schemas + create annotation guidelines
- **Week 3-4**: Create/collect documents for golden set, benchmark queries
- **Week 5-6**: Annotation (golden set, benchmarks, NER partial)
- **Week 7-8**: Finalization + quality checks

### Phase 3 (Ongoing Annotation + Evaluation)
- **Week 1-4**: Continue NER + classification annotation
- **Weekly**: Run benchmarks on latest model
- **Monthly**: Report metric trends vs. baselines
- **Identify**: Edge cases for Phase 4 optimization

### Phase 4 (Refinement)
- Add 50-100 new edge cases discovered in production
- Expand NER/classification training data based on errors
- Run comprehensive multi-region evaluation

### Phase 5 (Maintenance)
- Monthly benchmark runs (regression testing)
- Archive old benchmarks (document model evolution)
- Update baselines as system improves

---

## Appendix: Inter-Annotator Agreement Calculation

**Cohen's Kappa Formula**:
```
κ = (P_o - P_e) / (1 - P_e)

Where:
  P_o = observed agreement (annotators agree)
  P_e = expected agreement by chance
```

**Interpretation**:
- κ > 0.80: Substantial agreement ✓
- 0.60-0.80: Moderate agreement (acceptable, refine guidelines)
- 0.40-0.60: Fair agreement (redo annotation, clarify labels)
- < 0.40: Poor agreement (major issues)

**Example**: 3 annotators, 100 documents
```
Annotator 1 vs 2: κ = 0.82 ✓
Annotator 2 vs 3: κ = 0.79 (acceptable)
Annotator 1 vs 3: κ = 0.85 ✓
Average: κ = 0.82 (Substantial agreement)
```

---

**Document Owner**: QA Lead + Data Engineering  
**Next Review**: August 15, 2026 (Golden Dataset Completion)  
**Approval**: [Pending Phase 2 Project Kickoff]

---

*Golden dataset is foundation for all Phase 2-5 evaluation. Invest in quality annotation to avoid later rework.*
