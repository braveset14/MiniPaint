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


def draw_shape(shape, selected=False):

    glPushMatrix()

    apply_shape_transformations(shape)

    if selected:
        glColor3f(1.0, 0.84, 0.0)
        glLineWidth(4)
    else:
        glColor3f(shape.color.r, shape.color.g, shape.color.b)
        glLineWidth(2)

    if shape.shape_type == LINE:

        glBegin(GL_LINES)

        for v in shape.vertices:
            glVertex2f(v.x, v.y)

        glEnd()

    elif shape.shape_type == POLYGON:

        glBegin(GL_LINE_LOOP)

        for v in shape.vertices:
            glVertex2f(v.x, v.y)

        glEnd()

    glPopMatrix()


def display():

    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()

    for i, shape in enumerate(canvas_shapes):

        draw_shape(
            shape,
            current_mode == SELECT_MODE and i == selected_shape_index
        )

    if temporary_shape and temporary_shape.vertices:

        glColor3f(
            active_color.r,
            active_color.g,
            active_color.b
        )

        glLineWidth(2)

        if current_mode == DRAW_LINE:
            glBegin(GL_LINES)
        else:
            glBegin(GL_LINE_STRIP)

        for v in temporary_shape.vertices:
            glVertex2f(v.x, v.y)

        glEnd()

    pygame.display.flip()


def setup():

    glClearColor(0.12, 0.12, 0.15, 1)

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    gluOrtho2D(
        -WIDTH / 2,
        WIDTH / 2,
        -HEIGHT / 2,
        HEIGHT / 2
    )

    glMatrixMode(GL_MODELVIEW)


def main():

    global current_mode
    global temporary_shape
    global selected_shape_index

    pygame.init()

    pygame.display.set_mode(
        (WIDTH, HEIGHT),
        DOUBLEBUF | OPENGL
    )

    setup()

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == QUIT:
                running = False

            elif event.type == MOUSEBUTTONDOWN:

                mx, my = pygame.mouse.get_pos()

                world = screen_to_world(mx, my)

                if current_mode == SELECT_MODE:

                    selected_shape_index = select_shape_at(world)

                elif current_mode == DRAW_LINE:

                    if temporary_shape is None:
                        temporary_shape = Shape(LINE)

                    temporary_shape.vertices.append(world)

                    if len(temporary_shape.vertices) == 2:

                        canvas_shapes.append(temporary_shape)

                        temporary_shape = None

                elif current_mode == DRAW_POLYGON:

                    if temporary_shape is None:
                        temporary_shape = Shape(POLYGON)

                    temporary_shape.vertices.append(world)

            elif event.type == KEYDOWN:
                print("Key pressed:", event.key)

                if event.key == K_l:

                    current_mode = DRAW_LINE

                    selected_shape_index = -1

                    temporary_shape = None

                elif event.key == K_p:

                    current_mode = DRAW_POLYGON

                    selected_shape_index = -1

                    temporary_shape = None

                elif event.key == K_s:

                    current_mode = SELECT_MODE

                    temporary_shape = None

                elif event.key == K_RETURN:

                    if (
                        current_mode == DRAW_POLYGON
                        and
                        temporary_shape
                        and
                        len(temporary_shape.vertices) >= 3
                    ):
                        canvas_shapes.append(temporary_shape)
                        temporary_shape = None

                elif (
                    event.key == K_r
                    and
                    selected_shape_index != -1
                ):

                    canvas_shapes[
                        selected_shape_index
                    ].rotation_angle += 5

                elif (
                    event.key in [K_EQUALS, K_PLUS]
                    and
                    selected_shape_index != -1
                ):

                    shape = canvas_shapes[selected_shape_index]

                    shape.scale_x += 0.1
                    shape.scale_y += 0.1

                elif (
                    event.key == K_MINUS
                    and
                    selected_shape_index != -1
                ):

                    shape = canvas_shapes[selected_shape_index]

                    shape.scale_x = max(0.1, shape.scale_x - 0.1)
                    shape.scale_y = max(0.1, shape.scale_y - 0.1)
                elif event.key in (K_DELETE, K_BACKSPACE):

                    if selected_shape_index != -1:
                        del canvas_shapes[selected_shape_index]
                        selected_shape_index = -1
                elif (
                    selected_shape_index != -1
                    and
                    current_mode == SELECT_MODE
                ):

                    shape = canvas_shapes[selected_shape_index]

                    step = 5

                    if event.key == K_UP:
                        shape.translate_y += step

                    elif event.key == K_DOWN:
                        shape.translate_y -= step

                    elif event.key == K_LEFT:
                        shape.translate_x -= step

                    elif event.key == K_RIGHT:
                        shape.translate_x += step
                elif event.key == K_c:
                    canvas_shapes.clear()

                    temporary_shape = None

                    selected_shape_index = -1

                
                
        display()

    pygame.quit()


if __name__ == "__main__":
    main()