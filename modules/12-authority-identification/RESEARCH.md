# Module 12: Authority Identification Module

## Research Document

---

## 1. Overview

The Authority Identification Module identifies responsible departments, divisions, and officers from defence documents, enabling governance mapping and accountability tracking.

---

## 2. Authority Types

**Government Levels**:
- Ministry (Ministry of Defence)
- Department (Department of Defence Research & Development)
- Division/Wing (Aeronautical Development Agency)
- Establishment (DRDO Lab, Defence Shipyard)

**Roles**:
- Secretary/Director
- Officer-in-charge
- Project Lead
- Technical Expert

**Organizations**:
- Armed Forces (Army, Navy, Air Force)
- Defence Agencies (DRDO, Defence Offset Office)
- Defence Undertakings (BEL, HAL, etc.)

---

## 3. Identification Methods

### Method 1: Named Entity Recognition (NER)

**Approach**: Recognize authority names using NER

**Advantages**:
✅ Fast  
✅ Easy to implement  
✅ Works for standard names  

**Disadvantages**:
❌ Doesn't understand organization structure  
❌ Can't disambiguate similar names  
❌ Doesn't extract relationships  

---

### Method 2: Semantic Mapping

**Approach**: Map authority mentions to canonical forms

**Components**:
1. NER (recognize authority names)
2. Fuzzy matching (handle variations)
3. Knowledge base lookup (canonical form)
4. Confidence scoring

**Advantages**:
✅ Handles variations ("MOD" → "Ministry of Defence")  
✅ Reliable disambiguation  

---

### Method 3: Organizational Hierarchy

**Approach**: Use known hierarchy to infer relationships

**Structure**:
```
Ministry of Defence
├─ Department of Defence
├─ Department of Defence Research
│  └─ DRDO
│     ├─ Aeronautical Development Agency
│     ├─ Defence Electronics Research Lab
│     └─ Vehicles Research & Development Establishment
└─ Department of Military Affairs
   ├─ Army Headquarters
   ├─ Navy Headquarters
   └─ Air Force Headquarters
```

**Advantages**:
✅ Understand relationships  
✅ Infer missing information  
✅ Validate extracted authorities  

---

### Method 4: Relation Extraction

**Approach**: Extract "X approved by Y" relationships

**Techniques**:
- Pattern matching (e.g., "approved by [Authority]")
- Sequence tagging (BiLSTM-CRF for relation extraction)
- Dependency parsing

**Advantages**:
✅ Explicit relationship capture  
✅ Understand authority responsibility  

---

## 4. Recommended Approach

**Multi-Stage Pipeline**:

1. **Stage 1 - NER**: Recognize authority names
2. **Stage 2 - Linking**: Map to canonical forms
3. **Stage 3 - Hierarchy**: Use organizational structure
4. **Stage 4 - Relations**: Extract approval relationships
5. **Stage 5 - Validation**: Consistency checking

---

## 5. Knowledge Base Structure

```json
{
  "authority_id": "MOD_001",
  "name": "Ministry of Defence",
  "abbreviations": ["MOD", "Defence Ministry"],
  "established": 1947,
  "parent_organization": "Government of India",
  "sub_organizations": [
    "Department of Defence",
    "Department of Defence Research"
  ],
  "roles": {
    "secretary": "Secretary (Defence)",
    "official": "Additional Secretary"
  },
  "contact_info": "https://mod.gov.in",
  "aliases": ["Ministry of Defence India"]
}
```

---

## 6. Handling Ambiguity

**Challenge**: "Army" could mean:
- Indian Army (official name)
- Department of Military Affairs
- Army Headquarters

**Solution**:
- Context-aware resolution
- Hierarchical disambiguation
- Confidence scoring

---

## 7. Responsibility Mapping

**Examples of Responsibility Assignment**:
- Secretary (Defence) approves major procurements
- Chairman DRDO oversees research
- Servicecommanders oversee training/operations
- Finance department manages budgets

**Implementation**:
- Define responsibility rules
- Extract authority + action pairs
- Validate against known patterns

---

## 8. Temporal Changes

**Challenge**: Authorities and structures change over time

**Solution**:
- Temporal authority database
- Track authority changes
- Version control
- Historical lookups

---

## 9. Performance Targets

✅ **Authority Recognition F1-Score**: >90%  
✅ **Canonical Mapping Accuracy**: >95%  
✅ **Relationship Extraction F1-Score**: >85%  
✅ **Processing Speed**: 2000+ documents/hour  

---

## 10. Implementation Roadmap

| Task | Timeline |
|------|----------|
| Build authority knowledge base | Week 1-2 |
| Implement NER for authorities | Week 2-3 |
| Create canonical mapping | Week 3-4 |
| Build hierarchy engine | Week 4-5 |
| Implement relation extraction | Week 5-6 |
| Validation & testing | Week 6-7 |
| Deployment | Week 7-8 |

---

## 11. Governance Dashboard Output

**Authority Report Generated**:
- Authority responsible for document
- Approval chain
- Related authorities
- Historical decisions
- Responsibility matrix

---

*Last Updated: May 26, 2026*
