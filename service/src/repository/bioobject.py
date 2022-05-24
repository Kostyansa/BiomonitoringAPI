from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy import select

from config.engine import InternalDatabaseConfiguration
from entity import Bioobject


class BioobjectRepository:
    __slots__ = "engine"
    instance = None

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = cls(InternalDatabaseConfiguration.get_engine())
        return cls.instance

    def save(self, bioobject: Bioobject):
        with Session(self.engine, expire_on_commit=False) as session:
            session.add(bioobject)
            session.commit()
            session.expunge(bioobject)
            return bioobject

    def get_all(self):
        with Session(self.engine) as session:
            statement = select(Bioobject)
            bioobjects = session.scalars(statement).all()
            session.expunge_all()
            return bioobjects

    def get(self, name: str):
        with Session(self.engine) as session:
            statement = select(Bioobject).where(Bioobject.uuid.is_(name))
            bioobject = session.scalars(statement).one()
            session.expunge(bioobject)
            return bioobject


