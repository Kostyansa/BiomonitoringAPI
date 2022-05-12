import service.cluster as model

class ModelController:
    __slots__ = ['model']

    def __init__(self, model_service: model.ModelService) -> None:
        self.model = model_service

    @staticmethod
    def ping() -> str:
        result_bool_obj: str = 'pong'
        return result_bool_obj

    def analyse(self, bioobject):
        result = self.model.analyse(bioobject)
        return result
