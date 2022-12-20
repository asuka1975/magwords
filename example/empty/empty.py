import atexit

import glfw
from OpenGL.GL import *

import magwords
from magwords.core.magtypes import Environment, DrawArraysIndirectCommand
from magwords.platform.monitor.glfw import get_inch_per_pixel
from magwords.platform.path import get_font_path


def main():
    if glfw.init() == glfw.FALSE:
        raise RuntimeError("failed to initialize GLFW")
    atexit.register(glfw.terminate)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 4)

    window = glfw.create_window(1500, 1080, "simple-character", None, None)
    if window is None:
        raise RuntimeError("failed to create GLFWwindow")
    atexit.register(glfw.destroy_window, window)
    glfw.make_context_current(window)

    ipp = get_inch_per_pixel()
    env = Environment((GLfloat * 2)(*ipp), (GLfloat * 2)(1500, 1080))
    engine = magwords.FontEngine(get_font_path(), env)


    glClearColor(1, 1, 1, 1)
    while glfw.window_should_close(window) == glfw.FALSE:
        glClear(GL_COLOR_BUFFER_BIT)

        engine.draw()

        glfw.swap_buffers(window)
        glfw.wait_events()

if __name__ == "__main__":
    main()