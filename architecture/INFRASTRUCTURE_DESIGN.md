# Infrastructure Architecture Design - DIRAS Phase 2-5 Progression

**Document Version**: 1.0  
**Last Updated**: May 28, 2026  
**Timeline**: Phase 2 (Q3 2026) → Phase 5 (Q2 2027)  
**Scope**: On-premises → Hybrid → Cloud-native evolution

---

## Executive Summary

DIRAS infrastructure evolves from lightweight on-premises setup (Phase 2) → hybrid cloud (Phase 3) → enterprise cloud-native (Phase 4+). This document specifies compute, storage, networking, and operational requirements for each phase, including scaling thresholds and disaster recovery.

---

## Architecture Evolution Overview

```
Phase 2: Local Dev/Test
├─ Single server (256GB RAM, 16 cores)
├─ NAS storage (20TB)
├─ ChromaDB in-memory vector DB
└─ Manual operations

Phase 3: Initial Scale
├─ 2 app servers + 1 DB server
├─ Weaviate evaluation
├─ 100 QPS target
└─ Basic monitoring

Phase 4: Production Scale
├─ Kubernetes (8-16 nodes)
├─ Managed Weaviate
├─ 1000+ QPS target
├─ Auto-scaling, multi-region DR
└─ Enterprise monitoring

Phase 5: Optimized Production
├─ Kubernetes (auto-scaling)
├─ Multi-region failover
├─ 10,000+ QPS capable
└─ Full observability, cost-optimized
```

---

## PHASE 2: Local Development & Proof of Concept

### 2.1 Compute Architecture

**Hardware Specification**
| Component | Quantity | Specification | Cost |
|-----------|----------|---------------|------|
| **Primary Server** | 1 | 256GB RAM, 16 cores, 2x SSD 2TB | ₹15 L |
| **Backup/Secondary** | 1 | 256GB RAM, 16 cores, 2x SSD 2TB | ₹15 L |
| **Network Switch** | 1 | 10GbE managed switch | ₹3 L |
| **Total Compute** | - | - | **₹33 L** |

**Deployment Topology**
```
On-Premises Datacenter (Single Location)
│
├─ Primary Server (256GB, 16c)
│  ├─ Docker containers (development)
│  ├─ ChromaDB (vector DB)
│  ├─ FastAPI (API server)
│  ├─ OCR service
│  ├─ Preprocessing
│  └─ Jupyter notebooks
│
├─ Backup Server (manual failover)
│  └─ Periodic backup of data + code
│
└─ NAS Storage (20TB, RAID-6)
   ├─ Raw documents (10TB)
   ├─ Processed documents (5TB)
   └─ Backups (5TB)
```

**Vector DB: ChromaDB**
- **Rationale**: Open-source, in-process, no external dependencies
- **Deployment**: Python library within API server
- **Capacity**: 1-2M vectors in-memory (sufficient for Phase 2)
- **Performance**: <10ms query latency for <100 QPS
- **Cost**: Free

**Scaling Limits (Phase 2)**
- Max concurrent queries: 50-100
- Max documents in vector DB: 2M
- Max document size: 100MB
- Storage capacity: 20TB (sufficient for 50K documents)

---

### 2.2 Storage Architecture

**Document Storage**
```
NAS (/mnt/diras-storage/)
├─ /raw/
│  ├─ ministry-defence/ (scraped PDFs)
│  ├─ gazette-india/ (gazette documents)
│  ├─ pib/ (press releases)
│  └─ drdo/ (research reports)
│
├─ /processed/
│  ├─ extracted-text/ (OCR output)
│  ├─ embeddings/ (vector data)
│  └─ metadata/ (JSON annotations)
│
└─ /backups/
   ├─ daily/ (keep 7 days)
   ├─ weekly/ (keep 4 weeks)
   └─ monthly/ (keep 12 months)
```

**Backup Strategy (Phase 2)**
- **Method**: Daily rsync to external drive (manual weekly to cloud)
- **Retention**: 7 days daily + 4 weeks weekly + 12 months monthly
- **RTO**: 24 hours (manual restore)
- **RPO**: 24 hours (daily backup window)
- **Cost**: ₹2-3 L for cloud backup storage

**Data Redundancy**
- NAS with RAID-6 (can survive 2 disk failures)
- Weekly backup to external SSD (kept off-site)
- Monthly cloud backup (AWS S3 cold storage)

---

### 2.3 Networking (Phase 2)

**Network Topology**
```
Internet
│
└─ Firewall (UFW on Linux)
   │
   └─ 10GbE Switch
      │
      ├─ Primary Server (10.0.1.10)
      ├─ Backup Server (10.0.1.11)
      └─ NAS Storage (10.0.1.20)
```

**Network Specs**
- **LAN**: 10GbE internal (low-latency communication)
- **Internet**: 1Gbps uplink (for cloud backup, external scraping)
- **Firewall**: UFW with restricted SSH access
- **DNS**: Internal DNS (no external resolution required)

**API Access**
- Local network only (no public internet initially)
- VPN access for remote team members
- Manual deployment (git pull + restart)

---

### 2.4 Operations (Phase 2)

**Deployment Process**
1. Developer pushes code to GitHub
2. Manual SSH to server
3. Pull latest code, run tests
4. Restart Docker containers
5. Verify with manual queries

**Monitoring**
- Basic system metrics: CPU, RAM, disk usage (simple scripts)
- Application logs: Syslog (centralized on server)
- No automated alerts initially
- Manual daily health check

**Team Operations**
- In-house datacentre or colocation (₹5-10 L/month)
- Manual 24/7 support (on-call engineer)
- Minimal documentation

---

## PHASE 3: Hybrid Cloud Scaling

### 3.1 Compute Architecture (Phase 3)

**Hardware Expansion**
| Component | Quantity | Specification | Cost |
|-----------|----------|---------------|------|
| **API Servers** | 2 | 64GB RAM, 8 cores each | ₹8 L |
| **Vector DB Server** | 1 | 256GB RAM, 16 cores | ₹15 L |
| **GPU Server** (optional) | 1 | NVIDIA A100, 80GB VRAM | ₹20 L |
| **Colocation** | - | Space + power + connectivity | ₹15-20 L |
| **Total Cost** | - | - | **₹60-80 L** |

**Deployment Topology (Hybrid)**
```
On-Premises (Private Datacenter)
│
├─ Load Balancer (HAProxy)
│  │
│  ├─ API Server 1 (64GB, 8c)
│  └─ API Server 2 (64GB, 8c)
│
├─ Vector DB Server (Weaviate) (256GB, 16c)
│  └─ 5-10M vectors, 1-5TB index size
│
├─ GPU Server (optional)
│  └─ Embedding generation
│
└─ NAS Storage (40TB)
   ├─ Documents (30TB)
   └─ Backups (10TB)

Cloud (AWS)
│
├─ Backup Vector DB (replica)
├─ Cold storage (documents)
├─ Batch processing (GPU instances)
└─ DR failover (standby)
```

**Vector DB: Weaviate Migration**
- **Rationale**: Handles 5-10M vectors, better indexing
- **Deployment**: Docker container on dedicated server
- **Capacity**: 5-10M vectors (sufficient for Phase 3)
- **Performance**: 50-100ms query latency for <500 QPS
- **Cost**: Self-hosted (free) vs. Weaviate Cloud (₹5-10 L/month)

**Scaling Thresholds (Phase 3)**
- Max concurrent queries: 100-500
- Max documents: 50K-100K
- API response time target: <500ms p95
- Vector DB query latency: <100ms

---

### 3.2 Load Balancing & Failover

**Load Balancer Configuration**
```
HAProxy (on-premises)
│
├─ Health checks every 5 seconds
├─ Session persistence (sticky cookies)
└─ Round-robin across 2 API servers
```

**Failover Logic**
- If API Server 1 down → all traffic to Server 2
- If Server 2 down → all traffic to Server 1
- If both down → manual switchover to cloud backup (4-6 hours)

---

### 3.3 Cloud Integration (Phase 3)

**AWS Services** (minimal, for DR + batch)
- **S3 for cold storage**: ₹2-3 L/year
- **RDS for metadata**: ₹3-5 L/year (optional, use PostgreSQL on-prem)
- **Lambda for batch jobs**: ₹1-2 L/year
- **Backup replication**: ₹2-3 L/year
- **Total cloud cost**: ₹8-13 L/year

---

### 3.4 Operations (Phase 3)

**Deployment Process** (Automated)
1. Developer pushes to GitHub
2. CI/CD pipeline (Jenkins/GitHub Actions)
3. Run tests + build Docker image
4. Deploy to staging server (validation)
5. Blue-green deploy to production (zero-downtime)

**Monitoring**
- Prometheus + Grafana (dashboards for CPU, RAM, latency)
- ELK Stack (log aggregation + search)
- Custom alerts (Slack notifications)
- Weekly review of metrics

**Team Operations**
- Colocation facility management
- On-call rotation (2 engineers)
- Documentation: Wiki for runbooks

---

## PHASE 4: Production Cloud-Native

### 4.1 Kubernetes Architecture

**Cluster Specification**
| Component | Count | Instance Type | Total Cost |
|-----------|-------|---------------|-----------|
| **Master Nodes** | 3 | t3.xlarge (4GB RAM, 2c) | ₹5 L |
| **Worker Nodes** | 8-12 | r5.2xlarge (64GB RAM, 8c) | ₹60-100 L |
| **GPU Nodes** | 2-4 | p3.8xlarge (NVIDIA V100) | ₹40-80 L |
| **Managed Services** | - | EKS/GKE | ₹30-50 L |
| **Load Balancer** | 1 | AWS ALB | ₹10-15 L |
| **Total Kubernetes** | - | - | **₹145-250 L** |

**Kubernetes Topology**
```
AWS EKS Cluster (Production)
│
├─ Namespace: default
│  ├─ API Deployment (3 replicas, r5.2xlarge)
│  ├─ Preprocessing Deployment (2 replicas)
│  └─ Query Service (4 replicas)
│
├─ Namespace: ml
│  ├─ Embedding Service (2 replicas, GPU)
│  ├─ OCR Service (1 replica, GPU)
│  └─ Classification Service (2 replicas, GPU)
│
├─ Namespace: data
│  ├─ Weaviate StatefulSet (3 replicas)
│  └─ PostgreSQL (managed RDS)
│
├─ Namespace: ingestion
│  ├─ Scraper CronJob (daily)
│  ├─ Batch Processing (on-demand)
│  └─ Indexing Job (nightly)
│
└─ Monitoring
   ├─ Prometheus
   ├─ Grafana
   └─ ELK Stack
```

**Auto-scaling Configuration**
- **API Pods**: 3-10 replicas (based on CPU 70%, memory 80%)
- **GPU Pods**: 2-8 replicas (based on job queue)
- **Worker Nodes**: 8-20 nodes (based on pod capacity)
- **Scaling time**: 2-5 minutes for node provisioning

**Vector DB: Managed Weaviate Cloud**
- **Deployment**: Weaviate Cloud Service (managed)
- **Capacity**: 10-50M vectors
- **Availability**: Multi-zone redundancy
- **Cost**: ₹20-30 L/month
- **Alternative**: Self-managed Weaviate on K8s (lower cost, more ops)

---

### 4.2 Database Architecture

**Primary Database (PostgreSQL)**
```
AWS RDS Multi-AZ
├─ Primary (us-east-1a)
├─ Standby replica (us-east-1b, automatic failover)
└─ Read replica (us-east-1c, for analytics)
```

**Database Schema**
```
Tables:
├─ documents (id, source, url, scraped_date, processed_date)
├─ document_metadata (doc_id, authority, date_published, budget_amount)
├─ entities (doc_id, entity_type, value, position)
├─ embeddings (doc_id, embedding_id, chunk_text)
├─ queries (query_text, intent, timestamp, user_id)
└─ query_results (query_id, retrieved_docs, ranking)

Indexes:
├─ documents (source, scraped_date)
├─ entities (entity_type, value)
└─ queries (timestamp, user_id)
```

**Backup & Recovery**
- Automated daily snapshots (kept 30 days)
- Point-in-time recovery (last 7 days)
- RTO: <5 minutes
- RPO: <1 minute (continuous replication)

---

### 4.3 Caching Architecture

**Redis Cluster** (Distributed Caching)
```
AWS ElastiCache (Redis)
├─ 3 nodes (multi-AZ)
├─ 50GB capacity
├─ Use cases:
│  ├─ Query result cache (1 hour TTL)
│  ├─ Embedding cache (24 hour TTL)
│  └─ Session state (24 hour TTL)
│
└─ Hit ratio target: 70%+ (save 70% of DB queries)
```

**Cost**: ₹5-8 L/month

---

### 4.4 CDN & Static Content

**CloudFront Distribution**
- Static assets (HTML, CSS, JS)
- API documentation
- Cached embeddings (reduce re-computation)
- Cost: ₹1-2 L/month

---

### 4.5 Storage (Phase 4)

**Document Storage**
- **Primary**: AWS S3 (standard, for hot data)
- **Archive**: S3 Glacier (for cold data >30 days)
- **Backup**: Cross-region replication

**Cost**: ₹5-8 L/month

---

### 4.6 Disaster Recovery (Phase 4)

**Multi-region Setup**
```
Primary Region (us-east-1)
├─ EKS Cluster
├─ RDS Primary
├─ Weaviate Primary
└─ S3 bucket

DR Region (eu-west-1)
├─ Standby EKS (auto-scale on failover)
├─ RDS Read Replica (promoted to primary on failover)
├─ Weaviate Replica (read-only)
└─ S3 cross-region replication
```

**Failover Procedure**
1. Automated detection of primary region failure (2 minutes)
2. Promote DR region to primary (5 minutes)
3. DNS failover (Route 53 health checks)
4. Total RTO: <15 minutes
5. RPO: <1 minute (continuous replication)

**Cost**: ₹50-80 L/month (double infrastructure)

---

### 4.7 Security (Phase 4)

**Network Security**
- VPC with public + private subnets
- Security groups (whitelist traffic)
- VPN for team access
- WAF for DDoS protection (₹3-5 L/month)

**Data Security**
- Encryption at rest (EBS, RDS, S3)
- Encryption in transit (TLS 1.3)
- Key management (AWS KMS)
- Access logging (CloudTrail)

**Compliance**
- ISO 27001 audit (annual)
- Security scanning (OWASP ZAP, Snyk)
- Penetration testing (quarterly)

---

### 4.8 Monitoring & Observability

**Prometheus + Grafana**
- Metrics collection (scrape every 15s)
- Dashboards: API latency, query throughput, error rates
- Cost: ₹2-3 L/month (managed service)

**ELK Stack (Elasticsearch, Logstash, Kibana)**
- Centralized logging from all pods
- Log retention: 30 days (hot), 1 year (cold)
- Full-text search across logs
- Cost: ₹10-15 L/month (managed or self-hosted)

**Distributed Tracing (Jaeger)**
- Request tracing across services
- Latency analysis per component
- Cost: ₹1-2 L/month

**Alerting**
- Slack integration for critical alerts
- PagerDuty for on-call escalation
- Custom rules (latency >500ms, error rate >1%)

---

## PHASE 5: Optimized Production

### 5.1 Cost Optimization

**Kubernetes Optimization**
- Reserved instances (30% discount): ₹40-50 L/month savings
- Spot instances (70% discount) for non-critical workloads: ₹20-30 L savings
- Node consolidation (reduce from 16 to 12 nodes): ₹15-20 L savings
- Vertical Pod Autoscaling (right-size containers): ₹10-15 L savings

**Total Phase 5 cost**: ₹80-120 L/month (vs. Phase 4: ₹120-160 L/month)

---

### 5.2 Auto-scaling Improvements

**Horizontal Pod Autoscaling (HPA)**
```
API Deployment:
├─ Min replicas: 3
├─ Max replicas: 10
├─ Scale up: CPU >70% or Memory >80%
├─ Scale down: CPU <30% (after 5 min idle)
└─ Cooldown: 3 min between scaling events

Embedding Service:
├─ Min replicas: 1
├─ Max replicas: 8
├─ Scale up: Job queue depth >100
└─ GPU utilization >60%
```

**Vertical Pod Autoscaling (VPA)**
- Auto-adjust CPU/memory requests based on usage
- Potential savings: 20-30% over-provisioning reduction

---

### 5.3 Multi-region Failover (Simplified)

In Phase 5, if primary region is healthy:
- Active-active setup (distribute traffic across regions)
- 50% traffic to us-east, 50% to eu-west
- Automatic failover if region becomes unavailable
- Load balancing at global level (Route 53)

---

### 5.4 Infrastructure as Code (Phase 5)

**Terraform**
```
├─ kubernetes/ (cluster config)
├─ databases/ (RDS, ElastiCache)
├─ networking/ (VPC, security groups)
├─ monitoring/ (Prometheus, Grafana)
├─ backup/ (snapshots, replication)
└─ variables.tf (environment-specific)
```

**Helm Charts**
- Deployments as templated Helm charts
- Version control for all infrastructure
- Reproducible deployments

**CI/CD Integration**
- Terraform plan on PR
- Automatic apply on merge to main
- Rollback capability (git revert)

---

## Scaling Progression Summary

| Metric | Phase 2 | Phase 3 | Phase 4 | Phase 5 |
|--------|---------|---------|---------|---------|
| **Concurrent Users** | 10-50 | 50-500 | 500-5,000 | 5,000-10,000 |
| **Queries/Day** | 100-500 | 1,000-10,000 | 10,000-100,000 | 100,000-500,000 |
| **Documents** | 5K | 50K | 200K | 300K+ |
| **Vector DB Vectors** | 1-2M | 5-10M | 10-50M | 50-100M |
| **Servers/Nodes** | 2 | 5 | 12-16 | 12-20 (auto-scaling) |
| **Response Time p95** | <500ms | <300ms | <200ms | <100ms |
| **Availability** | 99% | 99.5% | 99.9% | 99.99% |
| **Monthly Cost** | ₹10-15 L | ₹20-30 L | ₹120-160 L | ₹80-120 L |

---

## Technology Stack Evolution

| Component | Phase 2 | Phase 3 | Phase 4 | Phase 5 |
|-----------|---------|---------|---------|---------|
| **Container Runtime** | Docker | Docker | Kubernetes | Kubernetes |
| **Orchestration** | Manual | Manual | EKS/GKE | EKS/GKE |
| **Vector DB** | ChromaDB | Weaviate (self) | Weaviate Cloud | Weaviate Cloud |
| **Database** | SQLite | PostgreSQL (on-prem) | RDS | RDS Multi-region |
| **Cache** | In-memory | Redis | ElastiCache | ElastiCache Cluster |
| **Search** | Basic | Elasticsearch | ElasticSearch | Opensearch (cost optimized) |
| **Monitoring** | Scripts | Prometheus/Grafana | Prometheus/Grafana | Prometheus/Grafana + DataDog |
| **Logging** | Syslog | ELK Stack | ELK Stack | Opensearch + Loki |
| **CI/CD** | Manual | GitHub Actions | GitHub Actions + ArgoCD | GitHub Actions + ArgoCD |

---

## Appendix: Infrastructure Checklists

### Phase 2 Setup Checklist
- [ ] Procure 2 servers (256GB RAM, 16c)
- [ ] Set up NAS (RAID-6, 20TB)
- [ ] Install Linux (Ubuntu 20.04 LTS)
- [ ] Set up Docker + Docker Compose
- [ ] Configure firewall + SSH hardening
- [ ] Set up Git + CI/CD pipeline (GitHub Actions)
- [ ] Deploy ChromaDB
- [ ] Set up basic monitoring (Grafana)
- [ ] Create backup schedule (daily rsync)
- [ ] Document architecture (this file)

### Phase 3 Setup Checklist
- [ ] Procure additional servers (API x2, DB x1, GPU optional)
- [ ] Set up HAProxy load balancer
- [ ] Migrate to Weaviate (evaluation + setup)
- [ ] Configure AWS account (S3, Lambda, backup)
- [ ] Set up automated CI/CD (blue-green deployment)
- [ ] Implement Prometheus + Grafana monitoring
- [ ] Set up ELK stack for centralized logging
- [ ] Configure RDS for metadata (optional migration from SQLite)
- [ ] Test failover procedures
- [ ] Set up VPN for remote team access

### Phase 4 Setup Checklist
- [ ] Provision AWS EKS cluster (3 master, 8-12 worker nodes)
- [ ] Set up Kubernetes namespaces (default, ml, data, ingestion)
- [ ] Deploy applications as Helm charts
- [ ] Configure Horizontal Pod Autoscaling
- [ ] Set up managed Weaviate Cloud (or self-hosted on K8s)
- [ ] Implement distributed tracing (Jaeger)
- [ ] Configure multi-region DR setup
- [ ] Set up automated backup + recovery procedures
- [ ] Implement security scanning (OWASP ZAP, Snyk)
- [ ] Plan disaster recovery drill

### Phase 5 Setup Checklist
- [ ] Implement cost optimization (reserved instances, spot instances)
- [ ] Set up infrastructure as code (Terraform)
- [ ] Implement GitOps workflow (ArgoCD)
- [ ] Configure global load balancing (Route 53 active-active)
- [ ] Optimize caching strategy (70%+ hit ratio)
- [ ] Implement advanced monitoring (DataDog, custom dashboards)
- [ ] Automate capacity planning (Vertical Pod Autoscaling)
- [ ] Plan multi-region failover drills
- [ ] Implement cost tracking + allocation per team
- [ ] Archive Phase 2-4 infrastructure docs (for reference)

---

**Document Owner**: Infrastructure Lead  
**Next Review**: July 31, 2026 (Month 2 of Phase 2)  
**Approval**: [Pending Phase 2 Project Kickoff]

---

*Infrastructure is critical path for Phase 2 onboarding. Early decision on on-premises vs. cloud saves ₹30-50 L by Phase 3.*
