import os
from typing import Union, List

from pydantic import validator, BaseSettings
from functools import lru_cache


def check_environment():
    return os.environ.get('ENVIRONMENT', 'dev')


class APISettings(BaseSettings):
    class Config:
        env_file = f".env_{check_environment()}"
        case_sensitive = True

    ENVIRONMENT: str
    DEBUG: bool = True

    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    TITLE: str = 'Test Demo'
    DESCRIPTION: str = ''

    PROJECT_NAME: str
    PROJECT_VERSION: str
    SERVER_NAME: str = ''

    API_BASE_PATH: str
    API_NAME: str

    CORS_ORIGINS: Union[str, List[str]] = ['*']
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: Union[str, List[str]] = ['*']
    CORS_HEADERS: Union[str, List[str]] = ['*']

    # Test Case Database: Only for challenges or testing
    DATABASE_STRING: str

    WORKERS: int = 5

    # Validators
    @validator('CORS_ORIGINS', 'CORS_METHODS', 'CORS_HEADERS', pre=True, check_fields=False)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            v = v.replace('[', '').replace(']', '')

            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


@lru_cache()
def get_api_settings() -> APISettings:
    return APISettings()
