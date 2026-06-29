from dataclasses import dataclass, field
from typing import List


LINE = 0
POLYGON = 1


@dataclass
class Point2D:
    x: float
    y: float


@dataclass
class Color3f:
    r: float
    g: float
    b: float


@dataclass
class Shape:
    shape_type: int
    vertices: List[Point2D] = field(default_factory=list)
    color: Color3f = field(default_factory=lambda: Color3f(1.0, 0.1, 0.1))

    translate_x: float = 0.0
    translate_y: float = 0.0

    rotation_angle: float = 0.0

    scale_x: float = 1.0
    scale_y: float = 1.0

    def get_center(self):
        if not self.vertices:
            return Point2D(0.0, 0.0)

        cx = sum(v.x for v in self.vertices) / len(self.vertices)
        cy = sum(v.y for v in self.vertices) / len(self.vertices)

        return Point2D(cx, cy)