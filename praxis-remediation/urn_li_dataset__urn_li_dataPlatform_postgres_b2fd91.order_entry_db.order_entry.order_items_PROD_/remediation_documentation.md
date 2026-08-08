# order_items

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **D** (48.2/100)

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
| Provenance | 10.0/100 | No owners assigned (-30) |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 11 fields |
| Lineage | 70.0/100 | No upstream sources found (-30) |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract