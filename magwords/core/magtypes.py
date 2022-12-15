import ctypes

class DrawArraysIndirectCommand(ctypes.Structure):
    _fields_ = [
        ("count", ctypes.c_uint),
        ("instanceCount", ctypes.c_uint),
        ("first", ctypes.c_uint),
        ("baseInstance", ctypes.c_uint)
    ]

class Environment(ctypes.Structure):
    _fields_ = [
        ("inch_per_dot", ctypes.c_float * 2),
        ("window", ctypes.c_float * 2)
    ]