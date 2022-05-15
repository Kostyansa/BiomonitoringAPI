import entity.bioobject as bioobject
from repository.bioobject import BioobjectRepository


class BioobjectService:

    def __init__(self):
        pass

    @staticmethod
    def build_path(name):
        return f"./{name}"

    def get_all(self):
        return None

    def get(self, id: int):
        return None

    def save(self, bioobject_entity: bioobject.Bioobject):
        with open(self.build_path(bioobject_entity.name), "wb") as f:
            f.write(bioobject_entity.content)
        pass
