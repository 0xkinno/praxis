# warehouses

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **B-** (72.9/100)

## Overview

Contains information about physical distribution centers

**Platform:** dbt
**Domain:** Data Platform Team
**Owners:** b2fd91.ORG_DATA_PLATFORM, b2fd91.EMP006

## Schema

| Column | Type | Description |
|--------|------|-------------|
| warehouse_id | NUMBER | Unique identifier for the warehouse |
| warehouse_name | STRING | Name of the warehouse location |
| location_id | NUMBER | Reference to the physical location |
| wh_geo_location | STRING | Geographic coordinates of the warehouse |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 100.0/100 | 2 owners assigned |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 4 fields |
| Lineage | 84.5/100 | 5 upstream sources |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract