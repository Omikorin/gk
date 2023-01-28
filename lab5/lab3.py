#!/usr/bin/env python3
import numpy
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0
movement_speed = 1 / 20

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0


mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [5.0, 0.0, 0.0, 1.0]

light_ambient_1 = [0.1, 0.1, 0.0, 1.0]
light_diffuse_1 = [0.9, 0.0, 0.5, 1.0]
light_specular_1 = [1.0, 0.0, 0.0, 1.0]
light_position_1 = [-5.0, 0.0, 0.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

light_modifier_index = -1
light_modifier = 0.0

pressed_a = False
pressed_d = False
pressed_s = False


def create_light_source(light_index, light_ambient, light_diffuse, light_specular, light_position):
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glLightfv(light_index, GL_AMBIENT, light_ambient)
    glLightfv(light_index, GL_DIFFUSE, light_diffuse)
    glLightfv(light_index, GL_SPECULAR, light_specular)
    glLightfv(light_index, GL_POSITION, light_position)

    glLightf(light_index, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(light_index, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(light_index, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(light_index)


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    create_light_source(GL_LIGHT0, light_ambient, light_diffuse, light_specular, light_position)
    create_light_source(GL_LIGHT1, light_ambient_1, light_diffuse_1, light_specular_1, light_position_1)


def shutdown():
    pass


def light_sphere(position):
    glTranslate(position[0], position[1], position[2])

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)

    glTranslate(-position[0], -position[1], -position[2])


def calc_light_position(position, radius, theta, phi, name):
    position[0] = radius * numpy.cos(theta) * numpy.cos(phi)
    position[1] = radius * numpy.sin(phi)
    position[2] = radius * numpy.sin(theta) * numpy.cos(phi)

    glLightfv(name, GL_POSITION, position)


def sphere():
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)


def render(time):
    global theta, phi
    global light_position, light_position_1
    global light_modifier_index

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle * movement_speed
        phi += delta_y * pix2angle * movement_speed

        theta %= 360
        phi %= 360

        calc_light_position(light_position, 5, theta, phi, GL_LIGHT0)
        calc_light_position(light_position_1, 5, theta, phi + numpy.pi, GL_LIGHT1)

    light_sphere(light_position)
    light_sphere(light_position_1)

    sphere()

    if light_modifier != 0.0:
        modify_light()

    glFlush()


def modify_light():
    global light_modifier_index
    global light_modifier
    global light_ambient_1, light_diffuse_1, light_specular_1
    global pressed_a, pressed_d, pressed_s

    if pressed_a:
        new_prop = light_ambient_1[light_modifier_index] + light_modifier

        if new_prop >= 0.0 and new_prop <= 1.0:
            light_ambient_1[light_modifier_index] = new_prop
            print(f"ambient {light_modifier_index} ({light_modifier}): {new_prop}")
    
    if pressed_d:
        new_prop = light_diffuse_1[light_modifier_index] + light_modifier

        if new_prop >= 0.0 and new_prop <= 1.0:
            light_diffuse_1[light_modifier_index] = new_prop
            print(f"diffusion {light_modifier_index} ({light_modifier}): {new_prop}")

    if pressed_s:
        new_prop = light_specular_1[light_modifier_index] + light_modifier

        if new_prop >= 0.0 and new_prop <= 1.0:
            light_specular_1[light_modifier_index] = new_prop
            print(f"specular {light_modifier_index} ({light_modifier}): {new_prop}")


    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient_1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse_1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular_1)

    light_modifier = 0.0


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


def keyboard_key_callback(window, key, scancode, action, mods) -> None:
    global light_modifier_index
    global light_modifier
    global pressed_a, pressed_d, pressed_s
    
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        light_modifier_index = 0
    
    if key == GLFW_KEY_2 and action == GLFW_PRESS:
        light_modifier_index = 1

    if key == GLFW_KEY_3 and action == GLFW_PRESS:
        light_modifier_index = 2

    if key == GLFW_KEY_4 and action == GLFW_PRESS:
        light_modifier_index = 3

    if key == GLFW_KEY_A and action == GLFW_PRESS:
        pressed_a = True
        pressed_d = False
        pressed_s = False

    if key == GLFW_KEY_D and action == GLFW_PRESS:
        pressed_a = False
        pressed_d = True
        pressed_s = False

    if key == GLFW_KEY_S and action == GLFW_PRESS:
        pressed_a = False
        pressed_d = False
        pressed_s = True

    if key == GLFW_KEY_UP and action == GLFW_PRESS:
        light_modifier = 0.1

    if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
        light_modifier = -0.1


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
    global right_mouse_button_pressed

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
