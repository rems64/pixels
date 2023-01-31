import pygame

class ColorsFG:
    Black = "\033[30m"
    Red = "\033[31m"
    Green = "\033[32m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Magenta = "\033[35m"
    Cyan = "\033[36m"
    White = "\033[37m"
    BrighBlack = "\033[90m"
    BrightRed = "\033[91m"
    BrightGreen = "\033[92m"
    BrightYellow = "\033[93m"
    BrightBlue = "\033[94m"
    BrightMagenta = "\033[95m"
    BrightCyan = "\033[96m"
    BrightWhite = "\033[97m"

class ColorsBG:
    Black = "\033[40m"
    Red = "\033[41m"
    Green = "\033[42m"
    Yellow = "\033[43m"
    Blue = "\033[44m"
    Magenta = "\033[45m"
    Cyan = "\033[46m"
    White = "\033[47m"
    BrighBlack = "\033[100m"
    BrightRed = "\033[101m"
    BrightGreen = "\033[102m"
    BrightYellow = "\033[103m"
    BrightBlue = "\033[104m"
    BrightMagenta = "\033[105m"
    BrightCyan = "\033[106m"
    BrightWhite = "\033[107m"


# =================================================
# ==================== Defines ====================
# =================================================
vec2 = pygame.Vector2
vec3 = pygame.Vector3

class Color:
    def __init__(self, r, g, b, alpha:int=255) -> None:
        self._col:vec3 = vec3(int(r), int(g), int(b))
        self._alpha = int(alpha)
    
    @property
    def r(self): return int(self._col.x)

    @property
    def g(self): return int(self._col.y)
    
    @property
    def b(self): return int(self._col.z)
    
    @property
    def a(self): return int(self._alpha)

    @r.setter
    def r(self, val:int): self._col.x = int(val)
    
    @g.setter
    def g(self, val:int): self._col.y = int(val)
    
    @b.setter
    def b(self, val:int): self._col.z = int(val)
    
    @a.setter
    def a(self, val:int): self._alpha = int(val)

    @property
    def to_pygame(self):
        return pygame.Color((self._col.x, self._col.y, self._col.z, self._alpha))
    
    def __mul__(self, other):
        if isinstance(other, Color):
            return Color(self.r*other.r, self.g*other.g, self.b*other.b)
        return Color(self.r*other, self.g*other, self.b*other)

    def __rmul__(self, other):
        if isinstance(other, Color):
            return Color(self.r*other.r, self.g*other.g, self.b*other.b)
        return Color(self.r*other, self.g*other, self.b*other)
    
    def __str__(self):
        return f"({self.r}, {self.g}, {self.b})"

class Colors:
    red         = Color(245, 90 , 66 )
    orange      = Color(245, 170, 66 )
    yellow      = Color(245, 252, 71 )
    green       = Color(92 , 252, 71 )
    blue        = Color(71 , 177, 252)
    purple      = Color(189, 71 , 252)
    white       = Color(255, 255, 255)
    gray        = Color(42 , 42 , 42 )
    lightgray   = Color(142, 142, 142)
    black       = Color(0  , 0  , 0  )

class logLevel:
    """
    Log levels
    """
    info    = Colors.green
    timer   = Colors.blue
    warning = Colors.yellow
    error   = Colors.red
    trace   = Colors.lightgray

class debugLevel:
    """
    Debug levels
    """
    none        = 0
    physics     = 1<<0
    drawing     = 1<<1
    collisions  = 1<<2
    
    all = ~0

class Key:
    unknown = pygame.K_UNKNOWN
    up = pygame.K_UP
    left = pygame.K_LEFT
    down = pygame.K_DOWN
    right = pygame.K_RIGHT
    space = pygame.K_SPACE
    leftCtrl = pygame.K_LCTRL
    rightCtrl = pygame.K_RCTRL
    leftShift = pygame.K_LSHIFT
    rightShift = pygame.K_RSHIFT
    leftAlt = pygame.K_LALT
    rightAlt = pygame.K_RALT
    enter = pygame.K_RETURN
    backspace = pygame.K_BACKSPACE
    tab = pygame.K_TAB
    escape = pygame.K_ESCAPE
    delete = pygame.K_DELETE

    a = pygame.K_a
    b = pygame.K_b
    c = pygame.K_c
    d = pygame.K_d
    e = pygame.K_e
    f = pygame.K_f
    g = pygame.K_g
    h = pygame.K_h
    i = pygame.K_i
    j = pygame.K_j
    k = pygame.K_k
    l = pygame.K_l
    m = pygame.K_m
    n = pygame.K_n
    o = pygame.K_o
    p = pygame.K_p
    q = pygame.K_q
    r = pygame.K_r
    s = pygame.K_s
    t = pygame.K_t
    u = pygame.K_u
    v = pygame.K_v
    w = pygame.K_w
    x = pygame.K_x
    y = pygame.K_y
    z = pygame.K_z

    one = pygame.K_1
    two = pygame.K_2
    three = pygame.K_3
    four = pygame.K_4
    five = pygame.K_5
    six = pygame.K_6
    seven = pygame.K_7
    eight = pygame.K_8
    nine = pygame.K_9
    zero = pygame.K_0

    f1 = pygame.K_F1
    f2 = pygame.K_F2
    f3 = pygame.K_F3
    f4 = pygame.K_F4
    f5 = pygame.K_F5
    f6 = pygame.K_F6
    f7 = pygame.K_F7
    f8 = pygame.K_F8
    f9 = pygame.K_F9
    f10 = pygame.K_F10
    f11 = pygame.K_F11
    f12 = pygame.K_F12