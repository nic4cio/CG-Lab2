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
right_side_computers = LoadMesh("assets/RightComputers.obj", GL_TRIANGLES)
right_side_keyboards = LoadMesh("assets/RightKeyboards.obj", GL_LINE_LOOP)
right_side_benches = LoadMesh("assets/RightBenches.obj", GL_TRIANGLES)
right_side_cabinets = LoadMesh("assets/RightCabinets.obj", GL_TRIANGLES)

left_side_computers = LoadMesh("assets/LeftComputers.obj", GL_TRIANGLES)
left_side_keyboards = LoadMesh("assets/LeftKeyboards.obj", GL_LINE_LOOP)
left_side_benches = LoadMesh("assets/LeftBenches.obj", GL_TRIANGLES)
left_side_cabinets = LoadMesh("assets/LeftCabinets.obj", GL_TRIANGLES)

fans = LoadMesh("assets/Fans.obj", GL_TRIANGLES)
fans2 = LoadMesh("assets/Fans2.obj", GL_TRIANGLES)
quadro = LoadMesh("assets/Quadro.obj", GL_TRIANGLES)
door = LoadMesh("assets/Porta.obj", GL_TRIANGLES)
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

## class Material >:(

class Material:
    def __init__(self, filepath):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_REPEAT)
        image = pygame.image.load(filepath).convert()
        image_width, image_height = image.get_rect().size
        image_data = pygame.image.tostring(image, "RGBA")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):
        glDeleteTextures(1, (self.texture,))

#######

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

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_COLOR_MATERIAL)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    init_camera()

    glLightfv(GL_LIGHT0, GL_AMBIENT,  (0.1, 0.1, 0.1, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  (0.3, 0.3, 0.3, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))
    glLightfv(GL_LIGHT0, GL_POSITION, (1.6, 1.5, 1.0, 2.0))

    glLightfv(GL_LIGHT1, GL_AMBIENT,  (0.1, 0.1, 0.1, 1.0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE,  (0.3, 0.3, 0.3, 1.0))
    glLightfv(GL_LIGHT1, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0))
    glLightfv(GL_LIGHT1, GL_POSITION, (-1.6, 1.5, 2.0, 1.0))

    #glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 0.25)) #amb1
    #glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1)) #dif2

    #glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 0.25)) #amb1
    #glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1)) #dif3
    
    #glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 0.25)) #amb1
    #glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1)) #dif4

    glPushMatrix()
    draw_world_axes()
    glPopMatrix()

    glPushMatrix()
    mesh.draw()

    glColor(0.4, 0.4, 0.4)
    # Define a reflectancia do material
    glMaterialfv(GL_FRONT,GL_SPECULAR, (1.0, 1.0, 1.0, 1))
    left_side_computers.draw()
    right_side_computers.draw()

    glColor(0.4, 0.4, 0.4)
    left_side_cabinets.draw()
    right_side_cabinets.draw()

    glColor(0.85, 0.85, 0.85)
    # left_side_keyboards.draw()
    # right_side_keyboards.draw()
    right_side_benches.draw()
    left_side_benches.draw()

    quadro.draw()
    mesaProfessor.draw()

    glColor(0.71, 0.494, 0.862)
    laptop.draw()
    glPopMatrix()

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
    glColor(1, 1, 0)
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


    for janelaZ in [ -3.45, -2.3, -1.15, 0 ]:
        glPushMatrix()
        glColor(.2, .5, .66)
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

    display()
    pygame.display.flip()

pygame.quit()
