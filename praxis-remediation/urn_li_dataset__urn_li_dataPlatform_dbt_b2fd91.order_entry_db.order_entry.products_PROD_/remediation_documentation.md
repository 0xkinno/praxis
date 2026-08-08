# products

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **B-** (72.9/100)

## Overview

Contains information about products available for sale

**Platform:** dbt
**Domain:** Data Platform Team
**Owners:** b2fd91.ORG_DATA_PLATFORM, b2fd91.EMP006, b2fd91.patrick1@example.com

## Schema

| Column | Type | Description |
|--------|------|-------------|
| product_id | NUMBER | Unique identifier for the product |
| product_name | STRING | Name of the product |
| product_description | STRING | Brief description of the product |
| category_id | NUMBER | Foreign key to the product_categories table |
| weight_class | NUMBER | Weight class for shipping calculations |
| warranty_period | STRING | Standard warranty period for the product |
| supplier_id | NUMBER | ID of the supplier for this product |
| product_status | STRING | Current status (e.g., Available, Discontinued, Planned) |
| list_price | NUMBER | Standard list price for the product |
| min_price | NUMBER | Minimum selling price for the product |
| catalog_url | STRING | URL to the product in the online catalog |
| date_added | STRING | Date when product was added to the catalog |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 100.0/100 | 3 owners assigned |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 12 fields |
| Lineage | 84.5/100 | 5 upstream sources |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract