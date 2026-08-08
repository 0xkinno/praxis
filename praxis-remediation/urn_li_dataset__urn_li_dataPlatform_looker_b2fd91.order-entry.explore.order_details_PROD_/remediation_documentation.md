# Order Details

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C+** (66.7/100)

## Overview




### Order Details

The **Order Details** table is a central component of the e-commerce data ecosystem, capturing detailed information about each order placed by customers. This table is of high business importance as it provides critical insights into customer purchasing behavior, product performance, and the overall health of the e-commerce operations.

The table is sourced from the [@order-entry-looker.view.order_details](urn:li:dataset:(urn:li:dataPlatform:looker,order-entry-looker.view.order_details,PROD)) view, which is likely a derived table from one or more underlying operational data sources. The table contains a wide range of dimensions related to the order, customer, product, and fulfillment details, as well as several measures such as order total, line item total, and quantity.

This table is likely consumed by various downstream reporting and analytics applications to support use cases such as sales performance analysis, customer segmentation, inventory management, and marketing campaign optimization. The table's detailed grain and comprehensive set of attributes make it a valuable source of information for data-driven decision-making across the e-commerce business.

#### Technical Notes

- The **Order Details** table is a view, meaning it is a derived dataset that is generated from one or more underlying tables.
- The table has a detailed grain, capturing information at the individual order line item level.
- The table contains several columns that may be considered Personally Identifiable Information (PII), such as customer names, email addresses, and phone numbers. Appropriate access controls and data governance policies should be in place to ensure the proper handling of this sensitive data.

#### Potential PII Columns

The following columns in the **Order Details** table may contain Personally Identifiable Information (PII):

- `cust_email`
- `cust_first_name`
- `cust_last_name`
- `phone_number`
- `billing_address_line1`
- `billing_address_line2`
- `billing_town_city`
- `billing_region`
- `billing_country`
- `billing_zipcode`
- `shipping_address_line1`
- `shipping_address_line2`
- `shipping_town_city`
- `shipping_region`
- `shipping_country`
- `shipping_zipcode`

**Platform:** looker
**Domain:** Data Platform Team
**Owners:** b2fd91.ORG_DATA_PLATFORM, b2fd91.ORG_BACKEND_ENG, b2fd91.EMP006

## Schema

| Column | Type | Description |
|--------|------|-------------|
| order_details.billing_address_line1 | STRING |  |
| order_details.billing_address_line2 | STRING |  |
| order_details.billing_country | STRING |  |
| order_details.billing_region | STRING |  |
| order_details.billing_town_city | STRING |  |
| order_details.billing_zipcode | NUMBER |  |
| order_details.category_id | NUMBER |  |
| order_details.category_name | STRING |  |
| order_details.condition | STRING |  |
| order_details.cost_of_delivery | NUMBER |  |
| order_details.cust_email | STRING |  |
| order_details.cust_first_name | STRING |  |
| order_details.cust_last_name | STRING |  |
| order_details.customer_class | STRING |  |
| order_details.customer_id | NUMBER |  |
| order_details.delivery_status | STRING |  |
| order_details.delivery_type | STRING |  |
| order_details.discount_amount | NUMBER |  |
| order_details.discount_percent | NUMBER |  |
| order_details.dispatch_date | STRING |  |
| order_details.estimated_delivery | STRING |  |
| order_details.gift_wrap | STRING |  |
| order_details.line_item_id | NUMBER |  |
| order_details.line_total | NUMBER |  |
| order_details.list_price | NUMBER |  |
| order_details.order_date | STRING |  |
| order_details.order_date_timestamp | TIME |  |
| order_details.order_id | NUMBER |  |
| order_details.order_mode | STRING |  |
| order_details.order_status | NUMBER |  |
| order_details.order_total | NUMBER |  |
| order_details.payment_method_code | STRING |  |
| order_details.phone_number | STRING |  |
| order_details.product_description | STRING |  |
| order_details.product_id | NUMBER |  |
| order_details.product_name | STRING |  |
| order_details.product_status | STRING |  |
| order_details.promotion_description | STRING |  |
| order_details.promotion_id | NUMBER |  |
| order_details.promotion_name | STRING |  |
| order_details.quantity | NUMBER |  |
| order_details.quantity_on_hand | NUMBER |  |
| order_details.return_date | STRING |  |
| order_details.return_status | STRING |  |
| order_details.shipping_address_line1 | STRING |  |
| order_details.shipping_address_line2 | STRING |  |
| order_details.shipping_country | STRING |  |
| order_details.shipping_region | STRING |  |
| order_details.shipping_town_city | STRING |  |
| order_details.shipping_zipcode | NUMBER |  |
| order_details.stock_status | STRING |  |
| order_details.unit_price | NUMBER |  |
| order_details.updated_date | DATE |  |
| order_details.updated_month | DATE |  |
| order_details.updated_quarter | DATE |  |
| order_details.updated_raw | TIME |  |
| order_details.updated_time | TIME |  |
| order_details.updated_week | TIME |  |
| order_details.updated_year | DATE |  |
| order_details.wait_till_complete_yn | STRING |  |
| order_details.warehouse_id | NUMBER |  |
| order_details.warehouse_name | STRING |  |
| order_details.count | NUMBER |  |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 75.0/100 | 3 owners assigned |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 63 fields |
| Lineage | 84.5/100 | 72 upstream sources |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract