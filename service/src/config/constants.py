import os


class Constants:
    IMG_PATH = "picture/"
    DB_URL = f'postgresql://{os.environ.get("POSTGRES_USER")}:{os.environ.get("POSTGRES_PASSWORD")}@{os.environ.get("DBHOST")}/postgres'
