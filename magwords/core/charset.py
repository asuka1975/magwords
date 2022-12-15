import typing as tp
import string

from OpenGL.GL import *
import glm
import freetype

from scipy.spatial import ConvexHull

from .decomposer import *
from .magtypes import DrawArraysIndirectCommand

class Charset(tp.Protocol):
    convex_vbo: GLuint
    beziers_vbo: GLuint
    inner_vbo: GLuint

    advances: list[float]
    charset: str

    def create_command_convex(self, char: str, index: int) -> DrawArraysIndirectCommand:
        ...

    def create_command_beziers(self, char: str, index: int) -> DrawArraysIndirectCommand:
        ...

    def create_command_inner(self, char: str, index: int) -> DrawArraysIndirectCommand:
        ...

class StaticCharset:
    def __init__(self, fontfamily: str, charset: str) -> None:
        self.charset: str = charset
        
        self.convex_ranges = []
        self.beziers_ranges = []
        self.inner_ranges = []

        convex_list = []
        beziers_list = []
        inner_list = []

        self.advances = []

        self._buffers = glGenBuffers(4)
        self.convex_vbo: GLuint
        self.beziers_vbo: GLuint
        self.inner_vbo: GLuint
        self.convex_vbo, self.beziers_vbo, self.inner_vbo, self.advances_ssbo = self._buffers

        face = freetype.Face(fontfamily)
        face.set_char_size(48*64)
        bbox = face.bbox
        max_height = bbox.yMax - bbox.yMin
        self.line_height = max_height

        for c in self.charset:
            face.load_char(c, freetype.FT_LOAD_NO_BITMAP)
            outline = face.glyph.outline

            self.advances.append(face.glyph.metrics.horiAdvance / max_height)
            d = { "convex" : [], "beziers" : [], "inner" : [] }
            outline.decompose(d, move, line, conic, cubic)

            if c in string.whitespace:
                convex = []
                beziers = []
                inner = []
                inner = []
            else:
                convex = [glm.vec2(x / max_height, y / max_height) for x, y in ConvexHull(d["convex"]).points]
                beziers = [glm.vec2(x / max_height, y / max_height) for x, y in d["beziers"]]
                inner = [v for ls in d["inner"] for j in range(1, len(ls) - 1) for v in [ls[0], ls[j], ls[j + 1]]]
                inner = [glm.vec2(x / max_height, y / max_height) for x, y in inner]

            self.convex_ranges.append((len(convex_list), len(convex)))
            self.beziers_ranges.append((len(beziers_list), len(beziers)))
            self.inner_ranges.append((len(inner_list), len(inner)))

            convex_list.extend(convex)
            beziers_list.extend(beziers)
            inner_list.extend(inner)

        convex_data = glm.array(convex_list)
        beziers_data = glm.array(beziers_list)
        inner_data = glm.array(inner_list)
        advances_data = (GLfloat * len(self.advances))(*self.advances)
        glBindBuffer(GL_ARRAY_BUFFER, self.convex_vbo)
        glBufferData(GL_ARRAY_BUFFER, convex_data.nbytes, convex_data.ptr, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.beziers_vbo)
        glBufferData(GL_ARRAY_BUFFER, beziers_data.nbytes, beziers_data.ptr, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.inner_vbo)
        glBufferData(GL_ARRAY_BUFFER, inner_data.nbytes, inner_data.ptr, GL_STATIC_DRAW)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, self.advances_ssbo)
        glBufferData(GL_SHADER_STORAGE_BUFFER, ctypes.sizeof(advances_data), advances_data, GL_STATIC_DRAW)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 4, self.advances_ssbo)

    def __del__(self):
        if self._buffers is not None:
            glDeleteBuffers(len(self._buffers), self._buffers)
            self._buffers = None

    def create_command_convex(self, char: str, index: int) -> DrawArraysIndirectCommand:
        i = self.charset.index(char)
        first, count = self.convex_ranges[i]
        return DrawArraysIndirectCommand(count, 0, first, index)

    def create_command_beziers(self, char: str, index: int) -> DrawArraysIndirectCommand:
        i = self.charset.index(char)
        first, count = self.beziers_ranges[i]
        return DrawArraysIndirectCommand(count, 0, first, index)

    def create_command_inner(self, char: str, index: int) -> DrawArraysIndirectCommand:
        i = self.charset.index(char)
        first, count = self.inner_ranges[i]
        return DrawArraysIndirectCommand(count, 0, first, index)


class DynamicCharset:
    def __init__(self, fontfamily: str) -> None:
        raise NotImplementedError()

    def create_command_convex(self, char: str, index: int) -> DrawArraysIndirectCommand:
        raise NotImplementedError()

    def create_command_beziers(self, char: str, index: int) -> DrawArraysIndirectCommand:
        raise NotImplementedError()

    def create_command_inner(self, char: str, index: int) -> DrawArraysIndirectCommand:
        raise NotImplementedError()
    