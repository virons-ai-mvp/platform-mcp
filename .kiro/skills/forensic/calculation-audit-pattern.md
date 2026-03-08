# Calculation Audit Pattern

**Name**: calculation-audit-pattern
**Description**: Mandatory write_audit() pattern for BaFin AT 8.1 compliance. MUST be called BEFORE forensic_flags write.
**Namespace**: forensic
**User-invocable**: false

## The Pattern (Non-Negotiable)

```python
from virons_common import write_audit

async def calculate_and_flag(inputs: CalculationInputs, db: AsyncSession) -> CalculationResult:
    # 1. Perform calculation
    result = _compute(inputs)

    # 2. Write audit FIRST
    await write_audit(
        db=db,
        rule_id="BEN_001",
        input_values=inputs.model_dump(),
        formula_applied="M = -4.84 + 0.920*DSRI + ...",
        result_value=float(result.score),
        threshold_used=-1.78,
        flag_triggered=result.score > -1.78,
        source_doc_hash=inputs.doc_hash,
        academic_ref="Beneish (1999)",
    )

    # 3. Write flag AFTER audit
    if result.score > -1.78:
        await db.execute(
            insert(ForensicFlag).values(
                entity_id=inputs.entity_id,
                rule_id="BEN_001",
                score=result.score,
            )
        )
        await db.commit()

    return result
```

## write_audit() Signature

```python
async def write_audit(
    db: AsyncSession,
    rule_id: str,
    input_values: dict,
    formula_applied: str,
    result_value: float,
    threshold_used: float | None,
    flag_triggered: bool,
    source_doc_hash: str,
    academic_ref: str | None = None,
) -> UUID:
    pass
```
