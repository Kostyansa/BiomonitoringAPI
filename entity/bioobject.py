from dataclasses import dataclass
import cv2

@dataclass
class Bioobject:
    id: int
    name: str
    path: str

    def img(self):
        return cv2.imread(self.path)