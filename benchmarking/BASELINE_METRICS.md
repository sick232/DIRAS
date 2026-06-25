# Baseline Metrics & Success Criteria - DIRAS Phase 2-5

**Document Version**: 1.0  
**Last Updated**: May 28, 2026  
**Scope**: Phase 1 targets to be measured in Phase 2-5  
**Focus**: Clear, measurable success criteria per module

---

## Executive Summary

This document defines baseline metrics and success criteria for all DIRAS modules, to be measured during Phase 2-5. Metrics organized by module with specific targets, measurement methodology, and escalation criteria.

---

## Metric Philosophy

- **Specific**: Each metric has clear definition, unit, methodology
- **Measurable**: Data-driven, trackable, reportable
- **Achievable**: Targets based on research + industry benchmarks
- **Relevant**: Aligned with project goals + user needs
- **Time-bound**: Measurement frequency + review schedule

---

## Phase 2 Baseline Metrics

### MODULE 1: OCR & Document Understanding

**Metric 1.1: Character Accuracy Rate**
```
Definition: (Characters correctly recognized) / (Total characters in ground truth)
Unit: Percentage (%)
Target: ≥90%
Measured on: Golden dataset (960 documents) + edge cases (OCR-heavy subset)
Frequency: Weekly during Phase 2
Pass/Fail Threshold:
  - ≥90%: PASS (acceptable)
  - 85-89%: WARN (needs optimization)
  - <85%: FAIL (blocker, needs immediate action)
```

**Metric 1.2: Word Accuracy Rate**
```
Definition: (Words correctly recognized) / (Total words in ground truth)
Unit: Percentage (%)
Target: ≥88%
Measured on: Golden dataset
Frequency: Weekly during Phase 2
Context: More important than character accuracy (user perspective)
```

**Metric 1.3: Table Extraction Accuracy**
```
Definition: (Correctly extracted table cells) / (Total cells in ground truth tables)
Unit: Percentage (%)
Target: ≥70%
Measured on: Documents with tables (subset of golden dataset)
Frequency: Bi-weekly
Note: Tables are challenging; 70% is realistic for Phase 2
```

**Metric 1.4: Layout Understanding Score**
```
Definition: (Correctly identified text blocks + order) / (Total blocks)
Unit: Percentage (%)
Target: ≥85%
Measured on: Complex layout documents (charts, multi-column)
Frequency: Bi-weekly
Context: LayoutParser contribution measurement
```

**Metric 1.5: Processing Latency (OCR)**
```
Definition: Time to OCR a single document
Unit: Seconds (s)
Target: <5s per page (avg 10-15 min for 200-page document)
Measured on: Golden dataset documents
Frequency: Weekly
Context: CPU vs. GPU impact measurement
```

---

### MODULE 2: Preprocessing Pipeline

**Metric 2.1: Information Retention Rate**
```
Definition: (Content preserved after preprocessing) / (Original content)
Unit: Percentage (%)
Target: ≥98%
Measured on: Golden dataset documents
Frequency: Bi-weekly
Context: Measure if lemmatization/stemming losing important terms
Calculation: 
  - Original tokens: N
  - Tokens after preprocessing: M
  - Retention = (M / N) * 100
```

**Metric 2.2: Preprocessing Latency**
```
Definition: Time to preprocess one document
Unit: Milliseconds (ms)
Target: <500ms per document (average)
Measured on: Golden dataset
Frequency: Weekly
Context: Pipeline efficiency (should be fast, not ML bottleneck)
```

**Metric 2.3: Duplicate Detection Rate**
```
Definition: (Near-duplicate documents correctly identified) / (Total near-duplicates in dataset)
Unit: Percentage (%)
Target: ≥90% (high precision: <1% false positives)
Measured on: Documents with known duplicates/near-duplicates
Frequency: Monthly
Context: Prevent inflated retrieval results
```

---

### MODULE 3: Document Classification

**Metric 3.1: Overall Classification Accuracy**
```
Definition: (Correctly classified documents) / (Total documents)
Unit: Percentage (%)
Target: ≥90%
Measured on: Golden dataset (960 documents, 10 classes)
Frequency: Weekly during Phase 2-3
Context: Macro accuracy across all classes
```

**Metric 3.2: Per-Class F1 Score**
```
Definition: F1 = 2 * (Precision * Recall) / (Precision + Recall)
Unit: Score (0-1)
Target per class:
  - Financial: F1 ≥0.92
  - Memorandum: F1 ≥0.92
  - Gazette: F1 ≥0.90
  - Guidelines: F1 ≥0.90
  - Procurement: F1 ≥0.85 (rare class)
  - Technical: F1 ≥0.88
  - Administrative: F1 ≥0.88
  - Security: F1 ≥0.85 (rare class)
  - Tender: F1 ≥0.88
  - Other: F1 ≥0.80
Frequency: Weekly
Context: Ensure no class is ignored (especially rare classes)
```

**Metric 3.3: Classification Confidence Distribution**
```
Definition: % of predictions with confidence >0.80, 0.70-0.80, <0.70
Unit: Percentage distribution (%)
Target: >80% predictions with confidence ≥0.80
Measured on: Test set predictions
Frequency: Monthly
Context: Low-confidence preds → human review flag
```

**Metric 3.4: Classification Speed**
```
Definition: Time to classify one document
Unit: Milliseconds (ms)
Target: <100ms per document
Measured on: Golden dataset
Frequency: Weekly
Context: Should be negligible compared to OCR/retrieval
```

---

### MODULE 4: Named Entity Recognition (NER)

**Metric 4.1: Authority NER F1 Score**
```
Definition: Entity-level F1 (exact boundary + label match)
Unit: Score (0-1)
Target: ≥0.85
Measured on: Test set with 1500+ authority annotations
Frequency: Bi-weekly during Phase 2-3
Components:
  - Precision ≥0.87 (low false positives)
  - Recall ≥0.83 (capture most entities)
```

**Metric 4.2: Monetary Value NER F1 Score**
```
Definition: Entity-level F1 for amounts + currency
Unit: Score (0-1)
Target: ≥0.80
Measured on: Test set with 1500+ monetary annotations
Frequency: Bi-weekly
Components:
  - Precision ≥0.82
  - Recall ≥0.78
Context: Finance critical; lower bar than authority due to currency variations
```

**Metric 4.3: Date Entity F1 Score**
```
Definition: Entity-level F1 for temporal expressions
Unit: Score (0-1)
Target: ≥0.78
Measured on: Test set with 1000+ date annotations
Frequency: Bi-weekly
Context: Date format variations (15-03-2024 vs. March 15, 2024)
```

**Metric 4.4: Overall NER Token F1 Score**
```
Definition: F1 at token level (BIO tagging accuracy)
Unit: Score (0-1)
Target: ≥0.82
Measured on: All entity types combined
Frequency: Weekly
Context: More stringent than entity-level F1
```

**Metric 4.5: NER Processing Latency**
```
Definition: Time to extract entities from one document
Unit: Seconds (s)
Target: <2s per document
Measured on: Golden dataset
Frequency: Weekly
Context: Fast enough for real-time extraction
```

---

### MODULE 5: Embedding Generation

**Metric 5.1: Semantic Similarity Correlation**
```
Definition: Pearson correlation between embedding distance + semantic similarity
Unit: Correlation coefficient (0-1)
Target: ≥0.75
Measured on: Golden dataset document pairs + manually rated similarity scores
Frequency: Bi-weekly
Context: Measure if embeddings capture semantic meaning
Methodology:
  1. Select 500 document pairs from golden set
  2. Rate similarity 0-1 (domain expert)
  3. Compute embedding cosine distance
  4. Calculate Pearson correlation
```

**Metric 5.2: Embedding Inference Speed**
```
Definition: Time to generate embedding for one document
Unit: Milliseconds (ms)
Target: <50ms per document (CPU), <10ms (GPU)
Measured on: Golden dataset documents
Frequency: Weekly
Variants:
  - CPU latency: <50ms
  - GPU latency: <10ms
  - Batch latency (100 docs): <200ms (CPU), <50ms (GPU)
```

**Metric 5.3: Embedding Consistency**
```
Definition: Cosine similarity between embeddings of same doc generated at different times
Unit: Score (0-1)
Target: ≥0.99 (near-deterministic)
Measured on: Repeated embedding generation
Frequency: Monthly
Context: Ensure reproducibility
```

**Metric 5.4: Embedding Model Baseline Comparison**
```
Definition: Compare multiple embedding models on semantic similarity task
Unit: Correlation score (0-1)
Target: Select model with score ≥0.75
Models evaluated:
  - SentenceTransformers (all-MiniLM) - baseline
  - OpenAI Embeddings (if budget allows)
  - BGE Embeddings
  - E5 Embeddings
Frequency: Once at end of Phase 2
Context: Model selection critical for downstream retrieval
```

---

### MODULE 6: Vector Database & Retrieval

**Metric 6.1: Vector Database Query Latency**
```
Definition: Time to retrieve K nearest neighbors from vector DB
Unit: Milliseconds (ms)
Target (Phase 2): <100ms for K=100 queries on 1M vectors
Target (Phase 3): <100ms for K=100 queries on 5-10M vectors
Measured on: Query benchmark set against golden dataset vectors
Frequency: Weekly
Components:
  - p50 (median): <50ms
  - p95 (95th percentile): <100ms
  - p99 (99th percentile): <200ms
```

**Metric 6.2: Retrieval Precision@K**
```
Definition: (Relevant docs in top K) / K
Unit: Percentage (0-100%)
Targets:
  - Precision@5: ≥80%
  - Precision@10: ≥80%
  - Precision@50: ≥70%
Measured on: Benchmark query set (200 queries, golden dataset)
Frequency: Weekly during Phase 2-3
Context: Critical for user experience (results quality)
```

**Metric 6.3: Retrieval Recall@K**
```
Definition: (Relevant docs retrieved) / (Total relevant docs)
Unit: Percentage (%)
Targets:
  - Recall@50: ≥85%
  - Recall@100: ≥90%
Measured on: Benchmark query set
Frequency: Weekly
Context: Ensure we don't miss important documents
```

**Metric 6.4: Mean Reciprocal Rank (MRR)**
```
Definition: 1/K where K is rank of first relevant document
Unit: Score (0-1)
Target: ≥0.75
Measured on: Benchmark query set
Frequency: Weekly
Context: Measure how early relevant docs appear
```

**Metric 6.5: Normalized Discounted Cumulative Gain (NDCG)**
```
Definition: Ranking quality metric considering relevance scores
Unit: Score (0-1)
Target: ≥0.75
Measured on: Benchmark query set with relevance grades (0, 1, 2)
Frequency: Weekly
Variants:
  - NDCG@10: ≥0.78
  - NDCG@50: ≥0.75
```

**Metric 6.6: Vector DB Indexing Speed**
```
Definition: Time to index new documents (build vector indices)
Unit: Vectors per second
Target: ≥100 vectors/sec (with GPU), ≥10 vectors/sec (CPU)
Measured on: Batch indexing of golden dataset
Frequency: Monthly (after updates)
Context: Important for continuous indexing in production
```

---

### MODULE 7: RAG Pipeline

**Metric 7.1: Hallucination Rate**
```
Definition: (Hallucinated statements in RAG output) / (Total statements)
Unit: Percentage (%)
Target: ≤5%
Measured on: Benchmark query set with LLM-generated answers
Frequency: Bi-weekly during Phase 3-4
Context: Critical for defence domain (must be factually accurate)
Methodology:
  1. Run 50 queries through RAG pipeline
  2. Manual review of answers (domain expert)
  3. Flag hallucinations
  4. Calculate rate
```

**Metric 7.2: Answer Relevance**
```
Definition: Semantic similarity(user query, LLM answer)
Unit: Score (0-1)
Target: ≥0.88
Measured on: Benchmark query set
Frequency: Bi-weekly
Context: Measure if LLM answer addresses the query
Methodology:
  1. Embed query + answer
  2. Calculate cosine similarity
  3. Average across queries
```

**Metric 7.3: Answer Faithfulness (Ragas)**
```
Definition: "Facts in answer that can be verified in retrieved context"
Unit: Percentage (%)
Target: ≥90%
Measured on: Benchmark query set
Frequency: Bi-weekly
Context: Ragas framework (LLM-based evaluation)
```

**Metric 7.4: Context Precision**
```
Definition: (Relevant context chunks in top K) / K
Unit: Percentage (%)
Target: ≥80%
Measured on: Benchmark query set
Frequency: Bi-weekly
Context: Measure if retrieval provides good context for RAG
```

**Metric 7.5: RAG Latency End-to-End**
```
Definition: Time from query input to final answer generation
Unit: Seconds (s)
Target: <2s per query (Phase 2-3), <1s (Phase 4+)
Breakdown:
  - Retrieval: <100ms
  - Context compression: <100ms
  - LLM inference: 1-2s (most of latency)
Frequency: Weekly
```

**Metric 7.6: LLM Model Comparison**
```
Definition: Compare multiple LLMs on RAG quality metrics
Unit: Composite score (Hallucination + Relevance + Faithfulness)
Models evaluated (Phase 3):
  - Llama 3 70B (baseline)
  - Llama 3 8B (speed)
  - Mistral 7B (cost)
  - GPT-4 (quality)
Frequency: Once per phase
Context: Model selection critical
```

---

### MODULE 8: Financial Analysis

**Metric 8.1: Monetary Value Extraction Accuracy**
```
Definition: (Correctly extracted amounts) / (Total amounts in ground truth)
Unit: Percentage (%)
Target: ≥85%
Measured on: Golden dataset documents with 1500+ monetary annotations
Frequency: Bi-weekly
Components:
  - Amount accuracy: Extract ₹5000 correctly (not ₹5,00,0)
  - Currency accuracy: Distinguish INR vs. USD
  - Context accuracy: Financial vs. non-financial amounts
```

**Metric 8.2: Authority Approval Mapping Accuracy**
```
Definition: (Correctly identified approving authority) / (Ground truth authorities)
Unit: Percentage (%)
Target: ≥80%
Measured on: Golden dataset documents with authority annotations
Frequency: Bi-weekly
Context: Critical for financial auditability
```

**Metric 8.3: Procurement Analysis Accuracy**
```
Definition: Extract tender ID, amount, timeline, authority correctly
Unit: F1 score (0-1)
Target: ≥0.78
Measured on: Procurement documents subset
Frequency: Bi-weekly
Components:
  - Tender ID extraction: F1 ≥0.85
  - Amount extraction: F1 ≥0.82
  - Timeline extraction: F1 ≥0.75
```

---

### MODULE 9: Authority Identification

**Metric 9.1: Authority Hierarchy Extraction Accuracy**
```
Definition: "Correctly map authority relationships (reports-to, approves)"
Unit: Accuracy (%)
Target: ≥80%
Measured on: Golden dataset with explicit hierarchy annotations
Frequency: Monthly
Context: How well system understands approval chains
```

**Metric 9.2: Authority Disambiguation Accuracy**
```
Definition: When multiple entities named "Ministry", correctly identify specific one
Unit: Accuracy (%)
Target: ≥85%
Measured on: Documents with ambiguous references
Frequency: Bi-weekly
```

---

### MODULE 10: Query Understanding

**Metric 10.1: Intent Classification F1**
```
Definition: F1 for classifying query into 6 categories (financial, procurement, etc.)
Unit: Score (0-1)
Target: ≥0.80
Measured on: Benchmark query set (200 queries, 6 intent types)
Frequency: Bi-weekly
Per-intent targets:
  - Financial: F1 ≥0.85
  - Procurement: F1 ≥0.80
  - Authority: F1 ≥0.82
  - Guideline: F1 ≥0.78
  - General: F1 ≥0.75
  - Edge case: F1 ≥0.70
```

**Metric 10.2: Query Expansion Coverage**
```
Definition: "Expanded query retrieves more relevant docs than original"
Unit: Improvement (%)
Target: ≥15% improvement in recall
Measured on: Benchmark query set
Frequency: Monthly
Context: Query expansion should improve retrieval without hurting precision
```

---

## Phase 3-5 Targets (Incremental Improvement)

### Phase 3 Targets (Month 3-4)
Expect 10-15% improvement from Phase 2 baselines:

| Module | Phase 2 | Phase 3 | Improvement |
|--------|---------|---------|-------------|
| OCR Accuracy | 88% | 92% | +4% |
| Classification F1 | 0.88 | 0.91 | +3% |
| NER F1 | 0.82 | 0.85 | +3% |
| Retrieval P@10 | 0.80 | 0.83 | +3% |
| Hallucination Rate | 8% | 5% | -3% |
| RAG Latency | 2.0s | 1.5s | -25% |

### Phase 4 Targets (Month 5-8)
Additional 10-15% improvement, optimized systems:

| Module | Phase 3 | Phase 4 | Improvement |
|--------|---------|---------|-------------|
| OCR Accuracy | 92% | 94% | +2% |
| Classification F1 | 0.91 | 0.93 | +2% |
| Retrieval P@10 | 0.83 | 0.86 | +3% |
| Hallucination Rate | 5% | 2% | -3% |
| RAG Latency | 1.5s | 0.8s | -47% |
| System Availability | 99.5% | 99.9% | - |

### Phase 5 Targets (Month 9-12)
Operational targets, cost optimization:

| Module | Phase 4 | Phase 5 | Notes |
|--------|---------|---------|-------|
| OCR Accuracy | 94% | 94%+ | Maintain |
| Classification F1 | 0.93 | 0.93+ | Maintain |
| Retrieval P@10 | 0.86 | 0.87+ | Continuous improvement |
| Hallucination Rate | 2% | 1% | Improve with better context |
| RAG Latency | 0.8s | 0.5s | Cache optimization |
| Cost per Query | ₹0.50 | ₹0.10 | 5x improvement |
| System Availability | 99.9% | 99.99% | Enterprise-grade |

---

## Success Criteria Summary Table

| Module | Phase 2 Target | Phase 3 Target | Phase 4 Target | Phase 5 Target |
|--------|---|---|---|---|
| **OCR** | 88% word acc. | 92% | 94% | 94%+ |
| **Classification** | F1 0.88 | F1 0.91 | F1 0.93 | F1 0.93+ |
| **NER** | F1 0.82 | F1 0.85 | F1 0.87 | F1 0.87+ |
| **Retrieval** | P@10 0.80 | P@10 0.83 | P@10 0.86 | P@10 0.87+ |
| **RAG** | 8% halluc. | 5% halluc. | 2% halluc. | 1% halluc. |
| **Latency** | <2s | <1.5s | <0.8s | <0.5s |
| **Availability** | 99% | 99.5% | 99.9% | 99.99% |

---

## Metric Dashboards & Tracking

### Dashboard 1: Module Performance (Weekly)
- OCR accuracy trend (7-day moving average)
- Classification F1 per class (bar chart)
- NER F1 per entity type
- Retrieval P@10, Recall@50, MRR
- RAG hallucination rate + answer relevance

### Dashboard 2: System Health (Daily)
- API latency p50/p95/p99
- Error rate (%)
- Query throughput (queries/sec)
- Vector DB size (vectors, storage)
- Cost per query (₹)

### Dashboard 3: Phase Progress (Monthly)
- Metric vs. Phase target (% complete)
- Risk items (metrics below target)
- Burndown chart (story points)
- Team velocity (velocity trend)
- Blocking issues

---

## Escalation Criteria

### CRITICAL (Immediate action required)
- Any metric <70% of Phase target
- System availability <95%
- Hallucination rate >10%
- P@10 <0.70 (retrieval broken)
- **Action**: Halt new features, debug root cause, escalate to PM

### MAJOR (Address within 1 week)
- Metric 70-80% of Phase target
- Availability 95-99%
- Hallucination 5-10%
- **Action**: Root cause analysis, assign engineer, plan fix

### MINOR (Address in next sprint)
- Metric 80-90% of Phase target
- Latency 20% slower than target
- **Action**: Planning + implementation in normal sprint

---

**Document Owner**: QA Lead + Technical Lead  
**Next Review**: June 30, 2026 (Phase 2 Kickoff + Baseline Establishment)  
**Update Frequency**: Weekly (metric runs), Monthly (strategy review)

---

*Metrics drive discipline. Weekly tracking prevents metric surprises at phase gates.*
