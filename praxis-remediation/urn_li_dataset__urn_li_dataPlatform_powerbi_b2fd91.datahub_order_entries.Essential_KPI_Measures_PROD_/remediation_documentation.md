# Essential KPI Measures

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C-** (56.7/100)

## Overview



**Platform:** powerbi
**Domain:** Unassigned
**Owners:** 

## Schema

| Column | Type | Description |
|--------|------|-------------|
| Value | STRING | None |
| Total Revenue | NULL | SUMX('ORDER_DETAILS', 'ORDER_DETAILS'[order_total]) |
| Total Orders | NULL | DISTINCTCOUNT('ORDER_DETAILS'[order_id]) |
| Average Order Value | NULL | DIVIDE([Total Revenue], [Total Orders], 0) |
| Total Customers | NULL | DISTINCTCOUNT('ORDER_DETAILS'[customer_id]) |
| Revenue Per Customer | NULL | DIVIDE([Total Revenue], [Total Customers], 0) |
| Total Products Sold | NULL | SUM('ORDER_DETAILS'[quantity]) |
| YTD Revenue | NULL | CALCULATE([Total Revenue], DATESYTD('ORDER_DETAILS'[order_date])) |
| PY Revenue | NULL | CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('ORDER_DETAILS'[order_date])) |
| YoY Growth | NULL | DIVIDE([YTD Revenue] - [PY Revenue], [PY Revenue], 0) |
| Fulfillment Rate | NULL | DIVIDE(
    CALCULATE([Total Orders], 'ORDER_DETAILS'[delivery_status] <> "Not Shipped"),
    [Total Orders], 
    0
) |
| New Customers | NULL | 
CALCULATE(
    DISTINCTCOUNT('ORDER_DETAILS'[customer_id]),
    FILTER(
        'ORDER_DETAILS',
        'ORDER_DETAILS'[order_date] = 
        CALCULATE(
            MIN('ORDER_DETAILS'[order_date]),
            ALLEXCEPT('ORDER_DETAILS', 'ORDER_DETAILS'[customer_id])
        )
    )
) |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 35.0/100 | No owners assigned (-30) |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 12 fields |
| Lineage | 84.5/100 | 71 upstream sources |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract