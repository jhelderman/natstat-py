from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    natstat_api_key: str = ""
    natstat_req_per_hour: int = 500
    loglevel: str = "INFO"


CONFIG = Config()
