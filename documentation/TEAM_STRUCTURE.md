# Team Structure & Hiring Plan - DIRAS Phase 2-5

**Document Version**: 1.0  
**Last Updated**: May 28, 2026  
**Timeline**: Hiring begins June 2026 (Phase 2 starts July 2026)  
**Total Team Growth**: 12 engineers → 20 engineers by Phase 4

---

## Executive Summary

DIRAS requires skilled engineering team growing from 12 (Phase 2) → 14-16 (Phase 3) → 18-20 (Phase 4) → 16-18 (Phase 5). This document defines roles, skill requirements, hiring timeline, and onboarding/training strategy.

---

## Phase 2 Team Structure (12 Engineers)

### Organizational Chart (Phase 2)

```
Project Manager
├─ Technical Lead / Engineering Manager
│  ├─ ML Team (5 engineers)
│  │  ├─ Senior ML Engineer (2) - Lead OCR, embeddings, classification
│  │  └─ ML Engineer (3) - NER, preprocessing, entity extraction
│  │
│  ├─ Backend Team (3 engineers)
│  │  ├─ Senior Backend Engineer (1) - API architecture, vector DB
│  │  └─ Backend Engineer (2) - API endpoints, database design
│  │
│  ├─ Data Engineering (1 engineer)
│  │  └─ Data Engineer (1) - Scraping, document processing, ETL
│  │
│  ├─ DevOps (1 engineer)
│  │  └─ DevOps Engineer (1) - Infrastructure, deployment, monitoring
│  │
│  └─ QA (1 engineer)
│     └─ QA Engineer (1) - Testing, evaluation framework
```

**Team Summary**
| Role | Count | Seniority | Focus |
|------|-------|-----------|-------|
| Technical Lead / Manager | 1 | Senior | Architecture, mentorship, roadmap |
| Senior ML Engineer | 2 | Senior | Model development, research |
| ML Engineer | 3 | Mid | Implementation, training |
| Senior Backend Engineer | 1 | Senior | API design, system architecture |
| Backend Engineer | 2 | Mid | Feature development, integration |
| Data Engineer | 1 | Mid | Pipeline, ETL, data quality |
| DevOps Engineer | 1 | Mid | Infrastructure, automation |
| QA Engineer | 1 | Mid | Testing, evaluation |
| **Total** | **12** | - | - |

---

## Phase 2 Role Descriptions & Skill Requirements

### 1. Technical Lead / Engineering Manager
**Count**: 1  
**Seniority**: Senior (10+ years)  
**Reports to**: Project Manager

**Responsibilities**
- Oversee technical architecture (design decisions, code reviews)
- Lead sprint planning + retrospectives
- Mentor junior engineers (1-on-1s, growth)
- Manage inter-team dependencies
- Escalate risks + blockers to PM
- Lead technical hiring + interviews

**Required Skills**
- ✓ 10+ years software engineering
- ✓ Experience with ML systems (training, deployment)
- ✓ Team leadership (managed 5+ engineers)
- ✓ Python, Java or Go
- ✓ Agile/Scrum methodology
- ✓ Communication (clear documentation, public speaking)

**Desired Skills**
- Deep learning / transformer models
- NLP systems at scale
- Kubernetes / cloud infrastructure
- Defence/government domain experience

**Hiring Target**: Immediate (Month 1, June 2026)  
**Monthly Salary**: ₹8-10 L  
**Benefits**: Health insurance, PF, stock options (₹5-10 L over 3 years)

---

### 2. Senior ML Engineer (x2)
**Count**: 2  
**Seniority**: Senior (7+ years ML)  
**Reports to**: Technical Lead

**Responsibilities**
- Lead OCR module development (EasyOCR + fine-tuning)
- Lead embedding generation research (model selection, fine-tuning)
- Mentor junior ML engineers
- Experiment tracking + documentation
- Research + benchmarking

**Required Skills**
- ✓ 7+ years ML engineering
- ✓ Deep learning (PyTorch or TensorFlow)
- ✓ NLP/CV (text or image models)
- ✓ Model evaluation + metrics
- ✓ Python, Jupyter notebooks
- ✓ HuggingFace / transformer experience

**Desired Skills**
- OCR / document understanding
- NER / entity extraction
- Fine-tuning transformer models
- Production ML systems
- Defence domain knowledge

**Hiring Target**: Month 1 (June 2026)  
**Monthly Salary**: ₹8-10 L each  
**Hiring Challenge**: Scarce in India (may need relocation bonus ₹20-30 L)

---

### 3. ML Engineer (x3)
**Count**: 3  
**Seniority**: Mid (3-5 years)  
**Reports to**: Technical Lead or Senior ML Engineer (mentorship)

**Responsibilities**
- Implement preprocessing pipeline (NLTK, spaCy)
- Implement document classification (TF-IDF, BERT fine-tuning)
- Implement NER (spaCy, BERT NER)
- Experiment tracking + results reporting
- Write clean, documented code

**Required Skills**
- ✓ 3-5 years Python/ML
- ✓ NLP basics (tokenization, embedding concepts)
- ✓ PyTorch or TensorFlow
- ✓ HuggingFace library experience
- ✓ Git, GitHub, pull requests
- ✓ Unit testing + documentation

**Desired Skills**
- BERT / transformer fine-tuning
- Scikit-learn experience
- Docker for ML
- Linear algebra + probability

**Hiring Target**: Month 1-2 (June-July 2026)  
**Monthly Salary**: ₹5-7 L each  
**Hiring Challenge**: Medium (available, but competing with startups)

---

### 4. Senior Backend Engineer (x1)
**Count**: 1  
**Seniority**: Senior (8+ years backend)  
**Reports to**: Technical Lead

**Responsibilities**
- Design FastAPI backend architecture
- Design vector DB integration
- Design database schema + optimization
- Code review for backend team
- Mentoring junior backend engineer

**Required Skills**
- ✓ 8+ years backend engineering
- ✓ Python/FastAPI or Go/Gin
- ✓ REST API design
- ✓ SQL + database optimization
- ✓ System design thinking
- ✓ Testing + CI/CD

**Desired Skills**
- Vector database experience (FAISS, ChromaDB, Weaviate)
- Search engine experience (Elasticsearch)
- Microservices architecture
- Infrastructure as code

**Hiring Target**: Month 1 (June 2026)  
**Monthly Salary**: ₹8-10 L  
**Hiring Challenge**: High-demand role, may need premium salary

---

### 5. Backend Engineer (x2)
**Count**: 2  
**Seniority**: Mid (3-5 years)  
**Reports to**: Senior Backend Engineer (mentorship)

**Responsibilities**
- Implement FastAPI endpoints (query, search, retrieval)
- Implement database migrations + ORM
- Write unit + integration tests
- Participate in code reviews
- Deployment + monitoring support

**Required Skills**
- ✓ 3-5 years Python backend
- ✓ FastAPI or Flask
- ✓ SQL + ORM (SQLAlchemy)
- ✓ REST API design + testing
- ✓ Git, GitHub, CI/CD basics
- ✓ Docker + containerization

**Desired Skills**
- FastAPI best practices
- Async/await programming
- Request tracing + logging
- Performance optimization

**Hiring Target**: Month 1-2 (June-July 2026)  
**Monthly Salary**: ₹5-7 L each

---

### 6. Data Engineer (x1)
**Count**: 1  
**Seniority**: Mid (4-6 years)  
**Reports to**: Technical Lead

**Responsibilities**
- Build document scraping pipeline (Scrapy, BeautifulSoup)
- Build document extraction pipeline (PyPDF, pdfplumber)
- Build preprocessing ETL pipeline
- Monitor data quality + completeness
- Create data quality dashboards

**Required Skills**
- ✓ 4-6 years data engineering
- ✓ Python (Pandas, Numpy)
- ✓ Web scraping (BeautifulSoup, Scrapy)
- ✓ SQL + databases
- ✓ ETL pipeline design
- ✓ Git, version control

**Desired Skills**
- Apache Airflow (orchestration)
- Distributed processing (Spark)
- Data validation frameworks (Great Expectations)
- PDF processing libraries

**Hiring Target**: Month 1-2 (June-July 2026)  
**Monthly Salary**: ₹6-8 L

---

### 7. DevOps Engineer (x1)
**Count**: 1  
**Seniority**: Mid (4-6 years)  
**Reports to**: Technical Lead

**Responsibilities**
- Set up on-premises servers + networking
- Set up Docker + CI/CD pipeline
- Manage backups + disaster recovery
- Monitor system health + logs
- Troubleshoot deployment issues

**Required Skills**
- ✓ 4-6 years DevOps / SRE
- ✓ Linux administration
- ✓ Docker containerization
- ✓ CI/CD (GitHub Actions, Jenkins)
- ✓ Bash scripting
- ✓ Networking basics (IP, DNS, firewall)

**Desired Skills**
- Kubernetes (prepare for Phase 3)
- Infrastructure as code (Terraform)
- Monitoring (Prometheus, ELK)
- AWS / cloud basics

**Hiring Target**: Month 1 (June 2026)  
**Monthly Salary**: ₹6-8 L

---

### 8. QA Engineer (x1)
**Count**: 1  
**Seniority**: Mid (3-5 years)  
**Reports to**: Technical Lead

**Responsibilities**
- Build evaluation framework (metrics, benchmarking)
- Create test datasets (golden sets, edge cases)
- Run model evaluation tests
- Write integration tests
- Performance testing

**Required Skills**
- ✓ 3-5 years QA / testing
- ✓ Python scripting
- ✓ Test automation
- ✓ SQL + databases
- ✓ Metrics + measurement methodology
- ✓ Attention to detail

**Desired Skills**
- ML model testing
- Performance testing (load, stress)
- Test data generation
- Ragas framework (RAG evaluation)

**Hiring Target**: Month 2 (July 2026)  
**Monthly Salary**: ₹4-6 L

---

## Phase 2 Hiring Timeline & Execution

### Hiring Schedule

| Month | Role | Count | Status | Target |
|-------|------|-------|--------|--------|
| June | Technical Lead | 1 | Interview | Start July 1 |
| June | Senior ML Engineer | 2 | Interview | Start July 1 |
| June | Senior Backend Engineer | 1 | Interview | Start July 1 |
| July | ML Engineer | 3 | Interviews | Start mid-July |
| July | Backend Engineer | 2 | Interviews | Start mid-July |
| July | Data Engineer | 1 | Interviews | Start mid-July |
| July | DevOps Engineer | 1 | Interviews | Start mid-July |
| August | QA Engineer | 1 | Interviews | Start August |

**Total Hiring Timeline**: 8-10 weeks (June → August)

### Hiring Strategy

**Recruitment Channels**
1. **LinkedIn Recruiter** (₹2-5 L placement fee per senior hire)
2. **GitHub Jobs** (free, technical audience)
3. **AngelList** (startups looking to join)
4. **Internal referrals** (₹2-5 L bonus per referral)
5. **Targeted outreach** to:
   - Former FAANG engineers (relocation packages)
   - IIT/top college alumni networks
   - Defence/government background folks

**Hiring Process**
1. Resume screening (2-3 rounds)
2. Technical assessment (coding task or take-home)
3. Technical interview (1-2 hours)
4. System design interview (for senior roles)
5. Behavioral + culture fit interview
6. Reference checks
7. Offer + negotiation
8. Onboarding prep

**Timeline per role**: 4-6 weeks (from posting to offer)

---

## Phase 2 Onboarding & Training

### 2-Week DIRAS Bootcamp (Mandatory for all)

**Week 1: Foundations**
- Day 1: Project vision, roadmap, security briefing
- Day 2: Architecture overview, technology stack walkthrough
- Day 3: Development environment setup (laptops, VPN, access)
- Day 4: Git workflow, code review process, CI/CD demo
- Day 5: Team brainstorm, Q&A

**Week 2: Hands-On**
- Day 1: Run existing codebase (hello world task)
- Day 2: Contribute first PR (bug fix or documentation)
- Day 3: Full system walkthrough (from query → response)
- Day 4: Pair programming with mentor
- Day 5: Knowledge transfer + questions

**Resources Prepared**
- DIRAS Architecture (this document + diagrams)
- Research Module Summaries (from Phase 1)
- Quick Start Guide (setup + first query)
- Video recordings (architecture, tech stack)
- Mentor assignments (1 senior per 2-3 juniors)

---

### Role-Specific Training (Month 2-4)

**ML Engineers**: 
- Weeks 1-2: PyTorch + HuggingFace fundamentals
- Weeks 3-4: NLP (tokenization, embeddings, transformers)
- Weeks 5-8: DIRAS-specific (OCR research, classification design)

**Backend Engineers**:
- Weeks 1-2: FastAPI + REST API design
- Weeks 3-4: SQL + ORM (SQLAlchemy)
- Weeks 5-8: Vector DB integration, API design

**Data Engineer**:
- Weeks 1-2: ETL pipeline design
- Weeks 3-4: Web scraping (Scrapy, BeautifulSoup)
- Weeks 5-8: DIRAS data pipelines

**DevOps Engineer**:
- Weeks 1-2: Linux + Docker fundamentals
- Weeks 3-4: CI/CD (GitHub Actions)
- Weeks 5-8: Monitoring + infrastructure

**QA Engineer**:
- Weeks 1-2: Test automation + frameworks
- Weeks 3-4: ML evaluation metrics
- Weeks 5-8: DIRAS evaluation framework

---

## Phase 3 Team Expansion (14-16 Engineers)

### New Hires in Phase 3 (2-4 additional engineers)

**Kubernetes Expert** (1)
- Seniority: Senior (6-8 years K8s)
- Role: Lead Kubernetes setup, cluster design
- Monthly Salary: ₹8-10 L
- Hiring: Mid-Phase 2 (July 2026)
- **Why**: Phase 3 needs Kubernetes planning + setup

**NLP Specialist / RAG Expert** (1-2)
- Seniority: Senior (5-7 years NLP)
- Role: Lead RAG architecture, LLM integration
- Monthly Salary: ₹8-10 L each
- Hiring: Mid-Phase 2
- **Why**: RAG implementation is critical for Phase 3+

**QA Automation Engineer** (1)
- Seniority: Mid (3-5 years)
- Role: Build test automation, CI/CD testing
- Monthly Salary: ₹4-6 L
- Hiring: End of Phase 2 (August 2026)
- **Why**: Need better test automation before scaling

**Phase 3 Team Total**: 14-16 engineers

---

## Phase 4 Team Expansion (18-20 Engineers)

### New Hires in Phase 4 (2-4 additional engineers)

**Cloud Architects / SREs** (2)
- Seniority: Senior (6-8 years SRE)
- Role: Cloud infrastructure, scaling, monitoring
- Monthly Salary: ₹8-10 L each
- Hiring: Mid-Phase 3
- **Why**: Multi-region setup, production hardening

**Security Engineer** (1)
- Seniority: Senior (6-8 years security)
- Role: Security hardening, penetration testing, compliance
- Monthly Salary: ₹7-9 L
- Hiring: Mid-Phase 3
- **Why**: Production requires security audit + compliance

**Product Manager** (1)
- Seniority: Senior (5-7 years PM)
- Role: Requirements, prioritization, stakeholder management
- Monthly Salary: ₹6-8 L
- Hiring: Early Phase 4
- **Why**: Transition from dev-driven to product-driven

**Phase 4 Team Total**: 18-20 engineers

---

## Phase 5 Team Stabilization (16-18 Engineers)

### Phase 5 Changes
- **Phase 4 team transition**: Some engineers move to support/maintenance
- **No new hires** (stabilize existing team)
- **Hire support engineering team**: For production operations
- **Transition to handover**: Prepare for Phase 5 → operations team

**Phase 5 Team**:
- 12-14 core engineering team (continued development)
- 4-6 operations/support engineers (new hires or transitions)
- **Total**: 16-20 engineers

---

## Total Cost of Employment (Phase 2-5)

### Phase 2 Personnel Cost
**Base salaries**: 12 engineers × average ₹6.5 L = ₹78 L/month
**With benefits (18% overhead)**: ₹92 L/month
**Over 4 months (Phase 2)**: ₹368 L total

### Phase 3 Personnel Cost
**Base salaries**: 14-16 engineers × average ₹6.5 L = ₹91-104 L/month
**With benefits**: ₹107-122 L/month
**Over 4 months**: ₹428-488 L total

### Phase 4 Personnel Cost
**Base salaries**: 18-20 engineers × average ₹6.8 L = ₹122-136 L/month
**With benefits**: ₹144-160 L/month
**Over 4.5 months**: ₹648-720 L total

### Phase 5 Personnel Cost
**Base salaries**: 16-18 engineers × average ₹6.5 L = ₹104-117 L/month
**With benefits**: ₹123-138 L/month
**Over 4 months**: ₹492-552 L total

**Total Personnel (Phases 2-5)**: ₹1,936-2,160 L (₹19.4-21.6 Cr)

---

## Career Growth & Retention

### Growth Paths

**ML Engineer → Senior ML Engineer → Research Lead**
- Milestone 1 (6 months): Lead one module (NER, embeddings)
- Milestone 2 (12 months): Own model development for feature
- Milestone 3 (18 months): Senior role, mentor juniors

**Backend Engineer → Senior Backend Engineer → Architect**
- Milestone 1 (6 months): API design + database optimization
- Milestone 2 (12 months): Lead service architecture
- Milestone 3 (18 months): System architect, tech debt reduction

**DevOps Engineer → DevOps Lead → Infrastructure Architect**
- Milestone 1 (6 months): Kubernetes basics, basic cluster setup
- Milestone 2 (12 months): Multi-region setup, disaster recovery
- Milestone 3 (18 months): Infrastructure strategy, cost optimization

### Retention Strategies

1. **Competitive salary**: Market-rate + growth adjustments annually
2. **Stock options**: ₹5-10 L over 3-4 years (create ownership feeling)
3. **Learning budget**: ₹2-3 L per engineer per year (conferences, courses)
4. **Flexible work**: Work-from-home allowed (2 days/week minimum office)
5. **Clear roadmap**: Transparent career growth path
6. **Recognition**: Monthly/quarterly performance bonuses
7. **Team events**: Quarterly team outings, annual retreat

**Attrition Target**: <10% annually (industry standard: 15-20%)

---

## Leadership Structure

### Reporting Lines (Phase 2-5)

```
Project Manager
│
├─ Technical Lead / Engineering Manager
│  ├─ ML Team Lead
│  │  ├─ Senior ML Engineers (2-3)
│  │  └─ ML Engineers (3-5)
│  │
│  ├─ Backend Lead
│  │  ├─ Senior Backend Engineer (1)
│  │  └─ Backend Engineers (2-3)
│  │
│  ├─ Data & DevOps Lead
│  │  ├─ Data Engineer (1)
│  │  ├─ DevOps Engineer (1-2)
│  │  └─ Cloud Architect / SRE (2, Phase 4+)
│  │
│  ├─ QA & Evaluation Lead
│  │  └─ QA Engineers (1-2)
│  │
│  └─ Security Lead (Phase 4+)
│
└─ Product Manager (Phase 4+)
```

### Communication Structure

- **Daily**: Slack channels (#general, #diras, #engineering, #devops)
- **Weekly**: Team standup (15 min, each team)
- **Bi-weekly**: Engineering sync (cross-team coordination)
- **Monthly**: All-hands meeting (Project Manager + Technical Lead)
- **Monthly**: 1-on-1s (Engineering Manager with each direct report)
- **Quarterly**: Career development planning + goal setting

---

## Skills Matrix & Training Plan

### Phase 2 Skills Priority

| Role | Python | NLP | Backend | DevOps | ML Systems |
|------|--------|-----|---------|--------|-----------|
| ML Engineer | ★★★★★ | ★★★★☆ | ★★☆☆☆ | ★☆☆☆☆ | ★★★★★ |
| Backend Eng | ★★★★★ | ★★☆☆☆ | ★★★★★ | ★★★☆☆ | ★★☆☆☆ |
| Data Eng | ★★★★☆ | ★★☆☆☆ | ★★☆☆☆ | ★★★☆☆ | ★★★☆☆ |
| DevOps Eng | ★★★☆☆ | ★☆☆☆☆ | ★★☆☆☆ | ★★★★★ | ★★☆☆☆ |
| QA Eng | ★★★★☆ | ★★☆☆☆ | ★★☆☆☆ | ★★☆☆☆ | ★★★☆☆ |

**Training Investment**:
- Python: ₹1-2 L (workshops, online courses)
- NLP specifics: ₹2-3 L (HuggingFace courses)
- ML systems: ₹2-3 L (Advanced ML course)
- DevOps/Kubernetes: ₹1-2 L (Kubernetes certification courses)
- Total training Phase 2: ₹8-12 L

---

## Risk Mitigation: Key Person Dependencies

### High-Risk Roles (if person leaves)
1. **Technical Lead**: Impact HIGH (architecture decisions blocked)
   - Mitigation: Cross-train 2 senior engineers on architecture
   - Documentation: Architecture Decision Records (ADRs)
2. **Senior ML Engineer**: Impact MEDIUM (model development delayed)
   - Mitigation: Pair programming, shared knowledge
3. **DevOps Engineer**: Impact MEDIUM (deployments blocked)
   - Mitigation: Hire 2 DevOps engineers early (split responsibilities)

### Knowledge Transfer
- Code reviews (mandatory for all code)
- Wiki documentation (architecture, setup)
- Design docs (before implementation)
- Pair programming (2+ people know every critical component)
- Brown bag sessions (weekly knowledge sharing)

---

## Appendix: Job Descriptions Template

### Sample: ML Engineer Job Description

**Position**: ML Engineer (2-3 open)  
**Seniority**: Mid (3-5 years)  
**Location**: Bangalore, India (relocation support available)  
**Reports to**: Technical Lead

**About DIRAS**  
We're building an AI-powered retrieval system for Indian Defence documents. Join us to work on cutting-edge NLP, document understanding, and RAG systems.

**Responsibilities**
- Implement machine learning pipelines (preprocessing, classification, NER)
- Fine-tune transformer models (BERT, RoBERTa)
- Contribute to model evaluation + benchmarking
- Collaborate with backend team on model integration
- Write clean, tested, documented code

**Requirements**
- 3-5 years Python/ML development
- Experience with PyTorch or TensorFlow
- Understanding of NLP concepts (tokenization, embeddings)
- Git + collaborative development
- Strong communication skills

**Nice-to-have**
- HuggingFace library experience
- Experience with Weights & Biases
- Docker for ML development
- End-to-end ML project ownership

**What We Offer**
- Competitive salary (₹5-7 L/month)
- Stock options (₹2-5 L over 3 years)
- Learning budget (₹2-3 L/year)
- Flexible work (2 days/week WFH)
- Team outings + annual retreat

---

**Document Owner**: HR Lead + Technical Lead  
**Next Review**: July 15, 2026 (Hiring Halfway Point)  
**Approval**: [Pending Phase 2 Project Kickoff]

---

*Team composition and hiring timeline are critical to Phase 2 success. Early hiring (June) essential to start Phase 2 on time (July).*
