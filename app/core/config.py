from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str
    HOST: str
    PORT: str
    DB: str

    class Config:
        env_file = ".env"
