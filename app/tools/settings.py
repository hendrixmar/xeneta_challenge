import os
from dotenv import load_dotenv


class Settings:

    load_dotenv()
    config = {
        key: os.getenv(key)
        for key in ["DB_USER", "DB_PASS", "DB_HOST", "DB_NAME", "DB_PORT"]
    }
    DB_USER = config.get("DB_USER")
    DB_PASS = config.get("DB_PASS")
    DB_HOST = config.get("DB_HOST")
    DB_PORT = config.get("DB_PORT")
    DB_NAME = config.get("DB_NAME")
    DATABASE_URL = f"postgresql+psycopg2://{config.get('DB_USER')}:{config.get('DB_PASS')}@{config.get('DB_HOST')}:{config.get('DB_PORT')}/{config.get('DB_NAME')}"


# The first argument of the sorted will do the fuzzy search using process.extract for each of the dictionary
# of the list, and it will return a list of tuples that are formed by the following elements
# (value: str, score: float | int, key: str)
# it will automatically search for each value of the dictionary and will return a list
# of each value with their corresponding score and the key of the value in sorted order
# , list_of_ports: list[dict[str: str]]
