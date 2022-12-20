import os
from dotenv import load_dotenv


class Settings:
    load_dotenv()
    # It will retrieve any env variable that end with user pass, and db
    # in case you want to switch to mysql you can use this format
    # MYSQL_DB, MYSQL_USER, MYSQL_PASS
    config = {
        key.split("_").pop(): value
        for key, value in os.environ.items()
        if any(key.endswith(ending) for ending in ["USER", "PASSWORD", "DB"])
    }

    DB_USER = config.get("USER")
    DB_PASS = config.get("PASSWORD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = config.get("DB")
    DATABASE_URL = (
        f"postgresql+psycopg2://" f"{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
