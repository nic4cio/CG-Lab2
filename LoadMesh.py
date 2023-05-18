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

        self.filename = filename
        self.draw_type = draw_type
        self.load_drawing()

    def load_drawing(self):
        with open(self.filename) as fp:
            line = fp.readline()
            while line:
                if line[:2] == "v ":
                    vx, vy, vz = [float(value) for value in line[2:].split()]
                    self.vertices.append((vx, vy, vz))
                if line[:2] == "vn":
                    vx, vy, vz == [float(value) for value in line[3:].split()]
                    self.normals.append((vx, vy, vz))
                if line[:2] == "vt":
                    vx, vy == [float(value) for value in line[3:].split()]
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
                line = fp.readline()

    def draw(self):
        for t in range(0, len(self.triangles), 3):
            glBegin(self.draw_type)
            glVertex3fv(self.vertices[self.triangles[t]])
            glVertex3fv(self.vertices[self.triangles[t + 1]])
            glVertex3fv(self.vertices[self.triangles[t + 2]])
            glEnd()
