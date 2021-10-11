from gnt_api.config import gnt_config
from gnt_core.database import MongoConnector
from gnt_nlp_utils.clusterer import GNTClusterer

database_instance = MongoConnector(
    mongo_database=gnt_config.mongodb_database,
    mongo_host=gnt_config.mongodb_host,
    mongo_port=gnt_config.mongodb_port)

gnt_clusterer = GNTClusterer()
