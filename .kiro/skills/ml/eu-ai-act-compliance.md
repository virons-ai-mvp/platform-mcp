# EU AI Act Compliance

**Name**: eu-ai-act-compliance
**Description**: EU AI Act Art 13 model card requirements for high-risk AI systems.
**Namespace**: ml
**User-invocable**: false

**Regulation**: EU AI Act (2024/1689), Annex III — High-Risk AI Systems

**Affected**: `anomaly-detector` (:9405), `grandmaster-service` (:9421)

## Model Card Template

File: `ml/model-cards/{service-name}.md`

```markdown
# Model Card: {service-name}

## EU AI Act Classification
- Risk Level: HIGH-RISK (Annex III)
- Use Case: Fraud detection / financial risk assessment

## Model Information
- Model Type: IsolationForest k=5 Ensemble
- Version: {version}
- Training Data: {description, date range}
- Feature Count: 12

## Performance Metrics
- Precision: {value}
- Recall: {value}
- F1 Score: {value}
- False Positive Rate: {value}

## Human Oversight Mechanism
- Scores above {threshold} routed to human review
- Override capability: yes (with audit trail)

## Monitoring
- Feature drift monitored via {method}
- Retraining trigger: {condition}
```

## Human Oversight Gate

```python
HUMAN_REVIEW_THRESHOLD = 0.75

async def route_prediction(score: float, entity_id: str, queue: ReviewQueue):
    if score >= HUMAN_REVIEW_THRESHOLD:
        await queue.enqueue(
            entity_id=entity_id,
            score=score,
            reason="EU AI Act Art 14 — human oversight required",
        )
        return PredictionResult(status="pending_review", score=score)
    return PredictionResult(status="auto_processed", score=score)
```
