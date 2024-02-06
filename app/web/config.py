import typing
from dataclasses import dataclass

import yaml

if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class SessionConfig:
    key: str


@dataclass
class UserConfig:
    email: str
    password: str


@dataclass
class DatabaseConfig:
    host: str = "0.0.0.0"
    port: int = 5432
    user: str = "lidia"
    password: str = "qwerty123"
    database: str = "project"


@dataclass
class Config:
    user: UserConfig
    session: SessionConfig = None
    database: DatabaseConfig = None


def setup_config(app: "Application", config_path: str):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    app.config = Config(
        session=SessionConfig(
            key=raw_config["session"]["key"],
        ),
        user=UserConfig(
            email=raw_config["user"]["email"],
            password=raw_config["user"]["password"],
        ),
        database=DatabaseConfig(**raw_config["database"]),
    )
