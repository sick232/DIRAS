# Module 6: Embeddings & Vector Representations

## Research Document

---

## 1. Overview

The Embeddings Module converts text into dense vector representations that capture semantic meaning. These embeddings enable semantic search and similarity-based retrieval.

---

## 2. Embedding Models Comparison

### Model 1: OpenAI Embeddings (text-embedding-3)

**Description**: Proprietary embedding model by OpenAI (API-based)

**Specifications**:
- Embedding Dimension: 1536 (3072 optional)
- Input: Up to 8,000 tokens
- Cost: $0.02 per 1M tokens

**Advantages**:
✅ State-of-the-art quality  
✅ No infrastructure needed  
✅ API access, no model download  
✅ Excellent multilingual support  
✅ Regular updates  

**Disadvantages**:
❌ Proprietary (data privacy concerns)  
❌ API costs (recurring)  
❌ Latency dependent on API  
❌ Internet connectivity required  
❌ Limited control  

**Performance**: 
- Retrieval Quality: Excellent
- Cost per 1B embeddings: $20,000

---

### Model 2: Sentence Transformers (all-mpnet-base-v2, all-MiniLM-L6-v2)

**Description**: Open-source pre-trained models from Hugging Face

**Specifications**:
- Embedding Dimension: 384-768
- Models: 6M-335M parameters
- Speed: 1000-5000 embeddings/sec (CPU), 50000+/sec (GPU)

**Advantages**:
✅ Open source, free  
✅ No API costs  
✅ Can run locally  
✅ Fast inference  
✅ Good quality  
✅ Multiple model sizes  
✅ Hindi support available  

**Disadvantages**:
❌ Slightly lower quality than OpenAI  
❌ Requires model management  
❌ Need GPU for speed  
❌ Storage and memory needed  

**Performance**:
- Retrieval Quality: Very Good
- Cost: Free (self-hosted)

---

### Model 3: BGE Embeddings (Alibaba)

**Description**: Optimized embeddings from Alibaba's research team

**Specifications**:
- Embedding Dimension: 768
- Models: Base and large variants
- Speed: 2000-10000 embeddings/sec

**Advantages**:
✅ Excellent quality  
✅ Optimized for retrieval  
✅ Open source  
✅ Good multilingual support  
✅ No API costs  

**Disadvantages**:
❌ Newer (less community adoption)  
❌ Requires GPU for good speed  
❌ Smaller model zoo  

**Performance**:
- Retrieval Quality: Excellent
- Cost: Free (self-hosted)

---

### Model 4: E5 Embeddings (Microsoft)

**Description**: Efficient embeddings from Microsoft Research

**Specifications**:
- Embedding Dimension: 384-1024
- Models: Small, base, large variants
- Speed: 3000-15000 embeddings/sec

**Advantages**:
✅ Very high quality  
✅ Open source  
✅ Multiple size options  
✅ Efficient (fast on CPU)  
✅ Good multilingual  
✅ Specifically designed for retrieval  

**Disadvantages**:
❌ Requires model downloads  
❌ Some setup needed  
❌ Newer (less adoption)  

**Performance**:
- Retrieval Quality: Excellent
- Cost: Free (self-hosted)

---

## 3. Detailed Comparison Table

| Aspect | OpenAI | Sentence-BERT | BGE | E5 |
|--------|--------|---------------|-----|-----|
| **Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Speed (CPU)** | Depends on API | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Speed (GPU)** | Depends on API | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Cost** | $20K/1B embeds | Free | Free | Free |
| **Privacy** | ⚠️ Proprietary | ✅ Local | ✅ Local | ✅ Local |
| **Model Size** | Unknown | 22-335M params | 110-335M params | 22-335M params |
| **Multilingual** | Excellent | Very Good | Excellent | Excellent |
| **Defence Domain** | Good | Good | Very Good | Very Good |
| **Deployment** | Cloud API | Self-hosted | Self-hosted | Self-hosted |

---

## 4. Recommended Choice for DIRAS

**Decision**: Sentence-Transformers (all-MiniLM-L6-v2 or all-mpnet-base-v2)

**Rationale**:
1. ✅ Open source - No licensing concerns
2. ✅ No API costs - Significant cost savings at scale
3. ✅ Local control - Data never leaves server
4. ✅ Fast enough - 2000-5000 embeddings/sec on single CPU
5. ✅ Good quality - Near-OpenAI quality on retrieval tasks
6. ✅ Hindi models available - Future multilingual support
7. ✅ Mature and battle-tested

**Model Selection**:
- **Phase 2-3**: `all-MiniLM-L6-v2` (faster, lighter)
  - 22M parameters, 384 dimensions
  - 3000+ embeddings/sec on CPU
  - Good balance of speed and quality

- **Phase 5+ (if needed)**: `all-mpnet-base-v2` (better quality)
  - 110M parameters, 768 dimensions
  - 1500+ embeddings/sec on CPU
  - Better semantic understanding

---

## 5. Embedding Strategy

### Text Chunking
**Problem**: Documents too long to embed as single unit

**Solution**: Chunk documents into passages
- Chunk size: 384 tokens (~1500 characters)
- Chunk overlap: 64 tokens (for context preservation)
- Strategy: Preserve sentence boundaries

### Embedding Generation
```
Document
    ↓
Chunk into passages (384 tokens each, 64-token overlap)
    ↓
Generate embedding for each passage
    ↓
Store in vector database with metadata (chunk ID, document ID)
    ↓
Ready for similarity search
```

### Query Embedding
```
User Query
    ↓
Clean and normalize query
    ↓
Generate embedding using same model
    ↓
Search against stored passage embeddings
    ↓
Retrieve most similar passages
```

---

## 6. Embedding Quality Metrics

**Intrinsic Metrics**:
- Correlation with human similarity judgments
- Downstream task performance (retrieval quality)

**Extrinsic Metrics**:
- Retrieval Recall@K (how many relevant docs retrieved)
- MRR, NDCG (ranking quality)
- Human evaluation of relevance

**Target**: Recall@10 > 0.75, MRR > 0.60

---

## 7. Scaling Embeddings

**Volume Projections**:
- Year 1: 10K documents → ~50K embeddings (chunks) → 19MB storage
- Year 3: 50K documents → ~250K embeddings → 96MB storage
- Year 5: 100K documents → ~500K embeddings → 192MB storage

**Processing Speed**:
- Single CPU: 2000-3000 embeddings/hour
- 10,000 documents (50K embeddings): ~20 hours to embed
- Solution: GPU acceleration (50K embeddings/hour on GPU)

**Batch Processing Strategy**:
- Batch 1000 passages at a time
- Process in parallel on multiple GPUs
- Daily incremental updates

---

## 8. Defence-Specific Considerations

**Terminology**:
- Pre-trained models may not understand defence jargon
- Consider fine-tuning on defence corpus (Phase 5+)
- Current models adequate for retrieval tasks

**Domain Adaptation**:
- Could fine-tune on defence documents
- Would improve semantic understanding
- Requires 1000s of paired examples

---

## 9. Implementation Roadmap

| Task | Timeline |
|------|----------|
| Download and test SentenceTransformers | Week 1 |
| Implement chunking strategy | Week 1-2 |
| Set up embedding pipeline | Week 2-3 |
| Batch embedding generation | Week 3-4 |
| Embedding quality evaluation | Week 4-5 |
| Integration with vector database | Week 5-6 |
| Performance optimization | Week 6-7 |
| Production deployment | Week 7-8 |

---

## 10. Performance Targets

✅ **Embedding Generation**: 3000+ passages/hour (CPU)  
✅ **Embedding Dimension**: 384 (all-MiniLM) or 768 (all-mpnet)  
✅ **Storage per Document**: ~2-4KB per passage  
✅ **Retrieval Quality**: Recall@10 > 0.75  
✅ **Latency**: <100ms to embed a query  

---

## 11. Tools & Libraries

**Sentence Transformers**:
- sentence-transformers library
- PyTorch backend
- Hugging Face integration

**Vector Operations**:
- NumPy (vector operations)
- scikit-learn (similarity computations)

**Storage**:
- Vector database (FAISS, ChromaDB, Pinecone)

---

## Next Steps

1. Download SentenceTransformers model
2. Benchmark embedding quality on test documents
3. Design chunking strategy for defence documents
4. Set up batch embedding pipeline
5. Integrate with vector database

---

*Last Updated: May 26, 2026*
