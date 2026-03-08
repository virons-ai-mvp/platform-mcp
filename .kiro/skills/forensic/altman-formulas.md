# Altman Z-Score Formulas

**Name**: altman-formulas
**Description**: Altman Z-Score variants ALT_001–ALT_003 with company-type selection.
**Namespace**: forensic
**User-invocable**: false

**Reference**: Altman, E.I. (1968). "Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy." *Journal of Finance*, 23(4), 589–609.

## Variant Selection

```python
def select_variant(company: Company) -> str:
    if company.is_public and company.is_manufacturing:
        return "ALT_001"
    elif not company.is_public:
        return "ALT_002"
    else:
        return "ALT_003"
```

## ALT_001 — Original Z-Score (Public Manufacturing)

```
Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5
```

**Thresholds**: Z > 2.99 → safe | 1.81 < Z ≤ 2.99 → grey | Z ≤ 1.81 → distress

## ALT_002 — Z'-Score (Private Firms)

```
Z' = 0.717*X1 + 0.847*X2 + 3.107*X3 + 0.420*X4 + 0.998*X5
```

**Thresholds**: Z' > 2.9 → safe | 1.23 < Z' ≤ 2.9 → grey | Z' ≤ 1.23 → distress

## ALT_003 — Z''-Score (Non-Manufacturing)

```
Z'' = 6.56*X1 + 3.26*X2 + 6.72*X3 + 1.05*X4
```

**Thresholds**: Z'' > 2.6 → safe | 1.1 < Z'' ≤ 2.6 → grey | Z'' ≤ 1.1 → distress
