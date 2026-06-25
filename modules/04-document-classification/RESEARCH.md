# Module 4: Document Classification

## Research Document

---

## 1. Overview

The Document Classification Module categorizes documents into 10 predefined classes to enable targeted analysis and specialized processing workflows.

---

## 2. Document Taxonomy (10 Classes)

| Class | Definition | Examples | Volume (Est.) |
|-------|-----------|----------|----------------|
| **Financial** | Budget documents, expenditure reports, financial statements | Defence Budget, Financial Audit Reports | 15% |
| **Procurement** | Tender notices, RFQ, procurement policies | Tender Documents, Procurement Guidelines | 20% |
| **Guidelines** | Policy guidelines, standard operating procedures | Defence Procurement Policy, Strategic Guidelines | 15% |
| **Gazette** | Official gazette notifications | Gazette of India Defence Notifications | 15% |
| **Memorandum** | Official memorandums and circulars | Defence Ministry Circulars, Official Orders | 20% |
| **Technical** | Technical reports, research papers, specifications | DRDO Reports, Technical Specifications | 5% |
| **Administrative** | Administrative orders, organizational directives | Administrative Orders, Appointment Notices | 5% |
| **Security** | Security-related documents, protocols | Security Guidelines, Access Control Policies | 2% |
| **Budget** | Budget allocation, budget speeches, fiscal policies | Budget Speeches, Fund Allocation Documents | 2% |
| **Tender** | Tender documents, bid evaluation reports | Request for Quotation, Tender Evaluation | 1% |

---

## 3. Classification Algorithms Comparison

### Algorithm 1: Support Vector Machines (SVM)

**Description**: Linear classifier that finds optimal hyperplane separating classes

**Advantages**:
✅ Fast training  
✅ Works well with high-dimensional data  
✅ Interpretable decisions  
✅ Good on balanced datasets  

**Disadvantages**:
❌ Needs feature engineering  
❌ Slower prediction on large datasets  
❌ Requires class balancing  
❌ Limited to linear separation (without kernels)  

**Performance Estimate**: 85-88% accuracy

---

### Algorithm 2: Random Forest

**Description**: Ensemble of decision trees voting on classification

**Advantages**:
✅ Handles imbalanced data well  
✅ Fast inference  
✅ Feature importance available  
✅ Good generalization  

**Disadvantages**:
❌ Requires careful tuning  
❌ Black-box (less interpretable)  
❌ Large memory footprint  

**Performance Estimate**: 88-91% accuracy

---

### Algorithm 3: Logistic Regression

**Description**: Linear classifier using logistic function

**Advantages**:
✅ Simple and fast  
✅ Probabilistic outputs (confidence scores)  
✅ Efficient training  
✅ Interpretable coefficients  

**Disadvantages**:
❌ Assumes linear separability  
❌ Needs feature engineering  
❌ Struggles with complex patterns  

**Performance Estimate**: 80-85% accuracy

---

### Algorithm 4: BERT Classifier

**Description**: Fine-tuned pre-trained transformer model

**Advantages**:
✅ State-of-the-art accuracy  
✅ Contextual understanding  
✅ Transfer learning (pre-trained)  
✅ Handles variable-length text  

**Disadvantages**:
❌ Slow inference (need GPU)  
❌ Requires fine-tuning data  
❌ Large model size  
❌ Expensive to run  

**Performance Estimate**: 91-94% accuracy

---

## 4. Detailed Comparison Table

| Aspect | SVM | Random Forest | Logistic Regression | BERT |
|--------|-----|---------------|-------------------|------|
| **Accuracy** | 86% | 90% | 83% | 93% |
| **Training Time** | Fast | Medium | Very Fast | Slow (GPU needed) |
| **Inference Time** | Medium | Very Fast | Very Fast | Slow |
| **Interpretability** | Good | Medium | Excellent | Poor (black-box) |
| **Hyperparameter Tuning** | Moderate | High | Low | High |
| **Feature Engineering Needed** | Yes | No | Yes | No |
| **Handles Imbalance** | ⚠️ Moderate | ✅ Good | ❌ Poor | ✅ Good |
| **GPU Required** | No | No | No | Yes (recommended) |
| **Memory Required** | Low | High | Low | Very High |
| **Deployability** | Easy | Easy | Very Easy | Complex |

---

## 5. Recommended Approach: Ensemble

**Stage 1: Production Classifier (Fast)**
- Random Forest on TF-IDF features
- Accuracy: ~90%
- Speed: <10ms per document
- For initial classification

**Stage 2: Confidence Thresholding**
- If confidence > 0.95 → Use Random Forest result
- If confidence 0.70-0.95 → Secondary classifier
- If confidence < 0.70 → Manual review queue

**Stage 3: Secondary Classifier (Accurate)**
- BERT classifier for uncertain cases
- Accuracy: ~93%
- Speed: 100-500ms per document
- Use for final classification on low-confidence cases

---

## 6. Feature Engineering

**TF-IDF Features**:
- 5000-10000 most important terms
- IDF weighting to emphasize rare discriminative terms
- Works well for SVM and Random Forest

**Specialized Features**:
- Document length
- Average sentence length
- Presence of specific keywords per class
- Presence of tables, figures
- Date references

---

## 7. Implementation Strategy

**Phase 1: Data Collection**
- Label 1000-2000 sample documents
- Create balanced training set
- Hold out 20% for testing

**Phase 2: Baseline Classifier**
- Train SVM or Random Forest on TF-IDF
- Achieve 85-90% accuracy
- Deploy to production

**Phase 3: Improvement**
- Collect predictions and human feedback
- Fine-tune BERT on 500+ labeled examples
- Improve accuracy to 91-93%

**Phase 4: Deployment**
- Ensemble approach: Random Forest + BERT
- Confidence thresholding
- Manual review queue for uncertain cases

---

## 8. Handling Imbalanced Classes

**Problem**: Some classes (Budget, Tender) are rare (<2% of documents)

**Solutions**:

1. **Oversampling**: Duplicate rare class examples
2. **Undersampling**: Reduce common class examples
3. **Class Weights**: Higher weight for rare classes
4. **Synthetic Data**: Generate synthetic minority class examples (SMOTE)
5. **Ensemble Methods**: Use methods that handle imbalance well (Random Forest)

**Recommended**: Use Random Forest with class weights + manual review for rare classes

---

## 9. Performance Targets

✅ **Accuracy**: >90% overall, >85% per class  
✅ **Precision**: >92% (minimize false positives)  
✅ **Recall**: >88% (minimize false negatives)  
✅ **F1-Score**: >90%  
✅ **Processing Speed**: <50ms per document (average)  

---

## 10. Tools & Libraries

**ML Frameworks**:
- scikit-learn (SVM, Random Forest, Logistic Regression)
- Transformers library (BERT classifier)
- XGBoost (alternative ensemble method)

**Feature Engineering**:
- TfidfVectorizer (scikit-learn)
- CountVectorizer (scikit-learn)

**Evaluation**:
- sklearn.metrics (accuracy, precision, recall, F1)
- Confusion matrix analysis

---

## Next Steps

1. Create labeled training dataset (1000-2000 documents)
2. Train baseline SVM and Random Forest classifiers
3. Evaluate on test set
4. Plan BERT fine-tuning
5. Deploy ensemble classifier

---

*Last Updated: May 26, 2026*
