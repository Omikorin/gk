#!/usr/bin/env python3
import math
import random
import numpy
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    random.seed()
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def x_axis(u, v):
    u2 = u * u
    u3 = u2 * u
    u4 = u3 * u
    u5 = u4 * u

    return (-90 * u5 + 225 * u4 - 270 * u3 + 180 * u ** 2 - 45 * u) * numpy.cos(numpy.pi * v)


def y_axis(u):
    u2 = u * u
    u3 = u2 * u
    u4 = u3 * u

    return 160 * u4 - 320 * u3 + 160 * u2 - 5


def z_axis(u, v):
    u2 = u * u
    u3 = u2 * u
    u4 = u3 * u
    u5 = u4 * u

    return (-90 * u5 + 225 * u4 - 270 * u3 + 180 * u2 - 45 * u) * numpy.sin(numpy.pi * v)


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    axes()

    spin(time * 180 / numpy.pi)


    for x in range(N - 1):
        for y in range(N - 1):
            glColor3f(colors[x][y][0], colors[x][y][1], colors[x][y][2])
            
            glBegin(GL_TRIANGLES)
            glVertex(points[x][y])
            glVertex(points[x + 1][y])
            glVertex(points[x][y + 1])
            glEnd()

            glColor3f(colors[x + 1][y + 1][0], colors[x + 1][y + 1][1], colors[x + 1][y + 1][2])

            glBegin(GL_TRIANGLES)
            glVertex(points[x + 1][y])
            glVertex(points[x][y + 1])
            glVertex(points[x + 1][y + 1])
            glEnd()
    


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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
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

    global N
    global points
    global colors

    N = 25
    points = numpy.zeros((N, N, 3))
    colors = numpy.zeros((N, N, 3))

    for x in range(N):
        for y in range(N):
            points[x][y][0] = x_axis(x / (N - 1), y / (N - 1)) 
            points[x][y][1] = y_axis(x / (N - 1)) 
            points[x][y][2] = z_axis(x / (N - 1), y / (N - 1))

            colors[x][y] = [random.random(), random.random(), random.random()]

    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
