from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile
from uuid import uuid4

from service.bioobject import BioobjectService
from entity import Bioobject
from factory.service import ServiceFactory


class BioobjectController:
    __slots__ = ['bioobject_service']

    def __init__(self, bioobject_service: BioobjectService) -> None:
        self.bioobject_service = bioobject_service

    def get(self, id: str):
        return self.bioobject_service.get(id)

    def get_all(self):
        return self.bioobject_service.get_all()

    def save(self, name, file):
        content = file.read()
        bioobject_entity = Bioobject(uuid=name)
        return self.bioobject_service.save(bioobject_entity, content)


factory = ServiceFactory.get_instance()
bioobject_router = APIRouter(prefix='/bioobject', tags=['bioobject'])
bioobject_controller = BioobjectController(factory.bioobject())


@bioobject_router.get('/get/', response_class=JSONResponse)
async def get(id: str):
    response = bioobject_controller.get(id)
    return response


@bioobject_router.get('/get/', response_class=JSONResponse)
async def get():
    response = bioobject_controller.get_all()
    return response


@bioobject_router.post('/save/', response_class=JSONResponse)
async def save(name: str = uuid4().hex, file: UploadFile = File(...)):
    response = bioobject_controller.save(name, file)
    return response
