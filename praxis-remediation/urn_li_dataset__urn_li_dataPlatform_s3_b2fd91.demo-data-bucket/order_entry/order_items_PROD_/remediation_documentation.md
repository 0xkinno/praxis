# order_items

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C-** (55.8/100)

## Overview



**Platform:** s3
**Domain:** Unassigned
**Owners:** 

## Schema

| Column | Type | Description |
|--------|------|-------------|
| order_id | NUMBER | None |
| line_item_id | NUMBER | None |
| product_id | NUMBER | None |
| unit_price | NUMBER | None |
| quantity | NUMBER | None |
| dispatch_date | STRING | None |
| return_date | STRING | None |
| gift_wrap | STRING | None |
| condition | STRING | None |
| supplier_id | NUMBER | None |
| estimated_delivery | STRING | None |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 0.0/100 | No owners assigned (-35) |
| Integrity | 75.0/100 | No quality assertions defined (-25) |
| Stability | 90.0/100 | Schema has 11 fields |
| Lineage | 87.3/100 | 2 upstream sources |
| Adoption | 45.0/100 | No queries recorded in the last month (-35) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms