# customers

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **B-** (72.9/100)

## Overview

Contains customer demographic and contact information

**Platform:** dbt
**Domain:** Data Platform Team
**Owners:** b2fd91.ORG_DATA_PLATFORM, b2fd91.EMP006, b2fd91.jonny1@example.com

## Schema

| Column | Type | Description |
|--------|------|-------------|
| customer_id | NUMBER | Unique identifier for the customer |
| cust_first_name | STRING | Customer first name |
| cust_last_name | STRING | Customer last name |
| nls_language | STRING | Preferred language code |
| nls_territory | STRING | Geographical territory for localization settings |
| credit_limit | NUMBER | Maximum credit amount for the customer |
| cust_email | STRING | Customer email address |
| account_mgr_id | NUMBER | ID of the account manager assigned to the customer |
| customer_since | STRING | Date when customer was first registered |
| customer_class | STRING | Classification of the customer (e.g., Platinum, Gold, Silver) |
| suggestions | STRING | Customer product suggestions or preferences |
| dob | STRING | Customer date of birth |
| mailshot | NUMBER | Flag indicating if customer has opted for marketing emails (Y/N) |
| partner_mailshot | NUMBER | Flag indicating if customer has opted for partner marketing (Y/N) |
| phone_number | STRING | Customer contact phone number |
| address_line1 | STRING | First line of customer primary address |
| address_line2 | STRING | Second line of customer primary address |
| address_line3 | STRING | Third line of customer primary address |
| town_city | STRING | Town or city of customer primary address |
| country_id | NUMBER | Reference to country table for primary address |
| zipcode | NUMBER | Postal code of customer primary address |
| region_id | NUMBER | Reference to region table for primary address |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 100.0/100 | 3 owners assigned |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 22 fields |
| Lineage | 84.5/100 | 5 upstream sources |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract