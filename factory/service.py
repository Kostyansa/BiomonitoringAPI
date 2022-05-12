import logging

from factory.repository import RepositoryFactory


class ServiceFactory:
    instance = None

    def __init__(self, repository_factory: RepositoryFactory) -> None:
        self.repository_factory = repository_factory

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = ServiceFactory(RepositoryFactory.get_instance())
        return cls.instance
