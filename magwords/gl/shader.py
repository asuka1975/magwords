import sys
from OpenGL.GL import *

class Shader:
    def __init__(self, content, type_):
        self.handle = glCreateShader(type_)
        glShaderSource(self.handle, [content])
        glCompileShader(self.handle)

        status = ctypes.c_uint()
        glGetShaderiv(self.handle, GL_COMPILE_STATUS, status)
        if not status:
            print(glGetShaderInfoLog(self.handle).decode("utf-8"), file=sys.stderr)
            glDeleteShader(self.handle)
            self.handle = None

    def __del__(self):
        if hasattr(self, "handle") and self.handle is not None:
            glDeleteShader(self.handle)
            self.handle = None
