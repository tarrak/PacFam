import cocos
import pyglet
import sys

from cocos.scene import *
from cocos.director import *
from cocos.menu import *
from cocos.layer import *
from cocos.sprite import Sprite
from pyglet.app import exit
from pyglet.gl import *
from pyglet import image
from pyglet import font


class Victory(Menu):
    def __init__(self):
        super().__init__()

        menu_item = [(MenuItem("Replay!", self.play_game)), (MenuItem("Quit!", self.quit_game))]
        self.create_menu(menu_item)

    def play_game(self):
        from Game import game_scene
        director.replace(game_scene())

    def quit_game(self):
        sys.exit()

class VictoryLabel(Layer):
    def __init__(self):
        super().__init__()

        label = cocos.text.Label('Victory!',
                font_size=70,
                anchor_x='center',
                anchor_y='center',
                color=(255,255,255,255))
        label.position = 320, 640
        self.add(label)

def victory_scene():
    return Scene(Victory(), VictoryLabel())
