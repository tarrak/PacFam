import sys
import random
import cocos
import pyglet
import random
import math
from cocos.text import Label
from cocos import scene, tiles
from cocos.layer import Layer
from cocos.director import director
from cocos.sprite import Sprite
import cocos.collision_model as cm

SPEED = 7

MAP_TEMPLATE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,2,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,2,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1],
    [3,3,3,1,0,1,0,0,0,0,0,0,0,1,0,1,3,3,3],
    [1,1,1,1,0,1,0,1,1,3,1,1,0,1,0,1,1,1,1],
    [0,0,0,0,0,0,0,1,3,3,3,1,0,0,0,0,0,0,0],
    [1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1],
    [3,3,3,1,0,1,0,0,0,0,0,0,0,1,0,1,3,3,3],
    [1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
    [1,2,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,2,1],
    [1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class PacMan(Sprite):
    def __init__(self):
        super().__init__(pyglet.image.load_animation('images/pacmanAnimation.gif'))
        self.cshape = cm.AARectShape(self.position, 14, 14)
        self.touching_wall = False
        self.direction = (0,0)

    def respawn(self):
        self.position = 9*32+16, 9*32+16

    def hit_wall(self):
        self.direction = (0,0)

class Ghost(Sprite):
    def __init__(self, image):
        super().__init__(pyglet.image.load_animation(image))
        self.ghost_image = image
        self.cshape = cm.AARectShape(self.position, 14, 14)
        self.touching_wall = False
        self.direction = (SPEED,0)
        self.is_scared = False

    def respawn(self):
        self.position = 9*32+16, 13*32+16
        self.become_brave()

    def hit_wall(self):
        self.direction = (0,0)

    def become_scared(self):
        self.image = pyglet.image.load_animation('images/scaredGhost.gif')
        self.is_scared = True

    def become_brave(self):
        self.image = pyglet.image.load_animation(self.ghost_image)
        self.is_scared = False

    def make_decision(self):
        pass

class Inky(Ghost):
    def __init__(self):
        super().__init__('images/inkyAnimation.gif')

    def hit_wall(self):
        x,y = self.position[0] // 32, self.position[1] // 32
        print("current location: " + "(" + str(x) + "," + str(y) + ")")
        possible_directions = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        possible_moves = []
        for move in possible_directions:
            direction = list(reversed(MAP_TEMPLATE))[move[1]][move[0]]
            if direction == 0:
                if tuple(map(sum,zip((x,y),(0 - self.direction[0]/7,0 - self.direction[1]/7)))) == (move[0],move[1]):
                    pass
                else:
                    print("possible future location: " + "(" + str(move[0]) + "," + str(move[1]) + ")")
                    possible_moves.append(((move[0] - x) * SPEED,(move[1] - y) * SPEED))
        print("possible moves: " + str(possible_moves))
        try:
            self.direction = random.choice(possible_moves)
        except IndexError:
            self.direction = random.choice([(SPEED,0),(-SPEED,0),(0,SPEED),(0,-SPEED)])

    def make_decision(self):
        #self.direction = random.choice([(SPEED,0),(-SPEED,0),(0,SPEED),(0,-SPEED)])
        pass

class Clyde(Ghost):
    def __init__(self):
        super().__init__('images/clydeAnimation.gif')

    def hit_wall(self):
        self.direction = random.choice([(SPEED,0),(-SPEED,0),(0,SPEED),(0,-SPEED)])


class Blinky(Ghost):
    def __init__(self):
        super().__init__('images/blinkyAnimation.gif')
        self.last_visited = (0,0)

    def hit_wall(self):
        #self.direction = random.choice([(SPEED,0),(-SPEED,0),(0,SPEED),(0,-SPEED)])
        pass

    def make_decision(self):
        try:
            x,y = self.position[0] // 32, self.position[1] // 32
            if self.last_visited == (x,y):
                return
            self.last_visited = (x,y)
            print("current location: " + "(" + str(x) + "," + str(y) + ")")
            possible_directions = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
            possible_moves = []
            for move in possible_directions:
                direction = list(reversed(MAP_TEMPLATE))[move[1]][move[0]]
                if direction == 0:
                    if tuple(map(sum,zip((x,y),(0 - self.direction[0]/7,0 - self.direction[1]/7)))) == (move[0],move[1]):
                        pass
                    else:
                        print("possible future location: " + "(" + str(move[0]) + "," + str(move[1]) + ")")
                        possible_moves.append(((move[0] - x) * SPEED,(move[1] - y) * SPEED))
            print("possible moves: " + str(possible_moves))
            self.direction = random.choice(possible_moves)
        except IndexError:
            self.last_visited = None
            self.direction = random.choice([(SPEED,0),(-SPEED,0),(0,SPEED),(0,-SPEED)])

class Pinky(Ghost):
    def __init__(self, pacman):
        super().__init__('images/pinkyAnimation.gif')
        self.pacman = pacman
        self.last_visited = (0,0)

    def hit_wall(self):
        #self.direction = random.choice([(SPEED,0),(-SPEED,0),(0,SPEED),(0,-SPEED)])
        pass

    def make_decision(self):
        try:
            x,y = self.position[0] // 32, self.position[1] // 32
            if self.last_visited == (x,y):
                return
            self.last_visited = (x,y)
            print("current location: " + "(" + str(x) + "," + str(y) + ")")
            possible_directions = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
            possible_moves = []
            for move in possible_directions:
                direction = list(reversed(MAP_TEMPLATE))[move[1]][move[0]]
                if direction == 0:
                    if tuple(map(sum,zip((x,y),(0 - self.direction[0]/7,0 - self.direction[1]/7)))) == (move[0],move[1]):
                        pass
                    else:
                        print("possible future location: " + "(" + str(move[0]) + "," + str(move[1]) + ")")
                        possible_moves.append(((move[0] - x) * SPEED,(move[1] - y) * SPEED))
            print("possible moves: " + str(possible_moves))
            self.direction = self.compare_with_pac(possible_moves,(x,y))
        except IndexError:
            self.last_visited = None
            self.direction = random.choice([(SPEED,0),(-SPEED,0),(0,SPEED),(0,-SPEED)])

    def compare_with_pac(self,possible_moves,location):
        if len(possible_moves) > 1:
            distances = []
            for move in possible_moves:
                distances.append(math.sqrt(((self.pacman.position[0] // 32) - \
                    (move[0] // 7 + location[0])) ** 2 + ((self.pacman.position[1] // 32) \
                    - (move[1] // 7 + location[1])) ** 2))
            if self.is_scared:
                return possible_moves[distances.index(max(distances))]
            else:
                return possible_moves[distances.index(min(distances))]
        return possible_moves[0]

class Wall(Sprite):
    def __init__(self):
        super().__init__(pyglet.image.load_animation('images/actualWall.png'))
        self.cshape = cm.AARectShape(self.position, 16, 16)

class Pellet(Sprite):
    def __init__(self):
        super().__init__(pyglet.image.load_animation('images/pellet.png'))
        self.cshape = cm.AARectShape(self.position, 4, 4)

class PowerPellet(Sprite):
    def __init__(self):
        super().__init__(pyglet.image.load_animation('images/POWERpellet.png'))
        self.cshape = cm.AARectShape(self.position, 4, 4)

class Map(Layer):
    def __init__(self):
        super().__init__()
        self.offset = 16
        self.walls = []
        self.pellets = []
        self.POWpellets = []
        x = self.offset
        y = self.offset
        for row in reversed(MAP_TEMPLATE):
            for tile_type in row:
                if tile_type == 0:
                    pellet = Pellet()
                    self.pellets.append(pellet)
                    pellet.position = (x, y)
                    self.add(pellet)
                elif tile_type == 1:
                    sprite = Wall()
                    self.walls.append(sprite)
                    sprite.position = (x, y)
                    self.add(sprite)
                elif tile_type == 2:
                    POWpellet = PowerPellet()
                    self.POWpellets.append(POWpellet)
                    POWpellet.position = (x, y)
                    self.add(POWpellet)
                elif tile_type == 3:
                    pass
                x += 32
            y += 32
            x = self.offset

class CharacterLayer(Layer):

    is_event_handler = True

    def __init__(self):
        super().__init__()

        self.keys_pressed = set()

        self.actorPacMan = PacMan()
        self.actorPacMan.respawn()
        self.add(self.actorPacMan)

        self.actorInky = Inky()
        self.actorInky.respawn()
        self.add(self.actorInky)

        self.actorClyde = Clyde()
        self.actorClyde.respawn()
        self.add(self.actorClyde)

        self.actorBlinky = Blinky()
        self.actorBlinky.respawn()
        self.add(self.actorBlinky)

        self.actorPinky = Pinky(self.actorPacMan)
        self.actorPinky.respawn()
        self.add(self.actorPinky)

        self.schedule(self.on_update)
        self.time = 0
        self.actors = [self.actorPacMan, self.actorInky, self.actorClyde, self.actorBlinky, self.actorPinky]
        self.ghosts = [self.actorInky, self.actorClyde, self.actorBlinky, self.actorPinky]

    #Character movement handler
    def on_update(self, dt):
        self.time += dt

        #collision handling
        for actor in self.actors:
            x, y = actor.position
            dx, dy = actor.direction
            if actor in self.ghosts:
                centerx, centery = ((x//32)*32+16,(y//32)*32+16)
                distance = math.sqrt((x-centerx) ** 2 + (y-centery) ** 2)
                if distance < 4:
                    actor.make_decision()


            if actor.touching_wall:
                actor.hit_wall()
                actor.position = ((x//32)*32+16,(y//32)*32+16)
                continue
            actor.position = x+dx, y+dy
            if x < 16:
                actor.position = (608, y)
                return
            elif x > 608:
                actor.position = (17, y)
                return

        x,y = self.actorPacMan.position

        """#this is for pacman teleport
        if x < 16:
            self.actorPacMan.position = (608, y)
            return
        elif x > 608:
            self.actorPacMan.position = (17, y)
            return"""

        #Pacman movement
        if pyglet.window.key.UP in self.keys_pressed:
            self.actorPacMan.position = (x, y + SPEED)
            self.actorPacMan.rotation = 270
        if pyglet.window.key.DOWN in self.keys_pressed:
            self.actorPacMan.position = (x, y - SPEED)
            self.actorPacMan.rotation = 90
        if pyglet.window.key.LEFT in self.keys_pressed:
            self.actorPacMan.position = (x - SPEED, y)
            self.actorPacMan.rotation = 180
        if pyglet.window.key.RIGHT in self.keys_pressed:
            self.actorPacMan.position = (x + SPEED, y)
            self.actorPacMan.rotation = 0

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)


    def on_key_release(self, key, modifiers):
        self.keys_pressed.discard(key)

class LogicLayer(Layer):

    def __init__(self, map_layer, chara_layer):
        super().__init__()
        self.schedule(self.on_update)
        self.pacman = chara_layer.actorPacMan
        self.walls = map_layer.walls
        self.ghosts = chara_layer.ghosts
        self.pellets = map_layer.pellets
        self.POWpellets = map_layer.POWpellets
        self.map_layer = map_layer
        self.chara_layer = chara_layer
        self.score = 0
        self.lives = 3

        self.score_label = cocos.text.Label('Score: 0' ,
                font_size=30,
                anchor_x='center',
                anchor_y='center',
                color=(255,255,255,255))
        self.score_label.position = 300, 750
        self.add(self.score_label)

        self.lives_label = cocos.text.Label('Lives Left: 3',
                font_size=15,
                anchor_x='center',
                anchor_y='center',
                color=(255,255,255,255))
        self.lives_label.position = 300, 704
        self.add(self.lives_label)


        self.wall_manager = cm.CollisionManagerBruteForce()

        self.pellet_manager = cm.CollisionManagerBruteForce()

        self.ghost_manager = cm.CollisionManagerBruteForce()

        self.POWpellet_manager = cm.CollisionManagerBruteForce()

    def on_update(self, dt):
        self.wall_manager.clear()
        self.pellet_manager.clear()
        self.ghost_manager.clear()
        self.POWpellet_manager.clear()

        #here goes wall collision checking
        for wall in self.walls:
            wall.cshape.center = wall.position
            self.wall_manager.add(wall)
        for actor in self.chara_layer.actors:
            actor.cshape.center = actor.position
            colliding = self.wall_manager.objs_colliding(actor)
            if len(colliding) > 0:
                actor.touching_wall = True
            else:
                actor.touching_wall = False

        #hitting up eatable pellets here
        for pellet in self.pellets:
            pellet.cshape.center = pellet.position
            self.pellet_manager.add(pellet)
        colliding = self.pellet_manager.objs_colliding(self.pacman)
        for pellet in colliding:
            #updating the score for every pellet eaten
            self.score += 10
            self.update_text()
            self.map_layer.remove(pellet)
            self.pellets.remove(pellet)

        #going to hit up power pellets here soonish
        for POWpellet in self.POWpellets:
            POWpellet.cshape.center = POWpellet.position
            self.POWpellet_manager.add(POWpellet)
        colliding = self.POWpellet_manager.objs_colliding(self.pacman)
        for POWpellet in colliding:
            #updating the score for every POWpellet eaten
            #give pacman his powers to eat ghosts here
            self.score += 50
            self.update_text()
            for ghost in self.chara_layer.ghosts:
                ghost.become_scared()

            self.map_layer.remove(POWpellet)
            self.POWpellets.remove(POWpellet)

        #ghooOOOOOOOOOSSSTTTTTTSSS BOO
        for ghost in self.ghosts:
            ghost.cshape.center = ghost.position
            self.ghost_manager.add(ghost)
        colliding = self.ghost_manager.objs_colliding(self.pacman)
        for  ghost in colliding:
            if ghost.is_scared:
                ghost.respawn()
                self.score += 200
            else:
                self.lives -= 1
                self.update_text()
                if self.lives == 0:
                #put a game over screen here, with a restart button.
                    sys.exit(0)
                self.pacman.respawn()

    def update_text(self):
        self.score_label.element.text = "Score: " + str(self.score)
        self.lives_label.element.text = "lives Left: " + str(self.lives)

def game_scene():
    #  director.init(width=608, height=800)
    map_layer = Map()
    chara_layer = CharacterLayer()
    logic_layer = LogicLayer(map_layer, chara_layer)
    return scene.Scene(map_layer, chara_layer, logic_layer)
