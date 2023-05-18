from OpenGL.GL import *
from Mesh import *
import pygame


class LoadMesh(Mesh):
    def __init__(self, filename, draw_type):
        self.vertices = []
        self.triangles = []

        ## adding vnormals and uvs

        self.normals = []
        self.normal_ind = []
        self.uvs = []
        self.uvs_ind = []
        self.faces = []

        self.filename = filename
        self.draw_type = draw_type
        self.load_drawing()

        self.texture_id = None
        self.has_texture = False

    def load_drawing(self):
        with open(self.filename) as fp:
            line = fp.readline()
            while line:
                if line[:2] == "v ":
                    vx, vy, vz = [float(value) for value in line[2:].split()]
                    self.vertices.append((vx, vy, vz))
                if line[:2] == "vn":
                    vx, vy, vz = [float(value) for value in line[3:].split()]
                    self.normals.append((vx, vy, vz))
                if line[:2] == "vt":
                    vx, vy = [float(value) for value in line[3:].split()]
                    self.uvs.append((vx, vy))
                if line[:2] == "f ":
                    t1, t2, t3 = [value for value in line[2:].split()]
                    self.triangles.append([int(value) for value in t1.split('/')][0]-1)
                    self.triangles.append([int(value) for value in t2.split('/')][0]-1)
                    self.triangles.append([int(value) for value in t3.split('/')][0]-1)

                    self.uvs_ind.append([int(value) for value in t1.split('/')][1] - 1)
                    self.uvs_ind.append([int(value) for value in t2.split('/')][1] - 1)
                    self.uvs_ind.append([int(value) for value in t3.split('/')][1] - 1)

                    self.normal_ind.append([int(value) for value in t1.split('/')][2] - 1)
                    self.normal_ind.append([int(value) for value in t2.split('/')][2] - 1)
                    self.normals.append([int(value) for value in t3.split('/')][2] - 1)

                    data = line.strip().split()
                    face = []
                    for face_data in data[1:]:
                        indices = face_data.split("/")
                        face.append((int(indices[0]) - 1, int(indices[1]) - 1))
                    self.faces.append(face)

                line = fp.readline()

    def load_texture(self, file_name):
        self.has_texture = True

        texture_surface = pygame.image.load(file_name)
        texture_data = pygame.image.tostring(texture_surface, "RGB", 1)
        width, height = texture_surface.get_size()
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data
        )
        glGenerateMipmap(GL_TEXTURE_2D)
        return self.texture_id

    def draw(self):
        if self.has_texture:

            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glEnable(GL_TEXTURE_2D)
            glBegin(self.draw_type)

            #for u in self.uvs_ind:
            #    print(self.uvs[self.uvs_ind[u]])
#
            #for t in range(0, len(self.triangles), 3):
            #    glTexCoord2fv(self.uvs[self.uvs_ind[t]])
            #    glVertex3fv(self.vertices[self.triangles[t]])
            #    glVertex3fv(self.vertices[self.triangles[t + 1]])
            #    glVertex3fv(self.vertices[self.triangles[t + 2]])

            for face in self.faces:
                for vertex_index, texture_index in face:
                    vertex = self.vertices[vertex_index]
                    texture_coord = self.uvs[texture_index]
                    glTexCoord2fv(texture_coord)
                    glVertex3fv(vertex)

            glEnd()
            glDisable(GL_TEXTURE_2D)

        else:
            for t in range(0, len(self.triangles), 3):
                glBegin(self.draw_type)
                glVertex3fv(self.vertices[self.triangles[t]])
                glVertex3fv(self.vertices[self.triangles[t + 1]])
                glVertex3fv(self.vertices[self.triangles[t + 2]])
                glEnd()
