from sqlalchemy.engine import Engine
from sqlalchemy import text

from entity.bioobject import Bioobject


class BioobjectRepository:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    @staticmethod
    def rowmapper(row):
        if row:
            return Bioobject()

    def save(self, bioobject_entity: Bioobject):
        self.engine.execute()