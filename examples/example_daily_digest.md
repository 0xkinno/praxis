# PRAXIS Daily Intelligence Digest
Date: 2026-08-05
Run ID: `run_direct_1785942418`

## Catalog Overview
| Metric | Value |
|--------|-------|
| Total Assets Assessed | 67 |
| Average Trust Score | 55.3 |
| Trusted Assets | 0 |
| Review Assets | 27 |
| Untrusted Assets | 40 |

## Catalog Deltas (Changes Since Last Run)
*No score changes detected since the last run.*

## Domain Health
| Domain | Asset Count | Average Score | Grade | Weakest Dimension |
|--------|-------------|---------------|-------|-------------------|
| Data Platform Team | 14 | 70.9 | **TrustGrade.B_MINUS** | adoption |
| E-Commerce | 1 | 56.9 | **TrustGrade.C_MINUS** | adoption |
| Ecommerce Operations | 1 | 64.2 | **TrustGrade.C** | adoption |
| Unassigned | 51 | 50.8 | **TrustGrade.D** | provenance |

## Top 5 Trust Risks
| Asset | URN | Grade | Score | Reason |
|-------|-----|-------|-------|--------|
| ORDER_DETAILS_REPLICA | `urn:li:dataset:(urn:li:dataPlatform:snowflake,b2fd91.order_entry_db.analytics.order_details_replica,PROD)` | **TrustGrade.D** | 43.4 | Dataset ORDER_DETAILS_REPLICA is graded D with a composite score of 45.8/100. Key remediation required in the following dimensions: provenance, integrity, lineage, adoption. |
| ORDER_HISTORY | `urn:li:dataset:(urn:li:dataPlatform:snowflake,b2fd91.order_entry_db.analytics.order_history,PROD)` | **TrustGrade.D** | 45.9 | Dataset ORDER_HISTORY is graded D with a composite score of 48.2/100. Key remediation required in the following dimensions: provenance, integrity, lineage, adoption. |
| addresses | `urn:li:dataset:(urn:li:dataPlatform:postgres,b2fd91.order_entry_db.order_entry.addresses,PROD)` | **TrustGrade.D** | 48.2 | Dataset addresses is graded D with a composite score of 48.2/100. Key remediation required in the following dimensions: provenance, integrity, lineage, adoption. |
| countries | `urn:li:dataset:(urn:li:dataPlatform:postgres,b2fd91.order_entry_db.order_entry.countries,PROD)` | **TrustGrade.D** | 48.2 | Dataset countries is graded D with a composite score of 48.2/100. Key remediation required in the following dimensions: provenance, integrity, lineage, adoption. |
| customers | `urn:li:dataset:(urn:li:dataPlatform:postgres,b2fd91.order_entry_db.order_entry.customers,PROD)` | **TrustGrade.D** | 48.2 | Dataset customers is graded D with a composite score of 48.2/100. Key remediation required in the following dimensions: provenance, integrity, lineage, adoption. |

## Trust Propagation Summary
- Untrusted sources: 40
- Downstream assets affected: 55
- Max hop distance: 5

## Remediation & Delivery
- Total Remediations Generated: 335
- Remediation Pull Request: None

## Recommended Actions
- Address provenance, integrity, lineage, adoption gaps on dataset 'ORDER_DETAILS_REPLICA' (Score: 43.4, Grade: D).
- Address provenance, integrity, lineage, adoption gaps on dataset 'ORDER_HISTORY' (Score: 45.9, Grade: D).
- Address provenance, integrity, lineage, adoption gaps on dataset 'addresses' (Score: 48.2, Grade: D).