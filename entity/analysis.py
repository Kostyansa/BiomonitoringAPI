from dataclasses import dataclass


@dataclass
class Analysis:
    bioobject_id: int
    img_path: str
    data: dict
