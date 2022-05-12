from dataclasses import dataclass


@dataclass
class Analysis:
    bioobject_id: int
    data: dict
