# customers

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C-** (57.8/100)

## Overview



**Platform:** postgres
**Domain:** Unassigned
**Owners:** 

## Schema

| Column | Type | Description |
|--------|------|-------------|
| customer_id | NUMBER | None |
| cust_first_name | STRING | None |
| cust_last_name | STRING | None |
| nls_language | STRING | None |
| nls_territory | STRING | None |
| credit_limit | NUMBER | None |
| cust_email | STRING | None |
| account_mgr_id | NUMBER | None |
| customer_since | STRING | None |
| customer_class | STRING | None |
| suggestions | STRING | None |
| dob | STRING | None |
| mailshot | NUMBER | None |
| partner_mailshot | NUMBER | None |
| phone_number | STRING | None |
| address_line1 | STRING | None |
| address_line2 | STRING | None |
| address_line3 | STRING | None |
| town_city | STRING | None |
| country_id | NUMBER | None |
| zipcode | NUMBER | None |
| region_id | NUMBER | None |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 0.0/100 | No owners assigned (-35) |
| Integrity | 75.0/100 | No quality assertions defined (-25) |
| Stability | 90.0/100 | Schema has 22 fields |
| Lineage | 100.0/100 | Root source dataset (no upstream, feeds downstream consumers) |
| Adoption | 45.0/100 | No queries recorded in the last month (-35) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms