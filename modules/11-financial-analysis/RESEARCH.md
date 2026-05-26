# Module 11: Financial Analysis Module

## Research Document

---

## 1. Overview

The Financial Analysis Module extracts and analyzes financial information from defence documents, enabling budget intelligence and procurement analysis.

---

## 2. Financial Entities to Extract

**Monetary Values**:
- Budget figures: ₹100 crores, $5 million
- Expenditure amounts
- Allocation figures
- Cost estimates

**Financial Attributes**:
- Currency (INR, USD, EUR)
- Time period (FY 2024-25)
- Category (Capital, Revenue)
- Authority responsible

**Relationships**:
- Budget → Department → Officer
- Expenditure → Project → Equipment
- Allocation → Purpose → Duration

---

## 3. Extraction Methods

### Rule-Based Extraction

**Approach**: Regex patterns + rule engines

**Advantages**:
✅ Fast  
✅ Interpretable  
✅ Predictable  

**Disadvantages**:
❌ Brittle  
❌ Domain-specific  
❌ High false negatives  

---

### Transformer-Based Extraction

**Approach**: Fine-tuned BERT/RoBERTa for financial NER

**Advantages**:
✅ Better accuracy  
✅ Contextual  
✅ More robust  

**Disadvantages**:
❌ Requires training data  
❌ Slower  

---

## 4. Recommended Approach

**Hybrid**:
1. Rule-based detection (fast first pass)
2. Transformer confirmation (high confidence)
3. Post-processing (amount normalization)
4. Relationship extraction (context linking)

---

## 5. Amount Normalization

**Challenge**: Different formats
- ₹100 crores = ₹1,000,000,000
- $5 million = ₹42 crores (exchange rate dependent)
- 1000 lakhs = ₹10 crores

**Solution**: Normalization to standard unit (INR Crores)

---

## 6. Temporal Association

**Challenge**: Amount could refer to multiple years

**Solution**:
- Link to fiscal year (FY 2024-25)
- Link to quarter
- Infer from context

---

## 7. Authority Association

**Challenge**: Which department is budget for?

**Solution**:
- Named entity extraction (authority)
- Contextual understanding
- Relationship extraction

---

## 8. Financial Analysis Outputs

**Aggregations**:
- Total defence budget by year
- Spending by category
- Top procurement projects
- Authority-wise allocation

**Trend Analysis**:
- Budget growth trends
- Spending patterns
- Equipment procurement cycles

---

## 9. Performance Targets

✅ **Amount Extraction Accuracy**: >95%  
✅ **Authority Association Accuracy**: >90%  
✅ **Temporal Association Accuracy**: >85%  
✅ **Processing Speed**: 1000+ documents/hour  

---

## 10. Implementation Roadmap

| Task | Timeline |
|------|----------|
| Define financial entity types | Week 1 |
| Create extraction rules | Week 1-2 |
| Build rule-based extractor | Week 2-3 |
| Create training data | Week 3-4 |
| Fine-tune financial NER | Week 4-5 |
| Post-processing pipeline | Week 5-6 |
| Integration testing | Week 6-7 |
| Deployment | Week 7-8 |

---

*Last Updated: May 26, 2026*
