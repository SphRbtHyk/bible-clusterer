from pydantic import BaseSettings


class GNTConfig(BaseSettings):
    """Parent class for configuration files."""

    class Config:
        case_sensitive = False
        env_prefix = "GNT_"
    # Mongodb URI
    mongodb_uri: str = "mongodb://localhost:27017"
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
    # Mongodb password
    mongodb_password: str = None
    # Mongodb user
    mongodb_user: str = None

gnt_config = GNTConfig()
