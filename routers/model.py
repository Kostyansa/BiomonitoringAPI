from fastapi import APIRouter
from fastapi.responses import JSONResponse

from controller.model import ModelController

model_router = APIRouter(tags=['model'])

model_controller = ModelController()


@model_router.get('/ping/', response_class=JSONResponse)
async def ping():
    response = model_controller.ping()
    return response


@model_router.post('/analyse/', response_class=JSONResponse)
async def analyse():
    response = model_controller.analyse()
    return None
