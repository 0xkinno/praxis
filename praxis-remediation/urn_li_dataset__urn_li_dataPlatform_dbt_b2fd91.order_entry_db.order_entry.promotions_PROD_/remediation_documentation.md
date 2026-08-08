# promotions

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **B-** (72.9/100)

## Overview

Contains information about marketing promotions and campaigns

**Platform:** dbt
**Domain:** Data Platform Team
**Owners:** b2fd91.ORG_DATA_PLATFORM, b2fd91.EMP006

## Schema

| Column | Type | Description |
|--------|------|-------------|
| promotion_id | NUMBER | Unique identifier for the promotion |
| promotion_name | STRING | Name of the marketing promotion |
| promotion_start_date | STRING | Starting date of the promotion |
| promotion_end_date | STRING | Ending date of the promotion |
| promotion_description | STRING | Detailed description of the promotion |
| promotion_cost | NUMBER | Budgeted cost of running the promotion |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 100.0/100 | 2 owners assigned |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 6 fields |
| Lineage | 84.5/100 | 8 upstream sources |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract