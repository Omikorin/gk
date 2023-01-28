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

draw_normals = False

N = 15
vertices = []
normals = []

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
    global vertices, normals

    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    create_light_source(GL_LIGHT0, light_ambient, light_diffuse, light_specular, light_position)
    create_light_source(GL_LIGHT1, light_ambient_1, light_diffuse_1, light_specular_1, light_position_1)

    vertices, normals = init_egg_vertices_and_normals(N)


def calc_normal(u, v):
    xu = calc_xu(u, v)
    xv = calc_xv(u, v)

    yu = calc_yu(u, v)
    yv = calc_yv(u, v)
    
    zu = calc_zu(u, v)
    zv = calc_zv(u, v)

    return [yu * zv - zu * zv,
            zu * xv - xu * zv,
            xu * yv - yu * xv]


def normalize_vector(v):
    d = numpy.sqrt(pow(v[0], 2) + pow(v[1], 2) + pow(v[2], 2))

    if d == 0:
        return [0, 0, 0]

    x = v[0] / d
    y = v[1] / d
    z = v[2] / d

    return [x, y, z]    


def init_egg_vertices_and_normals(N):
    n_quantum = 1.0 / (N - 1)
    u_values = []
    v_values = []
    f_values = [[[0] * 3 for i in range(N)] for j in range(N)]
    normals = [[[0] * 3 for i in range(N)] for j in range(N)]

    u_values.append(0.0)
    v_values.append(0.0)

    for i in range(1, N - 1):
        u_values.append(i * n_quantum)
        v_values.append(i * n_quantum)

    u_values.append(1.0)
    v_values.append(1.0)

    for i in range(N):
        for j in range(N):
            f_values[i][j][0] = x(u_values[i], v_values[j])
            f_values[i][j][1] = y(u_values[i])
            f_values[i][j][2] = z(u_values[i], v_values[j])

            normal = calc_normal(u_values[i], v_values[j])
            normals[i][j] = normalize_vector(normal)

    return f_values, normals


def shutdown():
    pass


def x(u, v):
    return (-90 * pow(u, 5) + 225 * pow(u, 4) - 270 * pow(u, 3) + 180 * pow(u, 2) - 45 * u) * numpy.cos(numpy.pi * v)


def y(u):
    return 160 * pow(u, 4) - 320 * pow(u, 3) + 160 * pow(u, 2) - 5


def z(u, v):
    return (-90 * pow(u, 5) + 225 * pow(u, 4) - 270 * pow(u, 3) + 180 * pow(u, 2) - 45 * u) * numpy.sin(numpy.pi * v)


def calc_xu(u, v):
    return (-450 * pow(u, 4) + 900 * pow(u, 3) - 810 * pow(u, 2) + 360 * u - 45) * numpy.cos(numpy.pi * v)


def calc_xv(u, v):
    return numpy.pi * (90 * pow(u, 5) - 225 * pow(u, 4) + 270 * pow(u, 3) - 180 * pow(u, 2) + 45 * u) * numpy.sin(numpy.pi * v)


def calc_yu(u, v):
    return 640 * pow(u, 3) - 960 * pow(u, 2) + 320 * u


def calc_yv(u, v):
    return 0


def calc_zu(u, v):
    return (-450 * pow(u, 4) + 900 * pow(u, 3) - 810 * pow(u, 2) + 360 * u - 45) * numpy.sin(numpy.pi * v)


def calc_zv(u, v):
    return -numpy.pi * (90 * pow(u, 5) - 225 * pow(u, 4) + 270 * pow(u, 3) - 180 * pow(u, 2) + 45 * u) * numpy.cos(numpy.pi * v)


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


def normal_vertice(point, vector):
    x = point[0] + vector[0]
    y = point[1] + vector[1]
    z = point[2] + vector[2]
    
    return [x, y, z]


def egg():
    global vertices, normals, N

    for i in range(N):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glNormal3f(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])
            glVertex3f(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])

            if i + 1 < N:
                glNormal3f(vertices[i + 1][j][0], vertices[i + 1][j][1], vertices[i + 1][j][2])
                glVertex3f(vertices[i + 1][j][0], vertices[i + 1][j][1], vertices[i + 1][j][2])

        glEnd()
    
    if draw_normals:
        glBegin(GL_LINES)
        for i in range(N):
            for j in range(N):
                normal = normals[i][j]

                if i > N / 2 - 1:
                    normal[0] = -normal[0]
                    normal[1] = -normal[1]
                    normal[2] = -normal[2] 

                glVertex3fv(normal)
                glVertex3fv(normal_vertice(normal, vertices[i][j]))
        glEnd()


def render(time):
    global theta, phi
    global light_position, light_position_1
    global light_modifier_index

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # gluLookAt(viewer[0], viewer[1], viewer[2],
    #           0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle * movement_speed
        phi += delta_y * pix2angle * movement_speed

        theta %= 360
        phi %= 360

        calc_light_position(light_position, 5, theta, phi, GL_LIGHT0)
        calc_light_position(light_position_1, 5, theta, phi + numpy.pi, GL_LIGHT1)

    light_sphere(light_position)
    light_sphere(light_position_1)

    egg()

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


def keyboard_key_callback(window, key, scancode, action, mods) -> None:
    global light_modifier_index
    global light_modifier
    global pressed_a, pressed_d, pressed_s
    global draw_normals
    
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

    if key == GLFW_KEY_N and action == GLFW_PRESS:
        draw_normals = not draw_normals


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
