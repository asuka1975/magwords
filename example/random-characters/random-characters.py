import atexit
import random
from ctypes import sizeof

import glfw
from OpenGL.GL import *
import glm

import magwords
from magwords.core.magtypes import Environment, DrawArraysIndirectCommand
from magwords.platform.monitor.glfw import get_inch_per_pixel
from magwords.platform.path import get_font_path


def create_model_matrice(pos, font_size):
    return glm.mat3(
        font_size, 0, 0,
        0, font_size, 0,
        *pos, 1
    )


def main():
    if glfw.init() == glfw.FALSE:
        raise RuntimeError("failed to initialize GLFW")
    atexit.register(glfw.terminate)

    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 6)

    window = glfw.create_window(1500, 1080, "random-characters", None, None)
    if window is None:
        raise RuntimeError("failed to create GLFWwindow")
    atexit.register(glfw.destroy_window, window)
    glfw.make_context_current(window)

    ipp = get_inch_per_pixel()
    env = Environment((GLfloat * 2)(*ipp), (GLfloat * 2)(1500, 1080))
    engine = magwords.FontEngine(get_font_path(), env)

    num_chars = 100
    mats = glm.array([create_model_matrice((random.random() * 30, -random.random() * 20), 1) for _ in range(num_chars)])
    glNamedBufferSubData(engine.char_model_vbo, 0, mats.nbytes, mats.ptr)
    
    beziers_commands = (DrawArraysIndirectCommand * len(engine.charset.charset))()
    convex_commands = (DrawArraysIndirectCommand * len(engine.charset.charset))()
    inner_commands = (DrawArraysIndirectCommand * len(engine.charset.charset))()
    glGetNamedBufferSubData(engine.beziers_dibo, 0, sizeof(beziers_commands), beziers_commands)
    glGetNamedBufferSubData(engine.convex_dibo, 0, sizeof(convex_commands), convex_commands)
    glGetNamedBufferSubData(engine.inner_dibo, 0, sizeof(inner_commands), inner_commands)
    for _ in range(num_chars):
        j = random.randint(0, len(engine.charset.charset) - 1)
        beziers_commands[j].instanceCount += 1
        convex_commands[j].instanceCount += 1
        inner_commands[j].instanceCount += 1
    offset = 0
    for i in range(len(engine.charset.charset)):
        beziers_commands[i].baseInstance = offset
        convex_commands[i].baseInstance = offset
        inner_commands[i].baseInstance = offset
        offset += beziers_commands[i].instanceCount
    glNamedBufferSubData(engine.beziers_dibo, 0, sizeof(beziers_commands), beziers_commands)
    glNamedBufferSubData(engine.convex_dibo, 0, sizeof(convex_commands), convex_commands)
    glNamedBufferSubData(engine.inner_dibo, 0, sizeof(inner_commands), inner_commands)
    
    glClearColor(1, 1, 1, 1)
    while glfw.window_should_close(window) == glfw.FALSE:
        glClear(GL_COLOR_BUFFER_BIT)

        engine.draw()

        glfw.swap_buffers(window)
        glfw.wait_events()

if __name__ == "__main__":
    main()