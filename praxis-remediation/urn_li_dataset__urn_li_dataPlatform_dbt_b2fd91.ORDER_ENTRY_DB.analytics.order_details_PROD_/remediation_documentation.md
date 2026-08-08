# order_details

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **B-** (72.9/100)

## Overview

### order\_details

The `order_details` table is a central hub for order information, consolidating data from various upstream sources to provide a comprehensive view of customer orders, products, and fulfillment. This table is a critical component of the order entry data ecosystem, enabling data-driven decision making and reporting across the organization.

The table is constructed by joining data from several source tables, including [@table_name](urn:li:dataset:(urn:li:dataPlatform:dbt,order_entry_db.order_entry.orders,PROD)), [@table_name](urn:li:dataset:(urn:li:dataPlatform:dbt,order_entry_db.order_entry.customers,PROD)), [@table_name](urn:li:dataset:(urn:li:dataPlatform:dbt,order_entry_db.order_entry.addresses,PROD)), [@table_name](urn:li:dataset:(urn:li:dataPlatform:dbt,order_entry_db.order_entry.countries,PROD)), [@table_name](urn:li:dataset:(urn:li:dataPlatform:dbt,order_entry_db.order_entry.regions,PROD)), [@table_name](urn:li:dataset:(urn:li:dataPlatform:dbt,order_entry_db.order_entry.warehouses,PROD)), [@table_name](urn:li:dataset:(urn:li:dataPlatform:dbt,order_entry_db.order_entry.order_items,PROD)), [@table_name](urn:li:dataset:(urn:li:dataPlatform:dbt,order_entry_db.order_entry.products,PROD)), [@table_name](urn:li:dataset:(urn:li:dataPlatform:dbt,order_entry_db.order_entry.product_categories,PROD)), and [@table_name](urn:li:dataset:(urn:li:dataPlatform:dbt,order_entry_db.order_entry.promotions,PROD)).

The `order_details` table is consumed by several downstream systems, including a Snowflake view, Tableau dashboards, Power BI reports, and a Looker view. These downstream consumers leverage the comprehensive order data to support a variety of use cases, such as sales analytics, customer segmentation, inventory management, and marketing campaign evaluation.

The table is a materialized view, meaning the data is pre-computed and stored in a physical table for efficient querying. It has a grain of one row per order line item, providing detailed information about each product ordered, including pricing, discounts, inventory status, and delivery details.

The `order_details` table does contain some personally identifiable information (PII) data, such as customer names, email addresses, and phone numbers. As such, access to this table should be carefully managed and monitored in accordance with your organization's data privacy policies.

&nbsp;

**Platform:** dbt
**Domain:** Data Platform Team
**Owners:** b2fd91.1e0398a3-113f-475e-b6fc-32ab72a634d2, b2fd91.ORG_DATA_PLATFORM, b2fd91.ORG_DATA_PLATFORM, b2fd91.EMP006, b2fd91.brock1@example.com, b2fd91.bryan@example.com, b2fd91.jonny1@example.com, b2fd91.jonny2@example.com, b2fd91.kirk@example.com, b2fd91.marty@example.com, b2fd91.marty@example.com, b2fd91.sam@example.com

## Schema

| Column | Type | Description |
|--------|------|-------------|
| order_id | NUMBER | Unique identifier for the order |
| order_date | STRING | Date and time when the order was placed including timezone |
| order_mode | STRING | Method of order placement (e.g., online, phone, instore) |
| order_status | NUMBER | Current status of the order (e.g., 1=Pending, 2=Processing, 3=Shipped) |
| order_total | NUMBER | Total monetary value of the order |
| cost_of_delivery | NUMBER | Shipping and handling cost |
| delivery_type | STRING | Shipping method (e.g., Standard, Curbside, Overnight) |
| wait_till_complete_yn | STRING | Flag indicating whether to ship complete order or partial (Y/N) |
| payment_method_code | STRING | Code indicating payment method used |
| customer_id | NUMBER | Unique identifier for the customer |
| cust_first_name | STRING | Customer first name |
| cust_last_name | STRING | Customer last name |
| cust_email | STRING | Customer email address |
| phone_number | STRING | Customer contact phone number |
| customer_class | STRING | Classification of the customer (e.g., Retail, Enterprise, Online) |
| billing_address_line1 | STRING | First line of customer billing address |
| billing_address_line2 | STRING | Second line of customer billing address |
| billing_town_city | STRING | Town or city of customer billing address |
| billing_country | STRING | Country name for the billing address |
| billing_zipcode | NUMBER | Postal code of customer billing address |
| billing_region | STRING | Region/state/province name for the billing address |
| shipping_address_line1 | STRING | First line of customer shipping address |
| shipping_address_line2 | STRING | Second line of customer shipping address |
| shipping_town_city | STRING | Town or city of customer shipping address |
| shipping_country | STRING | Country name for the shipping address |
| shipping_zipcode | NUMBER | Postal code of customer shipping address |
| shipping_region | STRING | Region/state/province name for the shipping address |
| warehouse_id | NUMBER | Identifier of the warehouse fulfilling the order |
| warehouse_name | STRING | Name of the warehouse location |
| promotion_id | NUMBER | Identifier of the promotion applied to the order |
| promotion_name | STRING | Name of the marketing promotion |
| promotion_description | STRING | Detailed description of the promotion |
| line_item_id | NUMBER | Line item sequence number within the order |
| product_id | NUMBER | Identifier of the product ordered |
| product_name | STRING | Name of the product |
| product_description | STRING | Brief description of the product |
| category_id | NUMBER | Identifier of the product category |
| category_name | STRING | Name of the product category |
| unit_price | NUMBER | Selling price per unit at time of order |
| quantity | NUMBER | Number of units ordered |
| line_total | NUMBER | Total price for the line item (unit_price * quantity) |
| dispatch_date | STRING | Date when item was dispatched from warehouse |
| return_date | STRING | Date when item was returned if applicable |
| gift_wrap | STRING | Flag or type of gift wrapping requested |
| condition | STRING | Condition of product (e.g., New, Refurbished) |
| estimated_delivery | STRING | Estimated delivery date for this item |
| list_price | NUMBER | Standard list price for the product |
| product_status | STRING | Current status of the product (e.g., Active, Inactive, Backordered) |
| quantity_on_hand | NUMBER | Current inventory count for this product in the fulfilling warehouse |
| stock_status | STRING | Status of current inventory levels (Low Stock, In Stock, Overstocked) |
| discount_amount | NUMBER | Amount of discount applied (list_price - unit_price) |
| discount_percent | NUMBER | Percentage discount applied ((list_price - unit_price) / list_price * 100) |
| delivery_status | STRING | Current status of delivery (Not Shipped, In Transit, Delivered) |
| return_status | STRING | Status indicating if item was returned (Returned, Not Returned) |
| updated_at | TIME | Timestamp indicating when this record was last refreshed |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 100.0/100 | 12 owners assigned |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 55 fields |
| Lineage | 84.5/100 | 69 upstream sources |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract