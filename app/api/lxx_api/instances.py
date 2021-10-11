from lxx_api.config import lxx_config
from lxx_core.database import MongoConnector
from lxx_nlp_utils.clusterer import LXXClusterer

database_instance = MongoConnector(
    mongo_database=lxx_config.mongodb_database,
    mongo_host=lxx_config.mongodb_host,
    mongo_port=lxx_config.mongodb_port)

lxx_clusterer = LXXClusterer()
