from sqlalchemy.engine import Engine
import logging

from config.engine import InternalDatabaseConfiguration
from repository.bioobject import BioobjectRepository
from repository.analysis import AnalysisRepository


class RepositoryFactory:
    instance = None

    def __init__(self, internal_engine: Engine) -> None:
        self.internal_engine = internal_engine
        self.bioobject_repository = None
        self.analysis_repository = None

    def bioobject(self):
        if self.bioobject_repository is None:
            self.bioobject_repository = BioobjectRepository(self.internal_engine)
        return self.bioobject_repository

    def analysis(self):
        if self.analysis_repository is None:
            self.analysis_repository = AnalysisRepository(self.internal_engine)
        return self.analysis_repository

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = RepositoryFactory(InternalDatabaseConfiguration.get_engine())
        return cls.instance
