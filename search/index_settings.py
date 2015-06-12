from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

SEARCH_SETTINGS = settings.SEARCH


def get_mappings():
    mappings = {}
    if not SEARCH_SETTINGS:
        msg = "There are no search settings in the project settings"
        raise ImproperlyConfigured(msg)
    autocomplete_models = SEARCH_SETTINGS.get(
        'AUTOCOMPLETE_MODEL_FIELDS')

    for model_conf in autocomplete_models:
        for single_model in model_conf.get('models'):
            fields_conf = {
                "properties": {}
            }

            for field in single_model.get("fields"):
                field_mapping = {
                    "type": "string",
                    "index_analyzer": "autocomplete",
                    "search_analyzer": "autocomplete"
                }
                fields_conf["properties"][field] = field_mapping
            mappings[single_model.get("name")] = fields_conf
    return mappings


INDEX_SETTINGS = {
    "settings": {
        "index": {
            "creation_date": "1434101603851",
            "uuid": "HHzIptOYTxOowFCIxY7_eA",
            "number_of_replicas": "1",
            "analysis": {
                "analyzer": {
                    "autocomplete": {
                        "type": "custom",
                        "filter": [
                            "standard",
                            "lowercase",
                            "stop",
                            "kstem",
                            "ngram"
                        ],
                        "tokenizer": "standard"
                    },
                    "default": {
                        "type": "snowball"
                    }
                },
                "filter": {
                    "ngram": {
                        "min_gram": "4",
                        "type": "ngram",
                        "max_gram": "15"
                    }
                }
            },
            "number_of_shards": "5",
            "version": {
                "created": "1040001"
            }
        }
    },
    "mappings": get_mappings()
}
