SEARCH_DATASETS_QUERY = """
query searchDatasets($input: SearchInput!) {
    search(input: $input) {
        start
        count
        total
        searchResults {
            entity {
                urn
                type
                ... on Dataset {
                    name
                    platform { name }
                    properties { name description }
                    ownership {
                        owners {
                            owner {
                                ... on CorpUser { urn username }
                                ... on CorpGroup { urn name }
                            }
                            type
                        }
                    }
                    globalTags { tags { tag { urn name } } }
                    glossaryTerms { terms { term { urn name } } }
                    schemaMetadata {
                        fields {
                            fieldPath
                            type
                            description
                            glossaryTerms { terms { term { urn name } } }
                            globalTags { tags { tag { urn name } } }
                        }
                    }
                    deprecation { deprecated note }
                    editableProperties { description }
                    domain { domain { urn properties { name } } }
                    assertions(start: 0, count: 50) {
                        assertions {
                            urn
                            info { type }
                            runEvents(status: COMPLETE, limit: 1) {
                                total
                                runEvents { status timestampMillis result { type } }
                            }
                        }
                    }
                    usageStats(range: MONTH) {
                        aggregations {
                            totalSqlQueries
                            uniqueUserCount
                        }
                    }
                    health {
                        type
                        status
                        message
                    }
                    subTypes { typeNames }
                }
            }
        }
    }
}
"""

GET_ENTITY_DETAIL_QUERY = """
query getEntity($urn: String!) {
    dataset(urn: $urn) {
        urn
        name
        platform { name properties { displayName } }
        properties { name description qualifiedName created { time } lastModified { time } customProperties { key value } }
        editableProperties { description }
        ownership {
            owners {
                owner {
                    ... on CorpUser { urn username editableProperties { displayName } }
                    ... on CorpGroup { urn name }
                }
                type
            }
        }
        globalTags { tags { tag { urn properties { name description } } } }
        glossaryTerms { terms { term { urn properties { name definition } } } }
        domain { domain { urn properties { name } } }
        schemaMetadata {
            fields {
                fieldPath
                nativeDataType
                type
                description
                nullable
                glossaryTerms { terms { term { urn } } }
                globalTags { tags { tag { urn } } }
            }
            primaryKeys
        }
        deprecation { deprecated note decommissionTime }
        assertions(start: 0, count: 100) {
            total
            assertions {
                urn
                info { type description }
                runEvents(status: COMPLETE, limit: 5) {
                    total
                    runEvents { status timestampMillis result { type } }
                }
            }
        }
        usageStats(range: MONTH) {
            aggregations {
                totalSqlQueries
                uniqueUserCount
            }
        }
        health { type status message }
        subTypes { typeNames }
        institutionalMemory { elements { url description } }
    }
}
"""

GET_LINEAGE_QUERY = """
query getLineage($input: SearchAcrossLineageInput!) {
    searchAcrossLineage(input: $input) {
        searchResults {
            entity { 
                urn 
                type 
                ... on Dataset { name platform { name } } 
                ... on Dashboard { dashboardId properties { name } } 
                ... on Chart { chartId properties { name } } 
            }
            degree
        }
    }
}
"""
