from pydantic_settings import BaseSettings
import configparser


class AppSettings(BaseSettings):
    db_config_path: str = "./config.ini"


def get_settings():
    return AppSettings()


def read_db_config():
    parser = configparser.ConfigParser()
    settings = get_settings()
    with open(settings.db_config_path) as f:
        parser.read_file(f)
    return parser
