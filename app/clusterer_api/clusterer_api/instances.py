from clusterer_api.config import clusterer_config
from clusterer_core.database import MongoConnector
from clusterer_nlp_utils.clusterer import BibleClusterer


database_instance = MongoConnector(
    mongo_uri=clusterer_config.mongodb_uri,
    mongo_database=clusterer_config.mongodb_database,
    mongo_host=clusterer_config.mongodb_host,
    mongo_port=clusterer_config.mongodb_port,
    mongo_user=clusterer_config.mongodb_user,
    mongo_password=clusterer_config.mongodb_password)



bible_clusterer = BibleClusterer()
