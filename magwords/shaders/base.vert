#version 460

layout (location = 0) in vec2 position;
layout (location = 1) in mat3 model;

layout (std140, binding = 0) uniform Env {
    vec2 inch_per_dot;
    vec2 window;
};

const float inch_per_point = 1.0 / 72.0;

void main() {
    vec2 window_inch = window * inch_per_dot;
    mat3 proj = mat3(
        window.y / window.x, 0, 0,
        0, 1, 0,
        0, 0, 1
    );
    mat3 move = mat3(
        1, 0, 0,
        0, 1, 0,
        -1 + inch_per_point / window_inch.x * 2, 1 - inch_per_point / window_inch.y * 2 * 12, 1
    );
    vec3 p = vec3(inch_per_point / window_inch * 2 * 12, 1) * (model * vec3(position, 1));
    p = move * proj * vec3(p.xy, 1);
    gl_Position = vec4(p.xy, 0, 1);
}