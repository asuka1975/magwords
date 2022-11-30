from setuptools import setup
from codecs import open
from os import path

with open(path.join(path.abspath(path.dirname(__file__))), encoding="utf-8") as f:
    description = f.read()

setup(
    name="magwords",
    packages=[],
    version="1.0.0",
    license="MIT",
    install_requires=["cu2qu", "freetype-py", "glfw", "numpy", "PyGLM", "PyOpenGL", "scipy"],
    author="asuka1975",
    author_email="asuka197512@gmail.com",
    url="https://github.com/asuka1975/magwords",
    description="text-rendering library for OpenGL context",
    long_description=description,
    keywords="OpenGL FreeType2 TextRendering",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ]
)