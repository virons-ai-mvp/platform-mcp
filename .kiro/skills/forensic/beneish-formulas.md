# Beneish M-Score Formulas

**Name**: beneish-formulas
**Description**: Beneish M-Score formulas BEN_001–BEN_008 with thresholds.
**Namespace**: forensic
**User-invocable**: false

**Reference**: Beneish, M.D. (1999). "The Detection of Earnings Manipulation." *Financial Analysts Journal*, 55(5), 24–36.

**Threshold**: M-Score > -1.78 → likely manipulator

## Indices

### BEN_001 — DSRI (Days Sales in Receivables Index)
```
DSRI = (Receivables_t / Sales_t) / (Receivables_{t-1} / Sales_{t-1})
```
- Threshold: DSRI > 1.465 → flag
- Weight: +0.920

### BEN_002 — GMI (Gross Margin Index)
```
GMI = [(Sales_{t-1} - COGS_{t-1}) / Sales_{t-1}] / [(Sales_t - COGS_t) / Sales_t]
```
- Threshold: GMI > 1.193 → flag
- Weight: +0.528

### BEN_003 — AQI (Asset Quality Index)
```
AQI = [1 - (CA_t + PPE_t) / TA_t] / [1 - (CA_{t-1} + PPE_{t-1}) / TA_{t-1}]
```
- Threshold: AQI > 1.254 → flag
- Weight: +0.404

### BEN_004 — SGI (Sales Growth Index)
```
SGI = Sales_t / Sales_{t-1}
```
- Threshold: SGI > 1.607 → flag
- Weight: +0.892

## M-Score Formula

```python
M = (-4.84
     + 0.920 * DSRI
     + 0.528 * GMI
     + 0.404 * AQI
     + 0.892 * SGI
     + 0.115 * DEPI
     - 0.172 * SGAI
     + 4.679 * TATA
     - 0.327 * LVGI)
```
