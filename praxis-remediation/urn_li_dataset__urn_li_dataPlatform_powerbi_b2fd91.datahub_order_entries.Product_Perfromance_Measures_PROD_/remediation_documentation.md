# Product Perfromance Measures

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C** (63.3/100)

## Overview



**Platform:** powerbi
**Domain:** Unassigned
**Owners:** 

## Schema

| Column | Type | Description |
|--------|------|-------------|
| Value | STRING | None |
| Revenue by Category | NULL | CALCULATE([Total Revenue], VALUES('ORDER_DETAILS'[category_name])) |
| Top Selling Products | NULL | CALCULATE(SUM('ORDER_DETAILS'[quantity]), VALUES('ORDER_DETAILS'[product_name])) |
| Total Discount Amount | NULL | SUM('ORDER_DETAILS'[discount_amount]) |
| Average Discount % | NULL | AVERAGE('ORDER_DETAILS'[discount_percent]) |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 30.0/100 | No owners assigned (-35) |
| Integrity | 75.0/100 | No quality assertions defined (-25) |
| Stability | 90.0/100 | Schema has 5 fields |
| Lineage | 87.3/100 | 71 upstream sources |
| Adoption | 45.0/100 | No queries recorded in the last month (-35) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms