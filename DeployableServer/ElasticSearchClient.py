import json
from PyQt5 import QtCore

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk


def create_quotes_index(client, index):
    # we will use user on several places
    create_index_body = {
        # 'settings': {
        #     # just one shard, no replicas for testing
        #     'number_of_shards': 1,
        #     'number_of_replicas': 0,
        #
        #     # custom analyzer for analyzing file paths
        #     'analysis': {
        #         'analyzer': {
        #             'my_eng_analyzer' : {
        #                 'type' : 'custom',
        #                 'tokenizer': 'standard',
        #                 'filter': ['lowercase', 'my_stemmer']
        #             }
        #         },
        #         "filter": {
        #             "my_stemmer": {
        #                 "type": "stemmer",
        #                 "name": "english"
        #             }
        #         }
        #     },
        # },
        # 'mappings': {
        #     'line': {
        #             'type': 'string',
        #             'analyzer': 'my_eng_analyzer'
        #         }
        # }

        "settings": {
            'number_of_shards': 1,
            'number_of_replicas': 0,
                "analysis": {
                    "filter": {
                        "custom_english_stemmer": {
                            "type": "stemmer",
                            "name": "english"
                        },
                        "trigrams_filter": {
                            "type": "ngram",
                            "min_gram": 3,
                            "max_gram": 3
                        }
                    },
                    "analyzer": {
                        "custom_lowercase_stemmed": {
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "custom_english_stemmer",
                                "trigrams_filter"
                            ]
                        }
                    }
                }
        },
        "mappings": {
            "index": {
                "properties": {
                    "line":{
                        "type": "string",
                        "fields": {
                            "english":{
                                "type": "string",
                                "analyzer": "custom_lowercase_stemmed"
                            }
                        },
                        "index_options": "offsets"
                    }
                }
            }
        }
    }

    # create empty index
    try:
        client.indices.create(
            index=index,
            body=create_index_body,
        )
    except TransportError as e:
        # ignore already existing index
        if e.error == 'index_already_exists_exception':
            pass
        else:
            raise


class ElasticSearchClient(object):
    def __init__(self):
        self.es = Elasticsearch()
        self.index = 'index'

    def loadJSONFile(self):
        with open('C:\\Users\\tjdaw\PycharmProjects\\theofficequotesdb-backend\misc\quote_db_s06.json', 'rb') as fp:
            return json.load(fp)

    def indexStats(self):
        return self.es.indices.stats()

    def indexProgress(self):
        return self.es.indices.stats()['_all']['primaries']['indexing']['index_total']

    def indexES(self):
        quotes = self.loadJSONFile()['lines']
        line_ids = quotes.keys()
        create_quotes_index(self.es, self.index)
        for id in line_ids:
            self.es.index(index=self.index, doc_type='us_office_lines', id=id, body=quotes[id])

    def search(self, text):
        res = self.es.search(index=self.index, body=self.boolMatchQuery(text))
        res_list = []
        i = 0
        for hit in res['hits']['hits']:
            res_list.append(hit['_source'])
            i += 1
        return res_list

    def matchQuery(self, term):
        return \
            {
                "query": {
                    "match": {
                        "line": {
                            "query": term,
                            "fuzziness": "AUTO",
                            "operator": "and"
                        }
                    }
                },
                "highlight": {
                    "fields": {
                        "line": {}
                    }
                }
            }

    def boolMatchQuery(self, term):
        return {"query": {
            "bool": {
                "must": {
                    "match": {
                        "line": {
                            "query": term,
                            "minimum_should_match": "30%"
                        }
                    }
                },
                "should": {
                    "match_phrase": {
                        "line": {
                            "query": term,
                            "slop": 50
                        }
                    }
                }
            }
        }}

es = ElasticSearchClient()

es.indexES()

# # print(els.indexProgress())
#
# class Worker(QtCore.QThread):
#
#     updateProgress = QtCore.pyqtSignal(int)
#
#     def __init__(self, es):
#         QtCore.QThread.__init__(self)
#         self.es = es
#
#     def run(self):
#
#         #self.es.indices.delete("index")
#         quotes = self.loadJSONFile()['lines']
#         line_ids = quotes.keys()
#         create_quotes_index(self.es, self.es.index)
#         for id in line_ids:
#             self.es.index(index=self.es.index, doc_type='us_office_lines', id=id, body=quotes[id])
#             indexed = self.es.indices.stats()['_all']['primaries']['indexing']['index_total']
#             self.updateProgress.emit(indexed)

# els = ElasticSearchClient()
# worker = Worker(els)
# worker.start()
# while worker.isRunning():
#     print(worker.updateProgress.connect())
"""
curl -XGET 'localhost:9200/index/_analyze?pretty' -H 'Content-Type: application/json' -d'
{
    "line": "The quick & brown fox",
    "analyzer": "custom_lowercase_stem  
"""
{
    "settings": {
        "analysis": {
            "filter": {
                "custom_english_stemmer": {
                    "type": "stemmer",
                    "name": "english"
                }
            },
            "analyzer": {
                "custom_lowercase_stemmed": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "custom_english_stemmer"
                    ]
                }
            }
        }
    },
    "mappings": {
        "test": {
            "properties": {
                "text": {
                    "type": "string",
                    "analyzer": "custom_lowercase_stemmed"
                }
            }
        }
    }
}
