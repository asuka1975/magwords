import os
import platform
from .fontfamily import createFontFamilyDict

font_directories: list[str] = [os.path.join(os.environ.get("WINDIR"), "Fonts")]
font_dictionary: dict[str, dict[str, str]] = createFontFamilyDict(font_directories)

if platform.win32_ver()[0] == "10":
    default_font: tuple[str, str] = ("Yu Gothic", "Regular")
else:
    raise NotImplementedError()