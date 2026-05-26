# Module 7: Vector Database Research

## Research Document

---

## 1. Overview

The Vector Database stores embeddings for fast similarity search. This module evaluates different vector database solutions.

---

## 2. Vector Database Solutions Comparison

### FAISS (Facebook AI Similarity Search)

**Strengths**:
✅ Fast similarity search  
✅ Billions of vectors support  
✅ Open source  
✅ Excellent CPU/GPU optimization  
✅ Mature and production-tested  

**Limitations**:
❌ No built-in filtering  
❌ Static index (rebuild needed for updates)  
❌ No RBAC/security  
❌ In-memory only  

**Use Case**: Batch-oriented, large-scale search

---

### ChromaDB

**Strengths**:
✅ Easy to use  
✅ Built-in metadata filtering  
✅ Dynamic updates  
✅ Lightweight  
✅ Open source  

**Limitations**:
❌ Smaller scale (millions of vectors)  
❌ Slower than FAISS  
❌ Limited enterprise features  

**Use Case**: Development, medium-scale deployments

---

### Pinecone

**Strengths**:
✅ Fully managed cloud service  
✅ Built-in filtering, RBAC, replication  
✅ Scales to billions of vectors  
✅ Enterprise features  
✅ Easy deployment  

**Limitations**:
❌ Proprietary (data in cloud)  
❌ Cost ($0.4 per 1M vectors/month)  
❌ Vendor lock-in  
❌ Privacy concerns  

**Use Case**: Enterprise, cloud-first deployments

---

### Weaviate

**Strengths**:
✅ Self-hosted or cloud  
✅ Advanced filtering  
✅ GraphQL API  
✅ Multimodal support  
✅ Enterprise ready  

**Limitations**:
❌ More complex setup  
❌ Newer than alternatives  
❌ Higher resource requirements  

**Use Case**: Enterprise, complex filtering needs

---

## 3. Comparison Table

| Feature | FAISS | ChromaDB | Pinecone | Weaviate |
|---------|-------|----------|----------|----------|
| **Scale** | 1B+ vectors | 1M vectors | 1B+ vectors | 1B+ vectors |
| **Latency (p95)** | <100ms | <500ms | <100ms | <200ms |
| **Update Latency** | Minutes (rebuild) | <1s | <1s | <1s |
| **Metadata Filtering** | No | Yes | Yes | Yes |
| **RBAC/Security** | No | Limited | Yes | Yes |
| **Replication/HA** | No | No | Yes | Yes |
| **Cost** | Free | Free | $0.4/M vectors/mo | Free/paid |
| **Privacy** | Self-hosted only | Self-hosted | Cloud only | Both |
| **Learning Curve** | Steep | Easy | Easy | Medium |

---

## 4. Recommendation for DIRAS

**Primary**: ChromaDB (Phase 2-3)
- Easy setup and management
- Sufficient for 100K-1M documents
- No privacy concerns
- Free and open source

**Future**: Migrate to Weaviate (Phase 4+)
- Self-hosted on-premises
- Better enterprise features
- Advanced filtering capabilities
- RBAC and security

**Not Recommended**: Pinecone (data privacy concerns for defence)

---

## 5. Integration Strategy

```
Embeddings Generated
    ↓
Vector Database Writer
    ├─ Insert embeddings
    ├─ Add metadata (doc_id, chunk_id)
    └─ Index
    ↓
Vector Database
    (ChromaDB or Weaviate)
    ├─ Index for similarity search
    └─ Metadata store
    ↓
Vector Database Reader
    ├─ Query embeddings
    ├─ Similarity search (top-k)
    └─ Filter by metadata
```

---

## 6. Performance Targets

✅ **Query Latency**: <100ms (p95)  
✅ **Throughput**: 1000 queries/second  
✅ **Indexing Speed**: 10,000 vectors/second  
✅ **Memory Efficiency**: <200 bytes per vector  

---

*Last Updated: May 26, 2026*
