# inventories

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **B-** (70.4/100)

## Overview

Tracks product inventory levels across warehouses

**Platform:** dbt
**Domain:** Data Platform Team
**Owners:** b2fd91.ORG_DATA_PLATFORM, b2fd91.EMP006

## Schema

| Column | Type | Description |
|--------|------|-------------|
| product_id | NUMBER | Foreign key to the products table |
| warehouse_id | NUMBER | Foreign key to the warehouses table |
| quantity_on_hand | NUMBER | Current inventory count for this product in this warehouse |
| restock_level | NUMBER | Threshold at which restocking is initiated |
| max_stock_level | NUMBER | Maximum storage capacity for this product |
| reorder_quantity | NUMBER | Standard reorder quantity when restocking |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 90.0/100 | 2 owners assigned |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 6 fields |
| Lineage | 84.5/100 | 5 upstream sources |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract