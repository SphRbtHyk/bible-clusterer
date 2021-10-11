from pydantic import BaseSettings


class GNTConfig(BaseSettings):
    """Parent class for configuration files."""

    class Config:
        case_sensitive = False
        env_prefix = "GNT_"
    # Host of the mongo db
    mongodb_host: str = "localhost"
    # Port of the mongo db
    mongodb_port: int = 27017
    # Name of the mongo database
    mongodb_database: str = "gnt"
    # Host of API
    api_host: str = "localhost"
    # Port of the API
    api_port: int = 5000


gnt_config = GNTConfig()
