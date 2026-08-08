# order_history

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C-** (56.9/100)

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
| Provenance | 45.0/100 | No owners assigned (-30) |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 5 fields |
| Lineage | 69.5/100 | 71 upstream sources |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract
- Verify upstream sources are connected
- Confirm downstream consumers are tracked