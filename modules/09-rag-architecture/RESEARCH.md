# Module 9: RAG Architecture Research

## Research Document

---

## 1. Overview

Retrieval-Augmented Generation combines information retrieval with LLM reasoning to ground answers in retrieved documents.

---

## 2. RAG Architectures Comparison

### Traditional RAG

**Description**: Simple retrieve-then-generate pipeline

**Flow**:
1. Retrieve top-K documents
2. Assemble context
3. Generate answer with LLM

**Advantages**:
✅ Simple to implement  
✅ Fast  
✅ Effective baseline  

**Disadvantages**:
❌ May miss relevant documents  
❌ Context assembly quality-dependent  

---

### Hybrid RAG

**Description**: Multiple retrieval methods combined

**Features**:
- Dense + sparse retrieval fusion
- Cross-encoder reranking
- Maximal marginal relevance
- Better recall

**Advantages**:
✅ Better recall  
✅ More robust  
✅ Handles diverse queries  

**Disadvantages**:
❌ More complex  
❌ Higher latency  

---

### Graph RAG

**Description**: Using knowledge graphs for retrieval

**Features**:
- Entity extraction
- Relationship graphs
- Graph-based retrieval
- Multi-hop reasoning

**Advantages**:
✅ Better for complex queries  
✅ Relationship understanding  

**Disadvantages**:
❌ Requires graph construction  
❌ More complex  

---

### Multi-Query RAG

**Description**: Decomposing complex queries

**Strategy**:
1. Original query → Decompose into sub-queries
2. Retrieve for each sub-query
3. Combine retrievals
4. Generate unified answer

**Advantages**:
✅ Better for complex questions  
✅ Comprehensive coverage  

**Disadvantages**:
❌ Higher latency  
❌ Complex coordination  

---

### Agentic RAG

**Description**: LLM as an agent with tools

**Features**:
- Iterative retrieval
- Tool usage (search, calculate)
- Reasoning loops
- Dynamic query refinement

**Advantages**:
✅ Complex problem solving  
✅ Adaptive  
✅ Multi-step reasoning  

**Disadvantages**:
❌ Highest latency  
❌ Complex implementation  
❌ Unpredictable execution  

---

## 3. Comparison Table

| Approach | Simplicity | Speed | Quality | Hallucination |
|----------|-----------|-------|---------|---------------|
| Traditional | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⚠️ Medium |
| Hybrid | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Lower |
| Graph | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Lower |
| Multi-Query | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Lower |
| Agentic | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ Lowest |

---

## 4. Recommendation for DIRAS

**Phase 2-3**: Hybrid RAG
- Good balance of speed and quality
- Dense + sparse retrieval
- Cross-encoder reranking
- Expected answer quality: 87-90%

**Phase 4+**: Graph RAG or Agentic RAG
- Complex defence questions
- Multi-hop reasoning
- Expected answer quality: 91-95%

---

## 5. RAG Pipeline

```
Query Input
    ↓
Query Understanding
    ├─ Intent classification
    ├─ Query expansion
    └─ Query decomposition (if complex)
    ↓
Retrieval (Hybrid)
    ├─ Dense retrieval
    ├─ Sparse retrieval
    └─ RRF fusion + reranking
    ↓
Context Assembly
    ├─ Top-5 documents
    ├─ Passage selection
    └─ Context window assembly (8K tokens)
    ↓
Prompt Construction
    ├─ System prompt (role, constraints)
    ├─ Retrieved context
    ├─ User query
    └─ Optional: Few-shot examples
    ↓
LLM Inference
    ├─ Generate answer
    ├─ Check grounding
    └─ Extract citations
    ↓
Post-Processing
    ├─ Format response
    ├─ Add citations
    ├─ Calculate confidence
    └─ Flag hallucinations
    ↓
Output (with citations)
```

---

## 6. Hallucination Mitigation

**Multi-layer Defense**:

1. **Architecture Level**: Only use retrieved context
2. **Prompt Level**: Explicit instructions against hallucination
3. **Validation Level**: Check claims against documents
4. **Human Level**: Manual review queue

**Target**: <2% hallucination rate

---

## 7. Performance Targets

✅ **Answer Relevance**: >90%  
✅ **Faithfulness**: >95%  
✅ **Hallucination Rate**: <2%  
✅ **Latency**: <5 seconds  

---

*Last Updated: May 26, 2026*
