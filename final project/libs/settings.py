from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

GAME_FPS = 60
TIMER_INTERVAL_MS = int(1000 / GAME_FPS)
height = glutGet(GLUT_SCREEN_HEIGHT)
width = glutGet(GLUT_SCREEN_WIDTH)
ratio = width/height

class Settings:
    def __init__(self):
        self.GAME_FPS = 60
        self.time = 0

def time():
    return glutGet(GLUT_ELAPSED_TIME)/1000
