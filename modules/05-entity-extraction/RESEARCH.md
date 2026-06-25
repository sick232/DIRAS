# Module 5: Entity Extraction (Named Entity Recognition)

## Research Document

---

## 1. Overview

The Entity Extraction Module identifies and extracts structured information from documents using Named Entity Recognition (NER). This enables authority identification, financial analysis, and relationship mapping.

---

## 2. Entity Types to Extract

| Entity Type | Examples | Importance | Volume |
|-------------|----------|-----------|--------|
| **Authority/Department** | Ministry of Defence, DRDO, IAF, Navy | Critical | High |
| **Officer/Personnel** | Secretary, Defence Minister | High | Medium |
| **Dates** | June 15, 2024, FY 2024-25 | Critical | Very High |
| **Monetary Values** | ₹100 crores, $5 million | Critical | High |
| **Equipment/Platform** | Arjun Tank, INS Vikramaditya | High | Medium |
| **Location** | New Delhi, Pune | High | Medium |
| **Organization** | Private contractors, suppliers | High | Medium |
| **Project Names** | Pradhan Mantri Production-Linked Incentive Scheme | Medium | Low |
| **Document Type** | Tender, Circular, Order | Medium | High |
| **Procurement Items** | Weapons, vehicles, software | High | Medium |

---

## 3. NER Methods Comparison

### Method 1: SpaCy NER

**Description**: Rule-based and statistical NER using spaCy library

**Advantages**:
✅ Fast processing  
✅ Good English support  
✅ Easy to use  
✅ Low resource requirements  
✅ Can be trained on custom data  

**Disadvantages**:
❌ Limited accuracy on specialized entities (defence-specific)  
❌ Requires substantial training data  
❌ Limited Hindi support  
❌ Rule-based approach not contextual  

**Performance Estimate**: 75-82% F1-score

---

### Method 2: BERT-Based NER

**Description**: Pre-trained transformer model fine-tuned for NER

**Advantages**:
✅ High accuracy with minimal data  
✅ Contextual understanding  
✅ Transfer learning from pre-training  
✅ Good on specialized domains  

**Disadvantages**:
❌ Slower inference (need GPU)  
❌ Requires GPU for training  
❌ Large model size  
❌ Complex to deploy  

**Performance Estimate**: 85-88% F1-score

---

### Method 3: CRF (Conditional Random Fields)

**Description**: Statistical sequence labeling model

**Advantages**:
✅ Good for sequence tagging  
✅ Interpretable  
✅ Fast training and inference  
✅ Works with hand-crafted features  

**Disadvantages**:
❌ Requires feature engineering  
❌ Limited accuracy on complex patterns  
❌ Not contextual  
❌ Needs substantial labeled data  

**Performance Estimate**: 78-84% F1-score

---

### Method 4: BiLSTM-CRF

**Description**: Neural sequence model combining BiLSTM with CRF

**Advantages**:
✅ High accuracy  
✅ Contextual via LSTM  
✅ End-to-end learning  
✅ Good on domain-specific data  

**Disadvantages**:
❌ Slower than pure CRF  
❌ Requires GPU for training  
❌ Complex to debug  
❌ Hyperparameter tuning critical  

**Performance Estimate**: 84-89% F1-score

---

## 4. Detailed Comparison

| Method | spaCy | BERT | CRF | BiLSTM-CRF |
|--------|-------|------|-----|-----------|
| **Accuracy (F1-score)** | 78% | 87% | 81% | 87% |
| **Training Time** | Minutes | Hours | Minutes | Hours |
| **Inference Speed** | Very Fast | Slow | Very Fast | Medium |
| **GPU Required** | No | Recommended | No | Recommended |
| **Interpretability** | Good | Poor | Excellent | Medium |
| **Feature Engineering** | Low | None | High | Low |
| **Adaptation to New Entities** | Medium | Easy | Hard | Medium |
| **Defence Specialty** | Good | Excellent | Medium | Very Good |

---

## 5. Recommended Hybrid Approach

**Stage 1: Fast Recognition (spaCy)**
- Standard entity types (date, location, organization)
- Fast, real-time processing
- F1-score: ~80%
- Processing Speed: 5000+ docs/hour

**Stage 2: Specialized Recognition (BERT)**
- Defence-specific entities (authority, equipment, project)
- Higher accuracy
- Contextual understanding
- F1-score: ~88%
- Processing Speed: 500+ docs/hour

**Stage 3: Relationship Extraction**
- Link entities to create relationships
- Authority → Department → Responsibility
- Equipment → Procurement → Budget

---

## 6. Defence-Specific NER Challenges

**Abbreviations & Acronyms**:
- MOD, DRDO, IAF, INS, Army, Navy
- These must be recognized as authority entities, not generic abbreviations

**Technical Terminology**:
- Missile, platform, weapon system
- Complex compound nouns

**Named Variations**:
- "Ministry of Defence" vs "MOD" vs "Defence Ministry"
- Need entity linking to canonical forms

**Hindi-English Code-switching**:
- Future challenge when adding Hindi support

---

## 7. Entity Linking

**Problem**: Multiple entity names for same entity
- "Ministry of Defence India" = "MOD" = "Defence Ministry"

**Solution**: Entity Linking Pipeline
1. Recognize entity string from text
2. Look up canonical form in knowledge base
3. Link to unique entity ID
4. Create relationships

---

## 8. Training Data Requirements

**Minimum Training Data**: 500-1000 annotated documents
**Ideal Training Data**: 2000-5000 annotated documents

**Annotation Guidelines**:
- Clear boundary detection (start/end of entity)
- Handle multi-word entities
- Multiple entity types per text
- Inter-annotator agreement >0.85 (Cohen's Kappa)

---

## 9. Evaluation Metrics

**Precision**: Correctly identified entities / All identified entities
- Target: >90%

**Recall**: Correctly identified entities / All actual entities
- Target: >85%

**F1-Score**: Harmonic mean of precision and recall
- Target: >87%

**Per-Entity-Type Evaluation**: Metrics for each entity type separately
- Authority: F1 >90% (most critical)
- Monetary: F1 >92% (must be accurate)
- Date: F1 >95% (should be near-perfect)

---

## 10. Implementation Roadmap

**Phase 2**:
- Week 1-2: Create annotated training dataset (1000 docs)
- Week 2-3: Train spaCy and BERT models
- Week 3-4: Fine-tune on defence-specific data
- Week 4-5: Implement entity linking
- Week 5-6: Build relationship extraction
- Week 6-7: Integration and testing

---

## 11. Performance Targets

✅ **Authority Entity F1-Score**: >90%  
✅ **Monetary Entity F1-Score**: >92%  
✅ **Date Entity F1-Score**: >95%  
✅ **Overall F1-Score**: >87%  
✅ **Processing Speed**: 2000+ docs/hour  

---

## 12. Tools & Libraries

**spaCy**:
- spacy (main library)
- spacy-lookups-data (for lemmatization)

**BERT**:
- transformers library (HuggingFace)
- torch (PyTorch)

**CRF & BiLSTM**:
- python-crfsuite (CRF implementation)
- PyTorch (BiLSTM-CRF)

**Entity Linking**:
- Custom knowledge base (PostgreSQL)
- Fuzzy matching (fuzzywuzzy)

---

## Next Steps

1. Create entity annotation guidelines
2. Recruit annotators for training data
3. Annotate 1000+ documents
4. Train baseline spaCy model
5. Fine-tune BERT on defence data
6. Evaluate and iterate

---

*Last Updated: May 26, 2026*
