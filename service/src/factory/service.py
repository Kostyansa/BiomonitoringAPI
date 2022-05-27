from factory.repository import RepositoryFactory
from service.bioobject import BioobjectService
from service.cluster import ModelService


class ServiceFactory:
    instance = None

    def __init__(self, repository_factory: RepositoryFactory) -> None:
        self.repository_factory = repository_factory
        self.bioobject_service = None
        self.model_service = None

    def model(self):
        if self.model_service is None:
            self.model_service = ModelService(self.repository_factory.analysis())
        return self.model_service

    def bioobject(self):
        if self.bioobject_service is None:
            self.bioobject_service = BioobjectService(self.repository_factory.bioobject())
        return self.bioobject_service

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = ServiceFactory(RepositoryFactory.get_instance())
        return cls.instance
