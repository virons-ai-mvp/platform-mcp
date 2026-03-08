# IsolationForest k=5 Ensemble

**Name**: iforest-ensemble
**Description**: k=5 IsolationForest ensemble with 12-feature vector for anomaly detection.
**Namespace**: ml
**User-invocable**: false

## 12-Feature Vector

```python
FEATURE_NAMES = [
    "dsri", "gmi", "aqi", "sgi", "depi", "sgai", "lvgi", "tata",
    "altman_z", "qoe_score", "narrative_score", "governance_score",
]
```

## Ensemble Implementation

```python
from sklearn.ensemble import IsolationForest
import numpy as np

K = 5
CONTAMINATION = 0.05
RANDOM_SEEDS = [42, 137, 271, 314, 999]

def build_ensemble() -> list[IsolationForest]:
    return [
        IsolationForest(
            n_estimators=100,
            contamination=CONTAMINATION,
            random_state=seed,
        )
        for seed in RANDOM_SEEDS
    ]

def predict_ensemble(models: list[IsolationForest], features: np.ndarray) -> float:
    scores = []
    for model in models:
        raw = model.decision_function(features)[0]
        score = 1.0 / (1.0 + np.exp(raw * 5))
        scores.append(score)
    return float(np.mean(scores))
```

## ML Gate (Always Apply)

```python
def apply_ml_gate(ml_score: float, deterministic_flags: list) -> float:
    return ml_score if len(deterministic_flags) >= 1 else 0.0
```

## Nonlinear Fusion

```python
import math

def fuse_scores(s_iforest: float, s_beneish: float, s_altman: float) -> float:
    return 1.0 - math.prod(1.0 - s for s in [s_iforest, s_beneish, s_altman])
```
