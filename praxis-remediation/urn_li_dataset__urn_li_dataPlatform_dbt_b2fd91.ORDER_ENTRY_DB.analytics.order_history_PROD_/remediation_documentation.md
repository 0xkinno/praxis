# order_history

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C+** (65.0/100)

## Overview

Incremental table containing all historical order information

**Platform:** dbt
**Domain:** E-Commerce
**Owners:** 

## Schema

| Column | Type | Description |
|--------|------|-------------|
| order_id | NUMBER | None |
| customer_id | NUMBER | None |
| order_status | NUMBER | None |
| order_total | NUMBER | None |
| as_of_date | DATE | None |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 35.0/100 | No owners assigned (-35) |
| Integrity | 75.0/100 | No quality assertions defined (-25) |
| Stability | 90.0/100 | Schema has 5 fields |
| Lineage | 90.0/100 | 71 upstream sources |
| Adoption | 45.0/100 | No queries recorded in the last month (-35) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms