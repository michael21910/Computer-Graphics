#version 330 core
layout(location = 0) out vec4 FragColor;

in VS_OUT {
  vec3 position;
  vec3 normal;
  flat vec3 viewPosition;
} fs_in;

uniform samplerCube skybox;

uniform float fresnelBias;
uniform float fresnelScale;
uniform float fresnelPower;

void main() {
  // Refractive index of R, G, and B respectively
  vec3 Eta = vec3(1/ 1.39, 1 / 1.44, 1 / 1.47);
  // TODO2: fresnel reflection and refraction
  // Hint:
  //   1. You should query the texture for R, G, and B values respectively to create dispersion effect.
  //   2. You should use those uniform variables in the equation(1).
  // Note:
  //   1. The link 1 is not GLSL you just check the concept.
  //   2. We use the empirical approach of fresnel equation below.
  //      clamp(fresnelBias + fresnelScale * pow(1 + dot(I, N), fresnelPower), 0.0, 1.0); (1)
  // Reference:
  //   1. Overview: https://developer.download.nvidia.com/CgTutorial/cg_tutorial_chapter07.html
  //   2. Refract : https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/refract.xhtml
  //   3. Reflect : https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/reflect.xhtml
  //   3. Clamp   : https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/clamp.xhtml
  //   3. Mix     : https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/mix.xhtml

  // FragColor = vec4(0);
  vec3 I = normalize(fs_in.viewPosition);
  vec3 N = normalize(fs_in.normal);
  vec3 R = reflect(I, N);
  vec3 refractColor = vec3(0);
  vec3 reflectColor = vec3(0);
  for (int i = 0; i < 3; i++) {
    float eta = Eta[i];
    float cosi = clamp(dot(I, N), -1.0, 1.0);
    float etai = 1.0;
    float etat = eta;
    if (cosi < 0.0) {
      cosi = -cosi;
    } else {
      float tmp = etai;
      etai = etat;
      etat = tmp;
      N = -N;
    }
    float sint = etai / etat * sqrt(max(0.0, 1.0 - cosi * cosi));
    if (sint >= 1.0) {
      refractColor[i] = 0.0;
    } else {
      float cost = sqrt(max(0.0, 1.0 - sint * sint));
      vec3 t = refract(I, N, etai / etat);
      refractColor[i] = fresnelBias + fresnelScale * pow(1 + dot(I, N), fresnelPower);
    }
    reflectColor[i] = fresnelBias + fresnelScale * pow(1 + dot(I, N), fresnelPower);
  }
  FragColor = vec4(mix(refractColor, reflectColor, 0.5), 1.0);
}
