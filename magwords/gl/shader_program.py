import sys
from OpenGL.GL import *

class ShaderProgram:
    def __init__(self):
        self.handle = glCreateProgram()
    
    def __del__(self):
        if self.handle is not None:
            glDeleteProgram(self.handle)
            self.handle = None

    def attach_shader(self, content, type, log_always=False):
        shader = glCreateShader(type)
        glShaderSource(shader, [content])
        glCompileShader(shader)

        status = ctypes.c_uint()
        glGetShaderiv(shader, GL_COMPILE_STATUS, status)
        if log_always or not status:
            print(glGetShaderInfoLog(shader).decode("utf-8"), file=sys.stderr)
            glDeleteShader(shader)
            return False
        
        glAttachShader(self.handle, shader)
        glDeleteShader(shader)
        return True

    def link(self, log_always=False):
        glLinkProgram(self.handle)
        status = ctypes.c_uint()
        glGetProgramiv(self.handle, GL_LINK_STATUS, status)
        if log_always or not status:
            print(glGetProgramInfoLog(self.handle).decode("utf-8"), file=sys.stderr)
            return False
        return True
    
    def use(self):
        glUseProgram(self.handle)

    def unuse(self):
        glUseProgram(0)