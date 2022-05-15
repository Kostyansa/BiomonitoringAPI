from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile
from uuid import uuid4

from service.bioobject import BioobjectService
from entity.bioobject import Bioobject


class BioobjectController:
    __slots__ = ['bioobject_service']

    def __init__(self, bioobject_service: BioobjectService) -> None:
        self.bioobject_service = bioobject_service

    def get(self, id: int):
        return self.bioobject_service.get(id)

    def save(self, name, file):
        content = file.read()
        bioobject_entity = Bioobject(name, content=content)
        return self.bioobject_service.save(bioobject_entity)


bioobject_router = APIRouter(prefix='/bioobject', tags=['bioobject'])
bioobject_controller = BioobjectController()


@bioobject_router.get('/get/', response_class=JSONResponse)
async def get(id: int):
    response = None
    return response


@bioobject_router.post('/save/', response_class=JSONResponse)
async def save(name: str = uuid4().hex, file: UploadFile = File(...)):
    response = bioobject_controller.save(name, file)
    return response
