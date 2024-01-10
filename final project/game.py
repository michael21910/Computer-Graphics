from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from libs.saveGame import *

# initializing glut and window because some imports depend on it
try:
    glutInit()
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(720, 500)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"PHRIX3D")
except Error:
    raise Error

# continuing importing
from libs.misc import drawOnScreen
from libs.game import *

def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, w / h, 0.1, 300.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def Timer(v):
    glutPostRedisplay()
    glutTimerFunc(TIMER_INTERVAL_MS, Timer, v + 1)

def draw():
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    game.player.camera.callPerspective()
    glPushMatrix()

    px, py, pz = game.player.camera.cam_pos.tuple()
    glTranslate(px, py, pz)
    glCallList(game.sky.gl_list)
    game.waterFog()
    light_position = (1922, 3354, 3391)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.001, 0.001, 0.001))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.0005, 0.0005, 0.0005))

    glPopMatrix()
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, game.terrain.texture)
    glPushAttrib(GL_CURRENT_BIT)
    glTranslate(32.0, game.terrain.heightPlus((32, 0, 32), 0), 32.0)
    glColor(.9, .4, .1, 1)
    glPopAttrib()
    glPopMatrix()

    game.loop()
    if game.firstFrame:
        game.saveGame()
        game.firstFrame = False
    drawOnScreen(game, 0, 0, 0)
    glutSwapBuffers()

def pressedKey(key, xx, yy):
    try:
        key = key.decode("utf8").lower()
    except:
        key = ""
    if key == "w":
        game.player.forward = True
    if key == "s":
        game.player.backward = True

    if key == "a":
        game.player.left = True
    if key == "d":
        game.player.right = True
    if key == " ":
        game.player.jump = True
    if key == "r":
        game.player.gun.forceReload = True
    if key == chr(27):
        glutLeaveMainLoop()

def releasedKey(key, x, y):
    try:
        key = key.decode("utf8").lower()
    except:
        return
    if key == "w":
        game.player.forward = False
    if key == "s":
        game.player.backward = False
    if key == "a":
        game.player.left = False
    if key == "d":
        game.player.right = False
    if key == "r":
        game.player.gun.forceReload = False
    game.lastEightChars.append(key)
    game.lastEightChars.pop(0)

def specialPressedKey(key, x, y):
    mod = glutGetModifiers()
    if mod == GLUT_ACTIVE_SHIFT:
        game.player.running = True

def specialReleasedKey(key, x, y):
    mod = glutGetModifiers()
    if mod != GLUT_ACTIVE_SHIFT:
        game.player.running = False
    if key == GLUT_KEY_F4:
        glutFullScreenToggle()

def mouseLookCallBack(xpos, ypos):
    if game.player.firstMovement:
        game.player.lastX = xpos
        game.player.lastY = ypos
        game.player.firstMovement = False
    game.player.camera.xOffset = xpos - game.player.lastX
    game.player.camera.yOffset = game.player.lastY - ypos
    game.player.camera.processMouseMotion()
    glutWarpPointer(350, 200)
    game.player.lastX = 350
    game.player.lastY = 200

def mouseButtonCallback(button, state, x, y):
    if state == GLUT_DOWN:
        if button == GLUT_RIGHT_BUTTON:
            pass
        if button == GLUT_LEFT_BUTTON:
            game.player.triggering = True

    if state == GLUT_UP:
        if button == GLUT_RIGHT_BUTTON:
            pass
        if button == GLUT_LEFT_BUTTON:
            pass
    else:
        pass
    glutPostRedisplay()

def loadingLoop():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1, 0, 0, 0)

    drawRect(1 * width / height, 1)
    glColor3f(0, 1, 0)
    glutSwapBuffers()

glutTimerFunc(TIMER_INTERVAL_MS, Timer, 1)
glutReshapeFunc(resize)
glutSetKeyRepeat(0)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glEnable(GL_LIGHT1)
glEnable(GL_FOG)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glutSetOption(GLUT_MULTISAMPLE, 8)
glutFullScreen()

game = Game()

# KEYBOARD
glutSpecialFunc(specialPressedKey)
glutSpecialUpFunc(specialReleasedKey)
glutKeyboardFunc(pressedKey)
glutKeyboardUpFunc(releasedKey)

# MOUSE
glutPassiveMotionFunc(mouseLookCallBack)
glutMotionFunc(mouseLookCallBack)
glutSetCursor(GLUT_CURSOR_NONE)
glutMouseFunc(mouseButtonCallback)

glutDisplayFunc(draw)
glutMainLoop()