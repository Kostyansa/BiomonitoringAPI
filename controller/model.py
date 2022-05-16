import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi import File, UploadFile
from pydantic import BaseModel
from uuid import uuid4

from service.cluster import ModelService
from service.bioobject import BioobjectService
from entity.bioobject import Bioobject


class BioobjectDao(BaseModel):
    pass


class ModelController:
    __slots__ = ['model_service', 'bioobject_service']

    def __init__(self, model_service: ModelService, bioobject_service) -> None:
        self.model_service = model_service
        self.bioobject_service = bioobject_service

    @staticmethod
    def ping() -> str:
        result_bool_obj: str = 'pong'
        return result_bool_obj

    async def analyse(self, file):
        logging.debug(type(file))
        content = await file.read()
        name = uuid4().hex
        bioobject = Bioobject(name, content=content)
        self.bioobject_service.save(bioobject)
        result = self.model_service.analyse(bioobject)
        return result


model_router = APIRouter(tags=['model'])
model_controller = ModelController(ModelService(), BioobjectService())


@model_router.get('/ping/', response_class=JSONResponse)
async def ping():
    response = model_controller.ping()
    return response


@model_router.post('/analyse/')
async def analyse(file: UploadFile = File(...)):
    response = await model_controller.analyse(file)
    return response
