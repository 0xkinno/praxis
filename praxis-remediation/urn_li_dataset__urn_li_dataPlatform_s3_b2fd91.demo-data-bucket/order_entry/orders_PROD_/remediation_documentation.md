# orders

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **D** (50.4/100)

## Overview



**Platform:** s3
**Domain:** Unassigned
**Owners:** 

## Schema

| Column | Type | Description |
|--------|------|-------------|
| order_id | NUMBER | None |
| order_date | STRING | None |
| order_mode | STRING | None |
| customer_id | NUMBER | None |
| order_status | NUMBER | None |
| order_total | NUMBER | None |
| sales_rep_id | NUMBER | None |
| promotion_id | NUMBER | None |
| warehouse_id | NUMBER | None |
| delivery_type | STRING | None |
| cost_of_delivery | NUMBER | None |
| wait_till_complete_yn | STRING | None |
| billing_address_id | NUMBER | None |
| delivery_address_id | NUMBER | None |
| payment_method_code | STRING | None |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 10.0/100 | No owners assigned (-30) |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 15 fields |
| Lineage | 84.5/100 | 2 upstream sources |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract