import datetime
from datetime import timezone

# Mock data representitive of the DataHub showcase-ecommerce sample catalog
MOCK_DOMAINS = [
    {
        "domain": "Analytics",
        "asset_count": 14,
        "average_score": 82.5,
        "grade": "B",
        "tier_distribution": {"trusted": 9, "review": 4, "untrusted": 1},
        "weakest_dimension": "integrity",
        "top_risks": [
            "urn:li:dataset:(urn:li:dataPlatform:dbt,b2fd91.ORDER_ENTRY_DB.analytics.customer_cohorts,PROD)"
        ]
    },
    {
        "domain": "Logistics",
        "asset_count": 8,
        "average_score": 58.0,
        "grade": "D",
        "tier_distribution": {"trusted": 1, "review": 4, "untrusted": 3},
        "weakest_dimension": "provenance",
        "top_risks": [
            "urn:li:dataset:(urn:li:dataPlatform:hive,warehouse.shipment_deliveries,PROD)",
            "urn:li:dataset:(urn:li:dataPlatform:hive,warehouse.carrier_routes,PROD)"
        ]
    },
    {
        "domain": "Customer",
        "asset_count": 10,
        "average_score": 89.2,
        "grade": "A-",
        "tier_distribution": {"trusted": 8, "review": 2, "untrusted": 0},
        "weakest_dimension": "lineage",
        "top_risks": []
    },
    {
        "domain": "Checkout",
        "asset_count": 12,
        "average_score": 77.4,
        "grade": "B-",
        "tier_distribution": {"trusted": 6, "review": 5, "untrusted": 1},
        "weakest_dimension": "stability",
        "top_risks": [
            "urn:li:dataset:(urn:li:dataset:(urn:li:dataPlatform:mysql,checkout.carts_active,PROD)"
        ]
    },
    {
        "domain": "Inventory",
        "asset_count": 8,
        "average_score": 91.0,
        "grade": "A",
        "tier_distribution": {"trusted": 8, "review": 0, "untrusted": 0},
        "weakest_dimension": "none",
        "top_risks": []
    }
]

MOCK_PROPAGATION = {
    "untrusted_sources": 2,
    "affected_assets": [
        {
            "urn": "urn:li:dataset:(urn:li:dataPlatform:dbt,b2fd91.ORDER_ENTRY_DB.analytics.order_details,PROD)",
            "name": "order_details",
            "score": 72.0,
            "grade": "C+",
            "penalty": 15.0,
            "source_urn": "urn:li:dataset:(urn:li:dataPlatform:hive,logging_events,PROD)"
        },
        {
            "urn": "urn:li:dataset:(urn:li:dataPlatform:dbt,b2fd91.ORDER_ENTRY_DB.analytics.daily_sales_summary,PROD)",
            "name": "daily_sales_summary",
            "score": 52.4,
            "grade": "F",
            "penalty": 10.5,
            "source_urn": "urn:li:dataset:(urn:li:dataPlatform:hive,logging_events,PROD)"
        }
    ],
    "paths": [
        {
            "source": "urn:li:dataset:(urn:li:dataPlatform:hive,logging_events,PROD)",
            "target": "urn:li:dataset:(urn:li:dataPlatform:dbt,b2fd91.ORDER_ENTRY_DB.analytics.order_details,PROD)",
            "hop": 1,
            "impact": 15.0
        },
        {
            "source": "urn:li:dataset:(urn:li:dataPlatform:dbt,b2fd91.ORDER_ENTRY_DB.analytics.order_details,PROD)",
            "target": "urn:li:dataset:(urn:li:dataPlatform:dbt,b2fd91.ORDER_ENTRY_DB.analytics.daily_sales_summary,PROD)",
            "hop": 2,
            "impact": 10.5
        }
    ]
}

MOCK_CATALOG = {
    "total_datasets": 52,
    "total_dashboards": 12,
    "total_charts": 45,
    "total_pipelines": 8,
    "total_ml_models": 4,
    "total_data_products": 3,
    "grade_distribution": {"A": 18, "B": 20, "C": 8, "D": 4, "F": 2},
    "tier_distribution": {"trusted": 38, "review": 10, "untrusted": 4}
}

MOCK_CONTRACTS = [
    {
        "id": 1,
        "target_urn": "urn:li:dataset:(urn:li:dataPlatform:dbt,b2fd91.ORDER_ENTRY_DB.analytics.order_details,PROD)",
        "name": "order_details",
        "artifact_type": "contract",
        "filename": "order_details_contract.yml",
        "content": "version: 2\nmodels:\n  - name: order_details\n    description: Active order details ledger\n    columns:\n      - name: order_id\n        tests:\n          - unique\n          - not_null\n",
        "grounding_evidence": ["Lineage dependency validation", "Integrity assertion checks"]
    },
    {
        "id": 2,
        "target_urn": "urn:li:dataset:(urn:li:dataPlatform:hive,logging_events,PROD)",
        "name": "logging_events",
        "artifact_type": "dbt_test",
        "filename": "logging_events_tests.yml",
        "content": "version: 2\nmodels:\n  - name: logging_events\n    columns:\n      - name: event_id\n        tests:\n          - not_null\n",
        "grounding_evidence": ["Missing primary key check", "No assertions configured"]
    }
]

MOCK_RUNS = [
    {
        "run_id": "run_9f8d7c",
        "started_at": datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=2),
        "completed_at": datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=1, minutes=50),
        "status": "completed",
        "assets_assessed": 52,
        "artifacts_generated": 6,
        "writebacks_completed": 156,
        "census_stats": MOCK_CATALOG,
        "pr_url": "https://github.com/praxis-data/ecommerce/pull/42",
        "pr_status": "open"
    },
    {
        "run_id": "run_0a1b2c",
        "started_at": datetime.datetime.now(timezone.utc) - datetime.timedelta(days=1, hours=2),
        "completed_at": datetime.datetime.now(timezone.utc) - datetime.timedelta(days=1, hours=1, minutes=52),
        "status": "completed",
        "assets_assessed": 50,
        "artifacts_generated": 8,
        "writebacks_completed": 150,
        "census_stats": MOCK_CATALOG,
        "pr_url": "https://github.com/praxis-data/ecommerce/pull/41",
        "pr_status": "merged"
    }
]

# Generate a list of 50+ mock dataset trust score details
MOCK_ASSETS = []
platform_choices = ["dbt", "hive", "mysql", "postgres"]
domain_choices = ["Analytics", "Logistics", "Customer", "Checkout", "Inventory"]

# Setup primary keys & details for 52 assets
for i in range(1, 53):
    platform = platform_choices[i % len(platform_choices)]
    domain = domain_choices[i % len(domain_choices)]
    
    if i == 1:
        urn = "urn:li:dataset:(urn:li:dataPlatform:dbt,b2fd91.ORDER_ENTRY_DB.analytics.order_details,PROD)"
        name = "order_details"
        score = 72.0
        grade = "C+"
        tier = "review"
    elif i == 2:
        urn = "urn:li:dataset:(urn:li:dataPlatform:hive,logging_events,PROD)"
        name = "logging_events"
        score = 33.8
        grade = "F"
        tier = "untrusted"
    else:
        # High and medium scores
        score = 95.0 - (i * 0.8)
        if score >= 75.0:
            grade = "A-" if score >= 85.0 else "B"
            tier = "trusted"
        elif score >= 55.0:
            grade = "C"
            tier = "review"
        else:
            grade = "D"
            tier = "untrusted"
            
    MOCK_ASSETS.append({
        "urn": urn if i in [1, 2] else f"urn:li:dataset:(urn:li:dataPlatform:{platform},{domain.lower()}.asset_{i},PROD)",
        "name": name if i in [1, 2] else f"asset_{i}",
        "platform": platform,
        "domain": domain,
        "composite_score": round(score, 1),
        "grade": grade,
        "tier": tier,
        "assessed_at": datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=1),
        "evidence_summary": f"Assessment completed for {name if i in [1, 2] else f'asset_{i}'}. Provenance and schema stability meet SLA baselines, with recent usage indicating high dataset freshness.",
        "dimensions": {
            "provenance": {"score": 90.0 if score >= 75 else 50.0, "evidence": ["Owner configured", "Description exists"]},
            "integrity": {"score": 80.0 if score >= 75 else 40.0, "evidence": ["No recent failures", "Quality checks passing"]},
            "stability": {"score": 100.0, "evidence": ["Schema keys valid"]},
            "lineage": {"score": 90.0 if score >= 75 else 30.0, "evidence": ["Upstream/downstream mapped"]},
            "adoption": {"score": 95.0 if score >= 75 else 50.0, "evidence": ["Frequent usage by downstream systems"]}
        }
    })
