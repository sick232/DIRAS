# Module 2: OCR & Document Understanding

## Research Document

---

## 1. Overview

The OCR and Document Understanding Module handles extraction of text from scanned PDFs, images, and complex document layouts. This is critical because a significant portion of defence documents are scanned/image-based.

---

## 2. OCR Technology Comparison

### Technique 1: Tesseract OCR

**Description**: Open-source OCR engine by Google, industry standard for 20+ years

**Architecture**:
- Optical character recognition using neural networks
- Supports 100+ languages including English and Hindi
- Can be trained on custom datasets
- Command-line tool or library integration

**Advantages**:
✅ Open source, free  
✅ Mature and stable (20+ years development)  
✅ Good English support  
✅ Can be fine-tuned  
✅ Low resource requirements  
✅ Excellent community support  

**Disadvantages**:
❌ Struggles with skewed/rotated images  
❌ Poor performance on low-quality scans  
❌ Limited Hindi support (needs training)  
❌ Slow on complex layouts  
❌ No table extraction  
❌ Requires preprocessing  

**Performance Metrics**:
- Character Error Rate (CER): 3-8% on good scans, 15-30% on poor scans
- Processing Speed: 50-200 images/hour (CPU)
- Memory: Minimal (~50MB)
- GPU Support: No

**Best For**: Clean, high-quality English scanned documents

**Hindi Support**: Limited, requires training on Hindi fonts

---

### Technique 2: EasyOCR

**Description**: PyTorch-based OCR with easy-to-use Python API

**Architecture**:
- Deep learning (CRAFT detector + CRNN recognizer)
- Pre-trained on 80+ languages
- Supports both CPU and GPU
- Built-in image preprocessing
- Multi-language support in single image

**Advantages**:
✅ Easy to use Python library  
✅ Good out-of-box performance  
✅ Excellent Hindi support  
✅ Handles skewed/rotated text  
✅ GPU acceleration available  
✅ Multi-language in single image  
✅ Good on scanned documents  

**Disadvantages**:
❌ Slower than Tesseract (without GPU)  
❌ Higher resource requirements  
❌ Can be overkill for simple documents  
❌ Less configurable than Tesseract  
❌ Table extraction still limited  

**Performance Metrics**:
- Character Error Rate (CER): 2-5% on good scans, 8-15% on poor scans
- Processing Speed: 10-50 images/hour (CPU), 200-500/hour (GPU)
- Memory: 2-4GB RAM
- GPU Support: Yes (CUDA)

**Best For**: Multi-language documents, Hindi support needed, varied quality scans

**Hindi Support**: Excellent (pre-trained)

---

### Technique 3: PaddleOCR

**Description**: Baidu's lightweight OCR system optimized for Chinese/Hindi

**Architecture**:
- Text detection (DB network) + recognition (CRNN)
- Lightweight models for fast inference
- Supports 80+ languages
- Optimized for Asian languages

**Advantages**:
✅ Very fast (even on CPU)  
✅ Lightweight models  
✅ Excellent multi-language support  
✅ Good Hindi support  
✅ Can run on edge devices  
✅ Easy Python API  
✅ Free and open source  

**Disadvantages**:
❌ Less accurate than EasyOCR on English  
❌ Lower quality on complex layouts  
❌ Less community support  
❌ No table extraction  
❌ Smaller model means lower accuracy  

**Performance Metrics**:
- Character Error Rate (CER): 3-7% on good scans, 10-20% on poor scans
- Processing Speed: 100-300 images/hour (CPU), 500+/hour (GPU)
- Memory: Minimal (500MB-1GB)
- GPU Support: Yes (CUDA, OpenCL)

**Best For**: Fast processing, mobile/edge deployment, Hindi documents

**Hindi Support**: Very good (optimized)

---

### Technique 4: LayoutParser + Detectron2

**Description**: AI system for document layout analysis and understanding

**Architecture**:
- Layout detection (identifies regions: text, table, figure, etc.)
- Region-specific OCR
- Structured output preserving document structure
- Built on Detectron2 framework

**Advantages**:
✅ Preserves document structure  
✅ Identifies tables, headers, figures  
✅ Region-specific processing  
✅ Outputs structured HTML/XML  
✅ Excellent for complex documents  
✅ Better handling of multi-column layouts  
✅ Good on low-quality scans  

**Disadvantages**:
❌ Slower than pure OCR  
❌ More complex to integrate  
❌ Higher resource requirements  
❌ Requires model downloads (large files)  
❌ Still uses underlying OCR (needs selection)  
❌ Less mature than Tesseract  

**Performance Metrics**:
- Layout Detection Accuracy: 92-98%
- Processing Speed: 5-20 images/hour (CPU)
- Memory: 4-8GB RAM
- GPU Support: Recommended

**Best For**: Complex layouts, tables, multi-column documents, preservation of structure

**Table Extraction**: Yes, extracts table structure

---

## 3. Detailed Comparison Table

| Aspect | Tesseract | EasyOCR | PaddleOCR | LayoutParser |
|--------|-----------|---------|-----------|-------------|
| **Accuracy (English)** | 85-90% | 88-94% | 82-88% | N/A (Layout) |
| **Accuracy (Hindi)** | 60-70% | 88-92% | 85-90% | N/A (Layout) |
| **Speed (CPU)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Speed (GPU)** | No GPU | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Skewed/Rotated Text** | Poor | Excellent | Very Good | Excellent |
| **Table Extraction** | ❌ No | ⚠️ Limited | ❌ No | ✅ Yes |
| **Scanned Document Quality** | Medium | Excellent | Very Good | Excellent |
| **Multi-Language (One Image)** | Limited | ✅ Yes | ✅ Yes | Depends on OCR |
| **Configuration Options** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Memory Required** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **Open Source** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Ease of Use** | Medium | Very Easy | Easy | Medium |
| **Hindi Support** | Limited | Excellent | Very Good | Depends on OCR |
| **Maintainability** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

---

## 4. Defence Document-Specific Considerations

### Document Types & Challenges

**Gazette Publications**:
- Challenge: Multi-column layouts, dense text
- Recommendation: LayoutParser + EasyOCR
- Critical: Preserve table structure

**Official Memorandums**:
- Challenge: Good quality scans, standard layout
- Recommendation: Tesseract (fast) or EasyOCR (accurate)
- Critical: Accurate text for policy understanding

**Budget Documents**:
- Challenge: Tables, financial figures, multi-page
- Recommendation: LayoutParser for structure + EasyOCR for text
- Critical: Accurate number extraction

**Parliamentary Reports**:
- Challenge: Older scans, varying quality
- Recommendation: EasyOCR for robustness
- Critical: Handle degraded documents

**Procurement Documents**:
- Challenge: Tables, specifications, structured data
- Recommendation: LayoutParser + EasyOCR
- Critical: Preserve table structure and figures

### Bilingual Challenges (English + Hindi)

**Current State**:
- English: All OCR systems perform well
- Hindi: Limited to EasyOCR, PaddleOCR (with preparation)

**Future: Full Hindi Support**
- Will require significant effort
- Pre-trained Hindi models development
- Validation on defence documents

---

## 5. OCR Pipeline Architecture

```
Scanned PDF / Image
    ↓
Image Preprocessing
  ├─ Rotation correction
  ├─ Skew detection & correction
  ├─ Contrast enhancement
  ├─ Noise removal
  └─ Resolution scaling
    ↓
Layout Detection (Optional)
  ├─ Region identification (text, table, figure)
  ├─ Bounding box extraction
  └─ Reading order detection
    ↓
Region-Specific OCR
  ├─ Text region → EasyOCR
  ├─ Table region → Table extraction + OCR
  └─ Figure region → Image analysis
    ↓
Post-Processing
  ├─ Language detection
  ├─ Spell correction
  ├─ Table reconstruction
  └─ Confidence scoring
    ↓
Output
  ├─ Plain text
  ├─ Structured HTML (with layout)
  └─ Metadata
```

---

## 6. Recommended Strategy for DIRAS

**Hybrid Approach**:

1. **Primary OCR**: EasyOCR
   - Best balance of accuracy and speed
   - Excellent Hindi support (future)
   - Handles varied document quality
   - Good on skewed/rotated text

2. **Layout Analysis**: LayoutParser + Detectron2
   - For complex documents (budgets, gazette, reports)
   - Preserves table structure
   - Identifies document sections

3. **Fallback**: Tesseract
   - Fast processing for simple documents
   - When EasyOCR is too slow
   - For preprocessing-heavy documents

**Quality Control**:
- Confidence thresholding (only accept OCR if >0.85 confidence)
- Manual review queue for low-confidence documents
- Periodic validation samples (1-5%)

---

## 7. Implementation Roadmap (Phase 2)

| Task | Timeline | Details |
|------|----------|---------|
| Set up EasyOCR pipeline | Week 1-2 | Model download, API creation |
| Integrate LayoutParser | Week 2-3 | Layout detection pipeline |
| Build preprocessing system | Week 3-4 | Image enhancement, rotation, skew |
| Implement confidence thresholding | Week 4-5 | Quality gates |
| Build manual review queue | Week 5-6 | For low-confidence documents |
| Performance benchmarking | Week 6-7 | Accuracy, speed, resource testing |
| Hindi support prep (future) | Week 7-8 | Training data collection |

---

## 8. Performance Targets

✅ **Character Accuracy**: >92% on clean scans, >85% on degraded  
✅ **Processing Speed**: 50+ documents/hour on single GPU  
✅ **Table Detection**: >90% accuracy  
✅ **Manual Review Rate**: <5% of documents  
✅ **Hindi Ready**: Infrastructure in place for Phase 5+  

---

## 9. Tools & Libraries

**Primary OCR**:
- EasyOCR (Python library)
- PyTorch (deep learning framework)

**Layout Analysis**:
- LayoutParser (document layout detection)
- Detectron2 (object detection)
- Camelot or Tabula (table extraction)

**Image Preprocessing**:
- OpenCV (image processing)
- Pillow (image manipulation)
- scikit-image (advanced image operations)

**Processing Pipeline**:
- Celery (distributed task queue)
- Ray (parallel processing)

---

## Next Steps

1. Evaluate Tesseract vs EasyOCR vs PaddleOCR on sample defence documents
2. Benchmark table extraction approaches
3. Design image preprocessing pipeline
4. Plan infrastructure for GPU-based processing
5. Prepare for Hindi support evaluation

---

*Last Updated: May 26, 2026*
