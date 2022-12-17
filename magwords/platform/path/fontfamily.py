"""
Created by modifying the answer of "List all system fonts as dictionary. | python" (© Yuuki Kuna (Licensed under CC BY 4.0))
https://stackoverflow.com/questions/63274244/list-all-system-fonts-as-dictionary-python
"""

from fontTools import ttLib
from os import walk, sep

def getFontsPath(path):
    return [
        dirpath.replace(sep*2, sep) + "\\" + filename
            for dirpath, _, filenames in walk(f"{path}") 
                for filename in filenames 
                    if any(filename.endswith(ext) for ext in ['.ttf', '.otf', '.ttc', '.ttz', '.woff', '.woff2'])
    ]

def getFont(font, font_path):
    x = lambda x: font['name'].getDebugName(x)
    if x(16) is None:
        return x(1), x(2), font_path
    else:
        return x(16), x(17), font_path

def genFontAndPathPair(fonts_path):
    for path in fonts_path:
        if not path.endswith('.ttc'):
            yield getFont(ttLib.TTFont(path), path)
        if path.endswith('.ttc'):
            try:
                for k in range(100):
                    yield getFont(ttLib.TTFont(path, fontNumber=k), path)
            except:
                pass

def createFontFamilyDict(directories):
    d = {}
    for directory in directories:
        fonts_path = getFontsPath(directory)
        for family, style, path in genFontAndPathPair(fonts_path):
            if family not in d:
                d[family] = {}
            d[family][style] = path
    return d
