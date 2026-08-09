# ORDER_DETAILS

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **B-** (73.2/100)

## Overview

Details of orders.

**Platform:** snowflake
**Domain:** Ecommerce Operations
**Owners:** b2fd91.1e0398a3-113f-475e-b6fc-32ab72a634d2, b2fd91.brock1@example.com, b2fd91.jonny1@example.com

## Schema

| Column | Type | Description |
|--------|------|-------------|
| order_id | NUMBER | None |
| order_date | STRING | None |
| order_mode | STRING | None |
| order_status | NUMBER | None |
| order_total | NUMBER | None |
| cost_of_delivery | NUMBER | None |
| delivery_type | STRING | None |
| wait_till_complete_yn | STRING | None |
| payment_method_code | STRING | None |
| customer_id | NUMBER | None |
| cust_first_name | STRING | None |
| cust_last_name | STRING | None |
| cust_email | STRING | None |
| phone_number | STRING | None |
| customer_class | STRING | None |
| billing_address_line1 | STRING | None |
| billing_address_line2 | STRING | None |
| billing_town_city | STRING | None |
| billing_country | STRING | None |
| billing_zipcode | NUMBER | None |
| billing_region | STRING | None |
| shipping_address_line1 | STRING | None |
| shipping_address_line2 | STRING | None |
| shipping_town_city | STRING | None |
| shipping_country | STRING | None |
| shipping_zipcode | NUMBER | None |
| shipping_region | STRING | None |
| warehouse_id | NUMBER | None |
| warehouse_name | STRING | None |
| promotion_id | NUMBER | None |
| promotion_name | STRING | None |
| promotion_description | STRING | None |
| line_item_id | NUMBER | None |
| product_id | NUMBER | None |
| product_name | STRING | None |
| product_description | STRING | None |
| category_id | NUMBER | None |
| category_name | STRING | None |
| unit_price | NUMBER | None |
| quantity | NUMBER | None |
| line_total | NUMBER | None |
| dispatch_date | STRING | None |
| return_date | STRING | None |
| gift_wrap | STRING | None |
| condition | STRING | None |
| estimated_delivery | STRING | None |
| list_price | NUMBER | None |
| product_status | STRING | None |
| quantity_on_hand | NUMBER | None |
| stock_status | STRING | None |
| discount_amount | NUMBER | None |
| discount_percent | NUMBER | None |
| delivery_status | STRING | None |
| return_status | STRING | None |
| updated_at | TIME | None |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 62.0/100 | 3 owners assigned |
| Integrity | 75.0/100 | No quality assertions defined (-25) |
| Stability | 90.0/100 | Schema has 55 fields |
| Lineage | 100.0/100 | 70 upstream sources |
| Adoption | 45.0/100 | No queries recorded in the last month (-35) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms