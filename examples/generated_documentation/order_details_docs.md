# order_details

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C+** (72.0/100)

## Overview

Details about each item in an order, including quantity, price, discount, and product links.

**Platform:** dbt
**Domain:** Ecommerce
**Owners:** Data Engineering Team

## Schema

| Column | Type | Description |
|--------|------|-------------|
| order_id | VARCHAR | Foreign key reference to orders |
| line_item_id | INT | Unique identifier for this line item in the order |
| product_id | VARCHAR | Foreign key reference to products |
| quantity | INT | Quantity ordered |
| unit_price | DECIMAL | Price per unit |
| discount | DECIMAL | Discount applied (if any) |
| _updated_at | TIMESTAMP | Last updated timestamp in source DB |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 80.0/100 | Ownership assigned to Data Engineering Team |
| Integrity | 50.0/100 | No quality assertions defined (-40) |
| Stability | 100.0/100 | Schema has 7 fields |
| Lineage | 60.0/100 | 1 upstream sources |
| Adoption | 80.0/100 | 125 queries in the last month |

## Recommended Actions
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract
- Verify upstream sources are connected
- Confirm downstream consumers are tracked