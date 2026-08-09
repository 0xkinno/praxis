# Promotions

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C+** (68.5/100)

## Overview



**Platform:** tableau
**Domain:** Unassigned
**Owners:** b2fd91.brock1@example.com

## Schema

| Column | Type | Description |
|--------|------|-------------|
| ORDERS_WITH_PROMOTION | NUMBER |  |
| AVERAGE_ORDER_VALUE | NUMBER |  |
| TOTAL_REVENUE | NUMBER |  |
| PROMOTION_NAME | STRING |  |
| Promotions | ARRAY |  |
| AVERAGE_DISCOUNT_PERCENT | NUMBER |  |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 40.0/100 | Single owner, no backup (-5) |
| Integrity | 75.0/100 | No quality assertions defined (-25) |
| Stability | 90.0/100 | Schema has 6 fields |
| Lineage | 100.0/100 | 72 upstream sources |
| Adoption | 50.0/100 | No queries recorded in the last month (-30) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms