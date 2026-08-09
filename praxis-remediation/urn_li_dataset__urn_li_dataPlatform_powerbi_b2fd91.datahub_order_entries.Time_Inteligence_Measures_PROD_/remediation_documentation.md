# Time Inteligence Measures

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C+** (68.5/100)

## Overview



**Platform:** powerbi
**Domain:** Unassigned
**Owners:** 

## Schema

| Column | Type | Description |
|--------|------|-------------|
| Value | STRING | None |
| Revenue by Month | NULL | CALCULATE([Total Revenue], DATESMTD('ORDER_DETAILS'[order_date])) |
| MoM Revenue Growth | NULL | 
VAR CurrentMonth = [Total Revenue]
VAR PreviousMonth1 = CALCULATE([Total Revenue], DATEADD('ORDER_DETAILS'[order_date], -1, MONTH))
RETURN DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth1, 0) |
| Current Year Revenue | NULL | [Total Revenue] |
| Previous Year Revenue | NULL | CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('ORDER_DETAILS'[order_date])) |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 40.0/100 | No owners assigned (-30) |
| Integrity | 75.0/100 | No quality assertions defined (-25) |
| Stability | 90.0/100 | Schema has 5 fields |
| Lineage | 100.0/100 | 71 upstream sources |
| Adoption | 50.0/100 | No queries recorded in the last month (-30) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms