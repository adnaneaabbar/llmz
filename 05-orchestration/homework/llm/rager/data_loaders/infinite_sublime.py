from typing import Dict, List, Union

import numpy as np
from elasticsearch import Elasticsearch

@data_loader
def search(*args, **kwargs) -> List[Dict]:
    query = "When is the next cohort?"
    connection_string = kwargs.get('connection_string', 'http://localhost:9200')
    index_name = "documents_20240813_2919"
    source = kwargs.get('source', "cosineSimilarity(params.query_vector, 'embedding') + 1.0")
    top_k = kwargs.get('top_k', 5)
    chunk_column = kwargs.get('chunk_column', 'content')

    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields"
                    }
                },
                "filter": {
                    "term": {
                        "course": "llm-zoomcamp"
                    }
                }
            }
        }
    }

    es_client = Elasticsearch(connection_string)

    response = es_client.search(
        index=index_name,
        body=search_query
    )

    return [hit['_source'] for hit in response['hits']['hits']]