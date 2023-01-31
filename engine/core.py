# =================================================
# ==================== imports ====================
# =================================================
import sys
import os
import uuid
from collections import deque
from typing import Callable
from .enums import *
from .math import *
from .utils import *
from .io import *

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = '1'
import pygame


# =================================================
# ===================== Hacks =====================
# =================================================
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    INSTALLED=True
else:
    INSTALLED=False

# =================================================
# ==================== Helpers ====================
# =================================================
def fire_event(event:'Event'):
    GS.game.fire_event(event)

def on(event:'Event.__class__'):
    def decorator(func:Callable[['Event'], None]):
        GS.game.register_event_listener(EventListenerFunctionCallback(event, func))
        return func
    return decorator

# =================================================
# ==================== Engine =====================
# =================================================
# Settings relative to the engine, game saves do not belong here
class Settings:
    # d_ stands for debug settings
    d_no_debug = False
    d_level = debugLevel.collisions
    d_max_frames = 100

# GameState class, holds main global variables
class GS:
    game:'Game' = None
    rm:'ResourceManager' = None

# Game class, should be alive for the entire app's lifetime
class Game:
    def __init__(self, name:str="New game", game_definition=vec2(128, 64), display_size:vec2=vec2(1280, 720), resizable:bool=True) -> None:
        if GS.game: raise RuntimeError("Only one game instance allowed")
        GS.game = self
        self._name = name

        self._definition:vec2 = game_definition
        self._display_size:vec2 = display_size
        self._temp_screen_size:vec2 = display_size
        self._resizable:bool = resizable
        self._clear_color:Color = Colors.gray
        self._screen:pygame.surface.Surface = None
        self._canvas:pygame.surface.Surface = pygame.surface.Surface(self._definition)
        self._temp_screen:pygame.surface.Surface = None
        self._pg_clock:pygame.time.Clock = pygame.time.Clock()
        self._rm:ResourceManager = ResourceManager()
        GS.rm = self._rm

        self._dt:float = 0
        self._is_alive:bool = False
        self._event_listeners:dict[Event.__class__, list[EventListener]] = {}
    
    def init(self) -> 'Game':
        pygame.init()
        flags = pygame.RESIZABLE | pygame.DOUBLEBUF
        self._screen = pygame.display.set_mode(self._display_size, flags)
        self._temp_screen = self._screen.copy()
        self._window_resize(EventWindowResize(self._display_size))
        pygame.display.set_caption(self._name)

        self._is_alive = True

        if INSTALLED or Settings.d_no_debug:
            return self
        return self._init_debug()
    
    def should_run(self) -> bool:
        return self._is_alive
    
    def quit(self):
        self._is_alive = False
    
    def set_clear_color(self, color:Color) -> 'Game':
        self._clear_color = color
        return self
    
    def register_event_listener(self, event_listener:'EventListener') -> 'Game':
        cl = event_listener._event_class
        if cl not in self._event_listeners:
            self._event_listeners[cl] = []
        self._event_listeners[cl].append(event_listener)
        return self
    
    def fire_event(self, event:'Event') -> 'Game':
        if event.__class__ in self._event_listeners:
            for listener in self._event_listeners[event.__class__]:
                listener.trigger(event)
        return self
    
    def begin_frame(self):
        if not self._is_alive: return
        events:list[pygame.event.Event] = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()
                fire_event(EventQuit())
            elif event.type == pygame.KEYDOWN:
                fire_event(EventKeydown(event.key))
            elif event.type == pygame.KEYUP:
                fire_event(EventKeyup(event.key))
            elif event.type == pygame.VIDEORESIZE:
                e = EventWindowResize(vec2(event.w, event.h))
                self._window_resize(e)
                self.fire_event(e)
        
        self._canvas.fill(self._clear_color.to_pygame)

    
    def draw_frame(self):
        pygame.draw.circle(self._canvas, pygame.Color(255, 0, 0), (10, 10), 10)
    
    def end_frame(self):
        if not self._is_alive:
            self._exit()
            return

        pygame.transform.scale(self._canvas, self._temp_screen_size, self._temp_screen)
        delta = (self._temp_screen_size-self._display_size)/2
        self._screen.blit(self._temp_screen, -delta)
        pygame.display.flip()
        fps = 1000/self._pg_clock.tick(60)
        pygame.display.set_caption(f"{self._name} - FPS: {fps:.0f}")
    
    def _init_debug(self) -> 'Game':
        self._dts:deque[float] = deque(maxlen=Settings.d_max_frames)
        return self
    
    def _window_resize(self, event:'EventWindowResize'):
        self._display_size = event.size
        screen_ratio = self._display_size.y/self._display_size.x
        game_ratio = self._definition.y/self._definition.x
        if screen_ratio<game_ratio:
            self._temp_screen_size = vec2(int(self._display_size.y/game_ratio), int(self._display_size.y))
        else:
            self._temp_screen_size = vec2(int(self._display_size.x), int(self._display_size.x*game_ratio))
        self._temp_screen = pygame.transform.scale(self._temp_screen, self._temp_screen_size)

    def _exit(self):
        if self._is_alive:
            raise RuntimeError("Internal exit called, but exit flag isn't set")
        pygame.quit()

# Holds buffers to prevent reloading from disk
class ResourceManager:
    def __init__(self) -> None:
        self._textures:dict[str, Texture] = {}
    
    def load_texture(self, path:str, name:str=None) -> 'Texture':
        from .io import convert_path, get_name_from_path, fixed_len
        _path = convert_path(path)
        surface = pygame.image.load(path).convert_alpha()
        _name:str = None
        if name: _name = name
        else: _name = get_name_from_path(_path)
        id = uuid.uuid4()
        size = vec2(int(surface.get_width()), int(surface.get_height()))
        log(f"Loaded texture {color(fixed_len(_name, 10), Colors.blue)}   {color(fixed_len(str(int(size.x))+'x'+str(int(size.y)), 9), Colors.lightgray)} {color(_path, Colors.lightgray)}", logLevel.trace)
        texture = Texture(_name, _path, surface, size)
        self._textures[_name] = texture
    
    def get_texture(self, name:str) -> 'Texture':
        if name in self._textures:
            return self._textures[name]
        return None

    def get_texture_from_id(self, id:int) -> 'Texture':
        for texture in self._textures.values():
            if texture.id==id: return texture
        return None
    
    def load_resources_from_folder(self, path:str):
        from .io import convert_path, image_extensions
        _path = convert_path(path)
        for p, folders, files in os.walk(_path):
            for file in files:
                name, ext = os.path.splitext(file)
                if ext.lower() in image_extensions:
                    self.load_texture(os.path.join(p, file), name)
        return None

class Asset:
    def __init__(self, name:str=None, path:str=None) -> None:
        self._name:str = name if name else "Asset"
        self._path:str = path if path else ""
        self._id:uuid.UUID = None
    
    @property
    def id(self) -> uuid.UUID: return self._id
    @id.setter
    def id(self, id:uuid.UUID) -> None: self._id = id
    
    @property
    def name(self) -> str: return self._name
    @name.setter
    def name(self, value:str): self._name = value
    
    @property
    def path(self) -> str: return self._path
    @path.setter
    def path(self, value:str): self._path = value

class Texture(Asset):
    def __init__(self, name:str=None, path:str=None, surface:pygame.Surface=None, size:vec2=None) -> None:
        Asset.__init__(self, name, path)
        if surface:
            self._size = size if size else vec2(surface.get_width(), surface.get_height())
            self._surface = surface
        else:
            self._size = size if size else vec2(0, 0)
            self._surface = pygame.Surface(self._size)
    
    def __str__(self) -> str:
        return f"Texture({self._name}, {self._size})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, o:object) -> bool:
        if isinstance(o, Texture):
            return Asset.__eq__(self, o) and self._surface == o._surface and self._size == o._size
        return False
    
    def __hash__(self) -> int:
        # Combine name, id and size
        return hash((self._name, self._id, self._size))
    
    def copy(self) -> 'Texture':
        # Perform a deep copy, even on pygame's side
        return Texture(self._name, self._surface.copy(), self._size)

# Event base class
class Event:
    def __init__(self):
        self._consumed = False

# Event triggered when the game is about to quit
class EventQuit(Event):
    def __init__(self):
        Event.__init__(self)

class EventKey(Event):
    def __init__(self, key:Key):
        Event.__init__(self)
        self._key:Key = key
    
    @property
    def key(self)->Key: return self._key

class EventKeydown(EventKey):
    def __init__(self, key:Key):
        EventKey.__init__(self, key)

class EventKeyup(EventKey):
    def __init__(self, key:Key):
        EventKey.__init__(self, key)

class EventWindowResize(Event):
    def __init__(self, size:vec2):
        Event.__init__(self)
        self.size:vec2 = size

# Event listener base class
class EventListener:
    def __init__(self, event_class:Event.__class__) -> None:
        self._event_class : Event.__class__ = event_class
    
    def get_event_class(self) -> Event.__class__:
        return self._event_class
        
    def trigger(self, event:Event):
        pass

class EventListenerFunctionCallback(EventListener):
    def __init__(self, event_class:Event.__class__, callback:Callable[[Event], any]):
        EventListener.__init__(self, event_class)
        self._callback:Callable[[Event], any] = callback
    
    def trigger(self, event:Event):
        self._callback(event)