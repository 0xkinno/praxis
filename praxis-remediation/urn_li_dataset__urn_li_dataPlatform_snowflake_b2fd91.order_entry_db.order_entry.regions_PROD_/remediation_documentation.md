# REGIONS

> Auto-generated documentation by PRAXIS Trust Assessment.
> Trust Score: **C-** (56.7/100)

## Overview




### REGIONS

The `REGIONS` table is a large, centralized reference table that provides a comprehensive view of geographic regions and countries. This table is a critical component of the data platform, as it underpins many downstream models and reports that require accurate and consistent geographic information.

The `REGIONS` table is sourced from an upstream system and serves as the authoritative source for region and country data across the organization. It is used to enrich and contextualize various business data, enabling analysts and decision-makers to gain deeper insights into geographic trends and patterns.

The downstream lineage information provided indicates that the `REGIONS` table is consumed by the [@order_details](urn:li:dataset:(urn:li:dataPlatform:dbt,ORDER_ENTRY_DB.analytics.order_details,PROD)) model, which combines data from multiple sources to provide a comprehensive view of customer orders. This denormalized view is designed to support reporting, analysis, and operational insights across the order management process.

The `REGIONS` table is a reference table, meaning it is not expected to change frequently. It is refreshed on query with the current timestamp, ensuring that downstream consumers have access to the most up-to-date geographic information.

The table contains the following columns:

- `region_id`: A unique identifier for the geographic region
- `region_name`: The name of the geographic region
- `country_id`: A unique identifier for the country
- `nls_language`: The language associated with the region or country

The `REGIONS` table does not directly contain any personally identifiable information (PII) data, such as names, emails, or addresses.

**Platform:** snowflake
**Domain:** Unassigned
**Owners:** 

## Schema

| Column | Type | Description |
|--------|------|-------------|
| region_id | NUMBER | None |
| region_name | STRING | None |
| country_id | NUMBER | None |
| nls_language | STRING | None |

## Trust Assessment

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Provenance | 35.0/100 | No owners assigned (-30) |
| Integrity | 60.0/100 | No quality assertions defined (-40) |
| Stability | 85.0/100 | Schema has 4 fields |
| Lineage | 84.5/100 | 4 upstream sources |
| Adoption | 30.0/100 | No queries recorded in the last month (-40) |

## Recommended Actions
- Add dataset description and column-level documentation
- Assign at least two owners (primary + backup)
- Link relevant glossary terms
- Define quality assertions (freshness, volume, field-level)
- Set up a data contract