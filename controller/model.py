class ModelController:
    __slots__ = ['model']

    def __init__(self, model_service) -> None:
        self.model = model_service

    @staticmethod
    def ping() -> str:
        result_bool_obj: str = 'pong'
        return result_bool_obj
