from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy import select

from config.engine import InternalDatabaseConfiguration
from entity import Analysis


class AnalysisRepository:
    __slots__ = "engine"
    instance = None

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls(InternalDatabaseConfiguration.get_engine())
        return cls.instance

    def save(self, analysis: Analysis):
        with Session(self.engine, expire_on_commit=False) as session:
            session.add(analysis)
            session.commit()


