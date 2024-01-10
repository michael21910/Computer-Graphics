import pygame
from OpenGL.GL import *
from libs.Texture import loadTexture
from libs.vector import *
from random import randrange

class Terrain:
    def __init__(self, heightmap, texture):
        self.heightMap = pygame.image.load(heightmap)
        self.width, self.height = self.heightMap.get_size()

        self.texCoords = []
        self.normals = []
        self.planeNormals = []
        self.heights = []
        self.scale = self.width / 256
        self.seaLevel = 3
        self.maxHeight = self.width / 13
        self.getHeightsFromImage()

        self.calcNormals()
        self.calcTexCoords()
        self.texture = loadTexture(texture)
        self.gl_list = glGenLists(1)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.makeList()

    def getHeightsFromImage(self):
        for x in range(self.height):
            tempHeights = []
            tempVertices = []
            for y in range(self.width):
                height = self.heightMap.get_at((x, y))[0] / 255 * self.maxHeight
                tempHeights.append(height)
                tempVertices.append((x, height, y))
            self.heights.append(tempHeights)

    def getPlaneNormal(self, x, y):
        x = int(x)
        y = int(y)
        if -1 < x < self.width and -1 < y < self.height:
            p1 = Vec3(x, self.heights[x][y], y)
            p2 = Vec3(x + 1, self.heights[x + 1][y], y)
            p3 = Vec3(x, self.heights[x][y + 1], y + 1)
            return getNormalVector(p1, p2, p3)
        else:
            return Vec3(0, 0, 0)

    def calcNormals(self):
        for i in range(self.height - 1):
            temp = []
            for j in range(self.height - 1):
                p1 = Vec3(i, self.heights[i][j], j)
                p2 = Vec3(i, self.heights[i][j + 1], j + 1)
                p3 = Vec3(i + 1, self.heights[i + 1][j], j)
                p4 = Vec3(i + 1, self.heights[i + 1][j + 1], j + 1)
                v1 = getNormalVector(p1, p2, p3)
                v2 = getNormalVector(p2, p4, p3)
                temp.append((v1, v2))
            self.planeNormals.append(temp)

        for i in range(self.height):
            temp = []
            for j in range(self.height):
                vList = []
                if i > 0 and j > 0:
                    vList.append(self.planeNormals[i - 1][j - 1][1])
                if i < self.width - 1 and j < self.height - 1:
                    vList.append(self.planeNormals[i][j][0])
                if i < self.width - 1 and j > 0:
                    vList.append(self.planeNormals[i][j-1][0])
                    vList.append(self.planeNormals[i][j-1][1])
                if i > 0 and j < self.width - 1:
                    vList.append(self.planeNormals[i-1][j][0])
                    vList.append(self.planeNormals[i-1][j][1])

                temp.append(meanVec(vList).normalize().tuple())
            self.normals.append(temp)

    def calcTexCoords(self):
        for i in range(self.height):
            temp = []
            s = 2.7 * self.scale
            for j in range(self.height):
                t = (i / s, j / s)
                temp.append(t)
            self.texCoords.append(temp)

    def calcVertices(self):
        for i in range(self.height):
            temp = []
            for j in range(self.height):
                v1 = (i, self.heights[i][j], j)
                temp.append(v1)
            self.vertices.append(temp)

    def interpolateHeight(self, x, y):
        return bilinear_interpolation(x, y,
                                      [(int(x), int(y), self.heights[int(x)][int(y)]),
                                       (int(x) + 1, int(y), self.heights[int(x) + 1][int(y)]),
                                       (int(x), int(y) + 1, self.heights[int(x)][int(y) + 1]),
                                       (int(x) + 1, int(y) + 1, self.heights[int(x) + 1][int(y) + 1])])

    def getRightPos(self, x, y):
        xi, yi = int(x), int(y)
        point = Vec3(xi, self.heights[xi][yi], yi)
        if firstTri(x, y, xi, yi):
            point = Vec3(xi, self.heights[xi][yi], yi)
            return pointYOnPlane(x, y, self.planeNormals[xi][yi][0], point)
        else:
            point = Vec3(xi + 1, self.heights[xi + 1][yi + 1], yi + 1)
            return pointYOnPlane(x, y, self.planeNormals[xi][yi][1], point)

    def getHeight(self, x, y):
        seaPlayer = self.getSeaLevel() - 0.15
        if self.checkIfInRange((x, 0, y)):
            height = self.interpolateHeight(x, y)
            if height < seaPlayer:
                return seaPlayer
            else:
                return height
        else:
            return seaPlayer

    def playerHeight(self, player):
        return self.getHeight(player.getPos()[0], player.getPos()[2]) + player.playerHeight

    def heightPlus(self, pos, height=0):
        return self.getHeight(pos[0], pos[-1]) + height

    def getRandomPlace(self, plus=0):
        x = randrange(1, self.width - 1)
        y = randrange(1, self.height - 1)
        return x, self.getHeight(x, y) + plus, y

    def checkIfInRange(self, cam_pos):
        if 0 < cam_pos[0] < self.width - 1 and 0 < cam_pos[2] < self.height - 1:
            return True
        else:
            return False

    def Draw(self):
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glPolygonMode(GL_FRONT, GL_FILL)
        glShadeModel(GL_SMOOTH)
        for i in range(self.height):
            glBegin(GL_TRIANGLE_STRIP)
            for j in range(self.width):
                glTexCoord(*self.texCoords[i][j])
                glNormal3f(*self.normals[i][j])
                glVertex3f(i, self.heights[i][j], j)

                glTexCoord(*self.texCoords[i + 1][j])
                glNormal3f(*self.normals[i + 1][j])
                glVertex3f(i + 1, self.heights[i + 1][j], j)
            glEnd()
        return

    def makeList(self):
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glPolygonMode(GL_FRONT, GL_FILL)
        for i in range(self.width - 1):
            glBegin(GL_TRIANGLE_STRIP)
            for j in range(self.height):
                glTexCoord(*self.texCoords[i][j])
                glNormal3f(*self.normals[i][j])
                glVertex3f(i, self.heights[i][j], j)
                glTexCoord(*self.texCoords[i + 1][j])
                glNormal3f(*self.normals[i + 1][j])
                glVertex3f(i + 1, self.heights[i + 1][j], j)
            glEnd()
        glEnable(GL_BLEND)
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)

        glEndList()

    def getSeaLevel(self):
        return self.seaLevel

def bilinear_interpolation(x, y, points):
    points = sorted(points)
    (x1, y1, q11), (xn1, y2, q12), (x2, yn1, q21), (xn2, yn2, q22) = points

    return (q11 * (x2 - x) * (y2 - y) +
            q21 * (x - x1) * (y2 - y) +
            q12 * (x2 - x) * (y - y1) +
            q22 * (x - x1) * (y - y1)) / ((x2 - x1) * (y2 - y1) + 0.0)