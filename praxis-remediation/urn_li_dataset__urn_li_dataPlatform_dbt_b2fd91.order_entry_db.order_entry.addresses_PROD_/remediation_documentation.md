# addresses

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **B-** (72.9/100)

## Overview

Contains multiple shipping and billing addresses for customers

**Platform:** dbt
**Domain:** Data Platform Team
**Owners:** b2fd91.ORG_DATA_PLATFORM, b2fd91.EMP006

## Schema

| Column | Type | Description |
|--------|------|-------------|
| address_id | NUMBER | Unique identifier for the address |
| customer_id | NUMBER | Foreign key to the customers table |
| date_created | STRING | Date when address was added to the system |
| address_line1 | STRING | First line of address |
| address_line2 | STRING | Second line of address |
| town_city | STRING | Town or city of the address |
| country_id | NUMBER | Reference to country table |
| zipcode | NUMBER | Postal code of address |
| region_id | NUMBER | Reference to region table |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 100.0/100 | 2 owners assigned |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 9 fields |
| Lineage | 84.5/100 | 5 upstream sources |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract