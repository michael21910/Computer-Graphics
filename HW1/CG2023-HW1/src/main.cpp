#include <algorithm>
#include <iostream>
#include <memory>
#include <vector>

#include <GLFW/glfw3.h>
#define GLAD_GL_IMPLEMENTATION
#include <glad/gl.h>
#undef GLAD_GL_IMPLEMENTATION
#include <glm/glm.hpp>

#include "camera.h"
#include "opengl_context.h"
#include "utils.h"

#define ANGLE_TO_RADIAN(x) (float)((x)*M_PI / 180.0f)
#define RADIAN_TO_ANGEL(x) (float)((x)*180.0f / M_PI)

#define CIRCLE_SEGMENT 64

#define ROTATE_SPEED 1.0f
#define FLYING_SPEED ROTATE_SPEED / 20.f

#define RED 0.905f, 0.298f, 0.235f
#define BLUE 0.203f, 0.596f, 0.858f
#define GREEN 0.18f, 0.8f, 0.443f

struct Position {
  float x;
  float y;
  float z;
} airplanePosition, rotatePosition;

int IsFlyingUp = 0;
int IsFlyingForward = 0;
float rotateValue = 0;
float wingRotationAngle = 0;

void resizeCallback(GLFWwindow* window, int width, int height) {
  OpenGLContext::framebufferResizeCallback(window, width, height);
  auto ptr = static_cast<Camera*>(glfwGetWindowUserPointer(window));
  if (ptr) {
    ptr->updateProjectionMatrix(OpenGLContext::getAspectRatio());
  }
}

int changeStatus(int attribute) { return (attribute + 1) % 2; }

void keyCallback(GLFWwindow* window, int key, int, int action, int) {
  // There are three actions: press, release, hold(repeat)
  if (action == GLFW_REPEAT) return;

  // Press ESC to close the window.
  if (key == GLFW_KEY_ESCAPE) {
    glfwSetWindowShouldClose(window, GLFW_TRUE);
    return;
  }
  /* TODO#4-1: Detect key-events, perform rotation or fly
   *       1. Use switch && case to find the key you want.
   *       2. Press "SPACE" for fly up, fly forward and wing rotate meanwhile.
   *       3. Press "GLFW_KEY_LEFT" for turn left.
   *       4. Press "GLFW_KEY_RIGHT" for turn right.
   * Hint:
   *       glfw3's key list (https://www.glfw.org/docs/3.3/group__keys.html)
   *       glfw3's action codes (https://www.glfw.org/docs/3.3/group__input.html#gada11d965c4da13090ad336e030e4d11f)
   * Note:
   *       You should finish rendering your airplane first.
   *       Otherwise you will spend a lot of time debugging this with a black screen.
   */
  if (action == GLFW_PRESS) {
    switch (key) {
      case GLFW_KEY_SPACE:
        IsFlyingUp = changeStatus(IsFlyingUp);
        IsFlyingForward = changeStatus(IsFlyingForward);
        break;
      case GLFW_KEY_LEFT:
        rotateValue += ROTATE_SPEED;
        break;
      case GLFW_KEY_RIGHT:
        rotateValue -= ROTATE_SPEED;
        break;
    }
  }
}

void initOpenGL() {
  // Initialize OpenGL context, details are wrapped in class.
#ifdef __APPLE__
  // MacOS need explicit request legacy support
  OpenGLContext::createContext(21, GLFW_OPENGL_ANY_PROFILE);
#else
  // OpenGLContext::createContext(21, GLFW_OPENGL_ANY_PROFILE);
  OpenGLContext::createContext(43, GLFW_OPENGL_COMPAT_PROFILE);
#endif
  GLFWwindow* window = OpenGLContext::getWindow();
  /* TODO#0: Change window title to "HW1 - `your student id`"
   *        Ex. HW1 - 312550000
   */
  glfwSetWindowTitle(window, "HW1 - 312551077");
  glfwSetKeyCallback(window, keyCallback);
  glfwSetFramebufferSizeCallback(window, resizeCallback);
  glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);
#ifndef NDEBUG
  OpenGLContext::printSystemInfo();
  // This is useful if you want to debug your OpenGL API calls.
  OpenGLContext::enableDebugCallback();
#endif
}

/* TODO#2: Render body, wing, tail
 * Hint:
 *       glBegin/glEnd (https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glBegin.xml)
 *       glColor3f (https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glBegin.xml)
 *       glVertex3f (https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glVertex.xml)
 *       glNormal (https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glNormal.xml)
 *       glScalef (https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glScale.xml)
 * Note:
 *       You can refer to ppt "Draw Cylinder" page and `CIRCLE_SEGMENT`
 *       You can use color defined above
 */

void drawCylinder() {
  // set height of the cylinder
  const float height = 4.0f;

  // Body of the cylinder
  glBegin(GL_QUAD_STRIP);
  const float radius = 0.5f;
  const float angle = 2.f * M_PI / CIRCLE_SEGMENT;
  for (int i = 0; i <= CIRCLE_SEGMENT; i++) {
    float x = radius * cos(i * angle);
    float y = radius * sin(i * angle);
    glNormal3f(x, 0, y);
    glVertex3f(x, -height / 2, y);
    glVertex3f(x, height / 2, y);
  }
  glEnd();

  // Top circle
  glBegin(GL_TRIANGLE_FAN);
  for (int i = 0; i <= CIRCLE_SEGMENT; i++) {
    float x = radius * cos(i * angle);
    float y = radius * sin(i * angle);
    glNormal3f(0, 1, 0);
    glVertex3f(-x, height / 2, y);
  }
  glEnd();

  // Bottom circle
  glBegin(GL_TRIANGLE_FAN);
  for (int i = 0; i <= CIRCLE_SEGMENT; i++) {
    float x = radius * cos(i * angle);
    float y = radius * sin(i * angle);
    glNormal3f(0, -1, 0);
    glVertex3f(x, -height / 2, y);
  }
  glEnd();
}

void airplaneBody() {
  glPushMatrix();
  glColor3f(BLUE);
  // translate y+0.5, since the bottom of the cylinder is (0, 0, 0)
  glTranslatef(0.0f, 0.5f, 0.0f);
  // rotate 90 degrees around x-axis
  glRotatef(90.0f, 1.0f, 0.0f, 0.0f);
  drawCylinder();
  glPopMatrix();
}

void drawWings() {
  // avoid culling
  glDisable(GL_CULL_FACE);

  // translate and rotate for wings rotation
  glTranslatef(0.0, 0.25, 0.0);
  glRotatef(wingRotationAngle, 0.0, 0.0, 1.0);
  glBegin(GL_QUADS);

  glNormal3f(0.0, -1.0, 0.0);
  glVertex3f(0.0, 0.0, 0.5);
  glVertex3f(0.0, 0.0, -0.5);
  glVertex3f(-4.0, 0.0, -0.5);
  glVertex3f(-4.0, 0.0, 0.5);

  glNormal3f(0.0, 1.0, 0.0);
  glVertex3f(0.0, 0.5, 0.5);
  glVertex3f(-4.0, 0.5, 0.5);
  glVertex3f(-4.0, 0.5, -0.5);
  glVertex3f(0.0, 0.5, -0.5);

  glNormal3f(0.0, 0.0, 1.0);
  glVertex3f(0.0, 0.0, 0.5);
  glVertex3f(0.0, 0.5, 0.5);
  glVertex3f(-4.0, 0.5, 0.5);
  glVertex3f(-4.0, 0.0, 0.5);

  glNormal3f(0.0, 0.0, -1.0);
  glVertex3f(0.0, 0.0, -0.5);
  glVertex3f(-4.0, 0.0, -0.5);
  glVertex3f(-4.0, 0.5, -0.5);
  glVertex3f(0.0, 0.5, -0.5);

  glNormal3f(-1.0, 0.0, 0.0);
  glVertex3f(0.0, 0.0, 0.5);
  glVertex3f(0.0, 0.5, 0.5);
  glVertex3f(0.0, 0.5, -0.5);
  glVertex3f(0.0, 0.0, -0.5);

  glNormal3f(1.0, 0.0, 0.0);
  glVertex3f(-4.0, 0.0, 0.5);
  glVertex3f(-4.0, 0.0, -0.5);
  glVertex3f(-4.0, 0.5, -0.5);
  glVertex3f(-4.0, 0.5, 0.5);

  glEnd();
  // -2 since the left and right wings must be symmetric
  glRotatef(-2 * wingRotationAngle, 0.0, 0.0, 1.0);
  glBegin(GL_QUADS);

  glNormal3f(0.0, -1.0, 0.0);
  glVertex3f(4.0, 0.0, 0.5);
  glVertex3f(4.0, 0.0, -0.5);
  glVertex3f(0.0, 0.0, -0.5);
  glVertex3f(0.0, 0.0, 0.5);

  glNormal3f(0.0, 1.0, 0.0);
  glVertex3f(4.0, 0.5, 0.5);
  glVertex3f(0.0, 0.5, 0.5);
  glVertex3f(0.0, 0.5, -0.5);
  glVertex3f(4.0, 0.5, -0.5);

  glNormal3f(0.0, 0.0, 1.0);
  glVertex3f(4.0, 0.0, 0.5);
  glVertex3f(4.0, 0.5, 0.5);
  glVertex3f(0.0, 0.5, 0.5);
  glVertex3f(0.0, 0.0, 0.5);

  glNormal3f(0.0, 0.0, -1.0);
  glVertex3f(4.0, 0.0, -0.5);
  glVertex3f(0.0, 0.0, -0.5);
  glVertex3f(0.0, 0.5, -0.5);
  glVertex3f(4.0, 0.5, -0.5);

  glNormal3f(-1.0, 0.0, 0.0);
  glVertex3f(4.0, 0.0, 0.5);
  glVertex3f(4.0, 0.5, 0.5);
  glVertex3f(4.0, 0.5, -0.5);
  glVertex3f(4.0, 0.0, -0.5);

  glNormal3f(1.0, 0.0, 0.0);
  glVertex3f(0.0, 0.0, 0.5);
  glVertex3f(0.0, 0.0, -0.5);
  glVertex3f(0.0, 0.5, -0.5);
  glVertex3f(0.0, 0.5, 0.5);
  glEnd();
}

void airplaneWings() {
  glPushMatrix();
  glColor3f(RED);
  drawWings();
  glPopMatrix();
}

void drawTail() {
  glBegin(GL_TRIANGLES);

  // four points: (0, 0.5, 2), (-1, 0.5, 3), (1, 0.5, 3), (0, 0, 3)
  glVertex3f(0.0f, 0.5f, -2.0f);
  glVertex3f(-1.0f, 0.5f, -3.0f);
  glVertex3f(1.0f, 0.5f, -3.0f);

  glVertex3f(0.0f, 0.5f, -2.0f);
  glVertex3f(-1.0f, 0.5f, -3.0f);
  glVertex3f(0.0f, 0.0f, -3.0f);

  glVertex3f(0.0f, 0.5f, -2.0f);
  glVertex3f(1.0f, 0.5f, -3.0f);
  glVertex3f(0.0f, 0.0f, -3.0f);

  glVertex3f(-1.0f, 0.5f, -3.0f);
  glVertex3f(1.0f, 0.5f, -3.0f);
  glVertex3f(0.0f, 0.0f, -3.0f);

  glEnd();
}

void airplaneTail() {
  glPushMatrix();
  glColor3f(GREEN);
  drawTail();
  glPopMatrix();
}

void drawAirplane() {
  airplaneBody();
  airplaneWings();
  airplaneTail();
}

void light() {
  GLfloat light_specular[] = {0.6, 0.6, 0.6, 1};
  GLfloat light_diffuse[] = {0.6, 0.6, 0.6, 1};
  GLfloat light_ambient[] = {0.4, 0.4, 0.4, 1};
  GLfloat light_position[] = {50.0, 75.0, 80.0, 1.0};
  // z buffer enable
  glEnable(GL_DEPTH_TEST);
  // enable lighting
  glEnable(GL_LIGHTING);
  glShadeModel(GL_SMOOTH);
  glEnable(GL_COLOR_MATERIAL);
  glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE);
  glEnable(GL_NORMALIZE);
  // set light property
  glEnable(GL_LIGHT0);
  glLightfv(GL_LIGHT0, GL_POSITION, light_position);
  glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse);
  glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular);
  glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient);
}

int main() {
  initOpenGL();
  GLFWwindow* window = OpenGLContext::getWindow();

  // Init Camera helper
  Camera camera(glm::vec3(0, 5, 20));
  camera.initialize(OpenGLContext::getAspectRatio());
  // Store camera as glfw global variable for callbasks use
  glfwSetWindowUserPointer(window, &camera);

  // Main rendering loop
  while (!glfwWindowShouldClose(window)) {
    // Polling events.
    glfwPollEvents();
    // Update camera position and view
    camera.move(window);
    // GL_XXX_BIT can simply "OR" together to use.
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    /// TO DO Enable DepthTest
    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LEQUAL);
    // Projection Matrix
    glMatrixMode(GL_PROJECTION);
    glLoadMatrixf(camera.getProjectionMatrix());
    // ModelView Matrix
    glMatrixMode(GL_MODELVIEW);
    glLoadMatrixf(camera.getViewMatrix());

#ifndef DISABLE_LIGHT
    glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
    glClear(GL_COLOR_BUFFER_BIT);
    glClearDepth(1.0f);
    light();
#endif

    /* TODO#4-2: Update
     *       You may update position and orientation of airplane here or not.
     *       Feel free to not follow TA's structure. However, don't violate the spec.
     *
     * Hint:
     * Note:
     *       You can use `ROTATE_SPEED` and `FLYING_SPEED` as the speed constant.
     *       If the rotate/flying speed is too slow or too fast, please change `ROTATE_SPEED` or `FLYING_SPEED` value.
     *       You should finish keyCallback first.
     */
    // if the left or the right key is pressed down, keep rotating
    if (glfwGetKey(window, GLFW_KEY_LEFT) == GLFW_PRESS) {
      rotateValue += ROTATE_SPEED;
    } else if (glfwGetKey(window, GLFW_KEY_RIGHT) == GLFW_PRESS) {
      rotateValue -= ROTATE_SPEED;
    }
    rotatePosition.x = std::sin(ANGLE_TO_RADIAN(rotateValue));
    rotatePosition.z = std::cos(ANGLE_TO_RADIAN(rotateValue));
    // set up value for flyingUp, flyingForward, wingRotationAngle
    if (glfwGetKey(window, GLFW_KEY_SPACE) == GLFW_RELEASE) {
      airplanePosition.y -= FLYING_SPEED;
      if (airplanePosition.y <= 0) {
        airplanePosition.y = 0;
      }
    } else {
      airplanePosition.x += rotatePosition.x * 0.3;
      airplanePosition.y += FLYING_SPEED;
      airplanePosition.z += rotatePosition.z * 0.3;
      wingRotationAngle = 20.0f * sin(glfwGetTime() * 5.0);
    }
    // Render a white board
    glPushMatrix();
    glScalef(3, 1, 3);
    glBegin(GL_TRIANGLE_STRIP);
    glColor3f(1.0f, 1.0f, 1.0f);
    glNormal3f(0.0f, 1.0f, 0.0f);
    glVertex3f(-5.0f, 0.0f, -5.0f);
    glVertex3f(-5.0f, 0.0f, 5.0f);
    glVertex3f(5.0f, 0.0f, -5.0f);
    glVertex3f(5.0f, 0.0f, 5.0f);
    glEnd();
    glPopMatrix();

    /* TODO#3: Render the airplane
     *       1. Render the body.
     *       2. Render the wings.(Don't forget to assure wings rotate at the center of body.)
     *       3. Render the tail.
     * Hint:
     *       glPushMatrix/glPopMatrix (https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glPushMatrix.xml)
     *       glRotatef (https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glRotate.xml)
     *       glTranslatef (https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glTranslate.xml)
     *       glColor3f (https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glColor.xml)
     *       glScalef (https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/glScale.xml)
     * Note:
     *       You may implement functions for drawing components of airplane first
     *       You should try and think carefully about changing the order of rotate and translate
     */
    // rotate first then translate
    glTranslatef(airplanePosition.x, airplanePosition.y, airplanePosition.z);
    glRotated(rotateValue, 0.0, 1.0, 0.0);
    drawAirplane();

#ifdef __APPLE__
    // Some platform need explicit glFlush
    glFlush();
#endif
    glfwSwapBuffers(window);
  }
  return 0;
}
