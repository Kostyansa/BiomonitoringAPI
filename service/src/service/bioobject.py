import os

from entity import Bioobject
from repository.bioobject import BioobjectRepository
from config.constants import Constants


class BioobjectService:
    __slots__ = "bioobject_repository"

    def __init__(self, bioobject_repository: BioobjectRepository):
        self.bioobject_repository = bioobject_repository

    @staticmethod
    def build_path(name):
        return os.path.join(Constants.IMG_PATH, name)

    def get_all(self):
        return self.bioobject_repository.get_all()

    def get(self, uuid: str):
        return self.bioobject_repository.get(uuid)

    def save(self, bioobject_entity: Bioobject, content):
        with open(self.build_path(bioobject_entity.uuid), "wb") as f:
            f.write(content)
        return self.bioobject_repository.save(bioobject_entity)


