import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from shape import *
from transform import *


WIDTH = 800
HEIGHT = 600

DRAW_LINE = 0
DRAW_POLYGON = 1
SELECT_MODE = 2

current_mode = DRAW_LINE

canvas_shapes = []
temporary_shape = None

selected_shape_index = -1

active_color = Color3f(1.0, 0.1, 0.1)


def screen_to_world(mx, my):
    x = mx - WIDTH / 2
    y = HEIGHT / 2 - my
    return Point2D(x, y)


def select_shape_at(point):

    for i in range(len(canvas_shapes) - 1, -1, -1):

        shape = canvas_shapes[i]

        if not shape.vertices:
            continue

        min_x = min(v.x for v in shape.vertices) + shape.translate_x
        max_x = max(v.x for v in shape.vertices) + shape.translate_x

        min_y = min(v.y for v in shape.vertices) + shape.translate_y
        max_y = max(v.y for v in shape.vertices) + shape.translate_y

        padding = 15

        if (
            min_x - padding <= point.x <= max_x + padding
            and
            min_y - padding <= point.y <= max_y + padding
        ):
            return i

    return -1


