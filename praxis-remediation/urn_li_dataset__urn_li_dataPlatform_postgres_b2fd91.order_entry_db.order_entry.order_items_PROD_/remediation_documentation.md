# order_items

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C** (62.2/100)

## Overview



**Platform:** postgres
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
| Provenance | 15.0/100 | No owners assigned (-30) |
| Integrity | 75.0/100 | No quality assertions defined (-25) |
| Stability | 90.0/100 | Schema has 11 fields |
| Lineage | 100.0/100 | Root source dataset (no upstream, feeds downstream consumers) |
| Adoption | 50.0/100 | No queries recorded in the last month (-30) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms