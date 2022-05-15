from dataclasses import dataclass
from typing import Optional


@dataclass
class Bioobject:
    name: str
    content: bytes = None
    id: Optional[int] = None
