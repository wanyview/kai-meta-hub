# DATMScore: A Four-Dimensional Knowledge Evaluation System

## Overview

DATMScore is a comprehensive framework for evaluating knowledge value in the AI era. It assesses knowledge from four essential dimensions:

| Dimension | Chinese | Description | Weight |
|-----------|---------|-------------|--------|
| **Truth** | 真 | Scientific accuracy and factual reliability | 25% |
| **Goodness** | 善 | Practical utility and application value | 25% |
| **Beauty** | 美 | Aesthetic quality and expression elegance | 25% |
| **Intelligence** | 智 | Deep insights and cognitive enhancement | 25% |

---

## The Four Dimensions

### 1. Truth (T) - Scientific Validity

- **Factual accuracy**: Claims must be factually correct
- **Source reliability**: Citations must be from credible sources
- **Methodology**: Research methods must be sound
- **Reproducibility**: Results should be reproducible

**Scoring criteria:**
- 90-100: Peer-reviewed, widely accepted
- 70-89: Well-sourced, minor uncertainties
- 50-69: Partially supported by evidence
- Below 50: Unsupported or contradicted

### 2. Goodness (G) - Practical Value

- **Problem solving**: Does it solve real problems?
- **Application potential**: Is it practically applicable?
- **Utility**: How useful is it to the target audience?
- **Impact**: What positive change does it drive?

**Scoring criteria:**
- 90-100: Immediately applicable, high impact
- 70-89: Useful with some adaptation
- 50-69: Theoretically useful, needs validation
- Below 50: Limited practical application

### 3. Beauty (A) - Aesthetic Quality

- **Clarity**: Is the expression clear and understandable?
- **Elegance**: Is the presentation aesthetically pleasing?
- **Engagement**: Does it engage the reader effectively?
- **Memorability**: Is it memorable and impactful?

**Scoring criteria:**
- 90-100: Masterful prose, highly engaging
- 70-89: Well-written, clear structure
- 50-69: Adequate but could be improved
- Below 50: Difficult to follow

### 4. Intelligence (I) - Wisdom and Insight

- **Depth**: Does it provide deep understanding?
- **Novelty**: Are there original insights?
- **Transferability**: Can insights apply to other contexts?
- **Cognitive enhancement**: Does it elevate thinking?

**Scoring criteria:**
- 90-100: Paradigm-shifting insights
- 70-89: Valuable new perspectives
- 50-69: Some useful observations
- Below 50: Conventional thinking

---

## Overall Score Calculation

```
DATMScore = (Truth + Goodness + Beauty + Intelligence) / 4
```

### Score Interpretation

| Score Range | Classification | Description |
|-------------|----------------|-------------|
| 90-100 | 🌟 Legendary | Exceptional, groundbreaking |
| 80-89 | 💎 Premium | Highly valuable, recommended |
| 70-79 | ✅ Good | Solid, useful knowledge |
| 60-69 | 🔶 Average | Decent, some value |
| Below 60 | ⚠️ Needs Work | Requires improvement |

---

## Application in Knowledge Capsules

Each knowledge capsule receives a DATMScore:

```python
@dataclass
class KnowledgeCapsule:
    title: str
    content: str
    datm_score: DATMScore  # Four-dimensional score
    
    @property
    def overall(self) -> float:
        return self.datm_score.overall
```

### Promotion Criteria

Capsules with `score.overall >= 70` are automatically promoted to wider distribution.

---

## Benefits of DATMScore

1. **Quality Assurance**: Ensures only valuable knowledge spreads
2. **Multi-dimensional View**: Avoids single-metric limitations
3. **Continuous Improvement**: Encourages iteration
4. **Comparative Analysis**: Enables meaningful comparisons
5. **Knowledge Graph**: Supports intelligent recommendations

---

## Future Enhancements

- **Dynamic Scoring**: Scores update based on feedback
- **Personalization**: Adapt weights to user preferences
- **Temporal Factors**: Consider knowledge时效性
- **Cross-domain**: Normalize scores across fields

---

*DATMScore - Making Knowledge Evaluation Scientific and Comprehensive*
