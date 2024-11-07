from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://postgres:wb_base@10.0.100.10:5432/
        return (f"postgresql+psycopg://"
                f"{self.DB_USER}"
                f":{self.DB_PASS}"
                f"@{self.DB_HOST}"
                f":{self.DB_PORT}"
                f"/{self.DB_NAME}"
                )

    model_config = SettingsConfigDict(env_file="new_pars/.env")


settings = Settings()
