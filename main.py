#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

###############################################################
# portage de planet.c
from map import *
from animation import *
###############################################################
# Variables Globales
cpt = 0.1
cpt_x = 0
cpt_y = 0
cpt_z = 0
# postitionement
x_pos, y_pos, z_pos = 0, 0, 0

eye_angle_x, eye_angle_y, eye_angle_z = 315, 50, 210
eye = [0, 0, 50]
center = [0, 0, 0]
up_vec = [1, 1, 0]

# Couleurs
diffuse = [0.7, 0.7, 0.7, 1.0]
specular = [0.001, 0.001, 0.001, 1.0]
pos = [1, 1, -1, 0]

anim = False
anim_bouton = False
quadric = None
DISPLAY_GRID = False

# matrice
############################################################## #

matrice_map = generation_matrice(10)
matrice_map = tukey(matrice_map, 2)

# matrice_map=tukey(matrice_map)


def init():
    global quadric, pos
    # clear color to black
    glClearColor(0.0, 0.0, 0.0, 0.0)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_POSITION, pos)

    glEnable(GL_LIGHTING)
    glShadeModel(GL_FLAT)

    quadric = gluNewQuadric()

    gluQuadricDrawStyle(quadric, GLU_FILL)


def display():
    global cpt_x, cpt_y, cpt_z, anim, anim_bouton
    global eye_angle_x, eye_angle_y, eye_angle_z
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()

    # Modelisation du repere othonorme
    # centre
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 1, 1, 1.0])
    gluSphere(quadric, 0.2, 20, 16)

    # Axe z Bleu
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0, 0, 1, 1.0])
    gluCylinder(quadric, 0.1, 0.1, 1000, 20, 16)

    # Axe y Vert
    glPushMatrix()
    glRotatef(90, 0, 1, 0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0, 1, 0, 1.0])
    gluCylinder(quadric, 0.1, 0.1, 1000, 20, 16)
    glPopMatrix()

    # Axe x Rouge
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 0, 0, 1.0])
    gluCylinder(quadric, 0.1, 0.1, 1000, 20, 16)
    glPopMatrix()

    # creation de la map
    grid_map(matrice_map)

    # decaleage de camera decalage de la bouel
    if anim == True and anim_bouton == False:
        # nouvel coord
        cpt_x = cpt_x+cpt+0.1
        cpt_y = cpt_y+cpt
        cpt_z = 0

        animation(cpt_x, cpt_y, matrice_map)

    else:

        animation(cpt_x, cpt_y, matrice_map)
    glPopMatrix()

    glutSwapBuffers()

    glLoadIdentity()

    gluLookAt(*eye, *center, *up_vec)
    glRotatef(eye_angle_y, 0.0, 1.0, 0.0)
    glRotatef(eye_angle_x, 1.0, 0, 0)
    glRotatef(eye_angle_z, 0, 0, 1.0)
    anim_bouton = False


def reshape(width, height):

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width/height, 1, 500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*eye, *center, *up_vec)


def keyboard(key, x, y):
    global DISPLAY_GRID, eye_angle_x, eye_angle_y, eye_angle_z, center, up_vec
    global pos, anim, anim_bouton
    if key == b'g':
        DISPLAY_GRID = not DISPLAY_GRID
        anim_bouton = True
    # Zoom deplacement de la cam era selon l'axe z
    elif key == b'z':
        eye[2] -= 1

        anim_bouton = True
    elif key == b's':
        eye[2] += 1
        anim_bouton = True
    # #deplacement de la camera selon l'axe y
    elif key == b'q':
        eye[1] += 1
        anim_bouton = True
    elif key == b'd':
        eye[1] -= 1
        anim_bouton = True
    # deplacement de la camera selon l'axe x
    elif key == b'w':
        anim_bouton = True
        eye[0] += 1
    elif key == b'x':
        eye[0] -= 1
        anim_bouton = True

    # Deplacement du centre sur l'axe x
    elif key == b'f':
        center[0] -= 1
        anim_bouton = True
    elif key == b'h':
        center[0] += 1
        anim_bouton = True
    # Rotation sur l'axe z
    elif key == b'Q':
        eye_angle_z = (eye_angle_z + 5) % 360
        anim_bouton = True
    elif key == b'D':
        eye_angle_z = (eye_angle_z - 5) % 360

        anim_bouton = True

    # Rotation sur l'axe y
    elif key == b'Z':
        eye_angle_y = (eye_angle_y + 5) % 360
        anim_bouton = True
    elif key == b'S':
        eye_angle_y = (eye_angle_y - 5) % 360
        anim_bouton = True

    # Rotation sur l'axe x
    elif key == b'W':
        eye_angle_x = (eye_angle_x + 5) % 360
        anim_bouton = True
    elif key == b'X':
        eye_angle_x = (eye_angle_x - 5) % 360
        anim_bouton = True
    elif key == b'a':
        anim = True
        anima(0)


# faire transaltion

    elif key == b'\033':
        glutDestroyWindow(WIN)
        sys.exit(0)
    glutPostRedisplay()  # indispensable en Python


def anima(cptt):
    global cpt
    glutTimerFunc(100, anima, 0)
    display()


###############################################################
# MAIN

if __name__ == "__main__":
    # initialization GLUT library
    glutInit()
    # initialization display mode RGBA mode and double buffered window
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA | GLUT_DEPTH)

    # creation of top-level window
    WIN = glutCreateWindow('projet')

    glutReshapeWindow(800, 800)

    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)

    init()

    glutMainLoop()
