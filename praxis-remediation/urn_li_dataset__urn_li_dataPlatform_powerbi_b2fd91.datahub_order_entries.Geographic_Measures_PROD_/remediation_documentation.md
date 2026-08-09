# Geographic Measures

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C** (62.1/100)

## Overview



**Platform:** powerbi
**Domain:** Unassigned
**Owners:** 

## Schema

| Column | Type | Description |
|--------|------|-------------|
| Value | STRING | None |
| Revenue by Country | NULL | CALCULATE([Total Revenue], VALUES('ORDER_DETAILS'[shipping_country])) |
| Domestic Sales | NULL | CALCULATE([Total Revenue], 'ORDER_DETAILS'[shipping_country] = "United States") |
| International Sales | NULL | [Total Revenue] - [Domestic Sales] |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 25.0/100 | No owners assigned (-35) |
| Integrity | 75.0/100 | No quality assertions defined (-25) |
| Stability | 90.0/100 | Schema has 4 fields |
| Lineage | 87.3/100 | 71 upstream sources |
| Adoption | 45.0/100 | No queries recorded in the last month (-35) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms