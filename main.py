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

mesh = LoadMesh("assets/Lab2.obj", GL_TRIANGLES)
mesh.load_texture("textures/img3_teste.jpg")

right_side_computers = LoadMesh("assets/RightComputers.obj", GL_TRIANGLES)
right_side_computers.load_texture("textures/PcsWallpaper.jpg")

right_side_keyboards = LoadMesh("assets/RightKeyboards.obj", GL_LINE_LOOP)

right_side_benches = LoadMesh("assets/RightBenches.obj", GL_TRIANGLES)
right_side_benches.load_texture("textures/mdf.jpg")

right_side_cabinets = LoadMesh("assets/RightCabinets.obj", GL_TRIANGLES)

left_side_computers = LoadMesh("assets/LeftComputers.obj", GL_TRIANGLES)
left_side_computers.load_texture("textures/PcsWallpaper.jpg")

left_side_keyboards = LoadMesh("assets/LeftKeyboards.obj", GL_LINE_LOOP)
left_side_benches = LoadMesh("assets/LeftBenches.obj", GL_TRIANGLES)
left_side_benches.load_texture("textures/mdf.jpg")

left_side_cabinets = LoadMesh("assets/LeftCabinets.obj", GL_TRIANGLES)

fans = LoadMesh("assets/Fans.obj", GL_TRIANGLES)
fans.load_texture("textures/madeira.jpg")

fans2 = LoadMesh("assets/Fans2.obj", GL_TRIANGLES)
fans2.load_texture("textures/madeira.jpg")

quadro = LoadMesh("assets/Quadro.obj", GL_TRIANGLES)
quadro.load_texture("textures/QuadroTexture.jpg")

door = LoadMesh("assets/Porta.obj", GL_TRIANGLES)
door.load_texture("textures/DoorTexture.jpg")

window = LoadMesh("assets/Window.obj", GL_TRIANGLES)
mesaProfessor = LoadMesh("assets/MesaProfessor.obj", GL_TRIANGLES)
laptop = LoadMesh("assets/Laptop.obj", GL_TRIANGLES)
camera = Camera()

portaAberta = False
portaAnimacao = False
rotationPorta = 0

janelasAbertas = False
janelasAnimacao = False
rotationJanelas = 0

rotationFan1 = 0
rotationFan2 = 0

luz1_ativa = True
luz2_ativa = True
luz3_ativa = True
luz4_ativa = True
luz5_ativa = True

modo_noturno = False

def initialise():
    glClearColor(background_color[0], background_color[1], background_color[2], background_color[3])
    glColor(drawing_color)

    # projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, (screen_width / screen_height), 0.1, 1000.0)

    glShadeModel(GL_SMOOTH)

    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHT3)
    glEnable(GL_LIGHT4)

    glEnable(GL_NORMALIZE)


def init_camera():
    # modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, screen.get_width(), screen.get_height())
    glEnable(GL_DEPTH_TEST)
    camera.update(screen.get_width(), screen.get_height())


def draw_cube(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor(0, 1, 0)
    glBegin(GL_QUADS)

    # Front face
    glVertex3f(-0.075, -0.075, 0.075)
    glVertex3f(0.075, -0.075, 0.075)
    glVertex3f(0.075, 0.075, 0.075)
    glVertex3f(-0.075, 0.075, 0.075)

    # Back face
    glVertex3f(-0.075, -0.075, -0.075)
    glVertex3f(0.075, -0.075, -0.075)
    glVertex3f(0.075, 0.075, -0.075)
    glVertex3f(-0.075, 0.075, -0.075)

    # Top face
    glVertex3f(-0.075, 0.075, 0.075)
    glVertex3f(0.075, 0.075, 0.075)
    glVertex3f(0.075, 0.075, -0.075)
    glVertex3f(-0.075, 0.075, -0.075)

    # Bottom face
    glVertex3f(-0.075, -0.075, 0.075)
    glVertex3f(0.075, -0.075, 0.075)
    glVertex3f(0.075, -0.075, -0.075)
    glVertex3f(-0.075, -0.075, -0.075)

    # Right face
    glVertex3f(0.075, -0.075, 0.075)
    glVertex3f(0.075, -0.075, -0.075)
    glVertex3f(0.075, 0.075, -0.075)
    glVertex3f(0.075, 0.075, 0.075)

    # Left face
    glVertex3f(-0.075, -0.075, 0.075)
    glVertex3f(-0.075, -0.075, -0.075)
    glVertex3f(-0.075, 0.075, -0.075)
    glVertex3f(-0.075, 0.075, 0.075)

    glEnd()
    glColor(1, 1, 1)
    glPopMatrix()


def draw_spotlight(pos, direction, cutoff, lightid):
    glLightfv(lightid, GL_POSITION, (pos))
    glLightfv(lightid, GL_SPOT_DIRECTION, (direction))
    glLightf(lightid, GL_SPOT_CUTOFF, cutoff)


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
    global rotationFan1, rotationFan2
    global rotationPorta, portaAnimacao
    global rotationJanelas, janelasAnimacao

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    init_camera()

    glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1))

    ### Iluminação
    # Ambiente
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.3, 0.3, 1.3, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))
    glLightfv(GL_LIGHT0, GL_POSITION, (1.25, 1.95, -1.15, 0))

    # Lado direito / Frente
    glLightfv(GL_LIGHT1, GL_POSITION, (1.25, 1.90, -1.15, 1))
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, (0, -1, 0))
    glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 30)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.3, 0.3, 1.3, 1.0))
    glLightfv(GL_LIGHT1, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))

    # Lado esquerdo
    glLightfv(GL_LIGHT2, GL_POSITION, (-3.0, 1.90, -1.15, 1))
    glLightfv(GL_LIGHT2, GL_SPOT_DIRECTION, (0, -1, 0))
    glLightf(GL_LIGHT2, GL_SPOT_CUTOFF, 30)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, (0.3, 1.3, 0.3, 1.0))
    glLightfv(GL_LIGHT2, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))

    # Lado direito / Trás
    glLightfv(GL_LIGHT3, GL_POSITION, (1.25, 1.90, 0.35, 1))
    glLightfv(GL_LIGHT3, GL_SPOT_DIRECTION, (0, -1, 0))
    glLightf(GL_LIGHT3, GL_SPOT_CUTOFF, 30)
    glLightfv(GL_LIGHT3, GL_DIFFUSE, (0.3, 1.3, 0.3, 1.0))
    glLightfv(GL_LIGHT3, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))

    # Luz projetor
    glLightfv(GL_LIGHT4, GL_POSITION, (-0.75, 0.75, -3, 1))
    glLightfv(GL_LIGHT4, GL_SPOT_DIRECTION, (0, 0, -1))
    glLightf(GL_LIGHT4, GL_SPOT_CUTOFF, 30)
    glLightfv(GL_LIGHT4, GL_DIFFUSE, (0.0, 0.0, 0.0, 1.0))
    glLightfv(GL_LIGHT4, GL_SPECULAR, (0.7, 0.7, 0.7, 1.0))

    # draw_cube(-0.75, 1, -3)

    ### FIM: Iluminação

    glPushMatrix()
    draw_world_axes()
    glPopMatrix()

    glPushMatrix()

    mesh.draw()

    glColor(1.0, 1.0, 1.0)
    # Define a reflectancia do material
    left_side_computers.draw()
    right_side_computers.draw()

    glColor(0.1, 0.1, 0.1)
    left_side_cabinets.draw()
    right_side_cabinets.draw()

    # glColor(0.85, 0.85, 0.85)
    glColor(1, 1, 1)
    # left_side_keyboards.draw()
    # right_side_keyboards.draw()
    right_side_benches.draw()
    left_side_benches.draw()

    quadro.draw()
    mesaProfessor.draw()

    glColor(0.85, 0.85, 1)
    laptop.draw()
    glPopMatrix()

    glColor(1, 1, 1)
    glPushMatrix()
    glTranslatef(0, 1.75, 0)
    glRotatef(rotationFan1, 0, 1, 0)
    fans.draw()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 1.75, -3)
    glRotatef(rotationFan2, 0, 1, 0)
    fans.draw()
    glPopMatrix()

    glPushMatrix()
    glColor(1, 1, 1)
    glTranslatef(2.68048, 0.345, -5.14363)

    if portaAnimacao:
        # Executa a animação da porta abrindo, ela vai de 0º a -90º
        if portaAberta:
            rotationPorta = rotationPorta - 1
            if rotationPorta <= -90:
                portaAnimacao = False
        # Executa a animação da porta fechando, ela vai de -90º a 0º
        else:
            rotationPorta = rotationPorta + 1
            if rotationPorta >= 0:
                portaAnimacao = False

        glRotatef(rotationPorta, 0, 1, 0)
    elif portaAberta:
        glRotatef(-90, 0, 1, 0)

    door.draw()
    glPopMatrix()

    for janelaZ in [-3.45, -2.3, -1.15, 0]:
        glPushMatrix()
        if modo_noturno:
            glColor(0.3, 0.3, 0.3)
        else:
            glColor(204/255, 230/255, 230/255)
        glTranslatef(-4, 1.5, janelaZ)
        if janelasAnimacao:
            # Executa a animação das janelas abrindo, ela vai de 0º a -45º
            if janelasAbertas:
                rotationJanelas = rotationJanelas - 1
                if rotationJanelas <= -45:
                    janelasAnimacao = False
            # Executa a animação das janelas fechando, ela vai de -45º a 0º
            else:
                rotationJanelas = rotationJanelas + 1
                if rotationJanelas >= 0:
                    janelasAnimacao = False

            glRotatef(rotationJanelas, 0, 0, 1)
        elif janelasAbertas:
            glRotatef(-45, 0, 0, 1)

        window.draw()
        glPopMatrix()

    rotationFan1 = (rotationFan1 + 2) % 360
    rotationFan2 = (rotationFan2 + 1) % 360


done = False
initialise()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)

            elif event.key == K_SPACE:
                pygame.mouse.set_visible(False)
                pygame.event.set_grab(True)

            elif event.key == K_p:
                portaAberta = not portaAberta
                portaAnimacao = True

            elif event.key == K_j:
                janelasAbertas = not janelasAbertas
                janelasAnimacao = True

            elif event.key == K_n:
                modo_noturno = not modo_noturno
                if modo_noturno:
                    glDisable(GL_LIGHT0)
                else:
                    glEnable(GL_LIGHT0)

            elif event.key == K_1:
                if luz1_ativa:
                    glDisable(GL_LIGHT0)
                else:
                    glEnable(GL_LIGHT0)
                luz1_ativa = not luz1_ativa

            elif event.key == K_2:
                if luz2_ativa:
                    glDisable(GL_LIGHT1)
                else:
                    glEnable(GL_LIGHT1)
                luz2_ativa = not luz2_ativa

            elif event.key == K_3:
                if luz3_ativa:
                    glDisable(GL_LIGHT2)
                else:
                    glEnable(GL_LIGHT2)
                luz3_ativa = not luz3_ativa

            elif event.key == K_4:
                if luz4_ativa:
                    glDisable(GL_LIGHT3)
                else:
                    glEnable(GL_LIGHT3)
                luz4_ativa = not luz4_ativa

            elif event.key == K_5:
                if luz5_ativa:
                    glDisable(GL_LIGHT4)
                else:
                    glEnable(GL_LIGHT4)
                luz5_ativa = not luz5_ativa

    display()
    pygame.display.flip()

pygame.quit()