#!/usr/bin/env python3
import math
import random
import sys

from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    random.seed()
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)


def shutdown():
    pass


def draw_triangle(x, y, a, color, invert=False):
    glColor3f(color, color, color)

    glBegin(GL_TRIANGLES)

    glVertex2f(x - a / 2, y)

    if invert:
        glVertex2f(x, y - (a * math.sqrt(3)) / 2)
    else:
        glVertex2f(x, y + (a * math.sqrt(3)) / 2)

    glVertex2f(x + a / 2, y)

    glEnd()


def render(time, self_similarity):
    glClear(GL_COLOR_BUFFER_BIT)

    # main triangle
    draw_triangle(0.0, -80.0, 200.0, 1.0)

    # list of current triangles
    triangles = [(0.0, -80.0, 200.0)]

    for _ in range(self_similarity):
        new_triangles = []

        for triangle in triangles:
            x = triangle[0]
            a = triangle[2] / 2
            y = triangle[1] + (a * math.sqrt(3)) / 2
            
            draw_triangle(x, y, a, 0.0, True)

            new_triangles.append((x, y, a))
            new_triangles.append((x - a / 2, y - (a * math.sqrt(3)) / 2, a))
            new_triangles.append((x + a / 2, y - (a * math.sqrt(3)) / 2, a))
        
        # next iteration will print all of these
        triangles = new_triangles

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main(self_similarity):
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), self_similarity)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main(6)
