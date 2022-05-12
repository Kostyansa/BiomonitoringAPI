from service.bioobject import BioobjectService
from entity.bioobject import Bioobject
from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import JSONResponse


class BioobjectSavingDto(BaseModel):
    name: str
    image: str


class BioobjectController:
    __slots__ = ['bioobject_service']

    def __init__(self, bioobject_service: BioobjectService) -> None:
        self.bioobject_service = bioobject_service

    def get(self, id: int):
        return self.bioobject_service.get(id)

    def save(self, bioobject_dao: BioobjectSavingDto):
        path = self.bioobject_service.save_image(bioobject_dao.image)
        bioobject_entity = Bioobject(bioobject_dao.name, path)
        return self.bioobject_service.save(bioobject_entity)


bioobject_router = APIRouter(prefix='bioobject', tags=['bioobject'])
bioobject_controller = BioobjectController()


@bioobject_router.get('/get/', response_class=JSONResponse)
async def get(id: int):
    response = None
    return response


@bioobject_router.post('/save/', response_class=JSONResponse)
async def analyse(bioobject_entity: BioobjectSavingDto):
    response = None
    return response
