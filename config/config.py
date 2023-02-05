from dataclasses import dataclass

from environs import Env


@dataclass
class Config:
    token: str
    admin_id: int


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)
    return Config(token=env("BOT_TOKEN"), admin_id=int(env("ADMIN_ID")))
