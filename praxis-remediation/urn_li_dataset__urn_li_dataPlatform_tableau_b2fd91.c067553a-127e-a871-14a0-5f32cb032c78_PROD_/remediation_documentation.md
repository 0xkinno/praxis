# Order Mode

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C-** (55.4/100)

## Overview



**Platform:** tableau
**Domain:** Unassigned
**Owners:** b2fd91.brock1@example.com

## Schema

| Column | Type | Description |
|--------|------|-------------|
| AVERAGE_ORDER_VALUE | NUMBER |  |
| TOTAL_REVENUE | NUMBER |  |
| ORDER_COUNT | NUMBER |  |
| Order Mode | ARRAY |  |
| ORDER_MODE | STRING |  |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 30.0/100 | Single owner, no backup (-10) |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 5 fields |
| Lineage | 84.5/100 | 72 upstream sources |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract