import logging
import json

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile
from uuid import uuid4

from service.bioobject import BioobjectService
from entity import Bioobject
from factory.service import ServiceFactory


class BioobjectController:
    __slots__ = ['bioobject_service']

    @staticmethod
    def mapper(bioobject):
        return json.dumps({
            "uuid": bioobject.uuid,
            "original": f'/picture/{bioobject.uuid}',
            "analysis": bioobject.analysis.content if bioobject.analysis is not None else None
        })

    def __init__(self, bioobject_service: BioobjectService) -> None:
        self.bioobject_service = bioobject_service

    def get(self, id: str):
        bioobject = self.bioobject_service.get(id)
        return self.mapper(bioobject)

    def get_all(self):
        bioobjects = self.bioobject_service.get_all()
        return list(map(self.mapper, bioobjects))

    def save(self, name, file):
        content = file.read()
        bioobject_entity = Bioobject(uuid=name)
        return self.bioobject_service.save(bioobject_entity, content)


factory = ServiceFactory.get_instance()
bioobject_router = APIRouter(prefix='/bioobject', tags=['bioobject'])
bioobject_controller = BioobjectController(factory.bioobject())


@bioobject_router.get('/get', response_class=JSONResponse)
async def get(id: str):
    try:
        response = bioobject_controller.get(id)
        logging.debug(response)
        return response
    except Exception as exc:
        logging.debug(exc)
        return None


@bioobject_router.get('/', response_class=JSONResponse)
async def get_all():
    try:
        response = bioobject_controller.get_all()
        logging.debug(response)
        return response
    except Exception as exc:
        logging.debug(exc)
        return None
