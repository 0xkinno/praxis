# Orders By Day

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C+** (65.2/100)

## Overview



**Platform:** tableau
**Domain:** Unassigned
**Owners:** b2fd91.brock1@example.com

## Schema

| Column | Type | Description |
|--------|------|-------------|
| ORDER_COUNT | NUMBER |  |
| TOTAL_SALES | NUMBER |  |
| ORDER_DATE | TIME |  |
| Orders By Day And Category | ARRAY |  |
| CATEGORY_NAME | STRING |  |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 30.0/100 | Single owner, no backup (-5) |
| Integrity | 75.0/100 | No quality assertions defined (-25) |
| Stability | 90.0/100 | Schema has 5 fields |
| Lineage | 100.0/100 | 72 upstream sources |
| Adoption | 45.0/100 | No queries recorded in the last month (-35) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms