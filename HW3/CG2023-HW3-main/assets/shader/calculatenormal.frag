#version 330 core
layout(location = 0) out vec4 normal;
layout(location = 1) out float height;

uniform float offset;

void main() {
  const float delta = 0.01;
  // TODO3: Generate the normal map.
  //   1. Get the position of the fragment. (screen space)
  //   2. Sample 4 points from combination of x +- delta, y +- delta
  //   3. Form at least 2 triangles from those points. Calculate their surface normal
  //   4. Average the surface normal, then tranform the normal [-1, 1] to RGB [0, 1]
  //   5. (Bonus) Output the H(x, y)
  // Note:
  //   1. Height at (x, y) = H(x, y) = sin(offset - 0.1 * y)
  //   2. A simple tranform from [-1, 1] to [0, 1] is f(x) = x * 0.5 + 0.5
  //   3. For sample points, z = H(x +- delta, y +- delta)

  vec2 fragCoord = gl_FragCoord.xy;

  vec2 dx = vec2(delta, 0.0);
  vec2 dy = vec2(0.0, delta);
  vec3 p0 = vec3(fragCoord, sin(offset - 0.1 * fragCoord.y));
  vec3 p1 = vec3(fragCoord + dx, sin(offset - 0.1 * (fragCoord.y + delta)));
  vec3 p2 = vec3(fragCoord + dy, sin(offset - 0.1 * (fragCoord.y + delta)));
  vec3 p3 = vec3(fragCoord + dx + dy, sin(offset - 0.1 * (fragCoord.y + delta)));

  vec3 normal1 = normalize(cross(p1 - p0, p2 - p0));
  vec3 normal2 = normalize(cross(p3 - p1, p2 - p1));

  vec3 avgNormal = normalize(normal1 + normal2) * 0.5 + 0.5;

  height = (p0.z + p1.z + p2.z + p3.z) * 0.25 * 0.5 + 0.5;

  normal = vec4(avgNormal, 1.0);
}