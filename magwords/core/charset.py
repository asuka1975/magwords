import typing as tp

from OpenGL.GL import *

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

