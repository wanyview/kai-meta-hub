# DATM Scoring System: Deep Dive

## Introduction to DATM

The Decentralized Autonomous Trust Mechanism (DATM) is the quality assurance backbone of the Knowledge Capsule system. Just as peer review validates academic papers, DATM validates knowledge capsules through a decentralized verification process.

## The Four Pillars of DATM

### 1. Accuracy (30%)

Does the content contain correct information?

**Evaluation Criteria**:
- Factual correctness
- Source credibility
- Logical consistency
- Up-to-date information

**Scoring Examples**:
- 1.0: Multiple authoritative sources confirm
- 0.7: Single authoritative source
- 0.5: Unverified claims
- 0.0: Demonstrably false

### 2. Depth (25%)

How thoroughly is the topic covered?

**Evaluation Criteria**:
- Comprehensiveness of explanation
- Background context provided
- Edge cases addressed
- Nuances explored

**Scoring Examples**:
- 1.0: Comprehensive coverage with examples
- 0.7: Good coverage, minor gaps
- 0.5: Surface-level treatment
- 0.0: Barely addresses topic

### 3. Novelty (25%)

How original is the insight?

**Evaluation Criteria**:
- Unique perspective
- New connections made
- Original research
- Fresh examples

**Scoring Examples**:
- 1.0: Novel framework or insight
- 0.7: Good synthesis of existing ideas
- 0.5: Standard treatment
- 0.0: Completely derivative

### 4. Utility (20%)

How practically applicable is the knowledge?

**Evaluation Criteria**:
- Actionable guidance
- Reproducible results
- Clear next steps
- Relevant examples

**Scoring Examples**:
- 1.0: Immediately applicable with clear steps
- 0.7: Useful with some adaptation
- 0.5: Interesting but impractical
- 0.0: No practical value

## The Scoring Process

### Phase 1: Initial Submission
```
Creator submits capsule → System calculates preliminary score
```

### Phase 2: Community Validation
```
Validators review → Multi-sig verification → Score adjustment
```

### Phase 3: Automatic Promotion
```
Score ≥ 0.7 → Auto-promoted to network
Score < 0.5 → Flagged for review
```

## Validation Network

### Validator Roles

| Role | Responsibility | Reward |
|------|---------------|--------|
| Expert Validator | Domain-specific review | Higher tier tokens |
| General Validator | Cross-domain review | Standard tokens |
| AI Validator | Automated fact-checking | Micro-rewards |

### Consensus Mechanism
- Minimum 5 validators required
- Outlier scores filtered
- Final score = median of valid scores

## Implementation Example

```python
def calculate_datm_score(capsule: Capsule, validators: List[Validator]) -> float:
    accuracy = avg([v.accuracy for v in validators])
    depth = avg([v.depth for v in validators])
    novelty = avg([v.novelty for v in validators])
    utility = avg([v.utility for v in validators])
    
    return (
        accuracy * 0.30 +
        depth * 0.25 +
        novelty * 0.25 +
        utility * 0.20
    )
```

## Trust and Security

### Preventing Manipulation
- Validator identity verification
- Reputation-weighted scoring
- Anomaly detection
- Slash for malicious behavior

### Transparency
- All validation records on-chain
- Appeal process available
- Regular audits

---

**Learn More**:
- [Knowledge Capsule System](./knowledge-capsules-en.md)
- [Future of Knowledge Capsules](./kai_meta_hub_article_03-en.md)
