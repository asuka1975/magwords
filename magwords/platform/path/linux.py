import os
import subprocess

from .fontfamily import createFontFamilyDict

font_directories: list[str] = [os.path.join(d, "fonts") for d in os.environ.get("XDG_DATA_DIRS").split(":")]
font_dictionary: dict[str, dict[str, str]] = createFontFamilyDict(font_directories)

try:
    default_font: str = font_dictionary[subprocess.run(["fc-match", "-f", "%{family}"], capture_output=True, text=True).stdout][subprocess.run(["fc-match", "-f", "%{style}"], capture_output=True, text=True).stdout]
except FileNotFoundError:
    raise NotImplementedError()