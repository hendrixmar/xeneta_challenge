import os
from dotenv import load_dotenv


class Settings:
    load_dotenv()
    # It will retrieve any env variable that end with user pass, and db
    # in case you want to switch to mysql you can use this format
    # MYSQL_DB, MYSQL_USER, MYSQL_PASS
    config = {
        key.split("_").pop(): value for key, value in os.environ.items()
        if any(key.endswith(ending) for ending in ["USER", "PASS", "DB"])
    }

    DB_USER = config.get("USER")
    DB_PASS = config.get("PASS")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = config.get("DB")
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# The first argument of the sorted will do the fuzzy search using process.extract for each of the dictionary
# of the list, and it will return a list of tuples that are formed by the following elements
# (value: str, score: float | int, key: str)
# it will automatically search for each value of the dictionary and will return a list
# of each value with their corresponding score and the key of the value in sorted order
# , list_of_ports: list[dict[str: str]]
