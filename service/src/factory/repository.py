from sqlalchemy.engine import Engine
import logging

from config.engine import InternalDatabaseConfiguration
from repository.bioobject import BioobjectRepository
from exception.uninitialized import FailedInitialization


class RepositoryFactory:
    instance = None

    def __init__(self, internal_engine: Engine) -> None:
        self.internal_engine = internal_engine
        self.bioobject_repository = None

    def bioobject(self):
        if self.bioobject_repository is None:
            self.bioobject_repository = BioobjectRepository(self.internal_engine)
        return self.bioobject_repository

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            try:
                cls.instance = RepositoryFactory(InternalDatabaseConfiguration.get_engine())
            except Exception as exc:
                logging.warning("Failled to initialize Weather Repository")
                raise FailedInitialization("WeatherRepository") from exc
        return cls.instance
