from typing import Optional

from service.bioobject import BioobjectService
from entity.bioobject import Bioobject
from pydantic import BaseModel

class BioobjectSavingDto(BaseModel):
    name: str
    image: str


class BioobjectController:
    __slots__ = ['bioobject']

    def __init__(self, bioobject_service: BioobjectService) -> None:
        self.bioobject_service = bioobject_service

    def get(self, id: int):
        return self.bioobject_service.get(id)

    def save(self, bioobject_dao: BioobjectSavingDto):
        path = self.bioobject_service.save_image(bioobject_dao.image)
        bioobject_entity = Bioobject(bioobject_dao.name, path)
        return self.bioobject_service.save(bioobject_entity)
