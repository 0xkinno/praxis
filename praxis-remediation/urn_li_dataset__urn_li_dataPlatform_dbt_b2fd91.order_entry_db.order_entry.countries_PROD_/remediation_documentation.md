# countries

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **B-** (70.4/100)

## Overview

Reference table for country information

**Platform:** dbt
**Domain:** Data Platform Team
**Owners:** b2fd91.ORG_DATA_PLATFORM, b2fd91.EMP006

## Schema

| Column | Type | Description |
|--------|------|-------------|
| country_id | NUMBER | Unique identifier for the country |
| country_name | STRING | Name of the country |
| country_code | STRING | ISO two-letter country code |
| nls_territory | STRING | NLS territory setting for localization |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 90.0/100 | 2 owners assigned |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 4 fields |
| Lineage | 84.5/100 | 5 upstream sources |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract