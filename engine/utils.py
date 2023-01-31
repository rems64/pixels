from .enums import *

def color_to_pygame(color:Color) -> pygame.Color:
    return pygame.Color(int(color.r), int(color.g), int(color.b), int(color.a))
