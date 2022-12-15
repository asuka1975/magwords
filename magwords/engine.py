import os
import string

from OpenGL.GL import *
import glm

from .core.charset import DynamicCharset, StaticCharset, Charset
from .core.magtypes import Environment, DrawArraysIndirectCommand
from .gl.shader import ShaderProgram

class FontEngine:
    LIMIT_NUM_CHARACTERS = 100000

    def __init__(self, fontfamily: str, env: Environment, charset: str=string.printable):
        self.charset: Charset  = DynamicCharset(fontfamily) if charset is None else StaticCharset(fontfamily, charset)
        self.num_characters = 0
        self.env: Environment = env
        
        self._vaos = glGenVertexArrays(3)
        self.convex_vao, self.beziers_vao, self.inner_vao = self._vaos
        self._buffers = glGenBuffers(2)
        self.env_ubo, self.char_model_vbo = self._buffers
        # for model matrice
        glBindBuffer(GL_ARRAY_BUFFER, self.char_model_vbo)
        glBufferData(GL_ARRAY_BUFFER, glm.sizeof(glm.mat3) * FontEngine.LIMIT_NUM_CHARACTERS, None, GL_DYNAMIC_DRAW)

        self._command_buffers = glGenBuffers(3)
        self.convex_dibo, self.beziers_dibo, self.inner_dibo = self._command_buffers
        
        convex_command = (DrawArraysIndirectCommand * len(self.charset.charset))(*[self.charset.create_command_convex(c, 0) for c in self.charset.charset])
        beziers_command = (DrawArraysIndirectCommand * len(self.charset.charset))(*[self.charset.create_command_beziers(c, 0) for c in self.charset.charset])
        inner_command = (DrawArraysIndirectCommand * len(self.charset.charset))(*[self.charset.create_command_inner(c, 0) for c in self.charset.charset])
        glBindBuffer(GL_DRAW_INDIRECT_BUFFER, self.convex_dibo)
        glBufferData(GL_DRAW_INDIRECT_BUFFER, ctypes.sizeof(DrawArraysIndirectCommand) * len(self.charset.charset), convex_command, GL_STATIC_DRAW)
        glBindBuffer(GL_DRAW_INDIRECT_BUFFER, self.beziers_dibo)
        glBufferData(GL_DRAW_INDIRECT_BUFFER, ctypes.sizeof(DrawArraysIndirectCommand) * len(self.charset.charset), beziers_command, GL_STATIC_DRAW)
        glBindBuffer(GL_DRAW_INDIRECT_BUFFER, self.inner_dibo)
        glBufferData(GL_DRAW_INDIRECT_BUFFER, ctypes.sizeof(DrawArraysIndirectCommand) * len(self.charset.charset), inner_command, GL_STATIC_DRAW)

        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, self.convex_dibo)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 1, self.beziers_dibo)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 2, self.inner_dibo)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 3, self.char_model_vbo)

        self.program1 = ShaderProgram()
        with open(os.path.join(os.path.dirname(__file__), "shaders", "base.vert"), "r") as f:
            self.program1.attach_shader(f.read(), GL_VERTEX_SHADER)
        with open(os.path.join(os.path.dirname(__file__), "shaders", "base.frag"), "r") as f:
            self.program1.attach_shader(f.read(), GL_FRAGMENT_SHADER)
        self.program1.link()

        self.program2 = ShaderProgram()
        with open(os.path.join(os.path.dirname(__file__), "shaders", "bezier.vert"), "r") as f:
            self.program2.attach_shader(f.read(), GL_VERTEX_SHADER)
        with open(os.path.join(os.path.dirname(__file__), "shaders", "bezier.frag"), "r") as f:
            self.program2.attach_shader(f.read(), GL_FRAGMENT_SHADER)
        self.program2.link()

        # for environment variables (DPI, window size, etc.)
        glBindBuffer(GL_UNIFORM_BUFFER, self.env_ubo)
        glBufferData(GL_UNIFORM_BUFFER, ctypes.sizeof(self.env), ctypes.byref(self.env), GL_STATIC_DRAW)
        glBindBufferBase(GL_UNIFORM_BUFFER, 0, self.env_ubo)

        glBindVertexArray(self.convex_vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.charset.convex_vbo)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, self.char_model_vbo)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 9 * ctypes.sizeof(GLfloat), GLvoidp(0))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 9 * ctypes.sizeof(GLfloat), GLvoidp(3 * ctypes.sizeof(GLfloat)))
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, 9 * ctypes.sizeof(GLfloat), GLvoidp(6 * ctypes.sizeof(GLfloat)))
        glVertexAttribDivisor(1, 1)
        glVertexAttribDivisor(2, 1)
        glVertexAttribDivisor(3, 1)
        glBindVertexArray(self.beziers_vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.charset.beziers_vbo)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, self.char_model_vbo)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 9 * ctypes.sizeof(GLfloat), GLvoidp(0))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 9 * ctypes.sizeof(GLfloat), GLvoidp(3 * ctypes.sizeof(GLfloat)))
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, 9 * ctypes.sizeof(GLfloat), GLvoidp(6 * ctypes.sizeof(GLfloat)))
        glVertexAttribDivisor(1, 1)
        glVertexAttribDivisor(2, 1)
        glVertexAttribDivisor(3, 1)
        glBindVertexArray(self.inner_vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.charset.inner_vbo)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, self.char_model_vbo)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 9 * ctypes.sizeof(GLfloat), GLvoidp(0))
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 9 * ctypes.sizeof(GLfloat), GLvoidp(3 * ctypes.sizeof(GLfloat)))
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, 9 * ctypes.sizeof(GLfloat), GLvoidp(6 * ctypes.sizeof(GLfloat)))
        glVertexAttribDivisor(1, 1)
        glVertexAttribDivisor(2, 1)
        glVertexAttribDivisor(3, 1)
        glBindVertexArray(0)

        glClearStencil(0)

    def __del__(self):
        if self._vaos is not None:
            glDeleteVertexArrays(len(self._vaos), self._vaos)
            self._vaos = None
        if self._buffers is not None:
            glDeleteBuffers(len(self._buffers), self._buffers)
            self._buffers = None
        if self._command_buffers is not None:
            glDeleteBuffers(len(self._command_buffers), self._command_buffers)
            self._command_buffers = None
        if self.program1 is not None:
            glDeleteProgram(self.program1.handle)
            self.program1 = None
        if self.program2 is not None:
            glDeleteProgram(self.program2.handle)
            self.program2 = None

    def draw(self):
        glClear(GL_STENCIL_BUFFER_BIT)
        glEnable(GL_STENCIL_TEST)

        glEnable(GL_SAMPLE_ALPHA_TO_COVERAGE)
        glStencilFunc(GL_ALWAYS, 0, ~0)
        glStencilOp(GL_KEEP, GL_INVERT, GL_INVERT)
        glColorMask(False, False, False, False)

        glBindBuffer(GL_DRAW_INDIRECT_BUFFER, self.beziers_dibo)
        glBindVertexArray(self.beziers_vao)
        self.program2.use()
        glMultiDrawArraysIndirect(GL_TRIANGLES, None, len(self.charset.charset), 0)
        self.program2.unuse()
        glBindVertexArray(0)

        glBindBuffer(GL_DRAW_INDIRECT_BUFFER, self.inner_dibo)
        glBindVertexArray(self.inner_vao)
        self.program1.use()
        glMultiDrawArraysIndirect(GL_TRIANGLES, None, len(self.charset.charset), 0)
        self.program1.unuse()
        glBindVertexArray(0)

        glDisable(GL_SAMPLE_ALPHA_TO_COVERAGE)
        glStencilFunc(GL_NOTEQUAL, 0, ~0)
        glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)
        glColorMask(True, True, True, True)

        glBindBuffer(GL_DRAW_INDIRECT_BUFFER, self.convex_dibo)
        glBindVertexArray(self.convex_vao)
        self.program1.use() 
        glMultiDrawArraysIndirect(GL_TRIANGLE_FAN, None, len(self.charset.charset), 0)
        self.program1.unuse()
        glBindVertexArray(0)

        glDisable(GL_STENCIL_TEST)