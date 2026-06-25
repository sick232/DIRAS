# DIRAS Phase 2: 100% FREE Technology Stack

**Objective**: Complete Phase 2 implementation with ZERO paid services  
**Last Updated**: May 28, 2026  
**All tools**: Open-source, self-hosted, or free-tier with no restrictions

---

## 🎯 FREE Stack Components

| Component | Technology | Cost | Notes |
|-----------|-----------|------|-------|
| **OCR** | EasyOCR | FREE | Open-source, 88-94% accuracy |
| **Layout** | LayoutParser | FREE | Open-source, complex layouts |
| **NLP** | spaCy | FREE | Open-source NLP, production-ready |
| **BERT** | HuggingFace Transformers | FREE | Open-source, fine-tuning included |
| **Embeddings** | SentenceTransformers | FREE | Open-source, 384-dim vectors |
| **Vector DB** | ChromaDB | FREE | Open-source, no subscription |
| **Search** | Elasticsearch (OSS) | FREE | Open-source version (no X-Pack) |
| **Reranking** | Cross-Encoder (HF) | FREE | Open-source models |
| **RAG** | LangChain | FREE | Open-source framework |
| **LLM** | Llama 3 70B | FREE | Open-source (Ollama/vLLM) |
| **Backend** | FastAPI | FREE | Open-source web framework |
| **Orchestration** | Docker | FREE | Open-source container runtime |
| **CI/CD** | GitHub Actions | FREE | Free tier (2000 mins/month) |
| **Monitoring** | Prometheus + Grafana | FREE | Open-source stack |
| **Database** | PostgreSQL | FREE | Open-source relational DB |
| **Storage** | Local NAS/Network Storage | FREE | On-premises, no cloud costs |
| **Git** | GitHub | FREE | Free tier (public/private repos) |
| **Code Editor** | VS Code | FREE | Open-source editor |
| **IDE** | Jupyter | FREE | Open-source notebooks |

---

## ⚡ KEY COST ELIMINATIONS

### ❌ Removed (Paid Options)
- ❌ OpenAI GPT-3.5/GPT-4 (₹50-100K+/month)
- ❌ AWS/Azure cloud infrastructure (₹2-5L/month)
- ❌ Weights & Biases (₹5K+/month)
- ❌ Commercial annotation tools
- ❌ Managed vector DB (Pinecone, Weaviate Cloud)

### ✅ Replaced With (Free Alternatives)
- ✅ Llama 3 70B locally (via Ollama or vLLM) - **SAME QUALITY, ZERO COST**
- ✅ Local NAS + Docker (on-premises servers) - **ONE-TIME HARDWARE, NO RECURRING COST**
- ✅ Label Studio (open-source annotation tool) - **FREE, SELF-HOSTED**
- ✅ ChromaDB (open-source vector DB) - **FREE, SELF-HOSTED**
- ✅ Prometheus + Grafana (open-source monitoring) - **FREE, SELF-HOSTED**

---

## 💰 Phase 2 Cost Breakdown (FREE VARIANT)

### Hardware (One-time, keep Phase 2-5)
```
Main Server (GPU): ₹3-4L
- 16-core CPU, 256GB RAM, 8x GPU (for Llama 3 inference)
- Used for: LLM inference, data processing
- Cost: ₹3-4L (amortized across 4 phases)

NAS Storage: ₹50-70K
- 20TB storage, RAID-6 redundancy
- Used for: Document storage, backups
- Cost: ₹50-70K (one-time)

Network: ₹10K/month
- 1Gbps internet connection
- Used for: VPN, backups to cloud (cold storage only)
- Cost: ₹10K/month (already paying for office)

Total Phase 2 Hardware: ₹4-4.5L (one-time)
```

### Software (Recurring, FREE)
```
Open-source stack: ₹0
- EasyOCR, LayoutParser, spaCy, BERT, Transformers
- SentenceTransformers, ChromaDB, Elasticsearch
- FastAPI, Docker, GitHub Actions, Prometheus, Grafana
- LangChain, Llama 3, PostgreSQL

All licensed under Apache 2.0, MIT, or compatible open-source licenses
```

### Personnel (Only cost)
```
Engineers (12): ₹30-45L/month
- Phase 2: ₹35-40L (6 months = ₹2.1-2.4Cr)

Total Phase 2 Cost (FREE VARIANT): ₹2.2-2.9Cr
vs. Original Plan (with OpenAI + AWS): ₹3.5-4.5Cr

SAVINGS: ₹1-1.5Cr (25-35% reduction!)
```

---

## 🚀 Hardware Requirements (Local Deployment)

### Server for Phase 2 (₹3-4L)
```
CPU: AMD EPYC 7542 or similar (32 cores)
RAM: 256GB DDR4 ECC
GPU: 8x NVIDIA A100 (80GB each) for Llama 3 70B inference
    OR 4x RTX 6000 (48GB each) as budget option
Storage: 20TB SSD for fast indexing + data
Network: 1Gbps+ to MoD office
```

### Why Local?
1. **Cost**: No recurring cloud charges
2. **Privacy**: Defence data stays in-house (important!)
3. **Control**: Can optimize for your specific workloads
4. **Security**: No data leaving MoD network
5. **Latency**: Faster response times

### Phase 2→3 Migration
- If data grows beyond 20TB: Expand NAS (add drives)
- If QPS exceeds 10: Add second server (load balance)
- No need to migrate to cloud (unless policy requires)

---

## 🔧 Tool Alternatives (If Main Tool Fails)

| Task | Primary | Fallback 1 | Fallback 2 |
|------|---------|-----------|-----------|
| **OCR** | EasyOCR | Tesseract | PaddleOCR |
| **Layout** | LayoutParser | Custom rules | Manual markup |
| **NER** | spaCy | FLAIR | CRF++ |
| **Embeddings** | SentenceTransformers | ONNX runtime | FastText |
| **Vector DB** | ChromaDB | Qdrant | Milvus |
| **Search** | Elasticsearch | Whoosh (Python) | Simple inverted index |
| **LLM** | Llama 3 70B | Mistral 7B | Phi 2.7B |
| **Backend** | FastAPI | Flask | Django |
| **Monitoring** | Prometheus+Grafana | ELK Stack | Custom logging |

---

## 📦 Phase 2 Free Stack Architecture

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│         DIRAS PHASE 2 (100% FREE STACK)            │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [FastAPI Backend] (Free)                           │
│         ↓                                           │
│  ┌──────────────────────────────────────────┐      │
│  │  Core Modules (All Free)                 │      │
│  ├──────────────────────────────────────────┤      │
│  │  1. Data Pipeline                        │      │
│  │     - Scrapy (free) → 5K documents       │      │
│  │     - EasyOCR (free) → ≥88% accuracy     │      │
│  │                                          │      │
│  │  2. Classification                       │      │
│  │     - spaCy (free) + Random Forest       │      │
│  │     - F1 ≥0.88                           │      │
│  │                                          │      │
│  │  3. NER                                  │      │
│  │     - spaCy (free) + BERT fine-tune      │      │
│  │     - F1 ≥0.82                           │      │
│  │                                          │      │
│  │  4. Embeddings                           │      │
│  │     - SentenceTransformers (free)        │      │
│  │     - 384-dim vectors                    │      │
│  │                                          │      │
│  │  5. Retrieval                            │      │
│  │     - ChromaDB (free) + Elasticsearch    │      │
│  │     - P@10 ≥0.75, <150ms latency         │      │
│  │                                          │      │
│  │  6. RAG Pipeline                         │      │
│  │     - LangChain (free) + Llama 3         │      │
│  │     - Hallucination ≤8%                  │      │
│  │                                          │      │
│  │  7. Financial Analysis (free rules)      │      │
│  │  8. Authority Identification (free DB)   │      │
│  └──────────────────────────────────────────┘      │
│         ↓                                           │
│  ┌──────────────────────────────────────────┐      │
│  │  Infrastructure (All Free/Self-Hosted)   │      │
│  ├──────────────────────────────────────────┤      │
│  │  - Docker (free)                         │      │
│  │  - PostgreSQL (free)                     │      │
│  │  - Prometheus + Grafana (free)           │      │
│  │  - GitHub Actions (free tier)            │      │
│  │  - Local NAS (one-time ₹50K)             │      │
│  └──────────────────────────────────────────┘      │
│         ↓                                           │
│  Monitoring Dashboard (Grafana, Free)              │
│  ┌──────────────────────────────────────────┐      │
│  │  - OCR Accuracy ≥88%                     │      │
│  │  - Classification F1 ≥0.88               │      │
│  │  - Retrieval P@10 ≥0.75                  │      │
│  │  - RAG Hallucination ≤8%                 │      │
│  │  - System Latency <2s                    │      │
│  │  - Resource utilization                  │      │
│  └──────────────────────────────────────────┘      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 Implementation Steps (FREE VARIANT)

### Step 1: Procurement (2-4 weeks)
1. Purchase server hardware (₹3-4L)
2. Install Linux (Ubuntu 22.04 LTS, free)
3. Setup Docker + networking
4. Ready for code deployment

### Step 2: Deploy Free Stack (Weeks 1-16 of Phase 2)
1. Clone DIRAS repo
2. Run docker-compose (all services start)
3. Follow Sprint 1-8 implementation prompts
4. All code is open-source (no licensing)

### Step 3: Data Pipeline (Weeks 3-4)
1. Scrapy spiders collect 5K documents
2. EasyOCR processes PDFs → OCR
3. All runs locally on your hardware

### Step 4: ML Models (Weeks 5-12)
1. Train classifiers on local GPU
2. Fine-tune BERT on local GPU
3. Generate embeddings on local GPU
4. All models stored locally (no cloud)

### Step 5: LLM Inference (Weeks 11-12)
1. Download Llama 3 70B (45GB model file)
2. Run via Ollama or vLLM on your GPU server
3. Zero inference costs (runs on your hardware)

### Step 6: Monitoring (Weeks 13-16)
1. Prometheus scrapes metrics
2. Grafana visualizes dashboards
3. All self-hosted, free

---

## ⚠️ Trade-offs (FREE STACK vs. PAID)

| Aspect | Free Stack | Paid Stack |
|--------|-----------|-----------|
| **LLM Quality** | Llama 3 70B (~GPT-3.5 level) | GPT-4 (slightly better) |
| **Latency** | 1-2s (GPU-dependent) | 0.5-1s (OpenAI optimized) |
| **Scalability** | Up to 10K QPS (add servers) | Unlimited (pay more) |
| **Availability** | 99% (your hardware) | 99.99% (AWS) |
| **Upfront Cost** | ₹4L (hardware, one-time) | ₹0 (use OpenAI API) |
| **Monthly Cost** | ₹10K (network) | ₹1L+ (OpenAI + AWS) |
| **Support** | Community (free) | Paid support available |
| **Privacy** | 100% (in-house) | Data on external servers |

**Recommendation**: FREE STACK is ideal for defence (privacy critical + cost-effective)

---

## 📋 Software Components (All Free)

```
Core Languages:
  - Python 3.10+ (free)
  - Shell scripting (free)

Web Framework:
  - FastAPI (free)
  - Starlette (free)

Data Processing:
  - Pandas (free)
  - NumPy (free)
  - SciPy (free)

ML/NLP:
  - scikit-learn (free)
  - spaCy (free)
  - HuggingFace Transformers (free)
  - SentenceTransformers (free)
  - LangChain (free)

OCR/Vision:
  - EasyOCR (free)
  - OpenCV (free)
  - LayoutParser (free)
  - pdf2image (free)

Databases:
  - PostgreSQL (free)
  - ChromaDB (free)
  - Elasticsearch OSS (free)

Infrastructure:
  - Docker (free)
  - Docker-Compose (free)

Monitoring:
  - Prometheus (free)
  - Grafana (free)

Testing:
  - pytest (free)
  - pytest-cov (free)

Annotation:
  - Label Studio (free, open-source)

All dependencies: requirements.txt (pip install, free)
```

---

## 🔐 Security (Self-Hosted Advantage)

With FREE STACK (on-premises):
- ✅ No data leaves MoD network
- ✅ Complete control over infrastructure
- ✅ No vendor lock-in
- ✅ Audit trail (complete visibility)
- ✅ Compliance with gov't data policies
- ✅ No third-party data sharing

---

## 📞 Questions Before We Start?

1. **Hardware**: Do you have server infrastructure, or should I recommend specs?
2. **GPU**: Do you have NVIDIA GPUs available, or prefer CPU-only inference (slower)?
3. **Timeline**: Still targeting July 1, 2026 Phase 2 start?
4. **Data**: Are you ready to start scraping public documents?

---

**Status**: Ready for Sprint 1 implementation with 100% free stack ✅

Next: Create Sprint 1 code files (Dockerfile, docker-compose.yml, requirements.txt, etc.)
