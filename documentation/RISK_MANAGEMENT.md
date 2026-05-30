# Risk Management Plan - DIRAS Phase 2-5 Implementation

**Document Version**: 1.0  
**Last Updated**: May 28, 2026  
**Status**: Phase 1 Completion Document  
**Applicable Phases**: Phase 2, Phase 3, Phase 4, Phase 5

---

## Executive Summary

This document identifies and mitigates 30+ risks across the DIRAS implementation roadmap spanning Phases 2-5. Each risk includes probability assessment, impact analysis, mitigation strategy, and contingency plans for critical risks.

**Risk Categories**: Technical (10 risks) | Data (8 risks) | Infrastructure (6 risks) | Organizational (4 risks) | Security/Compliance (2 risks)

**Critical Risks** (High Probability + High Impact): 5
**Major Risks** (Medium+ in both dimensions): 12
**Minor Risks** (Low probability or impact): 13

---

## Risk Assessment Matrix

### Severity Ratings
| Rating | Probability | Impact | Action |
|--------|-------------|--------|--------|
| **Critical** | High (>70%) | High (₹5+ Cr loss/delay) | Immediate mitigation required |
| **Major** | Medium (40-70%) | Medium (₹1-5 Cr) | Active monitoring, contingency ready |
| **Minor** | Low (<40%) | Low (<₹1 Cr) | Monitor, note in sprint retros |

---

## Technical Risks (10 total)

### T1: OCR Accuracy Below Baseline (CRITICAL)
**Probability**: High (75%)  
**Impact**: High - Classification/NER accuracy drops 15-20%  
**Current Baseline Target**: 88-90% word accuracy

**Root Causes**:
- Defence documents have varied formats (old scans, handwritten annotations, complex layouts)
- EasyOCR may struggle with defence-specific terminology (DRDO, procurement codes)
- Multi-page documents with different scan qualities
- Table extraction from PDFs often fails (15-25% accuracy loss)

**Mitigation Strategy**:
1. **Phase 2**: Conduct OCR baseline testing on representative sample (500 docs from each data source)
2. **Phase 2**: Implement OCR ensemble (EasyOCR + Tesseract fallback for low confidence)
3. **Phase 3**: Create OCR quality pipeline with confidence scoring + human review workflow
4. **Phase 3**: Build specialized OCR model fine-tuned on defence documents (if accuracy remains <85%)
5. **Continuous**: Collect OCR errors in production, create "hard cases" dataset

**Contingency Plan** (if accuracy <85% by end Phase 2):
- Extend Phase 2 by 2-3 weeks for OCR optimization
- Allocate 2 ML engineers to fine-tune PaddleOCR instead
- Budget ₹15-20 lakhs for specialized OCR service (Paddle HubOCR or commercial)
- Accept 85% accuracy and focus on downstream noise handling (preprocessing)

**Owner**: ML Team Lead  
**Monitoring Metric**: Word accuracy % per source, character error rate  
**Review Frequency**: Bi-weekly during Phase 2-3

---

### T2: Embedding Quality Insufficient for Retrieval (HIGH)
**Probability**: Medium-High (60%)  
**Impact**: High - RAG retrieval precision drops to <0.70  
**Current Baseline Target**: Semantic correlation ≥0.75

**Root Causes**:
- SentenceTransformers all-MiniLM may not handle defence-specific semantic relationships
- Limited training data on defence documents → poor domain adaptation
- Query-document semantic gap (query written by analyst, doc written by bureaucrat)
- Multi-lingual retrieval challenges (Hindi/English code-switching in documents)

**Mitigation Strategy**:
1. **Phase 2**: Benchmark multiple embedding models (BGE, E5, Instructor-XL) on golden dataset
2. **Phase 3**: Fine-tune selected embedding model on 10K defence document pairs
3. **Phase 3**: Implement two-stage retrieval: coarse (all-MiniLM) → fine (fine-tuned)
4. **Phase 4**: Explore multilingual embeddings for Hindi-English documents
5. **Continuous**: Monitor retrieval metrics from production queries

**Contingency Plan** (if semantic correlation <0.70 by Phase 3):
- Invest in commercial embedding API (OpenAI Embeddings, but cost +₹50L/year)
- OR: Hybrid approach - use dense embeddings for ranking, keyword match for recall
- Budget ₹10-15 lakhs for embedding fine-tuning infrastructure

**Owner**: ML Team Lead  
**Monitoring Metric**: Semantic correlation coefficient, retrieval precision@10  
**Review Frequency**: Monthly during embedding selection phase

---

### T3: Retrieval Precision Below 0.75 (HIGH)
**Probability**: High (65%)  
**Impact**: High - Users get irrelevant results, system unusable  
**Current Baseline Target**: Precision@10 ≥0.80, MRR ≥0.75

**Root Causes**:
- Hybrid retrieval setup (BM25 + dense) may not balance correctly
- Query understanding insufficient (no intent detection in Phase 2)
- Document chunking strategy impacts retrieval (chunk size, overlap)
- Reranking model not effective for defence documents

**Mitigation Strategy**:
1. **Phase 2**: Establish BM25 baseline on golden dataset (target: P@10 ≥0.75)
2. **Phase 3**: Add dense retrieval and optimize fusion (reciprocal rank fusion)
3. **Phase 3**: Implement cross-encoder reranking (mmarco-mMiniLMv2-L12-H384)
4. **Phase 4**: Add query expansion and intent-aware retrieval
5. **Phase 4**: Build domain-specific reranker fine-tuned on defence queries

**Contingency Plan** (if P@10 <0.70 by Phase 3):
- Extend Phase 3 by 1-2 weeks for retrieval optimization
- Implement k-NN graph-based retrieval (LightGBM/FAISS optimization)
- Allocate 1-2 engineers for query understanding pre-processing
- Accept lower precision (0.70) and focus on recall + filtering

**Owner**: Backend Lead + ML Engineer  
**Monitoring Metric**: Precision@10, Recall@100, MRR  
**Review Frequency**: Weekly during Phase 3 retrieval optimization

---

### T4: Vector Database Scalability Issues (MEDIUM)
**Probability**: Medium (50%)  
**Impact**: Medium-High - Latency increases >500ms, cost overruns  
**Current Plan**: ChromaDB (Phase 2-3) → Weaviate (Phase 4+)

**Root Causes**:
- ChromaDB not designed for >10M vectors (DIRAS target: 5-10M by Phase 4)
- Weaviate setup complexity with Kubernetes + GPU infrastructure
- Network latency if vector DB in different datacenter
- Indexing speed bottleneck during batch updates

**Mitigation Strategy**:
1. **Phase 2**: Load test ChromaDB with 1M+ vectors, measure latency
2. **Phase 3**: Begin Weaviate evaluation in parallel (if ChromaDB <100ms latency)
3. **Phase 3**: Implement sharding/partitioning strategy for vectors
4. **Phase 4**: Migrate to Weaviate with zero-downtime strategy (read both DBs, switch writes)
5. **Continuous**: Monitor query latency (target: <100ms p95)

**Contingency Plan** (if ChromaDB latency >200ms at 5M vectors):
- Fast-track Weaviate migration to Phase 3 (2 weeks early)
- Budget ₹30-50 lakhs for Weaviate cloud infrastructure
- OR: Use FAISS with periodic reindexing (lower cost, less dynamic)
- Scale vector DB across multiple instances with load balancing

**Owner**: Infrastructure Lead  
**Monitoring Metric**: Query latency p50/p95/p99, vector count, indexing time  
**Review Frequency**: Monthly during scaling phases

---

### T5: RAG Hallucination Rate Above 5% (MEDIUM-HIGH)
**Probability**: High (70%)  
**Impact**: Medium-High - LLM generates false information (critical for defence)  
**Current Baseline Target**: Hallucination rate ≤5%

**Root Causes**:
- LLM inherent hallucination (Llama 3, Mistral cannot be 100% faithful)
- Retrieval gaps - relevant context not retrieved → LLM fills gaps
- Poor context compression - irrelevant chunks in context window
- Lack of hallucination detection/filtering in output

**Mitigation Strategy**:
1. **Phase 3**: Implement context validation layer (verify retrieved docs are relevant)
2. **Phase 3**: Add hallucination detection (Ragas faithfulness scorer)
3. **Phase 4**: Implement output filtering - block answers with hallucination confidence >0.5
4. **Phase 4**: Add "source attribution" - every answer must cite document + page
5. **Phase 4**: Fine-tune LLM on defence documents (reduce hallucination tendency)
6. **Continuous**: Collect hallucination cases, build detection dataset

**Contingency Plan** (if hallucination >5% by Phase 3):
- Shift to retrieval-only mode (no LLM generation, just document retrieval + ranking)
- Use GPT-4 instead of Llama (higher quality, higher cost +₹1-2Cr/year)
- Build custom verification layer (ML model to detect hallucinations)
- Require human approval for all financial/procurement answers

**Owner**: NLP/RAG Lead  
**Monitoring Metric**: Hallucination rate %, faithfulness score, source attribution compliance  
**Review Frequency**: Bi-weekly during RAG implementation

---

### T6: Query Understanding Module Insufficient (MEDIUM)
**Probability**: Medium (55%)  
**Impact**: Medium - System cannot distinguish financial vs. procurement queries  
**Current Plan**: BERT intent classification + TF-IDF query expansion

**Root Causes**:
- Training data scarcity for intent classification (need 500+ labeled queries per intent)
- Domain specificity - "budget" could mean allocation vs. utilization vs. proposal
- Query ambiguity in defence context (codes, abbreviations, jargon)
- Multi-intent queries (financial AND procurement query together)

**Mitigation Strategy**:
1. **Phase 2**: Crowdsource 2K+ labeled queries from stakeholders (defence analysts)
2. **Phase 3**: Train BERT intent classifier with domain-specific data
3. **Phase 3**: Implement query decomposition for multi-intent queries
4. **Phase 4**: Build query rewriting engine (normalize abbreviations, expand codes)
5. **Phase 4**: Add semantic similarity-based query understanding

**Contingency Plan** (if intent F1 <0.80 by Phase 3):
- Extend Phase 3 by 1-2 weeks for more labeled data collection
- Implement rule-based intent detection as fallback (highest precision)
- Budget ₹5-10 lakhs for annotation of additional training data
- Accept lower accuracy (0.75) and handle intent-agnostic queries

**Owner**: NLP Engineer  
**Monitoring Metric**: Intent classification F1 score per intent type  
**Review Frequency**: Monthly during Phase 3

---

### T7: Document Classification Accuracy Below 88% (MEDIUM)
**Probability**: Medium (45%)  
**Impact**: Medium - Misclassified documents → wrong processing pipeline  
**Current Baseline Target**: F1 ≥0.88 across all 10 document types

**Root Causes**:
- Class imbalance (memorandums 60%, tenders 5%)
- Similar documents across classes (financial reports vs. budget guidelines)
- Sparse training data for rare classes (tender documents)
- No transfer learning baseline (BERT fine-tuning may not be standard)

**Mitigation Strategy**:
1. **Phase 2**: Analyze class distribution, oversample rare classes
2. **Phase 2**: Establish Random Forest baseline (target: F1 ≥0.85)
3. **Phase 3**: Fine-tune BERT classifier with focal loss for imbalanced data
4. **Phase 3**: Implement ensemble (RF + BERT + Logistic Regression)
5. **Phase 4**: Add confidence threshold - flag low-confidence classifications for human review

**Contingency Plan** (if F1 <0.85 by Phase 3):
- Merge similar classes (e.g., "guidelines" + "memorandums" → "directives")
- Reduce from 10 to 7-8 classes, retrain
- Allocate 1-2 weeks for additional manual labeling
- Accept lower accuracy and implement human-in-the-loop for <0.70 confidence

**Owner**: ML Engineer  
**Monitoring Metric**: Per-class precision/recall, F1 score, confidence distribution  
**Review Frequency**: Bi-weekly during Phase 2-3

---

### T8: Entity Extraction (NER) F1 Below 0.82 (MEDIUM)
**Probability**: Medium (50%)  
**Impact**: Medium - Missing authorities, monetary values, departments  
**Current Baseline Target**: Authority NER F1 ≥0.85, Monetary F1 ≥0.80

**Root Causes**:
- Sparse training data for defence-specific entities (DRDO subdivisions, rare organisations)
- Entity ambiguity (e.g., "Ministry" appears 100+ times, which one is "authority"?)
- Multi-token entities (e.g., "Defence Research Development Organisation of India")
- Lack of BIO/IOB tagging consistency in training data

**Mitigation Strategy**:
1. **Phase 2**: Create training dataset with 5K+ hand-annotated entities (authority, monetary, department)
2. **Phase 3**: Fine-tune spaCy NER baseline (target: F1 ≥0.80)
3. **Phase 3**: Fine-tune BERT NER (target: F1 ≥0.85)
4. **Phase 3**: Implement hybrid approach (spaCy fast + BERT accurate, ensemble votes)
5. **Phase 4**: Add post-processing rules (authority hierarchy validation)

**Contingency Plan** (if F1 <0.80 by Phase 3):
- Extend Phase 3 annotation by 1 week
- Use weak supervision (rule-based labeling) for additional training data
- Implement CRF post-processing layer for sequence constraints
- Accept lower accuracy and use LLM-based entity verification in RAG

**Owner**: NLP Engineer  
**Monitoring Metric**: Per-entity-type F1, precision, recall, false positive rate  
**Review Frequency**: Weekly during Phase 3

---

### T9: API Latency Exceeds 2 Seconds (MEDIUM)
**Probability**: Medium (50%)  
**Impact**: Medium - Poor user experience, SLA violations  
**Current Target**: <500ms p95 latency

**Root Causes**:
- Cascading latency: OCR (100-300ms) + embedding (50-100ms) + retrieval (100-200ms) + LLM (1-2s)
- Synchronous processing (sequential, not parallel)
- Vector DB network latency
- LLM inference on CPU instead of GPU

**Mitigation Strategy**:
1. **Phase 3**: Profile each component for latency
2. **Phase 3**: Implement async processing pipeline (queue + worker model)
3. **Phase 4**: Add GPU support for embedding generation + LLM inference
4. **Phase 4**: Implement caching layer (cache frequent queries + embeddings)
5. **Phase 4**: Add request batching for embedding generation
6. **Continuous**: Monitor latency distribution, set SLA alerts

**Contingency Plan** (if p95 latency >1000ms by Phase 4):
- Increase GPU allocation (budget +₹20-30 lakhs)
- Implement query routing (cache vs. fresh vs. approximate)
- Reduce LLM context window (speed up inference, lose some precision)
- Accept higher latency (1-2s) and optimize for throughput instead

**Owner**: Backend Lead  
**Monitoring Metric**: Query latency p50/p95/p99, per-component breakdown  
**Review Frequency**: Monthly during Phase 3-4

---

### T10: Preprocessing Pipeline Loses Critical Information (MEDIUM-LOW)
**Probability**: Medium (45%)  
**Impact**: Medium - Metadata lost, table information discarded  
**Current Baseline Target**: <2% information loss for standard documents

**Root Causes**:
- Aggressive stop-word removal removes financial terms (e.g., "allocation")
- Lemmatization may normalize important terms (e.g., "budget" → "bud"?)
- Table extraction skipped, only text processed
- Metadata (dates, authorities) stripped during regex cleaning

**Mitigation Strategy**:
1. **Phase 2**: Design domain-aware preprocessing (keep defence terminology)
2. **Phase 2**: Implement non-destructive preprocessing (preserve original in separate field)
3. **Phase 3**: Add table extraction pipeline (extract structure + content)
4. **Phase 3**: Create preprocessing ablation study (measure information loss)
5. **Phase 4**: Build custom stemmer/lemmatizer for defence terms

**Contingency Plan** (if >5% information loss by Phase 3):
- Revert to minimal preprocessing (regex + tokenization only)
- Implement two-pass processing: raw text + preprocessed text in retrieval
- Budget time for custom preprocessing rule development
- Use transformer-based preprocessing (maintains semantic)

**Owner**: Data Pipeline Lead  
**Monitoring Metric**: Information retention %, downstream accuracy impact  
**Review Frequency**: Bi-weekly during Phase 2-3

---

## Data Risks (8 total)

### D1: Document Source Quality Varies Significantly (HIGH)
**Probability**: High (85%)  
**Impact**: High - OCR accuracy varies 50-95% across sources  
**Observation**: Already validated from Phase 1 research

**Root Causes**:
- Ministry of Defence website uses PDF quality from ~2000-2023 (old scans very poor)
- Gazette of India has mix of native PDFs and scanned images
- PIB press releases are high-quality but may not cover all topics
- DRDO public reports use various publication standards

**Mitigation Strategy**:
1. **Phase 2**: Segment sources by quality tier (Tier 1: high quality, Tier 4: poor quality)
2. **Phase 2**: Apply source-specific preprocessing (heavier OCR for Tier 4)
3. **Phase 3**: Build source-specific OCR models (Tesseract vs. EasyOCR per source)
4. **Phase 3**: Implement quality scoring per document (OCR confidence × document completeness)
5. **Phase 4**: Request updated documents from Ministry for Tier 4 sources

**Contingency Plan** (if >40% docs fail OCR by Phase 2):
- Deprioritize Tier 4 sources in Phase 2
- Focus on Tier 1-2 sources (Ministry, Gazette) initially
- Plan manual digitization effort for critical Tier 4 documents
- Budget ₹50-100 lakhs for document quality improvement service

**Owner**: Data Engineering Lead  
**Monitoring Metric**: OCR success rate per source, quality tier distribution  
**Review Frequency**: Weekly during Phase 2 data ingestion

---

### D2: Insufficient Training Data for ML Models (MEDIUM-HIGH)
**Probability**: High (70%)  
**Impact**: High - Models underperform, need 3-6 month labeling effort  
**Current Need**: 10K+ labeled docs for classification, 5K+ for NER, 2K+ for intent

**Root Causes**:
- Defence documents require domain expert annotation (not crowdsourceable)
- Only 5-10 domain experts available (annotation is slow)
- Budget constraints (₹5-10 per annotation × 17K = ₹85-170 lakhs)
- Annotation guidelines not standardized initially

**Mitigation Strategy**:
1. **Phase 2**: Create annotation guidelines with examples (1-2 weeks)
2. **Phase 2**: Start annotation with 5-10 defence analysts (parallel with development)
3. **Phase 2**: Implement weak supervision (rules + distant supervision)
4. **Phase 3**: Use active learning (auto-label easy cases, focus human effort on hard cases)
5. **Phase 3**: Implement data augmentation (backtranslation, paraphrasing for text)
6. **Phase 4**: Build crowd annotation platform (expand beyond 5-10 people)

**Contingency Plan** (if <5K labeled docs available by Phase 3):
- Use pre-trained models without fine-tuning (lower accuracy, but avoids labeling)
- Implement zero-shot learning (use general classifiers)
- Budget ₹30-50 lakhs for rapid annotation service (Appen, Scale)
- Extend Phase 3 by 4-6 weeks for annotation backlog

**Owner**: Data Labeling Manager  
**Monitoring Metric**: Annotation rate (docs/week), inter-annotator agreement (κ), labeled dataset size  
**Review Frequency**: Weekly during Phase 2-3

---

### D3: Data Source Availability/Stability (MEDIUM)
**Probability**: Medium (55%)  
**Impact**: Medium - Scraping breaks when websites change, 1-2 week delays  
**Current Sources**: 8 Tier 1-2 sources (Ministry, Gazette, PIB, DRDO, etc.)

**Root Causes**:
- Government websites occasionally redesign (break scrapers)
- API rate limits if using official APIs
- Some documents removed/archived (dynamic content)
- No official bulk download API (web scraping is fragile)

**Mitigation Strategy**:
1. **Phase 2**: Implement robust scraper error handling (retry + exponential backoff)
2. **Phase 2**: Monitor scraper success rates daily (alert on <95% success)
3. **Phase 3**: Build fallback scrapers (multiple strategies per source)
4. **Phase 3**: Archive downloaded documents (avoid re-scraping)
5. **Phase 4**: Request official bulk download agreements from Ministry of Defence
6. **Continuous**: Maintain scraper maintenance schedule (review weekly)

**Contingency Plan** (if >20% documents unavailable by Phase 2):
- Shift to direct email requests to Ministry for bulk documents
- Partner with DRDO for official document access
- Reduce coverage from 8 sources to 4-5 most reliable sources
- Implement manual collection for critical missing documents

**Owner**: Data Engineering Lead  
**Monitoring Metric**: Scraper success rate %, documents collected per week, source uptime  
**Review Frequency**: Daily during Phase 2, weekly thereafter

---

### D4: Data Completeness Below 80% (MEDIUM)
**Probability**: Medium (60%)  
**Impact**: Medium - Missing documents → incomplete knowledge base  
**Current Target**: Cover 90%+ of important defence documents (by March 2027)

**Root Causes**:
- Estimated 50K-100K public defence documents exist; we may collect only 30K-40K
- Some documents archived or not web-accessible
- Duplicate documents across sources inflate count
- Real-time documents (new notices) may not be captured

**Mitigation Strategy**:
1. **Phase 2**: Audit major data sources for document counts (estimate total universe)
2. **Phase 2**: Implement continuous scraping (daily updates for new documents)
3. **Phase 3**: Build document de-duplication pipeline (detect near-duplicates)
4. **Phase 3**: Request historical archives from Ministry (all documents from past 10 years)
5. **Phase 4**: Implement real-time RSS/API feeds for latest documents
6. **Phase 4**: Build "missing documents" tracker (flag gaps from analysts)

**Contingency Plan** (if <70% coverage by Phase 3):
- Expand to secondary sources (Parliamentary Q&As, media archives)
- Conduct manual audit of critical documents (with Ministry)
- Accept 70% coverage and focus on quality of collected documents
- Budget ₹20-30 lakhs for historical document recovery service

**Owner**: Data Engineering Lead  
**Monitoring Metric**: Document count growth, coverage %, deduplication rate  
**Review Frequency**: Monthly during Phase 2-4

---

### D5: Document Metadata Missing/Inconsistent (MEDIUM)
**Probability**: Medium (50%)  
**Impact**: Medium - Authority identification fails, temporal queries break  
**Metadata Needed**: Publication date, author, approving authority, document type, version

**Root Causes**:
- OCR may extract incorrect dates (misread "20/05/2020" as "20/05/2020")
- Gazette documents may not have clear metadata in structured form
- PDF metadata may be incomplete or outdated
- Scanned documents lose metadata during digitization

**Mitigation Strategy**:
1. **Phase 2**: Extract metadata from document headers/footers during OCR
2. **Phase 2**: Build metadata validation rules (date range checks, authority whitelist)
3. **Phase 3**: Implement metadata enrichment (use NER to extract missing fields)
4. **Phase 3**: Create metadata quality scorecards per source
5. **Phase 4**: Add manual metadata verification workflow (for high-value documents)

**Contingency Plan** (if >30% documents lack key metadata by Phase 3):
- Implement zero-metadata handling (don't rely on metadata for critical features)
- Use NER to extract dates/authorities at query time (slower, more reliable)
- Accept lower accuracy for temporal/authority queries
- Budget time for manual metadata curation (30-50 person-days)

**Owner**: Data Engineering Lead  
**Monitoring Metric**: Metadata completeness %, metadata accuracy vs. ground truth  
**Review Frequency**: Bi-weekly during Phase 2-3

---

### D6: Data Privacy & Security Violations (MEDIUM-LOW)
**Probability**: Low-Medium (35%)  
**Impact**: High - Project shutdown, legal issues (if any personal data leaked)  
**Current Status**: Plan to use ONLY public documents

**Root Causes**:
- Accidentally scraping confidential annexures (marked as public but contain sensitive info)
- Personal information in documents (phone numbers, addresses, names of defence personnel)
- Storing documents in unsecured cloud infrastructure
- No data classification/access control mechanism

**Mitigation Strategy**:
1. **Phase 1**: Audit all collected documents for inadvertent sensitive data (ongoing)
2. **Phase 2**: Implement document validation (filter documents containing personal info)
3. **Phase 2**: Build document sanitization pipeline (redact names, phone numbers, addresses)
4. **Phase 3**: Implement access control (only authorized analysts can query sensitive documents)
5. **Phase 3**: Set up secure infrastructure (encrypted storage, access logging)
6. **Phase 4**: Conduct security audit (third-party penetration test)

**Contingency Plan** (if sensitive data discovered in corpus):
- Halt public access until data cleaned (1-2 weeks)
- Audit all collected documents for similar issues
- Implement stronger validation in scraping pipeline
- Notify Ministry of Defence, request guidance on handling

**Owner**: Security/Compliance Lead  
**Monitoring Metric**: Documents flagged for sensitive data, redaction rate, access logs reviewed  
**Review Frequency**: Monthly, plus ad-hoc audits

---

### D7: Data Inconsistency Across Versions (LOW-MEDIUM)
**Probability**: Low (30%)  
**Impact**: Medium - Conflicting information in RAG responses (e.g., two versions of same policy)  
**Current Observation**: Some documents have multiple versions (updated policies, corrections)

**Root Causes**:
- Multiple versions of guidelines published (V1.0, V2.0, V3.0)
- Superseded documents still available on government websites
- No clear version control on official sources
- Gazette publishes corrections/amendments separately

**Mitigation Strategy**:
1. **Phase 2**: Implement document version tracking (extract version from document)
2. **Phase 3**: Build version linkage (connect amendments to base documents)
3. **Phase 3**: Add temporal context to retrieval (retrieve latest version by default)
4. **Phase 4**: Implement version conflict detection (flag when RAG uses outdated doc)
5. **Phase 4**: Add "document history" view in UI (show version evolution)

**Contingency Plan** (if version conflicts cause RAG errors):
- Implement fallback to latest version only (sacrifices historical knowledge)
- Add human-in-the-loop for version-sensitive queries
- Build simple rule: "If multiple versions exist, use latest + note that older versions exist"

**Owner**: Data Engineering Lead  
**Monitoring Metric**: Version conflict detection rate, temporal query accuracy  
**Review Frequency**: Monthly during Phase 3-4

---

### D8: Duplicate Documents in Knowledge Base (MEDIUM-LOW)
**Probability**: Medium (45%)  
**Impact**: Low-Medium - Inflates document count, retrieval precision drops slightly  
**Current Estimate**: 10-20% duplicate documents across sources

**Root Causes**:
- Gazette republishes Ministry documents (same content, different source)
- Documents linked/referenced multiple times
- Different format versions (PDF vs. scanned image of same doc)
- Vendors republish official documents

**Mitigation Strategy**:
1. **Phase 2**: Implement document deduplication (hash-based + semantic similarity)
2. **Phase 2**: Build dedup pipeline for ingestion (prevent adding duplicates)
3. **Phase 3**: Merge duplicate metadata (consolidate authorities/dates)
4. **Phase 3**: Track source coverage (note which sources have duplicates)
5. **Continuous**: Monitor dedup rate, adjust thresholds

**Contingency Plan** (if >20% duplicates remain):
- Accept 15% duplicates (minor impact on retrieval)
- Implement downstream dedup in retrieval (remove duplicate results before ranking)
- Stricter threshold for semantic similarity dedup (may miss fuzzy duplicates)

**Owner**: Data Engineering Lead  
**Monitoring Metric**: Dedup rate %, unique vs. total document count  
**Review Frequency**: Monthly during Phase 2-3

---

## Infrastructure Risks (6 total)

### I1: Cloud Infrastructure Cost Overruns (HIGH)
**Probability**: High (65%)  
**Impact**: High - Budget increase 20-30%, ₹1.5-2 Cr additional cost  
**Current Budget**: ₹2-3 Cr Phase 2, ₹7-10 Cr total

**Root Causes**:
- Vector DB costs scale with vector count (Weaviate: 0.5-1 $/month per M vectors)
- LLM API costs scale with usage (GPT-4: ₹10-20/1K tokens at scale)
- GPU compute costs for fine-tuning + inference (₹50K-100K/month per GPU)
- Storage growth faster than projected (documents + embeddings + indices)
- Monitoring/logging infrastructure not budgeted initially

**Mitigation Strategy**:
1. **Phase 2**: Forecast costs monthly (vector count × unit cost, query volume × API cost)
2. **Phase 2**: Set cost alerts (Slack notification if costs exceed 80% of monthly budget)
3. **Phase 3**: Optimize LLM costs (batch API calls, use cheaper model for some queries)
4. **Phase 3**: Implement compression (quantize embeddings 8-bit to reduce storage)
5. **Phase 4**: Negotiate volume discounts with cloud provider (Weaviate, OpenAI)
6. **Phase 4**: Right-size infrastructure (remove unused resources, consolidate workloads)

**Contingency Plan** (if costs overrun >20% by Phase 3):
- Switch to open-source models (Llama 3 70B self-hosted) vs. GPT-4 API (save ₹50-100 lakhs/year)
- Migrate to cheaper vector DB (FAISS instead of Weaviate for non-production)
- Reduce query volume targets (smaller initial user base)
- Accept longer SLAs (batch processing instead of real-time)
- Budget ₹50-100 lakhs for infrastructure optimization engineer

**Owner**: Infrastructure Lead + Finance  
**Monitoring Metric**: Monthly cloud costs, cost per query, cost per document indexed  
**Review Frequency**: Weekly during Phase 2, monthly thereafter

---

### I2: Kubernetes/Containerization Complexity (MEDIUM)
**Probability**: Medium (50%)  
**Impact**: Medium - 2-4 week delay, team needs Kubernetes training  
**Current Plan**: Docker containers for Phase 3, Kubernetes for Phase 4

**Root Causes**:
- Team may lack Kubernetes expertise (DevOps engineer learning curve)
- Stateful services (vector DB, cache) harder to manage in K8s
- GPU resource management in K8s is complex
- Debugging/monitoring distributed system is challenging

**Mitigation Strategy**:
1. **Phase 2**: Hire/allocate 1-2 DevOps engineers with Kubernetes experience
2. **Phase 2**: Start Kubernetes POC early (1 engineer, 20% time)
3. **Phase 3**: Plan Kubernetes migration (architecture, resource limits, helm charts)
4. **Phase 3**: Build CI/CD pipeline for container deployment
5. **Phase 4**: Gradual Kubernetes adoption (start with stateless services, add stateful later)

**Contingency Plan** (if K8s becomes blocker by Phase 4):
- Delay Kubernetes until Phase 5 (use Docker + manual orchestration)
- Hire external Kubernetes consultant (₹20-50 lakhs for 2-3 months)
- Use managed Kubernetes service (AWS EKS, GCP GKE) to reduce complexity
- Accept single-server deployment initially, refactor for K8s later

**Owner**: DevOps Lead  
**Monitoring Metric**: Kubernetes readiness, container deployment success rate  
**Review Frequency**: Monthly during Phase 3-4

---

### I3: GPU Availability/Cost Constraints (MEDIUM-HIGH)
**Probability**: High (70%)  
**Impact**: High - Embedding generation 10x slower, fine-tuning not viable  
**Current Need**: 2-4 GPUs by Phase 3, 8+ by Phase 4

**Root Causes**:
- GPU shortage in India (supply constraints)
- Cloud GPU costs high (₹50K-200K/month per GPU)
- On-premises GPU procurement 3-6 month lead time
- Electricity costs in India may make on-premises unviable

**Mitigation Strategy**:
1. **Phase 2**: Reserve GPUs early with cloud provider (AWS/GCP)
2. **Phase 2**: Evaluate on-premises vs. cloud (cost analysis)
3. **Phase 3**: Implement GPU sharing (queue + scheduling system)
4. **Phase 3**: Optimize batch sizes for embedding generation (use GPUs efficiently)
5. **Phase 4**: Build auto-scaling (request GPUs when needed, release when done)
6. **Phase 4**: Explore A100/H100 rentals (cheaper than permanent allocation)

**Contingency Plan** (if GPUs unavailable/too expensive):
- Use CPU-based embedding generation (100x slower, but possible)
- Batch all embedding/fine-tuning jobs overnight (save costs)
- Use pre-trained models (no fine-tuning) to avoid GPU bottleneck
- Negotiate with MoD for Government cloud credits (₹2-5 Cr available)
- Budget ₹1-1.5 Cr for GPU infrastructure investment

**Owner**: Infrastructure Lead  
**Monitoring Metric**: GPU utilization %, embedding generation time, cost per embedding  
**Review Frequency**: Monthly during Phase 3+

---

### I4: Network Latency/Bandwidth Bottlenecks (MEDIUM-LOW)
**Probability**: Low-Medium (40%)  
**Impact**: Medium - Retrieval latency >500ms, API timeouts  
**Current Assumption**: All infrastructure in single datacenter (low latency)

**Root Causes**:
- Vector DB in different region (cloud) vs. API servers (on-premises)
- Network latency between datacenters (50-100ms)
- Large documents transferred multiple times (bandwidth inefficient)
- No caching/compression implemented initially

**Mitigation Strategy**:
1. **Phase 3**: Deploy infrastructure close together (same region/datacenter)
2. **Phase 3**: Implement caching (cache frequent queries, embeddings)
3. **Phase 3**: Add compression (gzip documents, quantize embeddings)
4. **Phase 4**: Deploy edge caches (geographically distributed)
5. **Phase 4**: Optimize network routing (CDN for static content)

**Contingency Plan** (if latency >500ms by Phase 4):
- Move vector DB to same network as API servers (eliminate remote DB latency)
- Implement approximate retrieval (HNSW instead of exact search)
- Accept higher latency (500ms-1s) and optimize for throughput
- Budget for network infrastructure optimization (dedicated links, etc.)

**Owner**: Infrastructure Lead  
**Monitoring Metric**: Latency by component, bandwidth usage, cache hit rate  
**Review Frequency**: Monthly during Phase 3-4

---

### I5: Disaster Recovery & Backup Failures (MEDIUM-LOW)
**Probability**: Low (25%)  
**Impact**: High - Data loss, system downtime 1-2 weeks  
**Current Status**: No DR/backup plan documented

**Root Causes**:
- No automated backups initially
- No disaster recovery test (untested DR = no DR)
- Vector DB backups may be incomplete
- Cold start time for recovery not estimated

**Mitigation Strategy**:
1. **Phase 2**: Implement automated daily backups (documents + metadata)
2. **Phase 3**: Set up DR infrastructure (standby system in different region)
3. **Phase 3**: Test DR monthly (restore from backup, verify completeness)
4. **Phase 4**: Implement real-time replication (eliminate RPO gap)
5. **Continuous**: Document recovery procedures, train team

**Contingency Plan** (if backup/DR fails):
- Implement "rebuild from source" procedure (re-scrape documents, rebuild vectors)
- Estimated recovery time: 1-2 weeks
- Minimize scope loss (prioritize critical documents for immediate backup)

**Owner**: Infrastructure Lead  
**Monitoring Metric**: Backup success rate, backup age, last successful restore test  
**Review Frequency**: Monthly, plus quarterly DR tests

---

### I6: Monitoring & Observability Gaps (MEDIUM-LOW)
**Probability**: Medium (45%)  
**Impact**: Medium - Difficult to debug issues, performance regressions missed  
**Current Status**: No monitoring/logging architecture planned

**Root Causes**:
- Complex distributed system (hard to track requests across components)
- No logging aggregation initially (errors may be missed)
- Performance metrics not defined upfront
- Alert thresholds not established

**Mitigation Strategy**:
1. **Phase 2**: Define key metrics (latency, accuracy, cost, errors)
2. **Phase 3**: Implement logging aggregation (ELK, Loki, or cloud-native)
3. **Phase 3**: Add tracing (request tracing across services)
4. **Phase 3**: Set up dashboards (Grafana, Kibana)
5. **Phase 4**: Implement auto-remediation (auto-retry, circuit breakers)
6. **Continuous**: Review logs weekly, adjust thresholds based on data

**Contingency Plan** (if observability inadequate):
- Simple file-based logging (write to disk, manual analysis)
- Add more instrumentation to code (more logging statements)
- Increase team size for manual monitoring (not scalable)

**Owner**: DevOps Lead  
**Monitoring Metric**: Alert coverage (% of errors detected), MTTR (mean time to recovery)  
**Review Frequency**: Monthly

---

## Organizational Risks (4 total)

### O1: Team Skill Gaps (HIGH)
**Probability**: High (70%)  
**Impact**: High - 4-8 week delays, low code quality, rework needed  
**Current Status**: Plan for 12-15 engineers, but specific skill gaps unknown

**Root Causes**:
- Limited Kubernetes expertise in team
- Defence domain knowledge learning curve (terminology, security requirements)
- RAG + LLM expertise scarce in India
- Limited multilingual NLP experience (Hindi/English)

**Mitigation Strategy**:
1. **Phase 1 (now)**: Hire 2-3 senior engineers with RAG/LLM experience
2. **Phase 2**: Conduct 2-week DIRAS bootcamp (architecture, domain, tech stack)
3. **Phase 2**: Pair junior + senior engineers (mentorship model)
4. **Phase 3**: Send 2-3 engineers to conferences/courses (LLM fine-tuning, Kubernetes)
5. **Phase 4**: Build internal training program (knowledge documentation)
6. **Continuous**: Hire specialized roles as needs emerge (DevOps, Security, Domain Expert)

**Contingency Plan** (if skill gaps block Phase 2 progress):
- Hire external consultant (₹50-100 lakhs for 2-3 months)
- Slow down Phase 2 timeline (16 weeks → 20 weeks)
- Extend Phase 2 bootcamp (2 weeks → 4 weeks)
- Outsource specific components (embedding service, OCR service)

**Owner**: HR Lead + Technical Manager  
**Monitoring Metric**: Team training hours, skill assessment scores, sprint velocity  
**Review Frequency**: Monthly

---

### O2: Timeline Slippage/Scope Creep (MEDIUM-HIGH)
**Probability**: High (75%)  
**Impact**: High - ₹1-2 Cr cost increase, 3-6 month delays  
**Current Timeline**: Phases 2-5 = 18-24 months (Phase 2 alone = 14-16 weeks)

**Root Causes**:
- Scope unclear initially (will expand during development)
- Integration challenges discovered late
- Stakeholder requests change priorities mid-phase
- Optimistic estimation (experienced teams often underestimate)

**Mitigation Strategy**:
1. **Phase 1 (now)**: Lock Phase 2 scope (detailed sprint plan, acceptance criteria)
2. **Phase 2**: Implement Agile/Scrum (2-week sprints, weekly demos)
3. **Phase 2**: Set up change control board (review all scope changes)
4. **Phase 2**: Add 15-20% buffer to timeline (for integration, testing, rework)
5. **Phase 3**: Monitor velocity (if falling behind, alert early)
6. **Continuous**: Communicate status weekly (transparent, escalate risks)

**Contingency Plan** (if Phase 2 slips 4+ weeks):
- Reduce scope (deprioritize lower-priority features)
- Add more engineers (₹50-100 lakhs additional cost)
- Extend timeline (negotiate with stakeholders for Phase 3 delay)
- Implement phased delivery (MVP in Phase 2, advanced features in Phase 3+)

**Owner**: Project Manager  
**Monitoring Metric**: Sprint velocity, actual vs. planned timeline, scope change requests  
**Review Frequency**: Weekly sprint review

---

### O3: Stakeholder Alignment/Expectation Gaps (MEDIUM)
**Probability**: Medium (55%)  
**Impact**: Medium - Rework, late-stage changes, team friction  
**Current Status**: Phase 1 planning done with MoD, but Phase 2 execution team may have different expectations

**Root Causes**:
- Stakeholders (MoD, DRDO) may expect different features than planned
- Expectations around accuracy/speed may be unrealistic
- No agreed-upon SLOs/SLAs defined
- Communication gaps between business + technical teams

**Mitigation Strategy**:
1. **Phase 1 (now)**: Create stakeholder engagement plan (monthly reviews, demos)
2. **Phase 2**: Build governance structure (steering committee, working groups)
3. **Phase 2**: Document SLOs/SLAs (accuracy targets, latency, uptime)
4. **Phase 2**: Conduct weekly demos (transparency, feedback loop)
5. **Phase 3**: Implement UAT testing with stakeholders (co-create success criteria)
6. **Continuous**: Maintain communication channels (email, calls, escalation process)

**Contingency Plan** (if stakeholder conflict emerges):
- Escalate to executive sponsors (Director level)
- Conduct requirements re-elicitation workshop
- Adjust scope/timeline based on priorities
- Implement staged rollout (reduce risk of massive mismatch)

**Owner**: Product Manager + Project Manager  
**Monitoring Metric**: Stakeholder satisfaction score, requirement change requests, escalations  
**Review Frequency**: Monthly steering committee meeting

---

### O4: Key Personnel Turnover (MEDIUM-LOW)
**Probability**: Medium (50%)  
**Impact**: Medium - 2-4 week knowledge transfer delay, quality dips  
**Assumption**: High-demand engineers (RAG/LLM) may leave for better opportunities

**Root Causes**:
- Competitive job market (FAANG companies hiring RAG engineers)
- No long-term career path defined
- Team burnout (tight deadlines, on-call rotations)
- Competitive compensation not available

**Mitigation Strategy**:
1. **Phase 1**: Conduct competitive salary analysis, adjust offers
2. **Phase 2**: Define career growth path (senior engineer, tech lead roles)
3. **Phase 2**: Distribute knowledge (code reviews, documentation, mentoring)
4. **Phase 2**: Build team culture (recognition, learning opportunities)
5. **Phase 3**: Implement cross-training (reduce single points of failure)
6. **Phase 3**: Offer stock options/bonus (long-term incentive)
7. **Continuous**: Conduct pulse surveys, address concerns early

**Contingency Plan** (if 2+ key engineers leave):
- Hire replacement (3-6 month lead time)
- Shift schedule/scope to match remaining team capacity
- Bring in contractor (₹30-50 lakhs/month for experienced engineer)
- Slow down timeline (extend Phase 2 by 4-6 weeks)

**Owner**: HR Lead + Technical Manager  
**Monitoring Metric**: Attrition rate, vacancy duration, knowledge transfer completion  
**Review Frequency**: Quarterly

---

## Security & Compliance Risks (2 total)

### S1: Hallucination Leading to Misinformation (HIGH)
**Probability**: High (70%)  
**Impact**: High - LLM provides false information, user makes wrong decisions  
**Severity**: Critical for defence (budget allocation, procurement decisions based on false info)

**Root Causes**:
- LLM inherent tendency to hallucinate (cannot be 100% avoided)
- Retrieval gaps (relevant context not retrieved)
- Poor quality context (retrieved irrelevant documents)
- No validation mechanism in RAG output

**Mitigation Strategy**:
1. **Phase 3**: Implement hallucination detection (Ragas scorer, custom validator)
2. **Phase 3**: Add output filtering (block low-confidence answers)
3. **Phase 3**: Implement source attribution (every answer cites document + page)
4. **Phase 4**: Build verification layer (cross-check answer with multiple documents)
5. **Phase 4**: Implement confidence scoring (user sees how confident system is)
6. **Phase 4**: Add "citation required" mode (system only answers if source found)
7. **Continuous**: Monitor hallucination rate in production, collect cases

**Contingency Plan** (if hallucination >5% by Phase 3):
- Disable LLM generation for critical queries (financial, procurement)
- Implement retrieval-only mode (return ranked documents, no synthesis)
- Require human approval for high-impact answers
- Budget time for custom verification model development

**Owner**: NLP/RAG Lead  
**Monitoring Metric**: Hallucination rate %, false information cases, user complaints  
**Review Frequency**: Weekly during Phase 3

---

### S2: Data Classification/Access Control Issues (MEDIUM)
**Probability**: Medium (45%)  
**Impact**: Medium-High - Unauthorized access to sensitive info, compliance violations  
**Current Assumption**: All documents are public, but some may contain inadvertent sensitive data

**Root Causes**:
- No document classification system implemented
- No access control mechanism (everyone sees everything)
- Sensitive data redaction not automated
- Audit logging not in place

**Mitigation Strategy**:
1. **Phase 2**: Build document classification system (public vs. restricted)
2. **Phase 3**: Implement access control (role-based document access)
3. **Phase 3**: Add sensitive data detection (PII, security numbers)
4. **Phase 3**: Implement audit logging (track who accessed what document)
5. **Phase 4**: Build data redaction pipeline (auto-redact sensitive fields)
6. **Phase 4**: Set up compliance monitoring (quarterly audits)
7. **Continuous**: Review logs monthly, address access anomalies

**Contingency Plan** (if sensitive data breach occurs):
- Immediately halt public access
- Audit all documents for similar issues
- Notify Ministry, legal counsel
- Implement emergency remediation (redact, remove, fix)
- Implement stronger controls going forward

**Owner**: Security/Compliance Lead  
**Monitoring Metric**: Access control coverage %, PII detection rate, audit log completeness  
**Review Frequency**: Monthly

---

## Critical Risk Summary

### Top 5 Critical Risks (Require Immediate Attention)

| Rank | Risk | Probability | Impact | Mitigation Priority | Owner |
|------|------|-------------|--------|---------------------|-------|
| 1 | **T1: OCR Accuracy** | 75% | High | **CRITICAL** | ML Team Lead |
| 2 | **I1: Cost Overruns** | 65% | High | **CRITICAL** | Infra Lead + Finance |
| 3 | **T3: Retrieval Precision** | 65% | High | **CRITICAL** | Backend Lead + ML |
| 4 | **T5: RAG Hallucination** | 70% | High | **CRITICAL** | RAG Lead |
| 5 | **O2: Timeline Slippage** | 75% | High | **CRITICAL** | Project Manager |

---

## Risk Review & Escalation

### Monthly Risk Review Cadence
- **First Monday**: Risk assessment update (are probabilities/impacts changing?)
- **Second Monday**: Mitigation status check (are strategies working?)
- **Third Monday**: New risks identification (emerging issues?)
- **Fourth Monday**: Executive summary (report to steering committee)

### Risk Escalation Criteria
- **Probability increases** OR **Impact increases** → Immediately escalate
- **Mitigation strategy failing** → Activate contingency plan
- **New critical risk emerges** → Call emergency review

### Risk Owners Responsibilities
- **Monthly**: Update risk status + mitigation progress
- **Upon trigger**: Notify PM/Steering Committee within 24 hours
- **When blocking**: Escalate to executive sponsor

---

## Appendix: Risk Probability Estimation Methodology

**High (>70%)**: Expected to occur in >7 out of 10 similar projects; take action now
**Medium (40-70%)**: May occur; monitor closely, prepare contingencies
**Low (<40%)**: Unlikely; minimal preparation needed

**High Impact (>₹2-3 Cr)**: Major cost increase, timeline slippage >3 months
**Medium Impact (₹0.5-2 Cr)**: Noticeable cost/timeline impact
**Low Impact (<₹0.5 Cr)**: Manageable within normal variation

---

**Document Owner**: Technical Lead  
**Next Review**: June 28, 2026 (Month 1 of Phase 2)  
**Approval**: [Pending Phase 2 Project Kickoff]
