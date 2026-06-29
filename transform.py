from OpenGL.GL import *


def apply_shape_transformations(shape):
    center = shape.get_center()

    glTranslatef(shape.translate_x, shape.translate_y, 0)

    glTranslatef(center.x, center.y, 0)

    glRotatef(shape.rotation_angle, 0, 0, 1)

    glScalef(shape.scale_x, shape.scale_y, 1)

    glTranslatef(-center.x, -center.y, 0)
