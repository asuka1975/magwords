#version 460

layout (location = 0) in vec2 p;


void main(void) {
    vec2 px = dFdx(p);
    vec2 py = dFdy(p);
    float fx = (2.0*p.x)*px.x - px.y;
    float fy = (2.0*p.x)*py.x - py.y;
    float sd = (p.x*p.x - p.y)/sqrt(fx*fx + fy*fy);
    float alpha = 0.5 - sd;
    if (alpha > 1.0) {
        // inside
        gl_FragColor = vec4(1.0);
    } else if (alpha < 0.0) {
        // outside
        discard;
    } else {
        // near boundary
        gl_FragColor = vec4(alpha);
    }
}