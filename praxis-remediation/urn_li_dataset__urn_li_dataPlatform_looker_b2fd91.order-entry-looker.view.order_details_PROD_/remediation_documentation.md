# order_details

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C** (60.4/100)

## Overview



**Platform:** looker
**Domain:** Data Platform Team
**Owners:** b2fd91.marty@example.com, b2fd91.EMP006, b2fd91.ORG_DATA_PLATFORM, b2fd91.alex@example.com

## Schema

| Column | Type | Description |
|--------|------|-------------|
| billing_address_line1 | STRING |  |
| billing_address_line2 | STRING |  |
| billing_country | STRING |  |
| billing_region | STRING |  |
| billing_town_city | STRING |  |
| billing_zipcode | NUMBER |  |
| category_id | NUMBER |  |
| category_name | STRING |  |
| condition | STRING |  |
| cost_of_delivery | NUMBER |  |
| cust_email | STRING |  |
| cust_first_name | STRING |  |
| cust_last_name | STRING |  |
| customer_class | STRING |  |
| customer_id | NUMBER |  |
| delivery_status | STRING |  |
| delivery_type | STRING |  |
| discount_amount | NUMBER |  |
| discount_percent | NUMBER |  |
| dispatch_date | STRING |  |
| estimated_delivery | STRING |  |
| gift_wrap | STRING |  |
| line_item_id | NUMBER |  |
| line_total | NUMBER |  |
| list_price | NUMBER |  |
| order_date | STRING |  |
| order_date_timestamp | TIME |  |
| order_id | NUMBER |  |
| order_mode | STRING |  |
| order_status | NUMBER |  |
| order_total | NUMBER |  |
| payment_method_code | STRING |  |
| phone_number | STRING |  |
| product_description | STRING |  |
| product_id | NUMBER |  |
| product_name | STRING |  |
| product_status | STRING |  |
| promotion_description | STRING |  |
| promotion_id | NUMBER |  |
| promotion_name | STRING |  |
| quantity | NUMBER |  |
| quantity_on_hand | NUMBER |  |
| return_date | STRING |  |
| return_status | STRING |  |
| shipping_address_line1 | STRING |  |
| shipping_address_line2 | STRING |  |
| shipping_country | STRING |  |
| shipping_region | STRING |  |
| shipping_town_city | STRING |  |
| shipping_zipcode | NUMBER |  |
| stock_status | STRING |  |
| unit_price | NUMBER |  |
| wait_till_complete_yn | STRING |  |
| warehouse_id | NUMBER |  |
| warehouse_name | STRING |  |
| updated | TIME |  |
| count | NUMBER |  |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 50.0/100 | 4 owners assigned |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 57 fields |
| Lineage | 84.5/100 | 71 upstream sources |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract