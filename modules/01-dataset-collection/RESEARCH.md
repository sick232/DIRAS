# Module 1: Dataset Collection & Acquisition

## Research Document

---

## 1. Overview

The Dataset Collection Module is responsible for automatically discovering, acquiring, validating, and maintaining a comprehensive corpus of defence-related public documents. This module is the foundation of the entire system.

---

## 2. Data Sources Architecture

### Tier 1: Official Government Sources (Primary)

**Ministry of Defence India (mod.gov.in)**
- Official MOD press releases and notices
- Defence policies and guidelines
- Public defence orders and circulars
- Defence procurement notices
- Budget speeches and financial reports
- Ministry organizational information

**Defence Research & Development Organisation (drdo.gov.in)**
- DRDO research summaries and abstracts
- Technical reports (public versions)
- Facility information
- Partnership announcements
- Publication lists

**Gazette of India (egazette.gov.in)**
- Defence-related gazette notifications
- Defence Ministry orders
- Defence personnel appointments
- Defence industrial policy updates

**Press Information Bureau - Defence Wing (pib.gov.in)**
- Daily defence-related press releases
- Minister speeches and statements
- Policy announcements
- Current defence news

### Tier 2: Parliamentary & Democratic Institutions

**Parliament of India Resources**:
- Parliamentary Lok Sabha defence debates
- Parliamentary Standing Committee on Defence reports
- Starred questions on defence matters
- Bills related to defence

**Parliamentary Reports**:
- Annual reports from Defence Ministry
- Defence budget presentations
- Defence committee recommendations

### Tier 3: Public Audit & Transparency

**CAG Reports (Comptroller & Auditor General)**:
- Defence ministry audit reports
- Defence procurement audits
- Defence spending audits

**RTI (Right to Information) Response Documents**:
- Public RTI responses (anonymized)
- Disclosure documents
- Public records

### Tier 4: Open Government Data

**Data.gov.in**:
- Defence-related datasets
- Public databases
- Government statistics

**Government Open Data Portal**:
- Defence statistics
- Procurement data
- Financial data

**Public Procurement Portal**:
- Tender documents
- Procurement notices
- Bid evaluation reports (public portions)

---

## 3. Data Collection Techniques

### Technique 1: Web Scraping

**Definition**: Automated extraction of content from websites

**Implementation**:
- Framework: Scrapy or BeautifulSoup
- Frequency: Daily crawls of main sources
- Scheduling: Off-peak hours to minimize server load
- Politeness: Respect robots.txt, reasonable request rates

**Advantages**:
✅ Covers most web-based sources  
✅ Flexible - can adapt to website changes  
✅ No API key dependencies  
✅ Can extract structured and unstructured content  

**Disadvantages**:
❌ Website structure changes break scrapers  
❌ Can be blocked if too aggressive  
❌ Requires regex/CSS selector maintenance  
❌ Doesn't work well for JavaScript-rendered sites  

**Best For**: Government websites with stable structure (MOD, DRDO, Gazette)

**Tools**: Scrapy, BeautifulSoup, Selenium (for JavaScript rendering)

---

### Technique 2: API Integration

**Definition**: Structured data acquisition through official APIs

**Implementation**:
- Identify which sources offer APIs
- Use REST APIs where available
- Implement proper error handling and retries
- Rate limiting compliance
- Scheduled API polling

**Advantages**:
✅ Structured, reliable data  
✅ Official sanctioned access  
✅ Stable interfaces  
✅ Lower server load  
✅ No parsing needed  

**Disadvantages**:
❌ Limited to sources with APIs  
❌ May require authentication  
❌ Limited query parameters  
❌ Rate limiting restrictions  

**Best For**: PIB (Press Information Bureau API), Data.gov.in API

**Tools**: requests library, GraphQL clients, Official SDKs

---

### Technique 3: Direct Download

**Definition**: Batch downloading of publicly available document archives

**Implementation**:
- Periodic bulk downloads from archives
- FTP/SFTP for bulk document transfer
- Version tracking and deduplication
- Checksum verification

**Advantages**:
✅ Complete archives available  
✅ Reliable and verifiable  
✅ Good for historical documents  
✅ Can include metadata  

**Disadvantages**:
❌ Limited to sources with archives  
❌ Less frequent updates  
❌ Large file sizes  
❌ Manual processing required  

**Best For**: Gazette archives, Parliamentary reports, CAG audit reports

---

### Technique 4: Email Subscriptions & Feeds

**Definition**: Automated monitoring of government notification services

**Implementation**:
- Subscribe to government email alerts
- Monitor RSS feeds
- Automated email parsing
- Document extraction from email attachments

**Advantages**:
✅ Timely notifications  
✅ Official sources  
✅ Structured metadata  
✅ Batch delivery  

**Disadvantages**:
❌ Limited coverage  
❌ Email parsing can be fragile  
❌ Attachment handling complexity  
❌ Manual filtering needed  

**Best For**: MOD circulars, Defence ministry notices, PIB emails

---

### Technique 5: OCR-Based Extraction

**Definition**: Scanning physical documents and extracting text

**Implementation**:
- Document digitization from archives
- OCR processing (Tesseract, EasyOCR)
- Layout analysis and reconstruction
- Confidence scoring

**Advantages**:
✅ Access to printed archives  
✅ Historical document preservation  
✅ Structured output from unstructured sources  

**Disadvantages**:
❌ High error rates  
❌ Slow processing  
❌ Quality varies with document condition  
❌ Requires manual QA  

**Best For**: Historical defence documents, archived reports

---

## 4. Collection Architecture

```
┌─────────────────────────────────────────────────┐
│              DATA SOURCE MONITORING              │
│  • MOD | DRDO | Gazette | PIB | Parliament      │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│         COLLECTION ORCHESTRATION                 │
│  ┌──────────────────────────────────────────┐   │
│  │ Web Scraper (MOD, DRDO, Gazette)         │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │ API Integration (PIB, Data.gov.in)       │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │ Direct Download (Archive.org, FTP)       │   │
│  └──────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────┐   │
│  │ Email/Feed Monitoring (Subscriptions)    │   │
│  └──────────────────────────────────────────┘   │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│          DOCUMENT VALIDATION                     │
│  • Format verification (PDF, HTML, Word)        │
│  • Size validation                              │
│  • Metadata extraction                          │
│  • Malware scanning                             │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│        DUPLICATE DETECTION & DEDUPLICATION      │
│  • Content hash (MD5, SHA-256)                  │
│  • Fuzzy matching (SimHash)                     │
│  • Near-duplicate detection                     │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│           METADATA EXTRACTION                    │
│  • Document title                               │
│  • Source URL                                   │
│  • Publication date                             │
│  • Author/Department                            │
│  • Document classification                      │
└──────────────┬──────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────┐
│        DOCUMENT STORE (STORAGE)                  │
│  • Original document preservation               │
│  • Metadata storage                             │
│  • Version tracking                             │
└─────────────────────────────────────────────────┘
```

---

## 5. Scheduling Strategy

**Crawling Schedule**:

| Source | Frequency | Time | Volume |
|--------|-----------|------|--------|
| MOD Website | Daily | 01:00 AM | 10-20 docs/day |
| DRDO Website | Daily | 02:00 AM | 5-10 docs/day |
| Gazette | Weekly | Sunday 01:00 AM | 50-100 docs/week |
| PIB | Daily | 12:00 AM | 20-30 docs/day |
| Parliament | Weekly | Monday 01:00 AM | 10-20 docs/week |
| Data.gov.in | Weekly | Friday 01:00 AM | Variable |

**Peak Load Distribution**:
- Stagger crawlers across different times
- Distribute load throughout the day
- Don't crawl during peak government hours
- No parallel crawls of same source

---

## 6. Quality Assurance

### Validation Checks

**Pre-Ingestion**:
- [ ] Document is publicly available (not behind login)
- [ ] File format is supported (PDF, DOC, HTML, TXT)
- [ ] File size within limits (< 100MB)
- [ ] No malware (VirusTotal scan)
- [ ] Character encoding is valid (UTF-8)

**Post-Download**:
- [ ] Document hash matches (integrity check)
- [ ] File is complete (not truncated)
- [ ] Metadata extracted successfully
- [ ] Not a duplicate of existing document
- [ ] Source URL is still valid

**Content Quality**:
- [ ] Document contains mostly text (not just images)
- [ ] Text extraction successful
- [ ] Language is English or Hindi
- [ ] Content is defence-related
- [ ] Not spam or advertising

---

## 7. Metadata Extraction

**Automatic Metadata Fields**:

```json
{
  "document_id": "MOD_2024_001",
  "title": "Defence Procurement Policy 2024",
  "source": "mod.gov.in",
  "source_url": "https://mod.gov.in/...",
  "retrieved_date": "2024-06-15",
  "publication_date": "2024-06-01",
  "document_type": "Policy",
  "author": "Ministry of Defence",
  "language": "English",
  "file_format": "PDF",
  "file_size_mb": 2.5,
  "page_count": 15,
  "text_length": 45000,
  "classification": "Gazette",
  "tags": ["Procurement", "Policy", "Defence"],
  "content_hash": "sha256:abc123..."
}
```

---

## 8. Deduplication Strategy

### Exact Duplicates
- MD5 hash of file content
- Binary comparison
- Remove one, keep original

### Near Duplicates
- SimHash for content fingerprinting
- Jaccard similarity on shingles
- Flag for manual review if >90% similar

### Content-Based Duplicates
- Different file formats, same content
- Latest version extraction
- Metadata-based detection

---

## 9. Estimated Data Volume

**Year 1 Projection**:
- 10,000-15,000 documents
- 2-5 GB total storage
- 50-100 documents per day

**Year 3 Projection**:
- 50,000-75,000 documents
- 10-20 GB total storage
- 30-50 documents per day

**Year 5 Projection**:
- 100,000+ documents
- 30-50 GB total storage
- 30-50 documents per day

---

## 10. Data Source Status Table

| Source | Collection Method | Frequency | Status | Documents |
|--------|------------------|-----------|--------|-----------|
| MOD Website | Web Scraping | Daily | ✅ Active | ~2000 |
| DRDO Website | Web Scraping | Daily | ✅ Active | ~1000 |
| Gazette of India | Direct Download + API | Weekly | ✅ Active | ~3000 |
| PIB | API + Email Feed | Daily | ✅ Active | ~2000 |
| Parliament | Web Scraping | Weekly | ✅ Active | ~1000 |
| CAG Reports | Direct Download | As Released | ✅ Active | ~500 |
| Data.gov.in | API | Weekly | ✅ Active | ~1000 |

---

## 11. Tools & Technologies

**Web Scraping**:
- Scrapy (Python framework)
- BeautifulSoup (HTML parsing)
- Selenium (JavaScript rendering)
- Requests (HTTP client)

**API Integration**:
- requests library
- aiohttp (async HTTP)
- Official Python SDKs

**Scheduling**:
- APScheduler (task scheduling)
- Celery (distributed task queue)
- Cron (system scheduling)

**Deduplication**:
- SimHash library
- HashLib (hashing)
- Elasticsearch (content search)

**Storage**:
- AWS S3 / MinIO (object storage)
- PostgreSQL (metadata)
- Redis (caching)

---

## 12. Implementation Timeline (Phase 2)

| Task | Timeline | Owner |
|------|----------|-------|
| Design collection architecture | Weeks 1-2 | Lead Engineer |
| Implement MOD scraper | Weeks 3-4 | Engineer 1 |
| Implement DRDO scraper | Weeks 3-4 | Engineer 2 |
| Implement PIB API integration | Weeks 5-6 | Engineer 3 |
| Implement deduplication system | Weeks 6-7 | Engineer 1 |
| Build validation pipeline | Weeks 7-8 | Engineer 2 |
| Set up scheduling | Weeks 8-9 | Engineer 3 |
| Quality assurance testing | Weeks 9-10 | QA Team |
| Operational handoff | Weeks 10-12 | All |

---

## 13. Success Metrics

✅ Collect 100+ documents per week  
✅ <1% document loss rate  
✅ <5% duplicate rate  
✅ 95%+ successful metadata extraction  
✅ Zero malware detected documents  
✅ <1 day latency from publication to collection  

---

## Next Steps

1. Finalize list of data sources with MOD/DRDO
2. Get technical access to APIs and systems
3. Begin implementation of scrapers (Phase 2)
4. Set up storage and deduplication infrastructure
5. Establish quality assurance procedures

---

*Last Updated: May 26, 2026*
