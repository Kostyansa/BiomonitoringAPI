from fastapi import APIRouter
from fastapi.responses import JSONResponse

import service.cluster as model


class ModelController:
    __slots__ = ['model_service']

    def __init__(self, model_service: model.ModelService) -> None:
        self.model_service = model_service

    @staticmethod
    def ping() -> str:
        result_bool_obj: str = 'pong'
        return result_bool_obj

    def analyse(self, bioobject):
        result = self.model_service.analyse(bioobject)
        return result


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
