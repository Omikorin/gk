#!/usr/bin/env python3
import sys

import numpy

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

eye_x = viewer[0]
eye_y = viewer[1]
eye_z = viewer[2]

theta = 0.0
phi = 0.0
pix2angle = 1.0
pix2scale = 0.05

scale = 1.0
R = 10.0

up_x = 0.0
up_y = 1.0
up_z = 0.0

at_x = 0.0
at_y = 0.0
at_z = 0.0

shift_x = 0.0
shift_y = 0.0
shift_z = 0.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0

w_pressed = False
a_pressed = False
s_pressed = False
d_pressed = False

move_speed = 0.05



def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


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


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def calc_eye_x(R, theta, phi):
    return R * numpy.cos(theta * numpy.pi / 180) * numpy.cos(phi * numpy.pi / 180)


def calc_eye_y(R, theta, phi):
    return R * numpy.sin(phi * numpy.pi / 180)


def calc_eye_z(R, theta, phi):
    return R * numpy.sin(theta * numpy.pi / 180) * numpy.cos(phi * numpy.pi / 180)


def piramid(x, y, z, a):
    half = a

    # rectangle
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1.0, 0.5, 0.8)
    glVertex3f(x - half, y - half, z - half)
    glVertex3f(half + x, y - half, z - half)
    glVertex3f(half + x, y - half, z + half)
    glVertex3f(x - half, y - half, z + half)
    glEnd()

    # walls
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0.5, 0.7, 0.8)
    glVertex3f(x, half + y, z)
    glVertex3f(x - half, y - half, z - half)
    glVertex3f(half + x, y - half, z - half)
    glVertex3f(half + x, y - half, z + half)
    glVertex3f(x - half, y - half, z + half)
    glVertex3f(x - half, y - half, z - half)
    glEnd()


def sierpinski_piramid(x, y, z, iterations, length):
    half = length / 2

    if iterations > 1:
        sierpinski_piramid(x - half, y - half, z - half, iterations - 1, half)
        sierpinski_piramid(x + half, y - half, z - half, iterations - 1, half)
        sierpinski_piramid(x - half, y - half, z + half, iterations - 1, half)
        sierpinski_piramid(x + half, y - half, z + half, iterations - 1, half)
        sierpinski_piramid(x, y + half, z, iterations - 1, half)
    else:
        piramid(x, y, z, length)


def update_movement(x, y, z):
    global w_pressed, s_pressed, a_pressed, d_pressed
    global shift_x, shift_y, shift_z
    global move_speed

    if w_pressed:
        shift_x -= x * move_speed
        shift_y -= y * move_speed
        shift_z -= z * move_speed
    
    if s_pressed:
        shift_x += x * move_speed
        shift_y += y * move_speed
        shift_z += z * move_speed

    if a_pressed:
        shift_x -= (up_y * z - up_z * y) * move_speed
        shift_y -= (up_z * x - up_x * z) * move_speed
        shift_z -= (up_x * y - up_y * x) * move_speed

    if d_pressed:
        shift_x += (up_y * z - up_z * y) * move_speed
        shift_y += (up_z * x - up_x * z) * move_speed
        shift_z += (up_x * y - up_y * x) * move_speed


def render(time):
    global theta
    global phi
    global scale
    global R

    global eye_x, eye_y, eye_z
    global up_x, up_y, up_z
    global at_x, at_y, at_z

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    if theta < 0 or theta >= 360:
        theta %= 360

    if phi < 0 or phi >= 360:
        phi %= 360


    if phi > 90 and phi < 270:
        up_y = -1.0
    else:
        up_y = 1.0

    eye_x = calc_eye_x(R, theta, phi)
    eye_y = calc_eye_y(R, theta, phi)
    eye_z = calc_eye_z(R, theta, phi)

    x = at_x - eye_x
    y = at_y - eye_y
    z = at_z - eye_z

    update_movement(x, y, z)

    gluLookAt(eye_x, eye_y, eye_z, at_x, at_y, at_z, up_x, up_y, up_z)

    glTranslate(shift_x, shift_y, shift_z)

    axes()
    sierpinski_piramid(0, 0, 0, 3, 5.0)

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global w_pressed
    global s_pressed
    global a_pressed
    global d_pressed

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_W and (action == GLFW_PRESS or action == GLFW_REPEAT):
        w_pressed = True

    if key == GLFW_KEY_W and action == GLFW_RELEASE:
        w_pressed = False

    if key == GLFW_KEY_S and (action == GLFW_PRESS or action == GLFW_REPEAT):
        s_pressed = True

    if key == GLFW_KEY_S and action == GLFW_RELEASE:
        s_pressed = False

    if key == GLFW_KEY_A and (action == GLFW_PRESS or action == GLFW_REPEAT):
        a_pressed = True

    if key == GLFW_KEY_A and action == GLFW_RELEASE:
        a_pressed = False

    if key == GLFW_KEY_D and (action == GLFW_PRESS or action == GLFW_REPEAT):
        d_pressed = True

    if key == GLFW_KEY_D and action == GLFW_RELEASE:
        d_pressed = False


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
