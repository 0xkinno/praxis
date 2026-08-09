# ORDER_DETAILS

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C** (63.3/100)

## Overview



**Platform:** powerbi
**Domain:** Unassigned
**Owners:** b2fd91.kirk@example.com

## Schema

| Column | Type | Description |
|--------|------|-------------|
| ORDER_ID | NUMBER | None |
| ORDER_DATE | STRING | None |
| ORDER_MODE | STRING | None |
| ORDER_STATUS | NUMBER | None |
| ORDER_TOTAL | NUMBER | None |
| COST_OF_DELIVERY | NUMBER | None |
| DELIVERY_TYPE | STRING | None |
| WAIT_TILL_COMPLETE_YN | STRING | None |
| PAYMENT_METHOD_CODE | STRING | None |
| CUSTOMER_ID | NUMBER | None |
| CUST_FIRST_NAME | STRING | None |
| CUST_LAST_NAME | STRING | None |
| CUST_EMAIL | STRING | None |
| PHONE_NUMBER | STRING | None |
| CUSTOMER_CLASS | STRING | None |
| BILLING_ADDRESS_LINE1 | STRING | None |
| BILLING_ADDRESS_LINE2 | STRING | None |
| BILLING_TOWN_CITY | STRING | None |
| BILLING_COUNTRY | STRING | None |
| BILLING_ZIPCODE | NUMBER | None |
| BILLING_REGION | STRING | None |
| SHIPPING_ADDRESS_LINE1 | STRING | None |
| SHIPPING_ADDRESS_LINE2 | STRING | None |
| SHIPPING_TOWN_CITY | STRING | None |
| SHIPPING_COUNTRY | STRING | None |
| SHIPPING_ZIPCODE | NUMBER | None |
| SHIPPING_REGION | STRING | None |
| WAREHOUSE_ID | NUMBER | None |
| WAREHOUSE_NAME | STRING | None |
| PROMOTION_ID | NUMBER | None |
| PROMOTION_NAME | STRING | None |
| PROMOTION_DESCRIPTION | STRING | None |
| LINE_ITEM_ID | NUMBER | None |
| PRODUCT_ID | NUMBER | None |
| PRODUCT_NAME | STRING | None |
| PRODUCT_DESCRIPTION | STRING | None |
| CATEGORY_ID | NUMBER | None |
| CATEGORY_NAME | STRING | None |
| UNIT_PRICE | NUMBER | None |
| QUANTITY | NUMBER | None |
| LINE_TOTAL | NUMBER | None |
| DISPATCH_DATE | STRING | None |
| RETURN_DATE | STRING | None |
| GIFT_WRAP | STRING | None |
| CONDITION | STRING | None |
| ESTIMATED_DELIVERY | STRING | None |
| LIST_PRICE | NUMBER | None |
| PRODUCT_STATUS | STRING | None |
| QUANTITY_ON_HAND | NUMBER | None |
| STOCK_STATUS | STRING | None |
| DISCOUNT_AMOUNT | NUMBER | None |
| DISCOUNT_PERCENT | NUMBER | None |
| DELIVERY_STATUS | STRING | None |
| RETURN_STATUS | STRING | None |
| UPDATED_AT | DATE | None |
| Order Size Category | STRING | None |
| Quarter | STRING | None |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 30.0/100 | Single owner, no backup (-5) |
| Integrity | 75.0/100 | No quality assertions defined (-25) |
| Stability | 90.0/100 | Schema has 57 fields |
| Lineage | 87.3/100 | 71 upstream sources |
| Adoption | 45.0/100 | No queries recorded in the last month (-35) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms