# How to Code DIRAS Phase 2 Using GitHub Copilot

**Complete Developer Guide for Copilot-Assisted Implementation**

---

## 🚀 Setup Copilot (5 minutes)

### 1. Install Copilot in VS Code

```bash
# Open VS Code
# Go to Extensions (Ctrl+Shift+X)
# Search "GitHub Copilot"
# Install "GitHub Copilot" by GitHub
# Sign in with GitHub account
```

### 2. Open DIRAS Project

```bash
code diras/  # Opens VS Code in diras directory
```

### 3. Start Services

```bash
docker-compose up -d  # Start all backend services
```

---

## 💡 Copilot Chat Workflow

### Method 1: Inline Copilot (Quick Suggestions)

```
1. Start typing code
2. Copilot suggests completions (press Tab to accept)
3. Use for small functions, variable names, comments
```

**Example**:
```python
# Type this:
def extract_

# Copilot suggests:
def extract_entities_from_text(text: str):
    """Extract named entities from text"""
    
# Press Tab to accept
```

### Method 2: Copilot Chat (Complete Explanations) ⭐ RECOMMENDED

```
1. Open Copilot Chat (Cmd+Shift+I on Mac, Ctrl+Shift+I on Windows)
2. Paste prompt from our prompt files
3. Follow step-by-step guidance
4. Ask clarifying questions if stuck
```

**Example Workflow**:
```
You: (Paste Sprint 2 data pipeline prompt)
Copilot: Here's the step-by-step approach...

You: How do I implement the Scrapy spider?
Copilot: Here's the code template...

You: Why are we using EasyOCR?
Copilot: Because Phase 1 research validated...
```

---

## 📋 Daily Development Cycle

### Morning: Check Metrics & Plan

```bash
# 1. Check API is running
curl http://localhost:8000/health

# 2. Check tests passing
pytest tests/unit/ -v

# 3. View current sprint goals
cat prompts/SPRINT_2_DATA_PIPELINE.md | head -50
```

### Mid-Day: Implement Feature

```bash
# 1. Create feature branch
git checkout -b feat/ocr-pipeline

# 2. Open file to edit
code src/01-data-pipeline/ocr.py

# 3. Use Copilot Chat
# - Cmd+Shift+I (open Copilot Chat)
# - Paste task description
# - Follow guidance

# 4. Run tests after implementation
pytest src/01-data-pipeline/tests/ -v

# 5. Commit
git add .
git commit -m "feat: Implement OCR pipeline"
```

### End-of-Day: Track Progress

```bash
# Push code
git push origin feat/ocr-pipeline

# Check CI/CD
# GitHub Actions automatically runs tests

# Update metrics
# Log accuracy, latency, etc. to BASELINE_METRICS.md
```

---

## 🎯 Sprint 1 Task-by-Task (Using Copilot Chat)

### Task 1: Docker Setup (Already Done ✅)

**Status**: Complete
- Dockerfile created
- docker-compose.yml created
- All services configured

**Verify**:
```bash
docker-compose ps  # Should show all services running
```

### Task 2: FastAPI Skeleton (Already Done ✅)

**Status**: Complete
- `/src/api/main.py` created
- Health check endpoints working
- API documentation at http://localhost:8000/docs

**Verify**:
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","timestamp":"..."}
```

### Task 3: Database Connection (Already Done ✅)

**Status**: Complete
- PostgreSQL running
- SQLAlchemy configured
- Pytest ready

**Verify**:
```bash
pytest tests/unit/test_imports.py::test_database_connection -v
```

### Task 4: Team Onboarding (Next)

**Instructions**:

1. **Copy this prompt into Copilot Chat**:
   ```
   Create a DIRAS Bootcamp curriculum for 12 engineers. 
   Duration: 2 days.
   Day 1 (4 hours): Project overview, architecture, technology stack
   Day 2 (4 hours): Hands-on - clone repo, run tests, merge first PR
   
   Include:
   - Project history (defence docs, ethical compliance)
   - Architecture diagram (text-based)
   - Tech stack table with rationale
   - Code standards (PEP 8, docstrings)
   - Communication protocols
   - Daily standup template
   
   Output: Markdown document (1000+ words)
   ```

2. **Copilot provides**: Complete curriculum document

3. **You deliver**: Run bootcamp with team (Days 1-2 of Phase 2)

---

## 📝 Sprint 2: Data Pipeline (Week 3-4)

### Task 1: Document Scraper (Days 1-2)

**Copy this prompt into Copilot Chat**:

```
Build a Scrapy spider to scrape defence documents.

Requirements:
1. Scrape 5 URLs from Ministry of Defence website
2. Extract document URLs + metadata (title, date, size)
3. Handle pagination (next button)
4. Respect robots.txt + add delays between requests
5. Avoid duplicates (URL + content hash)
6. Save to JSON with deduplication

Target: Collect 2000+ documents

The site structure:
- Homepage: defence.gov.in
- Section pages: /press-release, /announcements
- Document pages: PDF/HTML with title + date

Show me:
1. Project structure (scrapy startproject ...)
2. Base spider template (generic methods)
3. Specific MoD spider (MoA website scraping)
4. Deduplication pipeline
5. Commands to run spiders

Libraries: Scrapy, BeautifulSoup, Requests
```

**Copilot provides**: Complete Scrapy project with templates

**You implement**:
```bash
# 1. Create Scrapy project
cd src/01-data-pipeline
scrapy startproject moad_scrapers

# 2. Copy Copilot code into spiders/
nano moad_scrapers/spiders/base_spider.py
nano moad_scrapers/spiders/moad_spider.py

# 3. Test scraper
scrapy crawl moad_spider -o documents.json

# 4. Commit
git add .
git commit -m "feat: Add document scraper for MoD"
```

### Task 2: OCR Pipeline (Days 2-3)

**Copy this prompt into Copilot Chat**:

```
Implement an EasyOCR pipeline for processing PDFs.

Requirements:
1. Extract images from PDFs (pdf2image)
2. Run OCR on each image (EasyOCR, English + Hindi)
3. Handle complex layouts (LayoutParser for multi-column, tables)
4. Batch process 100s of documents in parallel
5. Measure accuracy (character accuracy, word accuracy)
6. Log results to metrics file

Target: 88%+ character accuracy, 86%+ word accuracy

Show me:
1. OCRPipeline class with pdf->text conversion
2. LayoutParser integration for complex layouts
3. Parallel processing (ThreadPoolExecutor)
4. Accuracy measurement function
5. Metrics logging
6. Main script to process 5000 documents

Libraries: easyocr, pdf2image, opencv, layoutparser, tqdm
```

**You implement**:
```bash
# 1. Create OCR module
nano src/01-data-pipeline/ocr.py

# 2. Copy Copilot code, test on sample PDF
python -c "from src.data_pipeline.ocr import OCRPipeline; ..."

# 3. Process all 1000 documents
python src/01-data-pipeline/batch_ocr.py

# 4. Check accuracy metrics
cat data/processed/metrics.json
# Should show: character_accuracy: 88.5%, word_accuracy: 86.2%

# 5. Commit
git commit -m "feat: Implement OCR pipeline with 88%+ accuracy"
```

### Task 3: Preprocessing Pipeline (Days 3-4)

**Copy this prompt into Copilot Chat**:

```
Build a text preprocessing pipeline for defence documents.

Requirements:
1. Tokenization (spaCy)
2. Lemmatization (spaCy neural)
3. Remove stopwords (keep defence terms)
4. Clean special characters
5. Normalize text (lowercase, spacing)
6. Measure information retention (<2% loss)
7. Handle multilingual (English + Hindi)

Target: <2% information loss

Show me:
1. PreprocessingPipeline class
2. Helper functions (normalize, tokenize, lemmatize)
3. Stopword handling (keep important terms)
4. Information retention measurement
5. Tests for preprocessing
6. Integration with OCR output

Libraries: spacy, nltk
```

**You implement**: Similar workflow to OCR

---

## 🔍 Asking Copilot Good Questions

### ❌ Bad Questions
```
"How do I implement this?"
"What code should I write?"
"Can you fix this error?"
```

### ✅ Good Questions
```
"I'm implementing a Scrapy spider for MoD documents. 
The spider should extract title + date + PDF URL.
What's the step-by-step approach?
Here's the HTML structure: [describe or paste HTML]"

"I got this error when running OCR:
[paste full error message]
I'm using EasyOCR on these document types:
[describe documents]
How should I fix it?"

"I implemented classification using Random Forest.
Accuracy is 87%, target is 90%.
What's the best way to improve: more data, better features, or different model?"
```

---

## 📊 Tracking Progress in Copilot Chat

### Session Tracking

```
Start of each sprint:
"I'm starting Sprint 2 (Data Pipeline).
Tasks: Scraper (2K docs), OCR (88%+), Preprocessing (<2% loss)
Timeline: 2 weeks
Which task should I start with?"

Copilot: "Start with scraper because it feeds OCR..."

Mid-sprint:
"Progress update: Scrapy spider completed (2.5K docs collected).
Accuracy: 90%, no errors.
Next: OCR pipeline.
What's the implementation order?"

End-of-sprint:
"Sprint 2 status:
- Scraper: ✅ Complete (2.8K docs)
- OCR: ✅ Complete (87% accuracy, target 88%)
- Preprocessing: ✅ Complete (<1.5% loss)
- Tests: ✅ All passing
Should I move to Sprint 3?"
```

---

## 🧪 Testing While You Code

### Run Tests After Each Feature

```bash
# After implementing OCR
pytest src/01-data-pipeline/tests/test_ocr.py -v

# After implementing classification
pytest src/03-classification/tests/test_classifier.py -v

# Full test suite
pytest tests/ -v --cov=src

# Coverage report
pytest --cov=src --cov-report=html
# Open htmlcov/index.html to see which code is tested
```

### Example Test Writing

**Copy this prompt into Copilot Chat**:

```
Write unit tests for an OCR pipeline.

The OCR class has:
- extract_text_from_pdf(pdf_path): str
- measure_accuracy(ground_truth, ocr_text): dict
- batch_process(pdf_dir, num_workers=4): None

Tests should:
1. Test extract_text returns valid string
2. Test accuracy measurement (example texts)
3. Test batch processing (mock PDFs)
4. Test error handling (missing file, corrupted PDF)
5. Test metrics logging

Output: pytest-compatible test class

Libraries: pytest, tempfile, unittest.mock
```

**You implement**:
```bash
nano src/01-data-pipeline/tests/test_ocr.py
# Paste Copilot code
pytest src/01-data-pipeline/tests/test_ocr.py -v
```

---

## 🐛 Debugging with Copilot

### Scenario: Test Failing

```bash
# Run test
pytest tests/unit/test_ocr.py::test_extract_text -v

# See error:
# FAILED test_ocr.py::test_extract_text - AssertionError: 87.5 != 88

# Paste into Copilot:
"I'm testing an OCR function.
Expected accuracy: 88%
Got: 87.5%
The test:
  assert accuracy >= 0.88
  
The code extracts text from a sample PDF.
Is 87.5% close enough? Should I adjust test or improve OCR?"

# Copilot: "87.5% is very close. Phase 1 research says..."
```

### Scenario: Import Error

```bash
# Run code
python src/api/main.py

# Error:
# ModuleNotFoundError: No module named 'easyocr'

# Paste into Copilot:
"Getting import error: easyocr not found.
I have requirements.txt with easyocr==1.7.0
I installed with: pip install -r requirements.txt
Still failing. What should I do?"

# Copilot: "Try reinstalling: pip install easyocr --force-reinstall..."
```

---

## 📈 Using Prompts from `/prompts/` Directory

### For Each Sprint

1. **Read the prompt file**
   ```bash
   cat prompts/SPRINT_2_DATA_PIPELINE.md
   ```

2. **Copy the prompt into Copilot Chat**
   ```
   [Open Copilot Chat with Cmd+Shift+I]
   [Paste entire prompt file]
   Copilot responds with step-by-step guidance
   ```

3. **Ask clarifying questions**
   ```
   "I don't understand the Scrapy deduplication logic.
   Can you show me an example with fake URLs?"
   ```

4. **Implement step-by-step**
   ```
   "Now show me how to implement the first function..."
   ```

5. **Test and commit**
   ```bash
   pytest src/01-data-pipeline/ -v
   git commit -m "feat: Complete scraper module"
   ```

---

## ✅ Checklist for Each Sprint

```
Sprint: [N]
Week: [1-2]
Theme: [Data Pipeline / Classification / etc.]

Pre-Sprint:
☐ Read Master prompt
☐ Review Phase 1 research modules
☐ Understand success criteria (BASELINE_METRICS.md)
☐ Plan sprint tasks

During Sprint:
☐ Daily: Run tests, check metrics
☐ Each task: Use Copilot Chat with sprint prompt
☐ Each day: Commit code (at least once per day)
☐ Each feature: Write tests before implementation

End-of-Sprint:
☐ All tests passing (100%)
☐ Metrics meet targets (see BASELINE_METRICS.md)
☐ Code reviewed by team lead
☐ Documentation updated
☐ Metrics logged to tracking system

Sign-off:
☐ Sprint review completed
☐ Stakeholder approval obtained
☐ Ready for next sprint
```

---

## 🎓 Learning from Phase 1 Research

### When Copilot Suggests Code

**Always ask**: "Why is this the best approach?"

Example:
```
You: "How do I choose between EasyOCR and Tesseract?"

Copilot: "EasyOCR is better because [reason]."

You: "That makes sense. What does Phase 1 research say?"

Copilot: "Phase 1 evaluated both. EasyOCR: 88-94% accuracy, 
Tesseract: 75-80% accuracy. Also, EasyOCR supports Hindi.
See /modules/02-ocr-document-understanding/RESEARCH.md"

You: "Got it, I'll use EasyOCR as Phase 1 recommends."
```

---

## 🚀 Next Steps

1. **Verify Sprint 1 is complete**
   ```bash
   docker-compose ps  # All services running?
   curl http://localhost:8000/health  # API working?
   pytest tests/unit/test_imports.py -v  # Tests passing?
   ```

2. **Read Sprint 2 prompt**
   ```bash
   cat prompts/SPRINT_2_DATA_PIPELINE.md
   ```

3. **Start Task 1 (Scraper)**
   - Open Copilot Chat
   - Paste Sprint 2 prompt
   - Follow step-by-step guidance

4. **Daily cycle**
   - Morning: Check metrics, plan day
   - Mid-day: Code + Copilot + Test
   - Evening: Commit + Push + Track

---

## 📞 When Copilot Can't Help

**Ask Tech Lead / Google / Stack Overflow**:
- Errors specific to your hardware
- Docker network issues
- Database connection problems
- Performance bottlenecks not covered in Phase 1

**Escalate to Project Manager**:
- Budget concerns
- Timeline changes
- Scope changes
- Stakeholder blockers

---

**Version**: 1.0  
**For**: DIRAS Phase 2 Developers  
**Updated**: May 28, 2026

---

*Happy coding! Use Copilot chat, reference Phase 1 research, follow sprints sequentially.* 🚀
