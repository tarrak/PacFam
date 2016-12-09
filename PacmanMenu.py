import cocos
import pyglet
import sys
from Game import game_scene
from cocos.scene import *
from cocos.director import *
from cocos.menu import *
from cocos.layer import *
from cocos.sprite import Sprite
from pyglet.app import exit
from pyglet.gl import *
from pyglet import image
from pyglet import font

class PacmanMenu(Menu):
    def __init__(self):
        super().__init__()

        menu_item = [(MenuItem("Play!", self.play_game)), (MenuItem(" ", None)), (MenuItem("Quit!", self.quit_game))]

        self.create_menu(menu_item)

    def play_game(self):
        director.replace(game_scene())

    def quit_game(self):
        sys.exit()

class PacmanLogo(Layer):
	def __init__( self ):
		super().__init__()
		x,y	= director.get_window_size()
		self.logo = Sprite('images/pacmanLogo.gif')
		self.logo.position	= x//2+16,600
		self.add(self.logo)

director.init(width=608, height=800)
director.run(Scene(PacmanMenu(), PacmanLogo()))
