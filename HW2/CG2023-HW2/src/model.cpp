#include "model.h"

#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

#include <glm/vec3.hpp>

Model* Model::fromObjectFile(const char* obj_file) {
  Model* m = new Model();

  std::ifstream ObjFile(obj_file);

  if (!ObjFile.is_open()) {
    std::cout << "Can't open File !" << std::endl;
    return NULL;
  }

  /* TODO#1: Load model data from OBJ file
   *         You only need to handle v, vt, vn, f
   *         Other fields you can directly ignore
   *         Fill data into m->positions, m->texcoords m->normals and m->numVertex
   *         Data format:
   *           For positions and normals
   *         | 0    | 1    | 2    | 3    | 4    | 5    | 6    | 7    | 8    | 9    | 10   | 11   | ...
   *         | face 1                                                       | face 2               ...
   *         | v1x  | v1y  | v1z  | v2x  | v2y  | v2z  | v3x  | v3y  | v3z  | v1x  | v1y  | v1z  | ...
   *         | vn1x | vn1y | vn1z | vn1x | vn1y | vn1z | vn1x | vn1y | vn1z | vn1x | vn1y | vn1z | ...
   *           For texcoords
   *         | 0    | 1    | 2    | 3    | 4    | 5    | 6    | 7    | ...
   *         | face 1                                  | face 2        ...
   *         | v1x  | v1y  | v2x  | v2y  | v3x  | v3y  | v1x  | v1y  | ...
   * Note:
   *        OBJ File Format (https://en.wikipedia.org/wiki/Wavefront_.obj_file)
   *        Vertex per face = 3 or 4
   */

  // object file parser
  std::string line;
  std::string prefix;
  std::stringstream ss;

  // iterate through data
  std::vector<glm::vec3> currPositions;
  std::vector<glm::vec3> currNormals;
  std::vector<glm::vec2> currTextcoords;

  glm::vec2 tempVec2;
  glm::vec3 tempVec3;

  // add foo element, since index of object file starts from 1
  currPositions.push_back(tempVec3);
  currNormals.push_back(tempVec3);
  currTextcoords.push_back(tempVec2);

  GLint tempGlint = 0;

  // read line by line
  while (getline(ObjFile, line)) {
    ss.clear();
    ss.str(line);
    ss >> prefix;
    // positions
    if (prefix == "v") {
      ss >> tempVec3.x >> tempVec3.y >> tempVec3.z;
      currPositions.push_back(tempVec3);
    }
    // normals
    else if (prefix == "vn") {
      ss >> tempVec3.x >> tempVec3.y >> tempVec3.z;
      currNormals.push_back(tempVec3);
    }
    //textcoords
    else if (prefix == "vt") {
      ss >> tempVec2.x >> tempVec2.y;
      currTextcoords.push_back(tempVec2);
    }
    // push data
    else if (prefix == "f") {
      int counter = 0;
      while (ss >> tempGlint) {
        if (counter == 0) {
          m->positions.push_back(currPositions[tempGlint].x);
          m->positions.push_back(currPositions[tempGlint].y);
          m->positions.push_back(currPositions[tempGlint].z);
        } else if (counter == 1) {
          m->texcoords.push_back(currTextcoords[tempGlint].x);
          m->texcoords.push_back(currTextcoords[tempGlint].y);
        } else if (counter == 2) {
          m->normals.push_back(currNormals[tempGlint].x);
          m->normals.push_back(currNormals[tempGlint].y);
          m->normals.push_back(currNormals[tempGlint].z);
        }
        // ignore '/' and space
        if (ss.peek() == '/') {
          counter++;
          ss.ignore(1, '/');
        } else if (ss.peek() == ' ') {
          counter++;
          ss.ignore(1, ' ');
        }
        // new vector
        if (counter > 2) {
          counter = 0;
        }
      }
    }
  }

  // set num of vertex
  m->numVertex = m->positions.size();

  if (ObjFile.is_open()) ObjFile.close();

  return m;
}
