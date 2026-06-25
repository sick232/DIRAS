# Module 3: Preprocessing Pipeline

## Research Document

---

## 1. Overview

The Preprocessing Pipeline transforms raw text from OCR into clean, normalized, and ready-for-analysis text. This module ensures data quality and consistency across all documents.

---

## 2. Preprocessing Techniques Comparison

### Technique 1: Regex-Based Cleaning

**Description**: Pattern-based text cleaning using regular expressions

**Operations**:
- Remove special characters and artifacts
- Fix common OCR errors (replace "0" with "O", "1" with "l")
- Remove HTML tags and formatting
- Normalize whitespace
- Remove URLs and email addresses
- Fix common abbreviations

**Advantages**:
✅ Fast (microseconds per operation)  
✅ Deterministic and predictable  
✅ Easy to understand and maintain  
✅ No external dependencies  
✅ Can be tuned for domain-specific patterns  
✅ Minimal memory footprint  

**Disadvantages**:
❌ Requires manual rule creation  
❌ Domain-specific rules not portable  
❌ Can inadvertently remove important content  
❌ Regex complexity grows with requirements  
❌ No contextual understanding  

**Best For**: Standardization, removing artifacts, fixing common OCR errors

---

### Technique 2: NLTK (Natural Language Toolkit)

**Description**: Python library with built-in tokenization and text processing

**Operations**:
- Tokenization (sentence and word-level)
- Stopword removal (common words like "the", "a")
- Lemmatization (reduce words to base form)
- Part-of-speech (POS) tagging
- Named entity recognition basics

**Advantages**:
✅ Mature library (20+ years)  
✅ Good English support  
✅ Comprehensive functionality  
✅ Well-documented  
✅ Easy to use  
✅ Open source  

**Disadvantages**:
❌ Rule-based, not neural  
❌ Doesn't understand context  
❌ Limited Hindi support  
❌ Slower than spaCy  
❌ Limited accuracy on complex text  

**Best For**: Basic preprocessing, tokenization, standard operations

**Processing Speed**: 500-1000 docs/hour on single CPU

---

### Technique 3: spaCy

**Description**: Modern NLP library with neural network models

**Operations**:
- Fast tokenization
- Lemmatization with neural context
- POS tagging
- Dependency parsing
- Named entity recognition (NER)
- Custom processing pipelines
- Multi-language support

**Advantages**:
✅ Fast (10x faster than NLTK)  
✅ Neural-based for better accuracy  
✅ Contextual understanding  
✅ Easy pipeline extension  
✅ Good Hindi models available  
✅ Production-ready  
✅ Excellent documentation  

**Disadvantages**:
❌ Requires model downloads  
❌ Higher memory than NLTK  
❌ Model-dependent accuracy  
❌ Slower than regex on simple tasks  

**Best For**: Production systems, contextual understanding, NLP tasks

**Processing Speed**: 2000-5000 docs/hour on single CPU

---

### Technique 4: Transformer-Based (BERT)

**Description**: Using pre-trained transformer models for preprocessing

**Operations**:
- Contextual tokenization
- Semantic normalization
- Context-aware lemmatization
- Multilingual preprocessing
- Domain-specific fine-tuning

**Advantages**:
✅ Best contextual understanding  
✅ Handles complex text  
✅ Multilingual (100+ languages)  
✅ Can be fine-tuned  
✅ State-of-the-art accuracy  

**Disadvantages**:
❌ Expensive (need GPU)  
❌ Slower (100-500 docs/hour on CPU, 5000+/hour on GPU)  
❌ Overkill for simple cleaning  
❌ Large memory footprint  
❌ Requires maintenance  

**Best For**: Complex understanding, multilingual, when accuracy critical

**Processing Speed**: 100-500 docs/hour (CPU), 5000+/hour (GPU)

---

## 3. Detailed Comparison Table

| Aspect | Regex | NLTK | spaCy | Transformers |
|--------|-------|------|-------|--------------|
| **Speed (CPU)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ |
| **Accuracy** | ⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Contextual Understanding** | ❌ | ⚠️ Limited | ✅ Good | ✅ Excellent |
| **Memory Required** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Customizability** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **English Support** | ✅ | ✅ | ✅ | ✅ |
| **Hindi Support** | ❌ | ⚠️ Limited | ✅ Good | ✅ Excellent |
| **Maintenance** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Scalability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Production-Ready** | ✅ | ✅ | ✅ | ✅ |

---

## 4. Recommended Preprocessing Pipeline for DIRAS

**Hybrid Multi-Stage Approach**:

### Stage 1: Basic Cleaning (Regex)
- Remove HTML tags
- Fix common OCR artifacts
- Normalize whitespace
- Remove extra punctuation
- Decode special characters

**Processing Speed**: 10,000+ docs/hour

### Stage 2: Tokenization (spaCy)
- Sentence tokenization
- Word tokenization
- Preserve document structure
- Handle special cases (URLs, dates)

**Processing Speed**: 3000+ docs/hour

### Stage 3: Lemmatization & Normalization (spaCy)
- Convert to base form (walking → walk)
- Normalize numbers
- Handle contractions
- Case normalization

**Processing Speed**: 3000+ docs/hour

### Stage 4: Optional NER (spaCy)
- Extract named entities
- Flag for later processing
- Preserve for authority/financial analysis

**Processing Speed**: 2000+ docs/hour

### Stage 5: Quality Checks
- Check for anomalies
- Flag for manual review
- Confidence scoring

---

## 5. Preprocessing Operations Detail

### Text Cleaning
```
Input: "The Defence  ministry's---<TAG>offical  orders &lt;PDF&gt;  "
↓
Output: "The Defence ministry's official orders PDF"
```

**Operations**:
- Remove extra whitespace
- Remove HTML entities
- Fix encoding issues
- Remove special characters (keep only alphanumeric, spaces, basic punctuation)

### Tokenization
```
Input: "Defence procurement policy was issued on June 15, 2024."
↓
Sentences: ["Defence procurement policy was issued on June 15, 2024."]
↓
Tokens: ["Defence", "procurement", "policy", "was", "issued", "on", "June", "15", ",", "2024", "."]
```

### Lemmatization
```
Input Tokens: ["The", "organisations", "were", "procuring", "defence", "equipment"]
↓
Lemmatized: ["the", "organisation", "be", "procure", "defence", "equipment"]
```

### Stopword Removal (Optional)
```
Input: ["the", "Defence", "ministry", "has", "issued", "procurement", "guidelines"]
↓
Filtered: ["Defence", "ministry", "issued", "procurement", "guidelines"]
(Keep content words, remove function words)
```

---

## 6. Data Quality Metrics

**Pre-Preprocessing Validation**:
- Text encoding valid (UTF-8)
- Non-empty content
- Minimum length (>100 characters)
- No binary content

**Post-Preprocessing Validation**:
- Successfully tokenized
- Sufficient content remains (>50 tokens)
- No cascading errors
- Lemmatization successful
- Entity extraction (if applicable)

---

## 7. Scaling Considerations

**Single-Machine Processing**:
- spaCy pipeline: 2000-5000 docs/hour
- 100K documents: ~24 hours

**Distributed Processing**:
- Batch documents by size
- Parallel processing (multi-process/multi-machine)
- Stream processing (Kafka, RabbitMQ)
- Target: 10,000+ docs/hour

---

## 8. Handling Defence-Specific Content

**Challenges**:
- Abbreviations (MOD, DRDO, IAF, INS)
- Acronyms (Should NOT be lemmatized)
- Technical terms (missile, platform, procurement)
- Dates and temporal expressions
- Monetary values

**Solutions**:
- Custom stopword list (don't remove important defence terms)
- Preserve acronyms during lemmatization
- Custom lemmatization rules for defence vocabulary
- Separate handling of dates/monetary values

---

## 9. Implementation Roadmap (Phase 2)

| Task | Timeline |
|------|----------|
| Design pipeline architecture | Week 1 |
| Implement regex cleaning | Week 1-2 |
| Integrate spaCy models | Week 2-3 |
| Build quality checks | Week 3-4 |
| Performance optimization | Week 4-5 |
| Hindi support evaluation | Week 5-6 |
| Testing & validation | Week 6-7 |
| Deployment | Week 7-8 |

---

## 10. Performance Targets

✅ **Throughput**: 5000+ documents/hour (on single machine)  
✅ **Accuracy**: >99% successful tokenization and lemmatization  
✅ **Data Retention**: Preserve 95%+ of document content after cleaning  
✅ **Quality**: <1% documents requiring manual review  
✅ **Latency**: <100ms per document  

---

## 11. Tools & Libraries

**Primary Pipeline**:
- spaCy (tokenization, lemmatization, NER)
- NLTK (backup for specific operations)
- Regex (custom cleaning rules)

**Supporting**:
- re (Python regex library)
- unicodedata (character normalization)
- ftfy (encoding fixes)

---

## Next Steps

1. Define defence-specific vocabulary and acronyms
2. Create custom lemmatization rules
3. Benchmark preprocessing speed on sample documents
4. Evaluate Hindi support requirements
5. Design distributed processing strategy

---

*Last Updated: May 26, 2026*
