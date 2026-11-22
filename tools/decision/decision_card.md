# Decision card: {{company}} ({{ticker}}) · {{decision_date}}

{{banner}}

| Card | Value |
|---|---|
| Card version | {{card_version}} · worksheet {{worksheet_version}} |
| Price used | {{price_line}} |
| Stages feeding this card | 2 hard filters · 3 signals · 4 deep dive ({{deep_dive}}) · 5 valuation worksheet |
| **Rule output** | {{gate_headline}} |
| Review date | **{{review_date}}** |
| Paper-call ids (stage 7) | {{paper_call_ids}} |

## 1. Thesis in one line
{{thesis}}

## 2. Variant view (what we believe that the price does not, and why we could know it)
{{variant_view}}

## 3. What the price implies (stage 5)
{{price_implies}}

## 4. Gates and flags
### 4.1 Stage 2: hard filters (non-overridable) and graded flags
{{stage2}}

### 4.2 Stage 3: signals
{{stage3}}

### 4.3 Stage 4: deep-dive soft flags and override log
{{stage4}}

## 5. Probabilities (5 years), with base rates alongside
{{probabilities}}

## 6. Expected value
{{expected_value}}

## 7. Position size (written rule)
{{sizing}}

## 8. Kill criteria (each one dated and checkable)
{{kill_criteria}}

## 9. Pre-mortem ("it is {{premortem_year}} and this went badly; why?")
{{pre_mortem}}

## 10. Gate log (how the rule output was reached)
{{gate_log}}

---
*Research, not SEBI-registered advice. Every probability on this card is also written as a dated paper call so it is scored later (Brier vs base rate). Template: `tools/decision/decision_card.md`; generator: `tools/decision/decision_card.py`.*
