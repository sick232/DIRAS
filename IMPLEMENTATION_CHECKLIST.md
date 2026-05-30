# DIRAS Phase 2 Implementation Checklist - START HERE

**Status**: 🟢 **FULLY READY FOR CODING**  
**Date**: May 28, 2026  
**Next Action**: Run `docker-compose up -d` and start Sprint 2

---

## ✅ Pre-Implementation Checklist

Before you start coding, verify everything:

### Environment Setup
- [ ] Git installed (`git --version`)
- [ ] Docker installed (`docker --version`)
- [ ] Docker Compose installed (`docker-compose --version`)
- [ ] VS Code installed (`code --version`)
- [ ] VS Code Copilot extension installed (search in Extensions)
- [ ] Signed in to GitHub in VS Code

### Repository Setup
- [ ] Cloned DIRAS repo (`git clone ...`)
- [ ] Changed to project directory (`cd diras`)
- [ ] Copied environment file (`cp .env.example .env`)
- [ ] Created data directories (`data/raw`, `data/processed`, etc.)
- [ ] Created .git hooks (optional but recommended)

### Services Verification
```bash
# Run this command
docker-compose up -d

# Then verify all are running
docker-compose ps

# Should show:
# NAME              STATUS              PORTS
# diras-app        Up (healthy)        0.0.0.0:8000->8000/tcp
# diras-postgres   Up (healthy)        0.0.0.0:5432->5432/tcp
# diras-chromadb   Up (healthy)        0.0.0.0:8001->8000/tcp
# diras-elasticsearch Up (healthy)     0.0.0.0:9200->9200/tcp
# diras-prometheus Up                  0.0.0.0:9090->9090/tcp
# diras-grafana    Up                  0.0.0.0:3000->3000/tcp
```

- [ ] All services showing "Up (healthy)"
- [ ] API accessible: `curl http://localhost:8000/health`
- [ ] Tests passing: `pytest tests/unit/test_imports.py -v`

---

## 🎯 Quick Start (Under 5 Minutes)

### 1. Start Services (30 seconds)
```bash
cd diras
docker-compose up -d
```

### 2. Verify Working (30 seconds)
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy","timestamp":"...","version":"0.1.0"}
```

### 3. View API Docs (30 seconds)
```
Open browser: http://localhost:8000/docs
# See all available endpoints
```

### 4. Run Tests (1 minute)
```bash
pytest tests/unit/test_imports.py -v
# Should pass all 5 tests
```

### 5. Open Copilot (30 seconds)
```
VS Code → Copilot Chat (Cmd+Shift+I or Ctrl+Shift+I)
```

---

## 📚 Documentation to Read (In Order)

1. **This file** (2 min) - Overview
2. **`STATUS_IMPLEMENTATION_READY.md`** (5 min) - What's ready
3. **`COPILOT_DEVELOPER_GUIDE.md`** (10 min) - How to use Copilot
4. **`prompts/SPRINT_2_DATA_PIPELINE.md`** (10 min) - Current sprint
5. **`FREE_STACK_VARIANT.md`** (5 min) - Cost breakdown

---

## 🚀 Sprint 2: Data Pipeline (CURRENT SPRINT)

### Timeline
- **Start**: June 15, 2026 (Week 3-4)
- **Duration**: 2 weeks
- **Team**: 4 engineers
- **Deliverable**: 5K documents + OCR (88%+)

### Tasks (In Order)

#### Task 1: Document Scraper
**Owner**: 1 Data Engineer  
**Duration**: 3 days  
**Copilot Prompt**: `prompts/SPRINT_2_DATA_PIPELINE.md` → "Task 1: Document Scraping Setup"

```bash
# Implementation steps:
1. Read section Task 1 from prompt
2. Open Copilot Chat
3. Paste task description
4. Follow code examples
5. Create scrapers/ directory and implement
6. Test: pytest src/01-data-pipeline/tests/test_scrapers.py
7. Commit: git commit -m "feat: Document scraper"
```

**Success Criteria**:
- ✅ Scraper collects 2,000+ documents
- ✅ Extracts title + URL + date metadata
- ✅ Handles pagination
- ✅ Removes duplicates
- ✅ Tests passing

#### Task 2: OCR Pipeline
**Owner**: 1 Backend Engineer  
**Duration**: 3 days  
**Copilot Prompt**: `prompts/SPRINT_2_DATA_PIPELINE.md` → "Task 2: OCR Pipeline Setup"

```bash
# Implementation steps:
1. Read section Task 2 from prompt
2. Open Copilot Chat
3. Paste task description
4. Create src/01-data-pipeline/ocr.py
5. Implement EasyOCR + LayoutParser
6. Test on 100 sample documents
7. Measure accuracy (char + word)
8. Commit: git commit -m "feat: OCR pipeline"
```

**Success Criteria**:
- ✅ Character accuracy ≥88%
- ✅ Word accuracy ≥86%
- ✅ Processes 100+ docs in parallel
- ✅ Logs metrics to file
- ✅ Tests passing

#### Task 3: Preprocessing Pipeline
**Owner**: 1 Backend Engineer  
**Duration**: 2 days  
**Copilot Prompt**: `prompts/SPRINT_2_DATA_PIPELINE.md` → "Task 3: Preprocessing Pipeline"

```bash
# Implementation steps:
1. Read section Task 3 from prompt
2. Open Copilot Chat
3. Paste task description
4. Create src/02-preprocessing/pipeline.py
5. Implement tokenization + lemmatization
6. Measure information retention
7. Test with sample texts
8. Commit: git commit -m "feat: Preprocessing pipeline"
```

**Success Criteria**:
- ✅ Information retention ≥98% (loss <2%)
- ✅ Processes 1000+ docs/hour
- ✅ Removes stopwords (keeps defence terms)
- ✅ Tests passing

#### Task 4: Data Quality Dashboard
**Owner**: 1 DevOps Engineer  
**Duration**: 2 days  
**Copilot Prompt**: `prompts/SPRINT_2_DATA_PIPELINE.md` → "Task 4: Data Quality Dashboard"

```bash
# Implementation steps:
1. Read section Task 4 from prompt
2. Setup Grafana dashboards
3. Configure Prometheus scraping
4. Create custom metrics
5. Display OCR accuracy + document counts
6. Setup alerts (OCR <85% alert)
```

**Success Criteria**:
- ✅ Grafana dashboard showing real-time metrics
- ✅ 5+ dashboard panels
- ✅ Alerts configured
- ✅ Metrics auto-updated hourly

---

## 📊 Success Criteria (End of Sprint 2)

| Metric | Target | How to Verify |
|--------|--------|---------------|
| **Documents Collected** | 5,000+ | `ls -1 data/raw/*.pdf \| wc -l` |
| **OCR Character Accuracy** | ≥88% | Check `data/processed/metrics.json` |
| **OCR Word Accuracy** | ≥86% | Check `data/processed/metrics.json` |
| **Info Retention** | ≥98% | Run preprocessing tests |
| **Tests Passing** | 100% | `pytest tests/01-data-pipeline/ -v` |
| **Code Coverage** | ≥80% | `pytest --cov=src/01-data-pipeline` |
| **Documentation** | 100% | All functions have docstrings |
| **Commits** | ≥10 per week | `git log --oneline \| wc -l` |

---

## 🔧 Daily Development Cycle

### Morning (9 AM)
```bash
# 1. Check services
docker-compose ps

# 2. Pull latest code
git pull origin develop

# 3. Check tests
pytest tests/ -v

# 4. Review metrics from yesterday
tail -f data/processed/metrics.json
```

### Mid-Day (10 AM - 4 PM)
```bash
# 1. Create feature branch
git checkout -b feat/your-task-name

# 2. Open VS Code
code .

# 3. Use Copilot Chat
# - Cmd+Shift+I (Mac)
# - Ctrl+Shift+I (Windows)
# - Paste task from sprint prompt

# 4. Implement code
# - Create files/functions
# - Write tests
# - Reference Phase 1 research

# 5. Test frequently
pytest src/01-data-pipeline/tests/ -v

# 6. Commit frequently
git add .
git commit -m "feat: [description]"
```

### Evening (4 PM - 5 PM)
```bash
# 1. Run full test suite
pytest tests/ -v --cov=src

# 2. Update metrics
echo "OCR accuracy: $(python scripts/measure_accuracy.py)" >> metrics.log

# 3. Push code
git push origin feat/your-task-name

# 4. Create PR on GitHub
# - Add description
# - Link to sprint task
# - Request review

# 5. Standup update
# "Completed: X"
# "Working on: Y"
# "Blocker: Z (if any)"
```

---

## 🎓 Before You Code - Key Concepts

### Phase 1 Research (Why These Choices?)

Read ONLY the relevant sections for your task:

**For Scraper Task**:
- `/modules/01-dataset-collection/RESEARCH.md` (why these sources?)

**For OCR Task**:
- `/modules/02-ocr-document-understanding/RESEARCH.md` (why EasyOCR?)

**For Preprocessing Task**:
- `/modules/03-preprocessing-pipeline/RESEARCH.md` (why spaCy?)

### Technology Stack (100% Free)

| Tech | Cost | Why |
|------|------|-----|
| EasyOCR | FREE | 88-94% accuracy, Hindi support, open-source |
| LayoutParser | FREE | Complex layouts (tables, multi-column) |
| spaCy | FREE | Fast, accurate, production-ready |
| Scrapy | FREE | Industrial-strength web scraping |
| PostgreSQL | FREE | Reliable relational database |
| ChromaDB | FREE | Vector storage, no subscription |
| FastAPI | FREE | Modern Python web framework |
| Docker | FREE | Reproducible environments |
| GitHub Actions | FREE | Auto-testing (2000 mins/month free) |
| Prometheus + Grafana | FREE | Monitoring dashboards |

**Total Phase 2 Cost**: ₹0 software + ₹35-40L personnel = ₹35-40L  
**vs. Original Plan**: ₹155-235L  
**Savings**: ₹120L+ (50%+)

---

## 🚨 Critical Reminders

### ✅ DO
- ✅ Commit code daily (at least 1 commit/day)
- ✅ Write tests FIRST, then code
- ✅ Use Copilot Chat for guidance (not code dumps)
- ✅ Test locally before pushing
- ✅ Reference Phase 1 research for decisions
- ✅ Update metrics weekly
- ✅ Ask questions in standup
- ✅ Escalate blockers immediately

### ❌ DON'T
- ❌ Skip tests
- ❌ Copy-paste large code blocks without understanding
- ❌ Ignore error messages
- ❌ Work on main branch (always feature branch)
- ❌ Push broken code
- ❌ Work in isolation (communicate daily)
- ❌ Miss standups
- ❌ Wait until Friday to commit

---

## 📈 Metrics Tracking (Weekly)

### Every Friday 5 PM

```bash
# 1. Measure current metrics
pytest --cov=src/01-data-pipeline --cov-report=json

# 2. Log to tracking file
cat > metrics_week1.txt << EOF
Date: $(date)
Documents: $(ls -1 data/raw/ | wc -l)
OCR Char Accuracy: $(python scripts/measure_accuracy.py | grep char)
OCR Word Accuracy: $(python scripts/measure_accuracy.py | grep word)
Tests Passing: $(pytest tests/ -v | grep passed)
Code Coverage: $(coverage report | grep TOTAL)
Commits: $(git log --since="1 week ago" --oneline | wc -l)
EOF

# 3. Share with team
# Post metrics in team Slack/meeting
# Compare to targets
```

### Update BASELINE_METRICS.md

```markdown
## Sprint 2 Actual Results (vs. Targets)

| Metric | Target | Week 1 | Week 2 |
|--------|--------|--------|--------|
| Documents | 5,000+ | 2,800 | 5,200 |
| OCR Char Acc | 88%+ | 87.5% | 88.2% |
| OCR Word Acc | 86%+ | 85.9% | 86.1% |
| Info Retention | 98%+ | 97.8% | 98.3% |
| Tests | 100% | 95% | 100% |
```

---

## 🔗 Important Links

| Resource | Path | Purpose |
|----------|------|---------|
| Master Prompt | `/prompts/MASTER_IMPLEMENTATION_PROMPT.md` | Full Phase 2 overview |
| Sprint 2 Prompt | `/prompts/SPRINT_2_DATA_PIPELINE.md` | Current sprint tasks |
| Copilot Guide | `/COPILOT_DEVELOPER_GUIDE.md` | How to use Copilot |
| Free Stack | `/FREE_STACK_VARIANT.md` | Zero-cost alternatives |
| Status | `/STATUS_IMPLEMENTATION_READY.md` | What's ready |
| Phase 1 Research | `/modules/01-12/RESEARCH.md` | Why these tech choices |
| Risk Management | `/documentation/RISK_MANAGEMENT.md` | 30 risks + mitigation |
| Baseline Metrics | `/benchmarking/BASELINE_METRICS.md` | Success criteria |
| Roadmap | `/RESEARCH_ROADMAP.md` | Big picture |

---

## 🚀 Next Steps (Right Now)

### Next 5 Minutes
- [ ] Verify Docker: `docker-compose ps`
- [ ] Test API: `curl http://localhost:8000/health`
- [ ] Read this file: ✅ (you're reading it!)

### Next 1 Hour
- [ ] Read `/STATUS_IMPLEMENTATION_READY.md`
- [ ] Read `/COPILOT_DEVELOPER_GUIDE.md`
- [ ] Read `/prompts/SPRINT_2_DATA_PIPELINE.md`
- [ ] Install VS Code Copilot

### Next 24 Hours
- [ ] Team standup: Assign Sprint 2 tasks
- [ ] Create feature branches
- [ ] Start first task (Scraper) with Copilot
- [ ] First commits pushed

### Next 1 Week
- [ ] Task 1 (Scraper) complete: 2,000+ documents
- [ ] Task 2 (OCR) in progress
- [ ] Tests for all tasks
- [ ] Metrics dashboard showing data

---

## ❓ FAQ

**Q: Do I need to know all the tech stack?**  
A: No. Phase 1 research explains each choice. Read only what's relevant to your task.

**Q: What if I get stuck?**  
A: Ask Copilot, check Phase 1 research, ask team lead. Don't spin wheels >30 min.

**Q: How long should each task take?**  
A: Task 1 (Scraper): 2-3 days. Task 2 (OCR): 2-3 days. Task 3 (Preprocessing): 1-2 days.

**Q: Should I wait for code review before pushing?**  
A: Push daily but request review. Don't block on reviews.

**Q: What if metrics don't hit target?**  
A: Log the gap, investigate, ask team lead. Aim for best effort, not perfection.

**Q: Can I work on multiple tasks?**  
A: No. One task at a time. Focus > speed.

---

## ✨ You're Ready!

All infrastructure set up. All docs created. All code templates ready.

**Now go code.** 🚀

**Start**:
1. Run `docker-compose up -d`
2. Open `/prompts/SPRINT_2_DATA_PIPELINE.md`
3. Open Copilot Chat
4. Paste the first task
5. Follow guidance
6. Code
7. Test
8. Commit
9. Repeat

**That's it. You're implementing DIRAS Phase 2.** ✅

---

**Version**: 1.0  
**Status**: Ready for Coding ✅  
**Next Review**: June 30, 2026 (End of Sprint 2)  
**Questions**: Ask Tech Lead in daily standup
