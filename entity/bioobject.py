from dataclasses import dataclass
from typing import Optional
import cv2

@dataclass
class Bioobject:
    name: str
    img_path: str
    id: Optional[int] = None

    def img(self):
        return cv2.imread(self.img_path)