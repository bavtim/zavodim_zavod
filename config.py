from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
    )

    bot_token: str = Field("6325869033:AAFMAsaluUPEpRYSonu05cFrfnMcaf866S8", env="BOT_TOKEN")


settings = Settings()
