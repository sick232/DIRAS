# Evaluation Framework

## Comprehensive Metrics for System Quality Assessment

---

## 1. Overview

This framework defines how we measure system performance across all components and the end-to-end system.

---

## 2. Retrieval Metrics

### Precision@K

**Definition**: Of the top-K retrieved documents, what % are relevant?

**Formula**: Relevant documents in top-K / K

**Targets**:
- Precision@5: >0.75
- Precision@10: >0.70

---

### Recall@K

**Definition**: Of all relevant documents, what % appear in top-K?

**Formula**: Retrieved relevant documents / Total relevant documents

**Targets**:
- Recall@10: >0.80
- Recall@20: >0.85

---

### Mean Average Precision (MAP)

**Definition**: Average of precision at each relevant document position

**Targets**: MAP@20 > 0.65

---

### Mean Reciprocal Rank (MRR)

**Definition**: Average of reciprocal rank of first relevant document

**Formula**: 1/N * Σ(1/rank of first relevant)

**Targets**: MRR > 0.70

---

### Normalized Discounted Cumulative Gain (NDCG)

**Definition**: Ranking quality considering position of relevant documents

**Targets**: NDCG@10 > 0.72

---

## 3. RAG/Answer Quality Metrics

### Faithfulness

**Definition**: % of claims in answer that are grounded in retrieved documents

**Measurement**: Human evaluation on sample of 100 answers

**Targets**: >95% faithfulness

---

### Answer Relevance

**Definition**: % of answer that addresses the user's query

**Measurement**: Human evaluation (Likert scale 1-5)

**Targets**: >4.0/5.0 average

---

### Hallucination Rate

**Definition**: % of answers containing false or unsupported claims

**Measurement**: Fact-checking against retrieved documents

**Targets**: <2% hallucination rate

---

### Context Precision

**Definition**: % of top-K retrieved documents that are actually relevant

**Targets**: >85% on test set

---

## 4. Component-Level Metrics

### OCR Accuracy

**Metrics**:
- Character Error Rate (CER): <8%
- Word Error Rate (WER): <5%

### Classification Accuracy

**Metrics**:
- Overall Accuracy: >90%
- Per-class F1-score: >85%
- Confusion matrix analysis

### Entity Extraction

**Metrics**:
- Precision: >90% (minimize false positives)
- Recall: >85% (minimize false negatives)
- F1-score: >87%
- Per-entity-type metrics

---

## 5. Performance Metrics

### Latency

**Targets**:
- Query embedding: <100ms
- Retrieval: <200ms
- LLM inference: 1-3 seconds
- End-to-end (p95): <5 seconds

### Throughput

**Targets**:
- 1000+ queries/second capacity
- 10,000+ documents/hour indexing

### Resource Utilization

**Targets**:
- Memory: <16GB for core system
- GPU memory (optional): <8GB
- CPU: <4 cores for baseline operations

---

## 6. Benchmark Datasets

### Test Set Creation

**Size**: Minimum 500 query-document pairs

**Composition**:
- 60% simple factual queries
- 20% multi-hop reasoning
- 15% comparative queries
- 5% edge cases

**Human Annotation**:
- Multiple annotators per query
- Inter-annotator agreement >0.85 (Cohen's Kappa)
- Conflict resolution procedure

---

## 7. Human Evaluation Protocol

### Annotation Guidelines

**For Retrieval**:
- Relevant if answers user's query
- 4-level relevance: Not Relevant, Somewhat, Relevant, Highly Relevant

**For Answers**:
- Factuality (0-5): Is answer true based on documents?
- Relevance (0-5): Does answer address query?
- Completeness (0-5): Does answer cover all aspects?

### Evaluation Process

1. Create evaluation set (100-500 examples)
2. Recruit annotators (minimum 2 per example)
3. Annotation round
4. Calculate agreement
5. Resolve conflicts
6. Final metrics

---

## 8. Quality Assurance Checklist

### Before Deployment
- [ ] Retrieval Precision@5 >0.75
- [ ] RAG Hallucination Rate <2%
- [ ] Entity Extraction F1 >0.87
- [ ] Classification Accuracy >90%
- [ ] End-to-end latency <5s (p95)
- [ ] No security vulnerabilities
- [ ] Documentation complete
- [ ] Team trained

### Regular Monitoring (Monthly)
- [ ] Collect user feedback
- [ ] Monitor key metrics
- [ ] Identify degradation
- [ ] Plan improvements
- [ ] Update documentation

### Quarterly Reviews
- [ ] Full quality assessment
- [ ] Benchmark on latest test set
- [ ] Performance trend analysis
- [ ] Plan optimizations
- [ ] Update roadmap

---

## 9. Continuous Improvement Process

**Feedback Loop**:
1. Collect user queries and feedback
2. Analyze errors and failures
3. Identify improvement opportunities
4. Implement fixes or retraining
5. Re-evaluate on test set
6. Deploy improvements

**Quarterly A/B Tests**:
- Test new retrieval methods
- Test new ranking approaches
- Test new LLM prompts
- Compare against baseline
- Deploy if improvements >2%

---

## 10. External Benchmarks

**Standard Benchmarks**:
- MS MARCO (passage retrieval)
- Natural Questions (QA)
- SQuAD (reading comprehension)
- TREC (information retrieval)

**Defence-Specific Benchmarks**:
- Create internal test set
- Annotate by domain experts
- Publish benchmarks if possible

---

*Last Updated: May 26, 2026*
