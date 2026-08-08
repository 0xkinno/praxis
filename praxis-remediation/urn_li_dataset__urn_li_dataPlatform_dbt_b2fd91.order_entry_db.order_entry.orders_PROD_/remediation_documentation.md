# orders

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **B-** (70.4/100)

## Overview

Contains header information for customer orders

**Platform:** dbt
**Domain:** Data Platform Team
**Owners:** b2fd91.ORG_DATA_PLATFORM, b2fd91.EMP006

## Schema

| Column | Type | Description |
|--------|------|-------------|
| order_id | NUMBER | Unique identifier for the order |
| order_date | STRING | Date and time when the order was placed including timezone |
| order_mode | STRING | Method of order placement (e.g., online, phone, direct) |
| customer_id | NUMBER | Foreign key to the customers table |
| order_status | NUMBER | Current status of the order (e.g., 1=Pending, 2=Processing, 3=Shipped) |
| order_total | NUMBER | Total monetary value of the order |
| sales_rep_id | NUMBER | ID of the sales representative handling the order |
| promotion_id | NUMBER | Foreign key to promotions table if applicable |
| warehouse_id | NUMBER | Foreign key to warehouses table for fulfillment location |
| delivery_type | STRING | Shipping method (e.g., Standard, Express, Overnight) |
| cost_of_delivery | NUMBER | Shipping and handling cost |
| wait_till_complete_yn | STRING | Flag indicating whether to ship complete order or partial (Y/N) |
| billing_address_id | NUMBER | Reference to the billing address |
| delivery_address_id | NUMBER | Reference to the shipping address |
| payment_method_code | STRING | Code indicating payment method used |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 90.0/100 | 2 owners assigned |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 15 fields |
| Lineage | 84.5/100 | 5 upstream sources |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract