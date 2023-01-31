import os
import sys
from .enums import *
import uuid

image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp"]

class AssetTypes:
    texture = 1<<0
    sound   = 1<<1
    music   = 1<<2
    font    = 1<<3

def convert_path(relative_path:str):
        try:
            # PyInstaller creates a temporary folder and stores path in _MEIPASS
            base_path = sys._MEIPASS  # type: ignore # pylint: disable=no-member
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)

def get_name_from_path(path:str) -> str:
    return os.path.splitext(path)[0]

# Copied from the colorit library
def clear_console():
    if sys.platform.startswith("win32"):
        os.system("cls")
    elif sys.platform.startswith("darwin") or sys.platform.startswith("linux"):
        os.system("clear")

def color(text, rgb:Color):
    return "\033[38;2;{};{};{}m{}\033[0m".format(str(int(rgb.r)), str(int(rgb.g)), str(int(rgb.b)), text)

def color_ansi(text, color:Color):
    return "{}{}\033[0m".format(color, text)

def background(text, rgb:Color):
    return "\033[48;2;{};{};{}m{}\033[0m".format(str(int(rgb.r)), str(int(rgb.g)), str(int(rgb.b)), text)

def log(msg, type:Color=logLevel.info) -> None:
    pretext = "[WARN]" if type==logLevel.warning else "[INFO]" if type==logLevel.info or type==logLevel.trace else "[TIME]" if type==logLevel.timer else "[ERRO]"
    print(color("{} {}".format(pretext, format(msg)), type))

def log_newline() -> None:
    print("")

def logf(frame: int, target_frame: int, *args, **kwargs) -> None:
    """
    Log if target_frame matches frame
    """
    if frame==target_frame:
        log(*args, **kwargs)

def fixed_len(string:str, length:int):
    if len(string)>length:
        if length>2:
            return string[:length-2]+'..'
        return string[:length]
    return string+' '*(length-len(string))


def key_to_str(key:Key) -> str:
    """
    Convert key code to string
    """
    if key==Key.a: return "a"
    if key==Key.b: return "b"
    if key==Key.c: return "c"
    if key==Key.d: return "d"
    if key==Key.e: return "e"
    if key==Key.f: return "f"
    if key==Key.g: return "g"
    if key==Key.h: return "h"
    if key==Key.i: return "i"
    if key==Key.j: return "j"
    if key==Key.k: return "k"
    if key==Key.l: return "l"
    if key==Key.m: return "m"
    if key==Key.n: return "n"
    if key==Key.o: return "o"
    if key==Key.p: return "p"
    if key==Key.q: return "q"
    if key==Key.r: return "r"
    if key==Key.s: return "s"
    if key==Key.t: return "t"
    if key==Key.u: return "u"
    if key==Key.v: return "v"
    if key==Key.w: return "w"
    if key==Key.x: return "x"
    if key==Key.y: return "y"
    if key==Key.z: return "z"

    if key==Key.zero: return "0"
    if key==Key.one: return "1"
    if key==Key.two: return "2"
    if key==Key.three: return "3"
    if key==Key.four: return "4"
    if key==Key.five: return "5"
    if key==Key.six: return "6"
    if key==Key.seven: return "7"
    if key==Key.eight: return "8"
    if key==Key.nine: return "9"
    
    if key==Key.unknown: return "unknown"
    if key==Key.up: return "up"
    if key==Key.left: return "left"
    if key==Key.down: return "down"
    if key==Key.right: return "right"
    if key==Key.space: return "space"
    if key==Key.leftCtrl: return "left ctrl"
    if key==Key.rightCtrl: return "right ctrl"
    if key==Key.leftShift: return "left shift"
    if key==Key.rightShift: return "right shift"
    if key==Key.leftAlt: return "left alt"
    if key==Key.rightAlt: return "right alt"
    if key==Key.enter: return "enter"
    if key==Key.backspace: return "backspace"
    if key==Key.tab: return "tab"
    if key==Key.escape: return "escape"
    if key==Key.f1: return "f1"
    if key==Key.f2: return "f2"
    if key==Key.f3: return "f3"
    if key==Key.f4: return "f4"
    if key==Key.f5: return "f5"
    if key==Key.f6: return "f6"
    if key==Key.f7: return "f7"
    if key==Key.f8: return "f8"
    if key==Key.f9: return "f9"
    if key==Key.f10: return "f10"
    if key==Key.f11: return "f11"
    if key==Key.f12: return "f12"

def key_to_print(key:Key) -> str:
    """
    Convert key code to printable string
    """
    if key==Key.a: return "a"
    if key==Key.b: return "b"
    if key==Key.c: return "c"
    if key==Key.d: return "d"
    if key==Key.e: return "e"
    if key==Key.f: return "f"
    if key==Key.g: return "g"
    if key==Key.h: return "h"
    if key==Key.i: return "i"
    if key==Key.j: return "j"
    if key==Key.k: return "k"
    if key==Key.l: return "l"
    if key==Key.m: return "m"
    if key==Key.n: return "n"
    if key==Key.o: return "o"
    if key==Key.p: return "p"
    if key==Key.q: return "q"
    if key==Key.r: return "r"
    if key==Key.s: return "s"
    if key==Key.t: return "t"
    if key==Key.u: return "u"
    if key==Key.v: return "v"
    if key==Key.w: return "w"
    if key==Key.x: return "x"
    if key==Key.y: return "y"
    if key==Key.z: return "z"
    
    if key==Key.one: return "1"
    if key==Key.two: return "2"
    if key==Key.three: return "3"
    if key==Key.four: return "4"
    if key==Key.five: return "5"
    if key==Key.six: return "6"
    if key==Key.seven: return "7"
    if key==Key.eight: return "8"
    if key==Key.nine: return "9"
    if key==Key.zero: return "0"

    if key==Key.space: return " "
    if key==Key.enter: return "\n"
    if key==Key.tab: return "\t"
    if key==Key.backspace: return "\b"
    return ""