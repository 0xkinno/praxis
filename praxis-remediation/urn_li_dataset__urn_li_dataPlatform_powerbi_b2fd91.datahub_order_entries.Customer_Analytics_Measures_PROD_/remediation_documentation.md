# Customer Analytics Measures

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C+** (67.5/100)

## Overview



**Platform:** powerbi
**Domain:** Unassigned
**Owners:** 

## Schema

| Column | Type | Description |
|--------|------|-------------|
| Value | STRING | None |
| Customer LTV | NULL | 
AVERAGEX(
    VALUES('ORDER_DETAILS'[customer_id]),
    CALCULATE(SUM('ORDER_DETAILS'[order_total]))
) |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 36.0/100 | No owners assigned (-30) |
| Integrity | 75.0/100 | No quality assertions defined (-25) |
| Stability | 90.0/100 | Schema has 2 fields |
| Lineage | 100.0/100 | 71 upstream sources |
| Adoption | 50.0/100 | No queries recorded in the last month (-30) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms