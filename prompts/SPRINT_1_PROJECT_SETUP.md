# DIRAS Sprint 1: Project Initialization & Environment Setup

**For: GitHub Copilot Chat**  
**Duration**: 2 weeks  
**Team Allocation**: All 12 engineers + DevOps  
**Outcome**: Team onboarded, dev environment reproducible, CI/CD automated

---

## 🎯 Sprint 1 Goals

By end of Sprint 1, all team members will:
1. ✅ Understand DIRAS architecture + Phase 1 research
2. ✅ Have local dev environment running (Docker + Python + tests)
3. ✅ Merge first code (GitHub workflow proven)
4. ✅ Understand code standards + communication protocols

---

## 📋 Task List

### Task 1: DIRAS Bootcamp (Team - All 12)

**Duration**: Days 1-2 (2 days)  
**Owner**: Tech Lead  
**Participants**: All engineers

**Curriculum**:

**Day 1: Foundations**
- Project history: Why DIRAS? (Defence Intelligence System, public documents only, ethical compliance)
- Use cases: What will DIRAS answer? (Financial queries, procurement, authority identification, etc.)
- Phase 1 completion: What research was done? (12 modules, technology validated)
- System architecture: Components + data flow (Retrieval → RAG → Answer)
- Technology stack: Why each choice? (EasyOCR, SentenceTransformers, ChromaDB, etc.)

**Day 2: Hands-On**
- Clone repository + run locally (`docker-compose up`)
- Run first test suite (`pytest tests/unit/`)
- Submit first PR (dummy code, proves Git workflow)
- Code standards: PEP 8, comments, docstrings
- Communication: Daily standups, Slack conventions, escalation

**Outcome**: All team members ready to code

**Copilot Prompt**:
> "Create a DIRAS Bootcamp curriculum document (markdown). Content: (1) Project overview (300 words), (2) Architecture diagram (text-based), (3) Technology stack table (why each choice), (4) Code standards (PEP 8, docstring format), (5) Daily standup template. Make it hands-on (not boring). Target: Junior engineer understands system in 2 hours."

---

### Task 2: CI/CD Pipeline Setup (DevOps - 1, Backend - 1)

**Duration**: Days 2-4 (3 days)  
**Owner**: DevOps Engineer  
**Participants**: DevOps + 1 Senior Backend

**What to Build**:

1. **GitHub Actions Workflow** (`.github/workflows/test.yml`)
   - Trigger: On every push to any branch
   - Run: `pytest tests/unit/ -v` (unit tests)
   - Run: `pytest tests/integration/ -v` (integration tests, if data available)
   - Report: Pass/fail badge on PR
   - Outcome: No broken code merges to main

2. **Staging Deployment Workflow** (`.github/workflows/deploy-staging.yml`)
   - Trigger: On merge to `develop` branch
   - Build: Docker image (`docker build -t diras:staging .`)
   - Push: To Docker registry (Docker Hub or private registry)
   - Deploy: To staging server (SSH + pull latest image)
   - Outcome: Automatic staging environment update

3. **Docker Setup** (`.dockerignore`, `Dockerfile`)
   - Multi-stage build: Requirements → Python deps → App
   - Final image: Python 3.10 + CUDA 12 (for GPU support)
   - Port: 8000 (FastAPI)
   - Health check: `curl http://localhost:8000/health`

4. **Environment Management** (`.env.example`, `.env`)
   - OpenAI API key, HuggingFace token, etc.
   - Local dev: Use `.env` (not checked in)
   - Staging/Prod: Use GitHub Secrets

**Code Template**:
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest tests/unit/ -v
      - run: pytest tests/integration/ -v
```

**Copilot Prompt**:
> "Create a GitHub Actions CI/CD pipeline for a Python FastAPI project. Requirements: (1) Auto-run pytest on every push, (2) Build Docker image on merge to develop, (3) Deploy to staging server via SSH. Here's my repo structure: [paste structure]. How should I set up .github/workflows/test.yml and .github/workflows/deploy-staging.yml?"

---

### Task 3: Repository Structure (Backend - 1, DevOps - 1)

**Duration**: Days 3-4 (2 days)  
**Owner**: Senior Backend Engineer  
**Participants**: 1 Backend + DevOps

**What to Create**:

```
/diras
├── src/
│   ├── 01-data-pipeline/      # Weeks 3-4
│   │   ├── __init__.py
│   │   ├── scraper.py         # Scrapy spiders
│   │   ├── ocr.py             # EasyOCR integration
│   │   └── tests/
│   │       └── test_ocr.py
│   │
│   ├── 02-preprocessing/      # Weeks 5-6
│   │   ├── __init__.py
│   │   ├── tokenizer.py       # spaCy tokenization
│   │   ├── cleaner.py         # Text cleaning
│   │   └── tests/
│   │
│   ├── 03-classification/     # Weeks 5-6
│   │   ├── __init__.py
│   │   ├── classifier.py      # Random Forest
│   │   ├── trainer.py         # Training logic
│   │   └── tests/
│   │
│   ├── 04-ner/                # Weeks 7-8
│   │   ├── __init__.py
│   │   ├── extractor.py       # spaCy NER
│   │   ├── linking.py         # Entity linking
│   │   └── tests/
│   │
│   ├── 05-embeddings/         # Weeks 9-10
│   │   ├── __init__.py
│   │   ├── embedding_model.py # SentenceTransformers
│   │   └── tests/
│   │
│   ├── 06-retrieval/          # Weeks 9-10
│   │   ├── __init__.py
│   │   ├── dense_search.py    # ChromaDB
│   │   ├── sparse_search.py   # BM25
│   │   ├── fusion.py          # RRF
│   │   └── tests/
│   │
│   ├── 07-rag/                # Weeks 11-12
│   │   ├── __init__.py
│   │   ├── pipeline.py        # RAG orchestration
│   │   ├── prompts.py         # Prompt templates
│   │   └── tests/
│   │
│   ├── 08-financial/          # Weeks 13-14
│   ├── 09-authority/          # Weeks 13-14
│   ├── 10-api/                # Throughout
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app
│   │   ├── routers.py         # API endpoints
│   │   └── tests/
│   │
│   ├── 11-cli/                # Throughout
│   │   ├── __init__.py
│   │   ├── commands.py        # Click CLI commands
│   │   └── tests/
│   │
│   ├── 12-evaluation/         # Week 15-16
│   │   ├── __init__.py
│   │   ├── metrics.py         # Accuracy, latency
│   │   └── tests/
│   │
│   └── shared/
│       ├── __init__.py
│       ├── config.py          # Configuration
│       ├── logging.py         # Logging setup
│       ├── constants.py       # Enums, constants
│       └── utils.py           # Common functions
│
├── tests/
│   ├── unit/                  # Unit tests
│   │   ├── test_imports.py    # Can we import everything?
│   │   ├── test_ocr.py
│   │   ├── test_classifier.py
│   │   └── ... (one per module)
│   │
│   ├── integration/           # End-to-end tests
│   │   ├── test_pipeline.py   # Query → Answer
│   │   └── test_api.py        # API endpoints
│   │
│   └── uat/                   # User acceptance test scenarios
│       ├── test_scenario_1_financial.py
│       ├── test_scenario_2_procurement.py
│       └── ... (5 scenarios)
│
├── data/
│   ├── raw/                   # Original PDFs
│   ├── processed/             # OCR'd text
│   ├── golden-dataset/        # 960 test docs
│   ├── embeddings/            # Vector cache
│   └── backup/                # S3 backups
│
├── models/
│   ├── classification/        # Trained classifiers
│   ├── ner/                   # NER weights
│   └── embeddings/            # Pre-computed vectors
│
├── notebooks/                 # Jupyter exploration
│   ├── 01-data-exploration.ipynb
│   ├── 02-ocr-accuracy.ipynb
│   └── ... (5 notebooks)
│
├── docs/
│   ├── architecture.md        # Design decisions
│   ├── api.md                 # API documentation
│   └── deployment.md          # DevOps guide
│
├── Dockerfile                 # Multi-stage build
├── docker-compose.yml         # Local dev environment
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Modern Python packaging
├── pytest.ini                 # Test configuration
├── .gitignore
├── .env.example
├── README.md                  # Quick start
├── CONTRIBUTING.md            # Code standards
└── .github/workflows/         # CI/CD pipelines
```

**Key Files to Create**:

1. `README.md` (Getting started guide)
2. `CONTRIBUTING.md` (Code standards + workflow)
3. `Dockerfile` (Production image)
4. `docker-compose.yml` (Local dev)
5. `requirements.txt` (Dependencies)
6. `src/shared/config.py` (Config management)

**Copilot Prompt**:
> "Create a well-structured Python project for a machine learning + FastAPI system. Structure should: (1) Separate modules by feature (01-data, 02-preprocessing, etc.), (2) Shared utilities (config, logging, utils), (3) Tests mirroring src/ structure, (4) Data + models directories, (5) Notebooks for exploration. Show me the directory structure and key files (README, requirements.txt, Dockerfile). This is for a Phase 2 16-week sprint."

---

### Task 4: Docker Environment (DevOps - 1, Backend - 1)

**Duration**: Days 4-5 (2 days)  
**Owner**: DevOps Engineer  
**Participants**: DevOps + 1 Senior Backend

**What to Build**:

1. **Dockerfile**
   - Base: `python:3.10-slim` (or `nvidia/cuda:12.0-runtime-ubuntu22.04` if GPU)
   - Install: Python deps (pip install -r requirements.txt)
   - Copy: Source code
   - Expose: Port 8000
   - CMD: `python src/10-api/main.py`

2. **docker-compose.yml**
   - Services:
     - `app`: FastAPI server (port 8000)
     - `chromadb`: Vector DB (port 8000, conflict? use 8001)
     - `elasticsearch`: BM25 search (port 9200)
     - `grafana`: Monitoring (port 3000)
     - `postgres`: Metadata DB (port 5432)
   - Volumes: Mounted `/data` for persistence
   - Environment: `.env` file loaded

3. **Health Checks**
   - App health: `curl http://localhost:8000/health`
   - ChromaDB health: `curl http://localhost:8001/api/v1`
   - Elasticsearch health: `curl http://localhost:9200/_cluster/health`

**Commands**:
```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f app

# Stop
docker-compose down

# Rebuild (after code changes)
docker-compose up -d --build
```

**Copilot Prompt**:
> "Create a Dockerfile and docker-compose.yml for a Python FastAPI ML system. Services: (1) FastAPI app (port 8000), (2) ChromaDB vector DB (port 8001), (3) Elasticsearch (port 9200), (4) Grafana monitoring (port 3000), (5) PostgreSQL (port 5432). Requirements: (1) All services start with docker-compose up -d, (2) Health checks implemented, (3) Persistent volumes for data, (4) Environment variables from .env. Show both files with explanations."

---

### Task 5: First Code Merge (All 12 engineers)

**Duration**: Days 5 (1 day, overlap with other tasks)  
**Owner**: Tech Lead  
**Participants**: All 12 engineers

**What to Do**:

1. **Each engineer**:
   - Clone repo: `git clone ...`
   - Create branch: `git checkout -b feat/engineer-name-first-task`
   - Add dummy code: Create `src/TEAM_ROSTER.md`
     ```markdown
     # DIRAS Phase 2 Team
     
     - Alice (Backend Lead)
     - Bob (ML Engineer)
     - ... etc (add yourself)
     ```
   - Commit: `git add . && git commit -m "Add [Name] to team roster"`
   - Push: `git push origin feat/engineer-name-first-task`
   - Create PR (pull request) on GitHub

2. **Tech Lead**:
   - Review each PR (even if dummy code)
   - Verify CI/CD tests pass (green checkbox)
   - Approve + merge to main

3. **Outcome**:
   - ✅ Each engineer has merged code (comfort with Git)
   - ✅ CI/CD pipeline proven (tests ran, passed)
   - ✅ No fear of breaking main branch

**Copilot Prompt** (for engineer creating TEAM_ROSTER.md):
> "I'm adding myself to a team roster in a GitHub repo. Create a markdown file listing: (1) Team member name, (2) Role (Backend, ML, DevOps, QA), (3) Email, (4) One-line about yourself. Format should be clean, easy to read. What's a good template?"

---

## ✅ Sprint 1 Deliverables

| Deliverable | Owner | Status |
|-------------|-------|--------|
| Bootcamp curriculum + delivery | Tech Lead | ✅ |
| GitHub Actions test workflow | DevOps | ✅ |
| GitHub Actions staging deployment | DevOps | ✅ |
| Repository structure created | Backend | ✅ |
| Dockerfile + docker-compose.yml | DevOps | ✅ |
| All engineers' first PR merged | All | ✅ |
| Development environment reproducible | DevOps + All | ✅ |
| Code standards document | Tech Lead | ✅ |

---

## 📊 Sprint 1 Success Criteria

**✅ PASS if**:
- All 12 engineers can `docker-compose up` and run tests locally
- First PR merged to main (proves Git + CI/CD working)
- CI/CD tests run automatically on every push
- Staging deployment automated (push to develop → auto-deploy)
- Team understands architecture + technology choices

**❌ FAIL if**:
- <10 engineers have working local environment
- Any engineer unable to merge code
- CI/CD not running tests automatically
- Staging environment not accessible

---

## 🔗 Sprint 1 → Sprint 2

**What happens next?**
- Sprint 2 (Weeks 3-4): Data pipeline (scrapers + OCR)
- You'll use this environment to code + test daily
- CI/CD will auto-test your code (no more manual testing setup!)

---

## 📞 Common Questions

**Q: What if I can't run docker-compose up?**  
A: Common issues: Docker not installed, port conflicts (use `docker ps` to see running containers), VPN blocking Docker registry. Escalate to DevOps engineer immediately.

**Q: Do I need to install Python locally?**  
A: No! Use Docker container instead. All Python code runs inside container, isolated from your machine.

**Q: What if CI/CD tests fail?**  
A: Fix the code, push again. GitHub Actions will re-run tests automatically. Repeat until green.

---

**Document Version**: 1.0  
**References**: 
- Master prompt: `/prompts/MASTER_IMPLEMENTATION_PROMPT.md`
- Team structure: `/documentation/TEAM_STRUCTURE.md`  
- Code standards: `/CONTRIBUTING.md` (to be created)

---

*Next: Sprint 2 Data Pipeline Prompt (Weeks 3-4)*
