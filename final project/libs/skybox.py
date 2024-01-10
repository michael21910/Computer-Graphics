from libs.Texture import *
from OpenGL.GL import *
from OpenGL.GLUT import *

class Skybox:
    def __init__(self, camera, location):
        ext = "png"
        self.faces = [
            location + "top." + ext,
            location + "front." + ext,
            location + "back." + ext,
            location + "right." + ext,
            location + "left." + ext
        ]

        self.vertices = [
            # vertices         # tex
            [[-1.0, 1.0, 1.0, 0.0, 0.0],
             [1.0, 1.0, 1.0, 0.0, 1.0],
             [1.0, 1.0, -1.0, 1.0, 1.0],
             [-1.0, 1.0, -1.0, 1.0, 0.0]],

            [[-1.0, 1.0, -1.0, 0.0, 1.0],
             [1.0, 1.0, -1.0, 1.0, 1.0],
             [1.0, -0.1, -1.0, 1.0, 0.5],
             [-1.0, -0.1, -1.0, 0.0, 0.5]],

            [[1.0, 1.0, 1.0, 0.0, 1.0],
             [-1.0, 1.0, 1.0, 1.0, 1.0],
             [-1.0, -0.1, 1.0, 1.0, 0.5],
             [1.0, -0.1, 1.0, 0.0, 0.5]],

            [[1.0, 1.0, -1.0, 0.0, 1.0],
             [1.0, 1.0, 1.0, 1.0, 1.0],
             [1.0, -0.1, 1.0, 1.0, 0.5],
             [1.0, -0.1, -1.0, 0.0, 0.5]],

            [[-1.0, 1.0, 1.0, 0.0, 1.0],
             [-1.0, 1.0, -1.0, 1.0, 1.0],
             [-1.0, -0.1, -1.0, 1.0, 0.5],
             [-1.0, -0.1, 1.0, 0.0, 0.5]]
        ]

        seaTexScale = 500
        self.underGround = [[-1.0, 0.0, -1.0, 0.0, seaTexScale],
                            [1.0, 0.0, -1.0, seaTexScale, seaTexScale],
                            [1.0, 0.0, 1.0, seaTexScale, 0.0],
                            [-1.0, 0.0, 1.0, 0.0, 0.0]]

        self.gl_list = glGenLists(1)
        self.gl_Water_list = glGenLists(1)
        self.groundTexPath = "assets/textures/ground/water5.jpg"
        self.groundTex = glGenTextures(1)
        self.tex2D = []
        self.load()
        self.cam = camera
        self.generate()

    def load(self):
        for i in range(len(self.faces)):
            self.tex2D.append(loadTexture(self.faces[i], True))
        self.groundTex = TexSeries("assets\\textures\\ground\\waterA_col", speed=0.5)

    def Draw(self, camera):
        glPushMatrix()
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_LIGHT0)
        glFogf(GL_FOG_DENSITY, 0.04)
        px, py, pz = camera.cam_pos.tuple()

        for i in range(len(self.vertices)):
            glBindTexture(GL_TEXTURE_2D, self.tex2D[i])
            glBegin(GL_QUADS)
            for j in self.vertices[i]:
                glTexCoord2f(*j[3:])
                x, y, z = j[:3]
                glVertex3f(5 * x, 5 * y, 5 * z)
            glEnd()

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glPopMatrix()
        glBindTexture(GL_TEXTURE_2D, 0)

    def generate(self):
        glNewList(self.gl_list, GL_COMPILE)
        self.Draw(self.cam)
        glEndList()

        glNewList(self.gl_Water_list, GL_COMPILE)
        self.water()
        glEndList()

    def water(self):
        glBindTexture(GL_TEXTURE_2D, self.groundTex.getNextFrame(True))
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glBegin(GL_QUADS)
        t = 0
        for i in self.underGround:
            glTexCoord2f(i[3:][0] + t, i[3:][1] + t)
            glNormal3f(0, 1, 0)
            x, y, z = i[:3]
            glVertex3f(x * 8000, 0, z * 8000)
        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)