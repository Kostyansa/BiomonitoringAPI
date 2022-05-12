from sqlalchemy.engine import Engine
from sqlalchemy import text

from entity import bioobject


class UserRepository:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    @staticmethod
    def rowmapper(row):
        if row:
            return bioobject.Bioobject(row['id', row['name'], row['path']])
