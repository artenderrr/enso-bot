import os
from dotenv import load_dotenv

load_dotenv()

class EnvVarMissingError(Exception):
    def __init__(self, missing_var: str) -> None:
        message = f"Missing environment variable: \"{missing_var}\""
        super().__init__(message)

class Config:
    def __init__(self) -> None:
        self.bot_token = self._load_env_var("BOT_TOKEN")
        self.admin_user_ids = self._load_admin_user_ids()
        self.db_url = self._load_env_var("DB_URL")

    def _load_env_var(self, env_var_key: str) -> str:
        env_var_value = os.getenv(env_var_key)
        if not env_var_value:
            raise EnvVarMissingError(env_var_key)
        return env_var_value

    def _load_admin_user_ids(self) -> list[int]:
        admin_user_ids = self._load_env_var("ADMIN_USER_IDS")
        return [int(user_id) for user_id in admin_user_ids.split(",")]

bot_config = Config()
