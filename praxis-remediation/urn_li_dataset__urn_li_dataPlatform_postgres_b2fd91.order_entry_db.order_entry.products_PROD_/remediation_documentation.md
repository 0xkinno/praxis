# products

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C-** (57.8/100)

## Overview



**Platform:** postgres
**Domain:** Unassigned
**Owners:** 

## Schema

| Column | Type | Description |
|--------|------|-------------|
| product_id | NUMBER | None |
| product_name | STRING | None |
| product_description | STRING | None |
| category_id | NUMBER | None |
| weight_class | NUMBER | None |
| warranty_period | STRING | None |
| supplier_id | NUMBER | None |
| product_status | STRING | None |
| list_price | NUMBER | None |
| min_price | NUMBER | None |
| catalog_url | STRING | None |
| date_added | STRING | None |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 0.0/100 | No owners assigned (-35) |
| Integrity | 75.0/100 | No quality assertions defined (-25) |
| Stability | 90.0/100 | Schema has 12 fields |
| Lineage | 100.0/100 | Root source dataset (no upstream, feeds downstream consumers) |
| Adoption | 45.0/100 | No queries recorded in the last month (-35) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms