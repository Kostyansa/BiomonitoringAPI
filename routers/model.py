from fastapi import APIRouter
from fastapi.responses import JSONResponse

from controller.model import ModelController

model_router = APIRouter(prefix='/prediction',
                         tags=['prediction'])

model_controller = ModelController()


@model_router.get('/ping/', response_class=JSONResponse)
async def ping():
    response = model_controller.ping()
    return response
