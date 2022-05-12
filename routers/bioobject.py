from fastapi import APIRouter
from fastapi.responses import JSONResponse

from controller.bioobject import BioobjectController

bioobject_router = APIRouter(prefix='bioobject', tags=['bioobject'])

bioobject_controller = BioobjectController()


@bioobject_router.get('/get/', response_class=JSONResponse)
async def get(id: int):
    response = None
    return response


@bioobject_router.post('/save/', response_class=JSONResponse)
async def analyse(bioobject_entity):
    response = None
    return response
