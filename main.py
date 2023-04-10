import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from LoadMesh import *
from Camera import *

pygame.init()

# project settings
screen_width = 1000
screen_height = 800
background_color = (0, 0, 0, 1)
drawing_color = (1, 1, 1, 1)

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Lab')
mesh = LoadMesh("Lab2.obj", GL_LINE_LOOP)
right_side_computers = LoadMesh("RightComputers.obj", GL_TRIANGLES)
right_side_keyboards = LoadMesh("RightKeyboards.obj", GL_LINE_LOOP)
right_side_benches = LoadMesh("RightBenches.obj", GL_LINE_LOOP)
right_side_cabinets = LoadMesh("RightCabinets.obj", GL_TRIANGLES)

left_side_computers = LoadMesh("LeftComputers.obj", GL_TRIANGLES)
left_side_keyboards = LoadMesh("LeftKeyboards.obj", GL_LINE_LOOP)
left_side_benches = LoadMesh("LeftBenches.obj", GL_LINE_LOOP)
left_side_cabinets = LoadMesh("LeftCabinets.obj", GL_TRIANGLES)

fans = LoadMesh("Fans.obj", GL_LINE_LOOP)
fans2 = LoadMesh("Fans2.obj", GL_LINE_LOOP)
camera = Camera()

def initialise():
    glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
    glColor(drawing_color)

    # projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 1000.0)

def init_camera():
    # modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)
    camera.update(screen.get_width(), screen.get_height())

def draw_world_axes():
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor(1, 0, 0)
    glVertex3d(-1000, 0, 0)
    glVertex3d(1000, 0, 0)
    glColor(0, 1, 0)
    glVertex3d(0, 1000, 0)
    glVertex3d(0, -1000, 0)
    glColor(0, 0, 1)
    glVertex3d(0, 0, 1000)
    glVertex3d(0, 0, -1000)
    glEnd()

    glColor(1, 1, 1)



def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    init_camera()
    glPushMatrix()
    # glTranslated(0, 1, -5)
    # glTranslated(0, -2, 0)
    draw_world_axes()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, 0)
    mesh.draw()
    fans.draw()
    fans2.draw()
    glColor(1, 0, 0)
    left_side_computers.draw()
    right_side_computers.draw()
    glColor(1, 0, 1)
    left_side_cabinets.draw()
    right_side_cabinets.draw()
    glColor(1, 1, 1)
    # left_side_keyboards.draw()
    # right_side_keyboards.draw()
    right_side_benches.draw()
    left_side_benches.draw()
    glPopMatrix()

    # sphere = gluNewQuadric()
    # glColor(1, 0, 0)
    # glPushMatrix()
    # glTranslatef(1, 0, 0)
    # glScalef(8, 8, 8)
    # glTranslatef(0, 0.04, 0)
    # glTranslatef(-0.06, 0, 0)
    # gluSphere(sphere, 0.05, 10, 10)
    # glPopMatrix()


done = False
initialise()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
            if event.key == K_SPACE:
                pygame.mouse.set_visible(False)
                pygame.event.set_grab(True)
    display()
    pygame.display.flip()

pygame.quit()
