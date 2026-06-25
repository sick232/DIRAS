# User Acceptance Testing (UAT) Strategy - DIRAS Phase 2-5

**Document Version**: 1.0  
**Last Updated**: May 28, 2026  
**Timeline**: UAT at end of Phase 2, Phase 3, Phase 4  
**Scope**: System validation with MoD stakeholders + end users

---

## Executive Summary

UAT validates DIRAS system meets Ministry of Defence requirements across phases. Tests real-world scenarios, ensures reliability, and gains stakeholder buy-in before each phase transition.

---

## UAT Phases

### Phase 2 UAT (End of Phase 2, Oct 2026)
**Goal**: Validate MVP works; identify blockers  
**Duration**: 2-3 weeks  
**Participants**: 5-10 MoD analysts, project team  
**Scope**: 5 real-world scenarios (simplified)  
**Pass Criteria**: 80%+ tests pass, no critical blockers

### Phase 3 UAT (End of Phase 3, Jan 2027)
**Goal**: Full system validation in near-production environment  
**Duration**: 3-4 weeks  
**Participants**: 15-20 MoD analysts, DRDO engineers  
**Scope**: 10 real-world scenarios (all use cases)  
**Pass Criteria**: 95%+ tests pass, <5% critical issues

### Phase 4 UAT (End of Phase 4, May 2027)
**Goal**: Production readiness validation  
**Duration**: 4 weeks  
**Participants**: 30-50 end users, stakeholders  
**Scope**: 15 scenarios + load testing, security validation  
**Pass Criteria**: 99%+ tests pass, zero critical issues

---

## Phase 2 UAT Test Scenarios

### Scenario 1: Defence Budget Query (Financial Module)
**User**: Finance Analyst at Ministry of Defence  
**Query**: "What was the defence budget allocation for 2023-24, and how much was spent on military procurement?"

**Expected System Flow**:
1. User enters query in web interface
2. System parses intent (financial + procurement)
3. Retrieves relevant documents (budget reports, procurement data)
4. Extracts key figures (total budget, procurement amount, authorities)
5. Generates RAG answer with citations
6. User verifies accuracy, downloads results

**Test Steps**:
1. Verify query understood correctly
2. Verify retrieved documents are relevant (P@10 ≥0.80)
3. Verify extracted figures match ground truth (±2% tolerance)
4. Verify approving authority identified (✓/✗)
5. Verify answer is factually correct (no hallucination)
6. Verify response time <2 seconds

**Success Criteria**:
- ✓ Retrieved documents relevant
- ✓ Financial figures accurate
- ✓ Authority identified
- ✓ No hallucination detected
- ✓ Response time <2s

**Pass/Fail**: PASS if all criteria met

---

### Scenario 2: Procurement Process Discovery (Guideline Module)
**User**: Procurement Officer at Defence Ministry  
**Query**: "What is the procedure for defence equipment procurement? Who approves it?"

**Expected System Flow**:
1. Query intent: Guideline + authority
2. Retrieve procurement policy documents
3. Extract procedure steps, approval chain
4. Present as structured answer or document summary

**Test Steps**:
1. Verify guideline documents retrieved (not budget/finance docs)
2. Verify procedure steps correct and complete
3. Verify authority chain matches official org structure
4. Verify document references provided (citations)

**Success Criteria**:
- ✓ Correct document type retrieved
- ✓ All major steps identified
- ✓ Authority chain correct
- ✓ User can understand procedure from answer

**Pass/Fail**: PASS if 3/4 criteria met

---

### Scenario 3: Authority Identification (Organizational)
**User**: Defence Administrator  
**Query**: "Which ministry is responsible for defence procurement? Can Air Force approve contracts above ₹100 crores?"

**Expected System Flow**:
1. Extract authority + delegation rules
2. Identify relevant circulars/policies
3. Map organizational hierarchy
4. Answer with citations

**Test Steps**:
1. Verify correct ministry identified
2. Verify approval limits correct
3. Verify organizational relationships accurate
4. Verify answer provides proper delegation chain

**Success Criteria**:
- ✓ Correct ministry identified
- ✓ Approval limits accurate
- ✓ Delegation rules correct
- ✓ Proper citations provided

**Pass/Fail**: PASS if 4/4 criteria met

---

### Scenario 4: Document Type Handling (Multilingual)
**User**: DRDO Researcher  
**Query**: "Find all technical guidelines for defence research projects."

**Expected System Flow**:
1. Classify documents as "technical" + "guideline"
2. Handle mix of English + Hindi documents
3. Retrieve and rank by relevance
4. Extract key technical requirements

**Test Steps**:
1. Verify correct document types retrieved
2. Verify multilingual documents handled
3. Verify retrieved docs are relevant
4. Verify technical content extracted correctly

**Success Criteria**:
- ✓ Correct doc types retrieved
- ✓ Language barrier not blocking retrieval
- ✓ High relevance (P@10 ≥0.75)
- ✓ Technical details extracted

**Pass/Fail**: PASS if 3/4 criteria met

---

### Scenario 5: Edge Case Handling (Complex Document)
**User**: QA Tester  
**Query**: (System searches for document with tables, multiple formats)

**Expected System Flow**:
1. OCR complex PDF with tables + images
2. Extract tabular financial data
3. Handle format variations
4. Retrieve in response to complex query

**Test Steps**:
1. Verify document OCR'd correctly (90%+ accuracy)
2. Verify tables extracted (structure + values)
3. Verify financial data retrieved correctly
4. Verify system handles format variations

**Success Criteria**:
- ✓ OCR ≥90% accuracy
- ✓ Tables extracted
- ✓ Values correct
- ✓ Format handling transparent

**Pass/Fail**: PASS if 3/4 criteria met

---

## Phase 2 UAT Test Cases (Detailed)

### Test Case UAT-P2-001: Query Processing Latency
```
Title: System response time within acceptable bounds
Scenario: User submits query, measures response time
Expected Result: <2 seconds p95 latency
Acceptance Criteria: 
  - Single query: <2s
  - 10 concurrent queries: <3s p95
  - 50 concurrent queries: <5s p95
Data: 50,000 documents indexed
Frequency: Phase 2 UAT week 1
Owner: QA Team
```

### Test Case UAT-P2-002: Document Retrieval Accuracy
```
Title: Retrieved documents match user intent
Scenario: User queries for financial reports
Expected Result: Top 5 results all financial documents
Acceptance Criteria:
  - Precision@5 ≥0.80
  - Precision@10 ≥0.75
  - No irrelevant documents in top 5
Data: 100 diverse queries
Frequency: Phase 2 UAT week 1-2
Owner: QA Team
```

### Test Case UAT-P2-003: NER Accuracy on Real Documents
```
Title: Entity extraction works on actual defence documents
Scenario: System extracts authorities, amounts, dates from procurement notice
Expected Result: All major entities correctly identified
Acceptance Criteria:
  - Authority extraction F1 ≥0.80
  - Amount extraction F1 ≥0.75
  - Date extraction F1 ≥0.75
Data: 20 procurement documents
Frequency: Phase 2 UAT week 2
Owner: QA Team
```

### Test Case UAT-P2-004: RAG Answer Hallucination Check
```
Title: LLM-generated answers factually correct
Scenario: User query → RAG pipeline → LLM answer
Expected Result: Answer matches document facts; no hallucination
Acceptance Criteria:
  - Zero hallucinations in 50 test queries
  - Faithfulness ≥0.90
  - All claims cite source documents
Data: 50 benchmark queries
Frequency: Phase 2 UAT week 2-3
Owner: Domain Expert + QA
```

### Test Case UAT-P2-005: System Error Handling
```
Title: System handles errors gracefully
Scenario: Malformed query, missing documents, network errors
Expected Result: User-friendly error messages, system continues
Acceptance Criteria:
  - No crashes on malformed input
  - Graceful timeout handling (>10s queries)
  - User informed of errors
Frequency: Phase 2 UAT week 3
Owner: QA Team
```

---

## Phase 3 UAT Test Scenarios (10 Real-World Scenarios)

### Scenario 1-5: (Same as Phase 2, validate continued accuracy)

### Scenario 6: Cross-document Financial Analysis
**User**: Financial Auditor  
**Query**: "Reconcile defence expenditure across budget docs, audit reports, and parliamentary Q&A"

**Expected System**: 
- Multi-doc retrieval + comparison
- Identify discrepancies
- Provide audit trail

**Success Criteria**: Identify 90%+ of actual discrepancies

---

### Scenario 7: Temporal Analysis
**User**: Policy Analyst  
**Query**: "Show evolution of defence procurement policy over past 5 years. What changed?"

**Expected System**:
- Retrieve policy documents across time
- Identify changes + amendments
- Version comparison

**Success Criteria**: Timeline accurate, all major changes captured

---

### Scenario 8: Regulatory Compliance Check
**User**: Compliance Officer  
**Query**: "Which defence projects require environmental clearance? What's the approval process?"

**Expected System**:
- Cross-reference regulations + projects
- Extract requirements
- Provide compliance checklist

**Success Criteria**: Accuracy ≥90%, completeness ≥85%

---

### Scenario 9: Multilingual Search
**User**: Hindi-speaking DRDO officer  
**Query**: "रक्षा बजट 2023-24" (Defence budget 2023-24 in Hindi)

**Expected System**:
- Handle Hindi input
- Translate/cross-match English documents
- Retrieve relevant results

**Success Criteria**: Results same quality as English query

---

### Scenario 10: Load Testing + Concurrent Users
**User**: All Ministry of Defence analysts simultaneously  
**Query**: 100 concurrent users, 50 diverse queries

**Expected System**:
- Handle 100 concurrent requests
- <1 second response time (p95)
- Zero dropped requests
- Zero data corruption

**Success Criteria**: All requests processed, <1s p95 latency, zero errors

---

## Phase 4 UAT Test Scenarios (15 Scenarios)

Phases 3 scenarios + 5 additional:
- Advanced analytics (e.g., "Predict defence spending trends")
- Multi-modal search (image search for equipment)
- Integration with external systems (Parliament data, CAG reports)
- Security validation (access control, audit logging)
- Disaster recovery drill (system recovery from failure)

---

## UAT Success Criteria (Cumulative)

| Phase | Overall Success Rate | Critical Issues | Major Issues | Blockers |
|-------|---------------------|-----------------|-------------|----------|
| **Phase 2** | ≥80% tests pass | Max 1 | Max 3 | Zero |
| **Phase 3** | ≥95% tests pass | Zero | Max 2 | Zero |
| **Phase 4** | ≥99% tests pass | Zero | Zero | Zero |

**Definition**:
- **Test Pass**: All acceptance criteria met
- **Critical Issue**: Blocks deployment (e.g., hallucination rate >10%)
- **Major Issue**: Needs fix but workaround available
- **Blocker**: Complete blocker to phase transition

---

## UAT Execution Process

### Phase 2 UAT Execution (3 weeks)

**Week 1: Setup**
- Standup 5-10 MoD analyst users in UAT environment
- 2-hour training on system (how to query, interpret results)
- Provide test scenario documents + expected answers
- Set up issue tracking (Jira/Asana)

**Week 2: Testing**
- Users execute 5 scenarios (1 per day)
- Each scenario: 2-3 hour session
- QA documents results, screenshots, issues
- Daily sync to address blockers

**Week 3: Analysis**
- Aggregate results
- Categorize issues (critical vs. major vs. minor)
- Root cause analysis for failures
- Prepare recommendations

**Handoff**:
- Pass UAT → plan Phase 3 start
- Fail UAT → create issue remediation plan (1-2 weeks), retry

---

## UAT Environment Setup

**Separate from production**:
- Clone golden dataset (960 documents)
- Fresh vector DB
- Isolated API servers
- User access controlled (VPN)

**No data leakage**:
- Use sanitized test data only
- No real classified information
- Clear audit trail (who accessed what)

---

## Stakeholder Involvement

### Phase 2 UAT Stakeholders
- **Ministry of Defence** (3-5 analysts)
  - Test queries reflecting real work
  - Provide feedback on usability
- **DRDO** (1-2 engineers)
  - Validate technical correctness
  - Test domain-specific scenarios
- **Project Team** (2-3)
  - Support, troubleshoot, document

### Phase 3 UAT Stakeholders
- **MoD Finance Division** (5 auditors)
  - Validate financial analysis accuracy
- **MoD Procurement** (3 officers)
  - Validate procurement workflows
- **DRDO Research** (3 scientists)
  - Validate technical content accuracy
- **Project Team** (4-5)
  - Support, troubleshoot, analytics

### Phase 4 UAT Stakeholders
- **All Phase 3 stakeholders** (expand 2-3x)
- **Additional**: IT security team, compliance officer
- **Extended pilot**: 30-50 users across MoD

---

## UAT Metrics & Reporting

### Daily Report (UAT week 1-3)
- Tests run today (count)
- Pass/fail breakdown (%)
- Critical issues identified
- Blockers / risks

### Weekly Report (UAT week 1, 2, 3)
- Overall progress (% of scenarios tested)
- Issue breakdown (critical/major/minor)
- User feedback summary
- Recommendations

### Final Report (End of UAT)
- Pass/fail per scenario
- Overall success rate (%)
- Issue resolution (fixed/deferred/documented)
- Recommendations for next phase
- Lessons learned

---

## UAT Sign-Off

### Phase 2 UAT Sign-Off
**Approval from**:
- Ministry of Defence representative (business owner)
- DRDO technical lead
- Project Manager
- QA Lead

**Gates**:
- ≥80% tests pass
- All critical issues resolved
- All blockers removed
- Stakeholder sign-off obtained

**If pass**: Phase 3 begins (4 weeks after Phase 2 end)  
**If fail**: 2-week remediation + retry UAT

---

## Risk Mitigation in UAT

### Risk: Users unfamiliar with AI systems
**Mitigation**: 2-hour hands-on training + demo sessions

### Risk: UAT environment differs from production
**Mitigation**: Use prod-like env (same infra, data sampling)

### Risk: Limited time for testing
**Mitigation**: Pre-test automation for regression; UAT focuses on new scenarios

### Risk: Cultural/organizational resistance
**Mitigation**: Executive sponsor involvement, demonstrable value in early scenarios

---

## UAT Learnings & Continuous Improvement

**Post-UAT analysis**:
- Analyze all failures → root cause
- Identify common issues (training? usability? accuracy?)
- Create action items for improvement
- Document lessons for next phase

**Example**: Phase 2 → Phase 3
- If 30% of users struggled with query formulation → add query templates in Phase 3
- If 25% of retrievals failed for procurement queries → improve retrieval for that category
- If latency exceeded SLA → prioritize performance optimization

---

## UAT Timeline Integration

```
Phase 2: Implementation
├─ Weeks 1-14: Development
├─ Weeks 15-16: UAT
│  ├─ Week 1: Setup + training
│  ├─ Week 2: Testing scenarios 1-5
│  └─ Week 3: Analysis + sign-off
│
Phase 3: Implementation
├─ Weeks 1-14: Development + UAT prep
├─ Weeks 15-17: UAT (3-4 weeks, 10 scenarios)
│
Phase 4: Implementation
├─ Weeks 1-18: Development + UAT prep
└─ Weeks 19-22: UAT (4 weeks, 15 scenarios + load testing)
```

---

**Document Owner**: QA Lead + Project Manager  
**Next Review**: August 31, 2026 (Finalize Phase 2 UAT Plan)  
**Approval**: [Pending Phase 2 Project Kickoff]

---

*UAT is proof-of-concept with real stakeholders. Schedule early; don't rush.*
