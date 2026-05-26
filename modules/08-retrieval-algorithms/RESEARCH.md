# Module 8: Retrieval Algorithms

## Research Document

---

## 1. Overview

The Retrieval Module finds relevant documents for user queries using multiple algorithms combined through hybrid search.

---

## 2. Retrieval Algorithm Comparison

### Algorithm 1: Cosine Similarity (Dense)

**Description**: Similarity between query and document embeddings

**Advantages**:
✅ Semantic understanding  
✅ Fast (vector operations)  
✅ Single embedding per document  

**Disadvantages**:
❌ Misses keyword matches  
❌ Needs good embeddings  

**Performance**: Recall@10: 0.65-0.75

---

### Algorithm 2: BM25 (Sparse)

**Description**: Probabilistic ranking function based on term frequencies

**Advantages**:
✅ Catches keyword matches  
✅ Fast search  
✅ Transparent (rule-based)  

**Disadvantages**:
❌ No semantic understanding  
❌ Struggles with synonyms  

**Performance**: Recall@10: 0.55-0.65

---

### Algorithm 3: Dense Passage Retrieval (DPR)

**Description**: Learning-to-rank using dense embeddings and negative mining

**Advantages**:
✅ Better semantic matching  
✅ Better than vanilla cosine  

**Disadvantages**:
❌ Requires training data  
❌ More complex  

**Performance**: Recall@10: 0.75-0.80

---

### Algorithm 4: Hybrid Search

**Description**: Combining dense and sparse retrieval with fusion

**Advantages**:
✅ Best of both worlds  
✅ Better recall  
✅ More robust  

**Disadvantages**:
❌ More complex  
❌ Tuning needed  

**Performance**: Recall@10: 0.80-0.85

---

## 3. Reranking Methods

### Cross-Encoder Reranking
- Re-score top-K retrieved documents
- More accurate ranking
- ~100ms per query with GPU

### Maximal Marginal Relevance (MMR)
- Reduce redundancy in results
- Ensure diverse results
- Preserve relevance

### Reciprocal Rank Fusion (RRF)
- Combine rankings from multiple methods
- Mathematically principled fusion
- Proven to work well

---

## 4. Recommendation

**Hybrid Retrieval Strategy**:

1. **Dense Retrieval**: Vector search (Cosine similarity)
2. **Sparse Retrieval**: BM25 keyword search
3. **Fusion**: Reciprocal Rank Fusion
4. **Reranking**: Cross-encoder (top-50 → top-5)

**Expected Performance**: Recall@10 > 0.80

---

## 5. Implementation

```
Query
    ↓
┌─ Dense Path:  Query → Embedding → Vector DB → Top-50
│                                    (Cosine Similarity)
└─ Sparse Path: Query → Tokenize → BM25 Index → Top-50
    ↓
Hybrid Fusion (RRF)
    ↓
Top-100 Ranked Results
    ↓
Cross-Encoder Reranking
    ↓
Top-5 Results
    ↓
Context Assembly
```

---

## 6. Performance Targets

✅ **Retrieval Precision@5**: >0.75  
✅ **Recall@10**: >0.80  
✅ **Retrieval Latency**: <200ms  
✅ **Throughput**: 100 queries/second  

---

*Last Updated: May 26, 2026*
