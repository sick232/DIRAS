# Detailed Cost Breakdown Analysis - DIRAS Implementation

**Document Version**: 1.0  
**Last Updated**: May 28, 2026  
**Timeline**: Phase 2 - Phase 5 (18-24 months)  
**Total Budget**: ₹7-10 Crores  
**Base Currency**: Indian Rupees (₹)

---

## Executive Summary

DIRAS implementation spans 4 phases over 18-24 months with total estimated cost of **₹7-10 Crores**. This breakdown provides component-level cost analysis, scaling progression, and cost optimization strategies.

### Budget Summary by Phase

| Phase | Duration | Personnel | Infrastructure | Tools/Licenses | Data/Ops | **Total** | Cumulative |
|-------|----------|-----------|-----------------|----------------|----------|----------|-----------|
| **Phase 2** | 14-16 weeks | ₹80-120 L | ₹40-60 L | ₹15-25 L | ₹20-30 L | **₹155-235 L** | **₹1.55-2.35 Cr** |
| **Phase 3** | 14-16 weeks | ₹80-120 L | ₹60-100 L | ₹20-35 L | ₹25-40 L | **₹185-295 L** | **₹3.40-5.30 Cr** |
| **Phase 4** | 16-20 weeks | ₹120-180 L | ₹100-150 L | ₹30-50 L | ₹30-50 L | **₹280-430 L** | **₹6.20-9.60 Cr** |
| **Phase 5** | 12-16 weeks | ₹100-160 L | ₹80-120 L | ₹20-35 L | ₹25-40 L | **₹225-355 L** | **₹8.45-13.15 Cr** |

**Note**: Phase 5 costs may exceed ₹10 Cr target if expansion/scaling deemed necessary. Cost optimization strategies in Phase 3-4 essential to stay within budget.

---

## PHASE 2 Budget: ₹155-235 Lakhs (~₹2 Crores)

### Phase 2 Overview
- **Goal**: Core system prototype + infrastructure setup
- **Duration**: 14-16 weeks (Q2-Q3 2026)
- **Team Size**: 12 engineers
- **Infrastructure**: Local servers + minimal cloud

### 2.1 Personnel Costs: ₹80-120 Lakhs

| Role | Count | Monthly Salary | Duration | Total Cost |
|------|-------|----------------|----------|-----------|
| **Engineering Lead** | 1 | ₹8-10 L | 16 weeks | ₹12-15 L |
| **Senior ML Engineers** | 2 | ₹8-10 L each | 16 weeks | ₹24-30 L |
| **ML Engineers** | 3 | ₹5-7 L each | 16 weeks | ₹24-33.6 L |
| **Backend Engineers** | 3 | ₹5-7 L each | 16 weeks | ₹24-33.6 L |
| **Data Engineer** | 1 | ₹6-8 L | 16 weeks | ₹9.6-12.8 L |
| **DevOps Engineer** | 1 | ₹6-8 L | 16 weeks | ₹9.6-12.8 L |
| **QA Engineer** | 1 | ₹4-6 L | 16 weeks | ₹6.4-9.6 L |
| **Subtotal (Base Salary)** | 12 | - | - | **₹110-147.2 L** |
| **Overhead (Benefits, GST)** | - | - | - | **₹-15%** |
| **Total Personnel** | - | - | - | **₹93.5-125 L** |

**Average**: ₹100-120 L / month (₹8.3-10 L/month)

**Notes**:
- Salaries include PF, health insurance, GST
- No bonuses/incentives in Phase 2 (focus on execution)
- Engineering Lead manages technical architecture + team
- Senior ML leads model development (OCR, classification, embeddings)

---

### 2.2 Infrastructure Costs: ₹40-60 Lakhs

#### On-Premises Hardware (Primary)
| Item | Quantity | Unit Cost | Total Cost |
|------|----------|-----------|-----------|
| **Server (CPU, 256GB RAM)** | 2 | ₹15 L | ₹30 L |
| **NAS Storage (20TB)** | 1 | ₹5 L | ₹5 L |
| **Networking (switches, cables)** | 1 set | ₹2 L | ₹2 L |
| **Installation/Setup** | - | - | ₹3 L |
| **On-Premises Subtotal** | - | - | **₹40 L** |

#### Cloud Services (Minimal)
| Service | Usage | Duration | Cost |
|---------|-------|----------|------|
| **AWS (backup, testing)** | Low | 16 weeks | ₹5-10 L |
| **Cloud Storage (cold backup)** | 100GB | 16 weeks | ₹2-3 L |
| **Cloud Subtotal** | - | - | **₹7-13 L** |

**Total Infrastructure**: ₹47-53 L

**Notes**:
- On-premises focus to reduce ongoing cloud costs
- 256GB RAM sufficient for 1-2M vector embeddings in memory
- NAS for document storage + backups
- Cloud used for disaster recovery, not primary workload
- GPU allocation: None in Phase 2 (use CPU for development)

---

### 2.3 Tools & Licenses: ₹15-25 Lakhs

| Tool/Service | Category | Cost/Month | Duration | Total |
|--------------|----------|-----------|----------|--------|
| **Development Tools** | - | - | - | - |
| VS Code + Extensions | IDE | Free | 16w | Free |
| GitHub Enterprise | Version Control | ₹1.5 L | 16w | ₹1.5 L |
| JetBrains (IDE for Java/Scala) | IDE | ₹3 L | 16w | ₹3 L |
| **ML/Data Tools** | - | - | - | - |
| Jupyter Hub | Notebooks | Free | 16w | Free |
| Weights & Biases | ML Tracking | ₹2 L | 16w | ₹2 L |
| DVC (Data Version Control) | Data Tools | Free | 16w | Free |
| **Infrastructure Tools** | - | - | - | - |
| Slack (100 users) | Collaboration | ₹2.5 L | 16w | ₹2.5 L |
| Jira (Agile) | Project Mgmt | ₹1.5 L | 16w | ₹1.5 L |
| Confluence | Documentation | ₹1.5 L | 16w | ₹1.5 L |
| **Optional Commercial** | - | - | - | - |
| Pinecone (vector DB trial) | Vector DB | Free trial | 16w | Free |
| HuggingFace Enterprise | Model Hub | ₹3 L | 8w | ₹1.5 L |
| **Phase 2 Total** | - | - | - | **₹15-20 L** |

**Notes**:
- Most tools free/open-source (HuggingFace, DVC, Jupyter)
- GitHub Enterprise for team collaboration + PR reviews
- Weights & Biases for experiment tracking (ML best practices)
- Pinecone/Weaviate: evaluate for free, decide purchase in Phase 3

---

### 2.4 Data & Operations: ₹20-30 Lakhs

| Cost Item | Description | Cost |
|-----------|-------------|------|
| **Data Acquisition** | - | - |
| Web Scraping Infrastructure | Servers + bandwidth | ₹5-8 L |
| Document Download/Storage | Gazette, PIB, MoD archives | ₹3-5 L |
| **Team Operations** | - | - |
| Office Space (Phase 2 team) | 1200 sq ft for 12 engineers | ₹6-10 L |
| Utilities (Power, Internet) | 24/7 operation | ₹2-3 L |
| Hardware (Laptops, monitors) | 12 engineers × ₹2 L | ₹2 L |
| **Training & Knowledge** | - | - |
| Initial DIRAS Bootcamp | 2-week onboarding | ₹1-2 L |
| Conference attendance | 2-3 engineers | ₹2-3 L |
| **Contingency (10%)** | Unforeseen expenses | ₹2-4 L |
| **Phase 2 Ops Total** | - | **₹25-35 L** |

**Notes**:
- Office space in Bangalore/Delhi (government datacenters could provide)
- Scrapers need 24/7 operation (3-5 servers)
- Training critical for team ramp-up (defence domain knowledge)
- Budget includes team meals, travel for site visits

---

### Phase 2 Contingency & Buffer
- **Base Cost**: ₹170-235 L
- **Contingency (10%)**: ₹17-23 L
- **Phase 2 Total**: **₹155-235 L** (₹1.55-2.35 Cr)

**Phase 2 Assumption**: Should be achievable at ₹200 L (mid-range) with tight cost control.

---

## PHASE 3 Budget: ₹185-295 Lakhs (~₹2.4 Crores)

### Phase 3 Overview
- **Goal**: Full system implementation + initial scaling
- **Duration**: 14-16 weeks (Q3-Q4 2026)
- **Team Size**: 14-16 engineers
- **Infrastructure**: Hybrid (on-prem + cloud)

### 3.1 Personnel: ₹80-120 Lakhs
- **Phase 2 team continues**: ₹93-125 L
- **New hires**: 2-3 more engineers
  - Kubernetes expert: ₹8-10 L (16 weeks) = ₹8-10 L
  - NLP specialist: ₹6-8 L (16 weeks) = ₹6-8 L
  - QA automation engineer: ₹4-6 L (16 weeks) = ₹4-6 L
- **Total Personnel**: ₹105-150 L → **Avg ₹100-120 L**

---

### 3.2 Infrastructure: ₹60-100 Lakhs
- **On-Premises**: ₹40 L (from Phase 2, amortized)
- **Additional Hardware**:
  - 2 more servers (GPU-enabled): ₹30-40 L
  - Additional storage: ₹5-10 L
- **Cloud Services**:
  - AWS/GCP (GPU instances for fine-tuning): ₹15-20 L
  - Weaviate evaluation + setup: ₹5-10 L
  - Data transfer + networking: ₹5-10 L
- **Total**: ₹70-100 L → **Avg ₹80-90 L**

---

### 3.3 Tools & Licenses: ₹20-35 Lakhs
- **Phase 2 tools continue**: ₹15-20 L
- **New tools**:
  - Weaviate cloud (pilot): ₹5-10 L
  - ELK Stack / Logging (annual): ₹3-5 L
  - Kubernetes training/certification: ₹1-2 L
  - Security scanning tools: ₹1-3 L
- **Total**: ₹25-40 L → **Avg ₹30 L**

---

### 3.4 Data & Operations: ₹25-40 Lakhs
- **Data acquisition** (continued): ₹8-10 L
- **Annotation service** (NER/classification): ₹10-15 L (5K+ labeled documents)
- **Operations** (office, utilities, team): ₹8-12 L
- **Testing/QA infrastructure**: ₹2-3 L
- **Total**: ₹28-40 L → **Avg ₹35 L**

---

### Phase 3 Total: ₹185-295 Lakhs
**Midpoint**: ₹240 L (₹2.4 Cr)
**Cumulative after Phase 3**: ₹3.4-5.3 Cr

---

## PHASE 4 Budget: ₹280-430 Lakhs (~₹3.5 Crores)

### Phase 4 Overview
- **Goal**: Production deployment + scaling for 1000+ concurrent users
- **Duration**: 16-20 weeks (Q4 2026 - Q1 2027)
- **Team Size**: 18-20 engineers
- **Infrastructure**: Cloud-first + Kubernetes

### 4.1 Personnel: ₹120-180 Lakhs
- **Phase 3 team continues**: ₹105-150 L
- **New hires**:
  - 2 Cloud architects/SRE: ₹8-10 L each = ₹16-20 L
  - 1 Security engineer: ₹7-9 L = ₹7-9 L
  - 1 Product Manager: ₹6-8 L = ₹6-8 L
- **Total**: ₹140-190 L → **Avg ₹165 L**

---

### 4.2 Infrastructure: ₹100-150 Lakhs
- **On-Premises** (maintenance): ₹10-15 L
- **Cloud Infrastructure** (AWS/GCP/Azure):
  - Kubernetes cluster (8-16 nodes): ₹40-60 L
  - Vector DB (Weaviate managed): ₹20-30 L
  - LLM API (GPT-4 for queries): ₹20-30 L
  - Caching layer (Redis): ₹5-8 L
  - CDN + networking: ₹10-15 L
  - Monitoring/logging (DataDog/Splunk): ₹10-12 L
- **Total**: ₹115-170 L → **Avg ₹140 L**

---

### 4.3 Tools & Licenses: ₹30-50 Lakhs
- **Phase 3 tools continue**: ₹25-40 L
- **New tools**:
  - Kubernetes training + certifications: ₹2-4 L
  - Advanced security (threat modeling, pentest): ₹5-8 L
  - Performance optimization tools: ₹2-3 L
  - LLM fine-tuning service (Anthropic/OpenAI): ₹5-10 L
  - Advanced analytics (BigQuery/Snowflake): ₹3-5 L
- **Total**: ₹42-70 L → **Avg ₹55 L**

---

### 4.4 Data & Operations: ₹30-50 Lakhs
- **Data annotation** (expand training sets): ₹10-15 L
- **Data ingestion infrastructure**: ₹5-8 L
- **Operations** (expanded team office, redundancy): ₹8-12 L
- **UAT environment** (production-like): ₹3-5 L
- **Disaster recovery setup**: ₹4-6 L
- **Compliance/audit**: ₹2-3 L
- **Total**: ₹32-49 L → **Avg ₹40 L**

---

### Phase 4 Total: ₹280-430 Lakhs
**Midpoint**: ₹355 L (₹3.55 Cr)
**Cumulative after Phase 4**: ₹6.2-9.6 Cr

---

## PHASE 5 Budget: ₹225-355 Lakhs (~₹2.9 Crores)

### Phase 5 Overview
- **Goal**: Production stabilization + continuous optimization
- **Duration**: 12-16 weeks (Q1-Q2 2027)
- **Team Size**: 16-18 engineers (some Phase 4 team transitions to support)
- **Infrastructure**: Stable production systems

### 5.1 Personnel: ₹100-160 Lakhs
- **Phase 4 team continues** (partial): ₹100-150 L
- **Support team onboarding**: ₹5-10 L
- **Total**: ₹105-160 L → **Avg ₹130 L**

---

### 5.2 Infrastructure: ₹80-120 Lakhs
- **Cloud infrastructure** (stable, fully operational): ₹60-100 L
- **On-Premises decommissioning**: ₹5-10 L
- **DR/Backup infrastructure**: ₹10-15 L
- **Total**: ₹75-125 L → **Avg ₹100 L**

---

### 5.3 Tools & Licenses: ₹20-35 Lakhs
- **Production monitoring/logging**: ₹10-15 L
- **Security maintenance**: ₹3-5 L
- **Training for support team**: ₹3-5 L
- **Optimization tools**: ₹2-3 L
- **Total**: ₹18-28 L → **Avg ₹23 L**

---

### 5.4 Data & Operations: ₹25-40 Lakhs
- **Ongoing data quality maintenance**: ₹8-12 L
- **Operations support**: ₹10-15 L
- **Knowledge transfer documentation**: ₹3-5 L
- **Post-deployment optimization**: ₹4-8 L
- **Total**: ₹25-40 L → **Avg ₹32 L**

---

### Phase 5 Total: ₹225-355 Lakhs
**Midpoint**: ₹290 L (₹2.9 Cr)
**Cumulative after Phase 5**: ₹8.45-13.15 Cr

**⚠️ Note**: Phase 5 may exceed ₹10 Cr target. Cost optimization critical in Phases 3-4.

---

## Detailed Cost Components Breakdown

### 1. Personnel Cost Evolution

| Category | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Total |
|----------|---------|---------|---------|---------|-------|
| **Engineering Team** | ₹93-125 L | ₹105-150 L | ₹140-190 L | ₹105-160 L | ₹443-625 L |
| **Average Team Size** | 12 | 14-16 | 18-20 | 16-18 | - |
| **Cost per Engineer/Phase** | ₹8-10 L | ₹8-10 L | ₹8-10 L | ₹7-9 L | - |

**Key**: Personnel is 50-60% of total cost. Team efficiency critical.

---

### 2. Infrastructure Cost Evolution

| Category | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Total |
|----------|---------|---------|---------|---------|-------|
| **Hardware (On-Prem)** | ₹40 L | ₹20 L | ₹10 L | ₹0 L | ₹70 L |
| **Cloud Services** | ₹7-13 L | ₹50-80 L | ₹105-170 L | ₹80-125 L | ₹242-388 L |
| **Operations (Utilities, etc)** | ₹8-12 L | ₹8-12 L | ₹8-12 L | ₹8-12 L | ₹32-48 L |
| **Total Infrastructure** | ₹47-53 L | ₹70-100 L | ₹115-170 L | ₹75-125 L | ₹307-448 L |

**Key**: Cloud costs dominate from Phase 3 onwards. Vector DB + LLM APIs major cost drivers.

---

### 3. Tools & Licenses Cost Evolution

| Category | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Total |
|----------|---------|---------|---------|---------|-------|
| **Development Tools** | ₹4-5 L | ₹5-6 L | ₹5-6 L | ₹3-4 L | ₹17-21 L |
| **ML/Data Tools** | ₹3-5 L | ₹5-8 L | ₹8-12 L | ₹3-4 L | ₹19-29 L |
| **Infrastructure/Ops** | ₹5-8 L | ₹8-12 L | ₹12-18 L | ₹8-10 L | ₹33-48 L |
| **Commercial Services** | ₹3-5 L | ₹2-9 L | ₹5-14 L | ₹2-5 L | ₹12-33 L |
| **Total Tools & Licenses** | ₹15-25 L | ₹20-35 L | ₹30-50 L | ₹20-35 L | ₹85-145 L |

**Key**: Most tools free/open-source; commercial tools selectively used.

---

### 4. Data & Operations Cost Evolution

| Category | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Total |
|----------|---------|---------|---------|---------|-------|
| **Data Acquisition** | ₹8-13 L | ₹8-10 L | ₹5-8 L | ₹3-5 L | ₹24-36 L |
| **Annotation/Labeling** | ₹3-5 L | ₹10-15 L | ₹10-15 L | ₹2-3 L | ₹25-38 L |
| **Operations** | ₹8-12 L | ₹8-12 L | ₹10-15 L | ₹12-18 L | ₹38-57 L |
| **QA/Testing** | ₹2-3 L | ₹2-3 L | ₹3-5 L | ₹2-3 L | ₹9-14 L |
| **Contingency (10%)** | ₹2-4 L | ₹3-5 L | ₹6-10 L | ₹3-5 L | ₹14-24 L |
| **Total Ops & Data** | ₹25-35 L | ₹28-40 L | ₹32-49 L | ₹25-40 L | ₹110-164 L |

**Key**: Annotation costs significant (₹25-38 L total). Data quality critical.

---

## Cost Drivers by Category

### Top 5 Cost Drivers
1. **Personnel (50-60%)**: ₹443-625 L total
2. **Cloud Infrastructure (25-30%)**: ₹242-388 L total
3. **LLM APIs (8-12%)**: ₹80-120 L (Part of infrastructure in Phase 4+)
4. **Data Annotation (4-6%)**: ₹25-38 L
5. **Tools & Licenses (3-5%)**: ₹85-145 L

---

## Cost Optimization Strategies

### Phase 2 Optimization (Target: Save ₹10-15 L)
1. **Maximize free tools**: Use open-source (HuggingFace, PyTorch, FastAPI)
2. **Negotiate cloud**: Multi-year discounts with AWS/GCP
3. **In-house hardware**: On-premises focus, minimize cloud initially
4. **Team efficiency**: Tight sprint planning, minimize context switching

**Potential Savings**: ₹5-10 L

### Phase 3 Optimization (Target: Save ₹20-30 L)
1. **Annotation outsourcing**: Use Appen/Scale instead of internal (cost per annotation lower)
2. **Cloud optimization**: Reserved instances (30% discount), spot instances for training
3. **Vector DB selection**: Start with ChromaDB (free) instead of Weaviate ($)
4. **Model selection**: Use Llama 3 (free) instead of GPT-4 API (cost ₹20-30 L/year)

**Potential Savings**: ₹30-50 L

### Phase 4 Optimization (Target: Save ₹40-50 L)
1. **LLM inference**: Fine-tune Llama 3 once, use locally (eliminate GPT-4 API costs)
2. **Infrastructure consolidation**: Kubernetes optimization, reduce node count
3. **Caching strategy**: Cache embeddings, reduce re-computation
4. **Batch processing**: Batch queries, reduce latency-critical path overhead

**Potential Savings**: ₹50-80 L (₹20-30 L just on LLM APIs)

### Phase 5 Optimization (Target: Sustain savings)
1. **Support team transition**: Phase 4 team → Phase 5 support (reduce headcount)
2. **Automation**: Auto-scaling infrastructure based on load
3. **Monitoring optimization**: DataDog → self-hosted ELK (₹5-10 L/year savings)
4. **On-demand licensing**: Move from fixed to usage-based (pay per query)

**Potential Savings**: ₹20-30 L

---

## Cost Scenarios

### Scenario A: Budget Adherence (Baseline Costs)
- **Target**: ₹8-9 Crores (stick to planned costs)
- **Approach**: Execute phases on schedule, optimize as planned
- **Assumption**: No major delays, tech choices execute as planned
- **Contingency**: 10% buffer per phase

### Scenario B: Cost Overrun (Conservative)
- **Range**: ₹10-13 Crores (20-45% over budget)
- **Causes**: Timeline slips (Phase 2→ 20 weeks), team expansion, cloud over-provisioning
- **Mitigation**: Accelerate cost optimization in Phase 3, reduce scope in Phase 5
- **Probability**: 35-40%

### Scenario C: Cost Reduction (Optimized)
- **Range**: ₹6-7.5 Crores (10-25% under budget)
- **Causes**: Efficient team execution, early cloud cost optimization, scope focus
- **Requirements**: Strict cost discipline, vendor negotiations, minimal rework
- **Probability**: 20-25%

---

## Cost by Document Type Processing

### Breakdown of Infrastructure Costs by Capability

| Capability | Hardware | Cloud | Tools | Personnel | Total/Month |
|------------|----------|-------|-------|-----------|------------|
| **Document Scraping** | ₹3-5 L | ₹2-3 L | ₹1 L | ₹4-6 L | ₹10-15 L |
| **OCR Processing** | ₹5-8 L | ₹3-5 L | ₹1 L | ₹6-8 L | ₹15-22 L |
| **Preprocessing** | ₹2-3 L | ₹1-2 L | ₹0.5 L | ₹3-4 L | ₹6.5-9.5 L |
| **Classification** | ₹2-3 L | ₹5-8 L | ₹1 L | ₹4-6 L | ₹12-18 L |
| **NER** | ₹2-3 L | ₹5-8 L | ₹1 L | ₹4-6 L | ₹12-18 L |
| **Embeddings** | ₹3-5 L | ₹5-8 L | ₹1-2 L | ₹4-6 L | ₹13-21 L |
| **Vector DB** | ₹3-5 L | ₹8-12 L | ₹2-3 L | ₹2-3 L | ₹15-23 L |
| **Retrieval** | ₹2-3 L | ₹3-5 L | ₹1 L | ₹3-4 L | ₹9-13 L |
| **RAG/LLM** | ₹1-2 L | ₹15-25 L | ₹2-3 L | ₹4-6 L | ₹22-36 L |

**Note**: "Cloud" column includes pay-per-use costs (LLM APIs, GPU instances). These are most controllable cost levers.

---

## Budget Control Mechanisms

### Monthly Cost Tracking
- **First of month**: Budget vs. actual analysis
- **Weekly**: Infrastructure cost monitoring (AWS/GCP billing)
- **Real-time**: Query-level cost tracking (cost per RAG query)
- **Escalation**: Alert if costs exceed 80% of monthly budget

### Approval Thresholds
- **<₹5 L**: Team lead approval
- **₹5-20 L**: Engineering manager approval
- **₹20-50 L**: Project manager + Finance approval
- **>₹50 L**: Executive sponsor approval

### Cost Reduction Triggers
- **>10% over budget in Phase 2**: Review scope, reduce non-critical features
- **>15% over budget in Phase 3**: Accelerate optimization initiatives
- **>20% over budget in Phase 4**: Consider phase delay, team restructure

---

## Cost Comparison with Alternatives

### Make vs. Buy Analysis

| Component | Build (In-House) | Buy (Commercial) | Cost Difference |
|-----------|------------------|------------------|-----------------|
| **Vector DB** | FAISS (Free) | Pinecone (₹20-30 L/yr) | Save ₹20-30 L |
| **LLM Service** | Llama 3 (Free) | GPT-4 API (₹20-30 L/yr) | Save ₹20-30 L |
| **Document Processing** | Custom (₹15-20 L) | Docling API (₹5-10 L) | Save ₹5-15 L |
| **Annotation** | Internal (₹25-40 L) | Outsourced (₹20-30 L) | Save ₹5-20 L |
| **Monitoring** | Open-source ELK (₹3-5 L/yr) | DataDog (₹10-15 L/yr) | Save ₹7-10 L |

**Strategy**: Build core components (vector DB, LLM), buy specialized services (annotation, monitoring). Estimated savings: ₹50-100 L.

---

## Return on Investment (ROI) Analysis

### Cost vs. Value Delivered

| Phase | Cost | Documents Indexed | Queries/Day | Value Unlocked |
|-------|------|-------------------|-------------|-----------------|
| **Phase 2** | ₹2 Cr | 5,000 | 10-50 | Tech prototype + proof of concept |
| **Phase 3** | ₹2.4 Cr | 50,000 | 100-500 | MVP for internal use |
| **Phase 4** | ₹3.5 Cr | 200,000 | 1,000-5,000 | Production system, public beta |
| **Phase 5** | ₹2.9 Cr | 300,000 | 5,000-10,000 | Operational system, ROI achieved |

### Cost per Capability
- **Phase 2**: ₹400-800 per document indexed
- **Phase 3**: ₹50-100 per document indexed
- **Phase 4**: ₹20-30 per document indexed
- **Phase 5**: ₹10-20 per document indexed (economies of scale)

### Break-Even Analysis
- **Total investment**: ₹8-10 Crores (over 18-24 months)
- **Annual operating cost** (Phase 5+): ₹50-80 Lakhs (personnel + infrastructure)
- **Break-even**: 10-15 years (if zero revenue model)
- **If monetized** (SaaS): Reduced break-even to 3-5 years (assuming ₹50 L/year ARR)

---

## Appendix: Cost Assumptions

### Salary Assumptions
- **Senior ML Engineer**: ₹8-10 L/month
- **ML Engineer**: ₹5-7 L/month
- **Backend Engineer**: ₹5-7 L/month
- **DevOps Engineer**: ₹6-8 L/month
- **Data Engineer**: ₹6-8 L/month
- **QA Engineer**: ₹4-6 L/month
- **Engineering Lead**: ₹8-10 L/month

**Include**: Base salary + PF (12%) + Health Insurance (₹1-1.5 L/year) + GST (18%)

### Infrastructure Assumptions
- **GPU instance** (AWS p3.8xlarge): ₹120K-150K/month
- **CPU instance** (32 core): ₹20K-30K/month
- **Vector DB** (Weaviate): ₹0.5-1$/month per M vectors
- **LLM API** (GPT-4): ₹10-20 per 1K tokens (avg ₹5-10 per query)
- **Cloud storage**: ₹0.02-0.03 per GB/month

### Timeline Assumptions
- **Phase 2-5**: 4 phases × 14-20 weeks = 18-24 months
- **Phase 2**: 16 weeks = 4 months (July-Oct 2026)
- **Phase 3**: 16 weeks = 4 months (Oct 2026-Jan 2027)
- **Phase 4**: 18 weeks = 4.5 months (Jan-May 2027)
- **Phase 5**: 16 weeks = 4 months (May-Aug 2027)

---

**Document Owner**: Finance Lead + Technical Lead  
**Next Review**: June 30, 2026 (Month 1 of Phase 2)  
**Approval**: [Pending Phase 2 Project Kickoff]

---

*Budget subject to change based on scope decisions, hiring delays, and market conditions. Monthly tracking and quarterly re-forecasting essential.*
