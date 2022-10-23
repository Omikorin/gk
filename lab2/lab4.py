#!/usr/bin/env python3
import random
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    random.seed()
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def draw_rect(x, y, width, height, color):
    glColor3f(color, color, color)

    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x, y + height)
    glVertex2f(x + width, y)
    glVertex2f(x, y + height)
    glVertex2f(x + width, y + height)
    glEnd()


def render(time, color, self_similarity):
    glClear(GL_COLOR_BUFFER_BIT)

    # main rect
    draw_rect(-100.0, -100.0, 200.0, 200.0, color)

    # list of current rectangles
    rectangles = [(-100.0, -100.0, 200.0, 200.0)]

    for _ in range(self_similarity):
        new_rects = []

        for rect in rectangles:
            x, y = rect[0], rect[1]
            width, height = rect[2] / 3, rect[3] / 3

            draw_rect(x + width, y + height, width, height, 0.0)

            new_rects.append((x, y, width, height))
            new_rects.append((x + width, y, width, height))
            new_rects.append((x + width * 2, y, width, height))
            new_rects.append((x, y + height, width, height))
            new_rects.append((x + width * 2, y + height, width, height))
            new_rects.append((x, y + height * 2, width, height))
            new_rects.append((x + width, y + height * 2, width, height))
            new_rects.append((x + width * 2, y + height * 2, width, height))

        # next iteration will print all of these
        rectangles = new_rects

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

    color = random.random()

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), color, self_similarity)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main(4)
