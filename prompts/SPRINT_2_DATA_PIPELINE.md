# DIRAS Sprint 2: Data Pipeline & OCR Foundation

**For: GitHub Copilot Chat**  
**Duration**: 2 weeks (Weeks 3-4)  
**Team Allocation**: Data Engineer (1) + Backend (2) + DevOps (1) + QA (1)  
**Outcome**: 5,000 documents collected, OCR accuracy ≥88%

---

## 🎯 Sprint 2 Goals

By end of Sprint 2:
1. ✅ 5,000 documents collected from 3-5 public sources
2. ✅ OCR accuracy measured ≥88% (character + word level)
3. ✅ Preprocessing pipeline v1 operational
4. ✅ Data quality dashboard in Grafana
5. ✅ Automated daily data ingestion pipeline

---

## 📋 Task List

### Task 1: Document Scraping Setup (Data Engineer - 1, Backend - 1)

**Duration**: Weeks 1-2  
**Owner**: Data Engineer  
**Goal**: 5,000 documents collected from public sources

**Approach**:

**Data Sources**:
1. Ministry of Defence website (defence.gov.in)
   - Press releases, annual reports, notifications
   - Estimated: 1,500-2,000 documents

2. Gazette of India (egazette.nic.in)
   - Defence-related notifications + rules
   - Estimated: 1,000-1,500 documents

3. PIB (Press Information Bureau) - pib.gov.in
   - Defence ministry press releases
   - Estimated: 1,000-1,500 documents

4. DRDO (Defence Research & Development) - drdo.gov.in
   - Technical documents, reports
   - Estimated: 500-1,000 documents

5. Budget documents (Indiabudget.gov.in)
   - Defence budget proposals
   - Estimated: 200-300 documents

**Total Target**: 5,000-6,500 documents (aim for 5,000+)

**Tech Stack**:
- Scrapy (web scraping framework)
- Selenium (if JavaScript-heavy pages)
- requests + BeautifulSoup (fallback)
- AWS S3 or NAS (document storage)

**Implementation**:

1. **Scrapy Project Structure**
   ```
   src/01-data-pipeline/
   ├── __init__.py
   ├── scrapers/
   │   ├── __init__.py
   │   ├── base_spider.py      # Common logic
   │   ├── moad_spider.py      # Ministry of Defence
   │   ├── gazette_spider.py   # Gazette of India
   │   ├── pib_spider.py       # Press Info Bureau
   │   ├── drdo_spider.py      # DRDO
   │   └── budget_spider.py    # Budget documents
   │
   ├── middlewares.py          # Request headers, delays
   ├── pipelines.py            # Save to disk + deduplicate
   └── settings.py             # Scrapy config
   ```

2. **Base Spider Template**
   ```python
   # src/01-data-pipeline/scrapers/base_spider.py
   import scrapy
   
   class BaseSpider(scrapy.Spider):
       """Common spider for all DIRAS sources"""
       
       allowed_domains = []  # Subclass defines
       start_urls = []       # Subclass defines
       
       def parse(self, response):
           # Extract document URLs
           for doc_url in self.extract_docs(response):
               yield scrapy.Request(
                   url=doc_url,
                   callback=self.parse_document,
                   meta={'source': self.name}
               )
       
       def parse_document(self, response):
           # Save document, extract metadata
           yield {
               'title': self.extract_title(response),
               'url': response.url,
               'source': response.meta['source'],
               'date': self.extract_date(response),
               'content_type': self.infer_type(response),
               'body': response.text,  # Full HTML/PDF
           }
       
       def extract_title(self, response):
           # Subclass implements
           pass
   ```

3. **Deduplication Pipeline**
   ```python
   # src/01-data-pipeline/pipelines.py
   class DeduplicationPipeline:
       """Remove duplicate documents"""
       
       def __init__(self):
           self.urls_seen = set()
           self.content_hashes = set()
       
       def process_item(self, item, spider):
           # Check URL not seen before
           if item['url'] in self.urls_seen:
               raise DropItem(f"Duplicate URL: {item['url']}")
           
           # Check content not too similar (hash)
           content_hash = hash(item['body'][:500])
           if content_hash in self.content_hashes:
               raise DropItem(f"Duplicate content: {item['url']}")
           
           self.urls_seen.add(item['url'])
           self.content_hashes.add(content_hash)
           return item
   ```

4. **Run Spiders**
   ```bash
   # Crawl each source
   scrapy crawl moad_spider -o data/raw/moad.json
   scrapy crawl gazette_spider -o data/raw/gazette.json
   scrapy crawl pib_spider -o data/raw/pib.json
   scrapy crawl drdo_spider -o data/raw/drdo.json
   scrapy crawl budget_spider -o data/raw/budget.json
   
   # Aggregate
   find data/raw -name "*.json" -exec cat {} \; > data/raw/all_documents.json
   ```

**Copilot Prompt**:
> "Create a Scrapy spider to scrape defence documents from [WEBSITE]. Requirements: (1) Extract document URL + metadata (title, date), (2) Handle pagination (next button), (3) Respect robots.txt + delays, (4) Save to JSON with metadata, (5) Avoid duplicates. Site structure: [describe]. What's the code structure? Show base_spider.py + specific_spider.py"

---

### Task 2: OCR Pipeline Setup (Backend - 1, Data Engineer - 1)

**Duration**: Weeks 1-2  
**Owner**: Backend Engineer  
**Goal**: OCR accuracy ≥88%, process 5,000 docs

**Implementation**:

1. **PDF/Image Extraction**
   ```python
   # src/01-data-pipeline/ocr.py
   import pdf2image
   import easyocr
   from pathlib import Path
   
   class OCRPipeline:
       def __init__(self):
           self.reader = easyocr.Reader(['en', 'hi'])  # English + Hindi
       
       def extract_text_from_pdf(self, pdf_path):
           """Extract images from PDF, then OCR each page"""
           images = pdf2image.convert_from_path(pdf_path)
           
           all_text = []
           for page_num, image in enumerate(images):
               text = self.reader.readtext(image)
               # text is list of (bbox, text, confidence)
               page_text = '\n'.join([t[1] for t in text])
               all_text.append({
                   'page': page_num + 1,
                   'text': page_text,
                   'confidence': sum(t[2] for t in text) / len(text),
               })
           
           return all_text
   ```

2. **Layout Preservation (Complex Documents)**
   ```python
   # Handle multi-column, tables, complex layouts
   from layoutparser.models import Detectron2LayoutModel
   
   def extract_with_layout(image):
       """Preserve layout for complex documents"""
       model = Detectron2LayoutModel(config_path="lp://PubLayNet/faster_rcnn_ResNet50_FPN_3x/config")
       layout = model.detect(image)
       
       # layout contains blocks: text, figures, tables, etc.
       # Re-order by position for natural reading order
       sorted_blocks = sorted(layout, key=lambda x: (x.coordinates[1], x.coordinates[0]))
       
       reconstructed_text = '\n'.join([block.text for block in sorted_blocks])
       return reconstructed_text
   ```

3. **Batch Processing**
   ```python
   from concurrent.futures import ThreadPoolExecutor
   
   def batch_ocr_documents(input_dir, output_dir, num_workers=4):
       """Process multiple documents in parallel"""
       pipeline = OCRPipeline()
       
       with ThreadPoolExecutor(max_workers=num_workers) as executor:
           for pdf_file in Path(input_dir).glob('*.pdf'):
               executor.submit(
                   process_single_document,
                   pipeline, pdf_file, output_dir
               )
   ```

4. **OCR Accuracy Measurement**
   ```python
   def measure_ocr_accuracy(ground_truth_text, ocr_text):
       """Compare OCR output against manually verified text"""
       from difflib import SequenceMatcher
       
       # Character accuracy
       ratio = SequenceMatcher(None, ground_truth_text, ocr_text).ratio()
       char_accuracy = ratio * 100
       
       # Word accuracy (more user-relevant)
       gt_words = ground_truth_text.split()
       ocr_words = ocr_text.split()
       
       match_count = sum(1 for gw, ow in zip(gt_words, ocr_words) if gw == ow)
       word_accuracy = (match_count / len(gt_words)) * 100
       
       return {
           'character_accuracy': char_accuracy,
           'word_accuracy': word_accuracy,
       }
   ```

5. **Run on All Documents**
   ```bash
   # Process 5,000 documents
   python -c "
   from src.data_pipeline.ocr import batch_ocr_documents
   batch_ocr_documents('data/raw/', 'data/processed/', num_workers=4)
   "
   
   # Monitor progress + measure accuracy
   python -c "
   from src.data_pipeline.ocr import measure_accuracy_batch
   accuracy_stats = measure_accuracy_batch('data/processed/', sample_size=100)
   print(f'Character Accuracy: {accuracy_stats[\"char_acc\"]}%')
   print(f'Word Accuracy: {accuracy_stats[\"word_acc\"]}%')
   "
   ```

**Copilot Prompt**:
> "Create an EasyOCR pipeline in Python to process PDFs + images. Requirements: (1) Extract images from PDFs, (2) Run OCR on each image (English + Hindi), (3) Preserve layout using LayoutParser for complex documents, (4) Batch process 5K documents in parallel, (5) Measure accuracy (character + word level). Show code structure + test on sample PDF."

---

### Task 3: Preprocessing Pipeline v1 (Backend - 1)

**Duration**: Weeks 1-2 (overlap with OCR)  
**Owner**: Backend Engineer  
**Goal**: Clean text, tokenize, measure information retention

**Implementation**:

```python
# src/02-preprocessing/pipeline.py
import spacy
from nltk.corpus import stopwords

class PreprocessingPipeline:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.stopwords = set(stopwords.words('english'))
    
    def preprocess_text(self, text):
        """Full preprocessing pipeline"""
        # Step 1: Normalize (lowercase, remove extra whitespace)
        text = text.lower().strip()
        text = ' '.join(text.split())  # Remove extra spaces
        
        # Step 2: Remove special characters (keep alphanumeric + basic punctuation)
        import re
        text = re.sub(r'[^\w\s₹$€£%]', '', text)
        
        # Step 3: Tokenize + Lemmatize
        doc = self.nlp(text)
        tokens = [token.lemma_ for token in doc if not token.is_punct]
        
        # Step 4: Remove stopwords (careful: keep important finance/defence terms)
        # Defence stopwords: 'defence', 'ministry', 'government' <- keep these!
        defence_terms = {'defence', 'ministry', 'government', 'authority', 'approval'}
        tokens = [t for t in tokens if t not in self.stopwords or t in defence_terms]
        
        return tokens
    
    def measure_retention(self, original, processed):
        """Measure information loss (<2% is good)"""
        original_tokens = set(original.lower().split())
        processed_tokens = set(processed)
        
        retention = len(processed_tokens & original_tokens) / len(original_tokens)
        return retention * 100
```

---

### Task 4: Data Quality Dashboard (DevOps - 1)

**Duration**: Week 2  
**Owner**: DevOps Engineer  
**Goal**: Visualize OCR accuracy + document statistics

**Grafana Dashboard**:
1. **OCR Accuracy Metrics**
   - Character accuracy trend (7-day moving avg)
   - Word accuracy by document type
   - Document count by source

2. **Data Statistics**
   - Total documents indexed
   - Documents per source (pie chart)
   - Average document size (pages, words)

3. **Quality Alerts**
   - Alert if OCR accuracy drops <85%
   - Alert if duplicate rate >5%
   - Alert if preprocessing info loss >2%

**Setup**:
```bash
# Add metrics to Prometheus (data/prometheus.yml)
scrape_configs:
  - job_name: 'diras-pipeline'
    static_configs:
      - targets: ['localhost:8001']  # Your metrics endpoint

# Import Grafana dashboard (or create custom)
# Connect Prometheus data source
# Create dashboard with panels above
```

---

## ✅ Sprint 2 Deliverables

| Deliverable | Owner | Target | Status |
|-------------|-------|--------|--------|
| 5,000 documents collected | Data Eng | 5K | ✅ |
| OCR accuracy measured | Backend | ≥88% | ✅ |
| Preprocessing pipeline | Backend | <2% info loss | ✅ |
| Data quality dashboard | DevOps | 5+ metrics | ✅ |
| Automated daily pipeline | Data Eng | Runs via cron | ✅ |

---

## 📊 Sprint 2 Success Criteria

**✅ PASS if**:
- 5,000+ documents collected from ≥3 sources
- OCR character accuracy ≥88%
- OCR word accuracy ≥86%
- Information retention ≥98%
- Dashboard shows metrics live

**⚠️ WARNING if**:
- OCR accuracy 85-88% (edge case: re-check process)
- <4,500 documents (source issue)
- Info loss 1.5-2% (may be acceptable)

**❌ FAIL if**:
- OCR accuracy <85%
- <3,000 documents
- Preprocessing breaks (can't parse output)

---

## 🔗 Sprint 2 → Sprint 3

**What happens in Sprint 3?**
- Classification training (3,000 documents manually labeled)
- Training document classifier (Random Forest)
- Target: Accuracy ≥90%

**Data Dependency**:
- Use 5,000 documents from Sprint 2 as training/test data
- Select 3,000 best-quality docs for classification training
- Reserve 1,000 for golden dataset (later)

---

## 📞 Common Issues & Solutions

**Q: OCR giving <85% accuracy**
- A: Check document quality (scans vs. native PDFs). Try Tesseract as fallback. Check if Hindi docs need separate model.

**Q: Scrapers blocked (rate limiting)**
- A: Add delays between requests, rotate user-agents, use Selenium for heavy JS sites

**Q: Memory error processing 5K docs**
- A: Use batch processing (process 100 at a time), reduce worker count

---

**Document Version**: 1.0  
**References**:
- Phase 1 research: `/modules/01-dataset-collection/RESEARCH.md`
- Phase 1 OCR research: `/modules/02-ocr-document-understanding/RESEARCH.md`
- Infrastructure: `/architecture/INFRASTRUCTURE_DESIGN.md`

---

*Next: Sprint 3 Classification (Weeks 5-6)*
