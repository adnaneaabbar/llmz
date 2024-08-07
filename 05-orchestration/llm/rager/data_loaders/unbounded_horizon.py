from typing import Dict, List, Union

import numpy as np
from elasticsearch import Elasticsearch, exceptions

SAMPLE_EMBEDDING = [
    [
    -0.20360085368156433,
    -0.3315528631210327,
    0.1444639265537262,
    -0.2442994862794876,
    0.05381917580962181,
    0.35884490609169006,
    0.0768091008067131,
    0.3295135200023651,
    0.013814866542816162,
    -0.017688507214188576,
    0.0075402106158435345,
    0.19742168486118317,
    -0.3771721124649048,
    0.03890518844127655,
    0.0499124750494957,
    0.12816651165485382,
    0.26722267270088196,
    -0.033373039215803146,
    0.04269425943493843,
    -0.08838776499032974,
    0.10090106725692749,
    0.24658042192459106,
    0.34495121240615845,
    0.021342532709240913,
    -0.13778556883335114,
    0.02999582514166832,
    0.4098532497882843,
    0.16116981208324432,
    0.22140976786613464,
    -0.09313986450433731,
    0.04749007895588875,
    -0.07585576176643372,
    0.32948777079582214,
    -0.19205760955810547,
    0.4720313549041748,
    -0.5495747923851013,
    0.7632429003715515,
    -0.06338296085596085,
    -0.42839184403419495,
    -0.16051389276981354,
    -0.15714329481124878,
    0.1562311351299286,
    0.1581667959690094,
    -0.08543067425489426,
    -0.1268032342195511,
    -0.055866703391075134,
    -0.024340754374861717,
    0.07555469870567322,
    -0.14874017238616943,
    0.010647554881870747,
    -0.47354984283447266,
    0.20203140377998352,
    0.04140305146574974,
    0.050302714109420776,
    0.03931433707475662,
    -0.25732043385505676,
    -0.2822035551071167,
    -0.36849769949913025,
    0.21846742928028107,
    -0.3808503746986389,
    -0.20695313811302185,
    0.08556049317121506,
    0.32011672854423523,
    -0.3063648045063019,
    -0.06404615938663483,
    0.13114820420742035,
    -0.33483269810676575,
    -0.33441779017448425,
    -0.027159372344613075,
    0.12156020849943161,
    0.048102863132953644,
    0.11652272939682007,
    0.1403800994157791,
    -0.12363354861736298,
    0.5879209041595459,
    -0.016437601298093796,
    0.03461925685405731,
    -0.2422015219926834,
    0.16396456956863403,
    -0.17811550199985504,
    0.0488409623503685,
    -0.06525808572769165,
    -0.16440047323703766,
    -0.0833543911576271,
    -0.08574052900075912,
    0.25954943895339966,
    0.1687183827161789,
    0.22222137451171875,
    -0.30138716101646423,
    0.23375806212425232,
    -0.05617089569568634,
    0.04484473541378975,
    0.3517010509967804,
    0.1831461787223816,
    -0.2622159421443939,
    -0.05530490726232529
    ]
]

@data_loader
def search(*args, **kwargs) -> List[Dict]:
    connection_string = kwargs.get('connection_string', 'http://localhost:9200')
    index_name = kwargs.get('index_name', 'documents')
    source = kwargs.get('source', "cosineSimilarity(params.query_vector, 'embedding') + 1.0")
    top_k = kwargs.get('top_k', 5)
    chunk_column = kwargs.get('chunk_column', 'content')

    query_embedding = None
    if len(args):
        query_embedding = args[0]
    if not query_embedding:
        query_embedding = SAMPLE_EMBEDDING[0]

    if isinstance(query_embedding, np.ndarray):
        query_embedding = query_embedding.tolist()

    script_query = {
        "script_score" : {
            "query" : {
                "match_all" : {}
            },
            "script" : {
                "source" : source,
                "params" : {
                    "query_vector" : query_embedding
                }
            }
        }
    }

    es_client = Elasticsearch(connection_string)
    try:
        response = es_client.search(
            index=index_name,
            body={
                "size" : top_k,
                "query" : script_query,
                "_source" : [chunk_column]
            }
        )

        print("Raw response from ES :", response)

        return [hit['_source'][chunk_column] for hit in response['hits']['hits']]

    except exceptions.BadRequestError as e:
        print(f"BadRequestError: {e.info}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []