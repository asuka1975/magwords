import importlib
import platform

try:
    system = importlib.import_module(f".{platform.system().lower()}", "magwords.platform.path")
except ModuleNotFoundError:
    raise NotImplementedError()

def get_font_path(family: str=None, style: str=None) -> str:
    global system
    if family is None:
        family = system.default_font[0]
    if style is None:
        style = list(system.font_dictionary[family].values())[0] if system.default_font[1] not in system.font_dictionary[family] else system.default_font[1]
    return system.font_dictionary[family][style]