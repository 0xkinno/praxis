# order_items

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **B-** (70.4/100)

## Overview

Contains line items for each order

**Platform:** dbt
**Domain:** Data Platform Team
**Owners:** b2fd91.ORG_DATA_PLATFORM, b2fd91.EMP006

## Schema

| Column | Type | Description |
|--------|------|-------------|
| order_id | NUMBER | Foreign key to the orders table |
| line_item_id | NUMBER | Line item sequence number within the order |
| product_id | NUMBER | Foreign key to the products table |
| unit_price | NUMBER | Selling price per unit at time of order |
| quantity | NUMBER | Number of units ordered |
| dispatch_date | STRING | Date when item was dispatched from warehouse |
| return_date | STRING | Date when item was returned if applicable |
| gift_wrap | STRING | Flag or type of gift wrapping requested |
| condition | STRING | Condition of product (e.g., New, Refurbished) |
| supplier_id | NUMBER | ID of the supplier if dropshipped |
| estimated_delivery | STRING | Estimated delivery date for this item |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 90.0/100 | 2 owners assigned |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 11 fields |
| Lineage | 84.5/100 | 5 upstream sources |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract