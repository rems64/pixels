from engine.core import *
from engine.io import *

game = Game("Le truc de construction à la overcooked qui n'a pas encore de nom", display_size=vec2(1280, 720), resizable=True)
game.init()

GS.rm.load_resources_from_folder("assets")

@on(EventKeydown)
def on_keydown(event:EventKeydown):
    if event.key == Key.escape:
        game.quit()

while game.should_run():
    game.begin_frame()
    game.draw_frame()
    game.end_frame()