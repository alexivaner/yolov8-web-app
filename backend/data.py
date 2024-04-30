from typing import Union
from pydantic import BaseModel


class Flags(BaseModel):
    name: str
    tag: str
    
class BasePoint(BaseModel):
    x: float
    y: float
    z: Union[float, None] = None
    
class Keypoint(BaseModel):
    name: str
    point: BasePoint
    flags: Union[list[Flags], None] = None

class Skeleton(BaseModel):
    name: str
    points: list[Keypoint]

class Line(BaseModel):
    name: str
    p1: BasePoint
    p2: BasePoint
    
class Rectangle(BaseModel):
    name: str
    c: BasePoint
    wh: BasePoint
    
class Polygon(BaseModel):
    name: str
    vertices: list[BasePoint]