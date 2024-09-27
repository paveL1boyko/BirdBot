from pydantic_settings import BaseSettings, SettingsConfigDict

logo = """
BIRDX - Telegram bot for crypto trading
"""


class BaseBotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="allow")

    API_ID: int
    API_HASH: str

    SLEEP_BETWEEN_START: list[int] = [10, 20]
    SESSION_AC_DELAY: int = 3
    ERRORS_BEFORE_STOP: int = 5
    USE_PROXY_FROM_FILE: bool = True
    ADD_LOCAL_MACHINE_AS_IP: bool = False

    RANDOM_SLEEP_TIME: int = 8

    BOT_SLEEP_TIME: list[int] = [30000, 35000]

    REF_ID: str = "1092379081"
    base_url: str = "https://birdx-api.birds.dog"
    bot_name: str = "birdx2_bot"
    bot_app: str = "birdx"


class Settings(BaseBotSettings): ...


config = Settings()
