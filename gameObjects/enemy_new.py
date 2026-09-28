from . import (Drawable, Animated, Heart, BigHeart, 
                Buck, FireShard, GreenHeart, Buck_B, Buck_R, Bombodrop, LargeBombo, GiantBombo)
from .weapons import *
from .types import *

from utils import SoundManager, SpriteManager, SCALE, RESOLUTION, vec
from random import randint
import pygame

from math import ceil
import os
from abc import abstractmethod

"""
All yur favorite delinquits are scripted here!
"""

#   -----   Engine  -----   #
#   *engine.npcs* stores currently loaded enemies
#   *engine.enemies* stores the enemies to-be-loaded
#   *engine.enemy_counter* keeps track of the number of defeated enemies
#
#   *placeEnemies()* places each enemy in the room
#   *disappear()* removes enemies from *self.npcs* but not *self.enemies*
#   *npcCollision()* directs enemy collision
#   - player.handleCollision() handles collision w/ player
#   - projectilesOnEnemies() handles collision w/ projectiles in the room
#       - calls enemy.handleCollision()
#
#   *update_enemy()* updates the enemy after handling events
#
#
#
#
#   ----    Pre-loading Sprites ----    #
#   Enemies with more complex pallet data,
#   including those that peform pallet swaps,
#   should load each of the images that they will use
#   so as to avoid pallet swapping every single frame
#   during draw().
#
#   These usually include enemies that come in different flavors:
#   
#   Stingers
#   Flappers
#   Slimers
# 
# 
#   -----   Enemy Types -----   #
#   Each enemy has a type (or types) and specific behavior.
#
#   --- Ids --- #
#   Ids tell the engine to handle the enemy in a specific way.
#
#   "spawn" -> spawn other objects
#
#   "noStop" -> allow the player to continue running past the enemy
#   after freezing it w/ Ice Dash
#   (projectiles like fireballs and lasers)
#
#   "shot" -> collision w/ player is handled like a block
#   (Shot-type enemies)
#
#   ---------------------   #
#
#
#   --- Drops ---   #
#   Each enemy drops something upon being killed.
#
#   *enemy.get_drop(full_health)* returns the item(s) the enemy drops
#       - The drop may change depending on the player's health.
#       - For example, at full health a Heart will be replaced by a Buck.
#
#
#   ---------------------   #
#
#
#   ----- Bosses -----  #
#   Bosses provide the only way for the player to increase their maximum health.
#   Each boss drops a Green Heart upon death.
#   Each boss also says something to Kyro before they die. An homage to Link's Awakening.
#   They are defined by 2 Boolean Flags:
#   (1xx) Whether or not they are defeated
#   (2xx) Whether or not their Heart has been picked up
#
#
#   (1) Light Cloaker
#   Your (not-so) flashy douchebag neighbor.
#
#   Flag: 100/200
#   Type: Light
#   Area: Wavering Grotto
#   Gimmicks: Teleport to 4 different locations, drain the player's health.
#       Fought on 1 hp, so his attacks are easy to dodge.
#
#
#   (2) Alpha Flapper
#   Master of the one-eyed bats.
#
#   Flag: 101/201
#   Type: Non-Elemental
#   Area: Chapel Hall
#   Gimmick: Gets faster the more you damage it
#
#
#   (3) Smiler
#   Who is this guy?
#
#   Flag: 102/202
#   Type: Phantom
#   Area: Stardust Quarry
#   Gimmick: 
#   Death Quote: "Do you wanna know my real name? It's John." *Dies*
#
#
#   (4) Lava Knight
#   A member of the ancient king's royal guard.
#
#   Flag: 103/203
#   Type: Fire
#   Area: Scorching Fields
#   Gimmick: Launch up off screen and fall on the player. 2 phases
#
#
#   (5) Robert (Round 1)
#   Chill guy who loves when people have a bone to pick with him.
#
#   Flag: 104/204
#   Type: Skeletal
#   Area: Chapel Hall
#   Gimmick: Extremely sturdy, but slow as hell. Faces one direction
#       and tosses endless bones at you. Can be fought multiple times, but
#       gets stronger each time. Each fight is unlocked after certain
#       story requirements are met.
#
#
#   [To-Implement]
#   Baller
#   Gamer
#   Viber
#   Faller
#   Rocker


    
#   -----   Abstract Enemy Class   -----   #
class Enemy(Drawable):
    """Abstract Enemy Class"""

    def __init__(self, position=vec(0,0), fileName="",
                 frame=0, row=0, nFrames=1, nRows = 1, fps=16,
                 max_hp = 5, hp=5, speed=50,
                 name = "", id = [], type=0,
                 top = False, i_frames = 20,
                 set_pallet = True, use_pallet = False,
                 push_player = True, pre_loaded = False):
        
        #   Enemy Identification    #
        self.id = id
        self.name = name
        self.use_pallet = use_pallet

        #   Animation Data  #
        self.file_name = fileName
        self.animation_timer = 0.0
        self.nFrames = nFrames
        self.fps = fps
        self.frame = frame
        self.row = row
        self.nRows = nRows
        self.image = None

        


        #   Draw Instructions   #
        self.drawn = False # The enemy has been drawn
        self.top = False # The enemy is drawn at the top layer

        #   State Data  #
        self.current_state = "idle"

        #   Color Pallet Dictionary #
        ##  Each color is mapped to a damage color  ##
        self.pallet = {}
        self.damage_pallet = {}
        self.heal_pallet = {}

        ##  Set animation data per state in the following format:
        ##  [start_frame, row, nFrames, fps]
        self.states = {
            "idle":[self.frame, self.row, self.nFrames, self.fps]
        }

        #   Pre-loading
        self.pre_loaded = pre_loaded
        if pre_loaded:
            #   State -> contains rows -> contains images
            self.images = {
                "idle": []
            }
            self.damage_images = {
                "idle":[]
            }

            # self.load_images()


        #   Pallet loading
        if set_pallet and not self.pre_loaded:
            self.set_damage_pallet()
            self.set_heal_pallet()

        #   Enemy Attributes    #
        self.position = position
        self.vel = vec(0,0)
        self.max_hp = max_hp
        self.hp = hp
        self.injury = 0
        self.status = None
        self.speed = speed
        self.type = type
        self.ignore_collision = False
        self.push_player = push_player
        self.hit = False
        self.dead = False
        self.dying = False
        self.frozen = False # If True, movement is halted; not a status effect
        self.i_frames = i_frames
        self.i_frame_counter = 0
        self.damaged = False # True if I-frames are active
        self.healed = False
        self.ignore_pallet = False # True if 0 damage dealt but still want I-frames

        if not self.pre_loaded:
            self.set_image()

    #   ----- Auxiliary Functions ----- #
    def print_pallet(self) -> None:
        for c in self.damage_pallet.keys():
            print("Color:", c, "\nDamage:", self.damage_pallet[c])

    def get_pallet(self) -> dict:
        """Returns the enemy's color pallet"""
        image = pygame.image.load(os.path.join("images", "enemies", self.file_name)).convert_alpha()

        colors = set()

        for y in range(image.get_height()):
            for x in range(image.get_width()):
                color = image.get_at((x, y))
                colors.add((color.r, color.g, color.b))

        return colors

    def set_damage_pallet(self) -> None:
        """Default function to set the enmey's I-frame pallet"""
        colors = self.get_pallet()
        for i in colors:
            red = (i[0] + i[1] + i[2]) // 3
            red = min(255, red+125)
            color = (red, 0, 0)
            self.damage_pallet[i] = color

        if self.pre_loaded:
            for state in self.images:
                for row in range(len(self.images[state])):
                    damage_row = []
                    for frame in range(len(self.images[state][row])):
                        temp_image = self.images[state][row][frame].copy()
                        temp_image.lock()
                        for x in range(temp_image.get_width()):
                            for y in range(temp_image.get_height()):
                                #   Set the color according to the enemy's pallet   #
                                color = temp_image.get_at((x, y))
                                for c in self.damage_pallet:
                                    if color == c:
                                        temp_image.set_at((x, y), self.damage_pallet[c])
                        temp_image.unlock()
                        damage_row.append(temp_image)
                    self.damage_images[state].append(damage_row)
                    damage_row = []
                        
                        
                

    def set_heal_pallet(self) -> None:
        """Default function to set the enmey's healing pallet"""
        colors = self.get_pallet()
        for i in colors:
            green = (i[0] + i[1] + i[2]) // 3
            green = min(255, green+70)
            color = (0, green, 0)
            self.heal_pallet[i] = color

        


    def set_image(self) -> None:
        """Set the enemy's image before drawing"""
        # 0 -> frame, 1 -> row, 2 -> nFrames, 3 -> fps
        if self.pre_loaded:
            self.image = self.images[self.current_state][0][self.frame]
        else:
            self.image = SpriteManager.getInstance().getEnemy(self.file_name, (self.row, self.frame))

    def load_images(self) -> None:
        """Pre-load all of the enemy's sprites
        **NOTE** Should exclude rows from this algorithm.
        Just add a list of sprites for each state.
        Each state is its own row;
        its not like each state will have multiple rows..."""
        for state in self.states:
            rowId = self.states[state][1]
            nFrames = self.states[state][2]
            row = []
            for frame in range(nFrames):
                image = SpriteManager.getInstance().getEnemy(self.file_name, (rowId, frame))
                row.append(image)
            self.images[state].append(row)

    def set_alpha(self, alpha : int = 255) -> None:
        self.image.set_alpha(alpha)

    def set_state(self, state: str = "") -> None:
        """Set the enemy's state and animation data"""
        if state in self.states:
            #   Update the current State    #
            self.current_state = state

            #   Update Animation Data   #
            data = self.states[state]
            self.frame = data[0]
            self.row = data[1]
            self.nFrames = data[2]
            self.fps = data[3]

    def add_state(self, state: str = "", starting_frame: int = 0, row: int = 0, nFrames: int = 0, fps: int = 0) -> None:
        """Add a state to the state dictionary"""
        self.states[state] = [starting_frame, row, nFrames, fps]
        if self.pre_loaded:
            self.images[state] = []
            self.damage_images[state] = []

    def getCollisionRect(self):
        return self.get_hit_box()
    
    def get_hit_box(self):
        """Get the hitbox"""
        rect = pygame.Rect((self.position[0], self.position[1], self.image.get_width(), self.image.get_height()))
        return rect
    
    def set_injury(self, damage):
        """Set the enemy's injury value"""
        self.injury = damage
    
    def get_injury(self):
        """Return the enemy's injury value so the engine can display the number"""
        return self.injury
    
    def reset_injury(self):
        """Reset the injur value to 0"""
        self.injury = 0

    def get_damage(self):
        return 1
    
    @abstractmethod
    def get_drop(self):
        return Heart(vec(self.position[0] + self.image.get_size()[0] // 2, self.position[1] + self.image.get_size()[1] // 2))
    
    @abstractmethod
    def get_money(self):
        return Buck(vec(self.position[0] + self.image.get_size()[0] // 2, self.position[1] + self.image.get_size()[1] // 2))
    
    def play_no_damage(self):
        """PLay the enemy's no damage sound"""
        SoundManager.getInstance().playSFX("dink.wav")

    def play_heal(self):
        """Play the enemy's heal sound"""
        return
    
    def play_damaged(self):
        SoundManager.getInstance().playLowSFX("enemyhit.wav", volume=0.5)

    def play_death(self):
        SoundManager.getInstance().playLowSFX("enemydies.wav", volume=0.2)

    def play_hurt_sound(self, damage):
        #   No Damage = Dink Sound  #
        if damage == 0:
            self.play_no_damage()
        
        #   Negative damage = Heal Sound   #
        elif damage < 0:
            self.play_heal()
        
        #   Normal Damage Sound #
        else:
            self.play_damaged()


    #   ----- Collision Detection ----- #
    def bounds_safety(self) -> bool:
        return False
    
    def collides_with_block(self, block) -> bool:
        """Determine whether or not to handle block collision"""
        return False

    def collides_with_projectile(self, proj) -> bool:
        """Determine whether or not to handle projectile collision."""
        if proj.pierce:
            return not self.damaged and self.get_hit_box().colliderect(proj.getCollisionRect())
        return not proj.hit and self.get_hit_box().colliderect(proj.getCollisionRect())

    def handle_player_collision(self, player) -> bool:
        """Determine whether or not to handle player collison"""
        return True
    
    def handle_projectile_collision(self, proj) -> None:
        """Handle collision with a projectile"""
        #   I-Frame Checker #
        if self.damaged:
            self.play_hurt_sound(0)
            return
        elif self.healed:
            return
        
        #   Calculate Damage based on Types  #
        proj.set_hit()
        other_type = proj.type.NAME
        damage = proj.damage

        #   Check Resistance    #
        if other_type in self.type.RESISTANCE:
            damage = damage // self.type.RES_FACTOR

        #   Check Weakness  #
        elif other_type in self.type.WEAKNESS:
            damage = int(damage * self.type.WEAK_FACTOR)

        #   Check Immunity  #
        elif other_type in self.type.IMMUNITY:
            damage = 0

        #   Check Absorption    #
        elif other_type in self.type.ABSORPTION:
            damage *= -1

        #   Deal the damage / effect    #
        self.hurt(damage)
        
    def hurt(self, damage):
        #   Decrease health #
        self.hit = True
        self.hp -= damage
        self.set_injury(damage)

        #   Check if dead   #
        if self.hp <= 0:
            self.dead = True
            self.play_death()

        #   Play a sound effect #
        else:
            self.play_hurt_sound(damage)

        #   Start I-Frames  #
        if damage <= -1:
            self.healed = True
        else:
            self.damaged = True
        if damage == 0:
            self.ignore_pallet = True

    def handle_collision(self, other) -> None:
        """Handle collision with another object"""
        return
    
    #   ----- Drawing ----- #
    def draw(self, drawSurface, drawHitbox=False, use_camera=True) -> None:
        #   Draw I-Frames   #
        if not self.ignore_pallet:
            if self.damaged:
                self.draw_pallet(drawSurface, "damage")
                return
            elif self.healed:
                self.draw_pallet(drawSurface, "heal")
                return

        if self.use_pallet:
            self.draw_pallet(drawSurface, "default")
        else:
            super().draw(drawSurface, drawHitbox, use_camera)
        # self.drawn = True
    

    def draw_pallet(self, drawSurface, pallet = "default"):
        #   Draw based on pre-loaded pallet
        if self.pre_loaded:
            if pallet == "damage":
                rowId = self.states[self.current_state][1]
                img = self.damage_images[self.current_state][0][self.frame]
                drawSurface.blit(img, self.position - Drawable.CAMERA_OFFSET)
                return
        
        temp_image = self.image.copy()
        temp_image.lock()
        for x in range(temp_image.get_width()):
            for y in range(temp_image.get_height()):
                #   Set the color according to the enemy's pallet   #
                color = temp_image.get_at((x, y))
                if pallet == "damage":
                    for c in self.damage_pallet:
                        if color == c:
                            temp_image.set_at((x, y), self.damage_pallet[c])
                
                elif pallet == "heal":
                    for c in self.heal_pallet:
                        if color == c:
                            temp_image.set_at((x, y), self.heal_pallet[c])

                elif pallet == "default":
                    for c in self.pallet:
                        if color == c:
                            temp_image.set_at((x, y), self.pallet[c])

        temp_image.unlock()
        drawSurface.blit(temp_image, self.position - Drawable.CAMERA_OFFSET)


    #   ----- Updating -----    #
    def update_movement(self, seconds, player) -> None:
        return
    
    def update(self, seconds, player=None) -> None:
        super().update(seconds)

        #   Update Animation    #
        self.animation_timer += seconds

        if self.animation_timer > 1 / self.fps:
            self.frame += 1
            self.frame %= self.nFrames
            self.animation_timer -= 1 / self.fps
            self.set_image()

        self.drawn = False

        #   Update I-Frames #
        if self.damaged or self.healed:
            self.i_frame_counter += 1
            if self.i_frame_counter == self.i_frames:
                self.i_frame_counter = 0
                self.damaged = False
                self.healed = False
                self.ignore_pallet = False

        #   Update Position #
        self.update_movement(seconds, player)
        self.position += self.vel * seconds


#   -----   Tester Class   -----   #
class Test_Boner(Enemy):
    """Tester Class for the Enemy Class"""
    def __init__(self, position=vec(0, 0)):
        super().__init__(position, "boner.png",
                         nFrames=6, fps=12,
                         max_hp = 2_000, hp = 2_000,
                         type=Skeletal)

        self.damage_pallet = {
             (240, 240, 217, 255) : (255, 0, 0, 255),
             (210, 75, 70, 255) : (116, 9, 5, 255)
        }
        
    def get_hit_box(self):
        return pygame.Rect(self.position[0] + 2, self.position[1] + 1, 14, 26)
    
    def get_drop(self):
        return Heart(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))
    
    def get_money(self):
        return Buck(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))
    

#   ====   Skeletal Enemies   ====   #
class Boner(Enemy):
    """A walking skeleton that throws bones at you.
    Always drops heart unless you're at full health."""
    def __init__(self, position=vec(0, 0), file_name = "boner.png",
                 type = Skeletal, hp = 20, speed = 20,
                 fps = 8, direction = 0):
        super().__init__(position, file_name,
                         nFrames=6, nRows = 4, fps=fps,
                         max_hp = hp, hp = hp,
                         type=type, speed=speed,
                         )

        #   Movement data   #
        self.center_position = self.position.copy()
        self.delta = 16
        self.direction = direction

        #   States  #
        self.walking = False

        self.set_damage_pallet()
        # self.damage_pallet = {
        #      (240, 240, 217, 255) : (255, 0, 0, 255),
        #      (210, 75, 70, 255) : (116, 9, 5, 255)
        # }

    def get_hit_box(self):
        return pygame.Rect(self.position[0] + 2, self.position[1] + 1, 14, 26)
    
    def get_drop(self):
        return Heart(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))
    
    def get_money(self):
        return Buck(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))


    def stop(self):
        self.vel = vec(0,0)
        self.walking = False

    def update_movement(self, seconds, player):
        """
        Boners start in the centle of their "movement area", which is x*2 pixels in any direction
        (1) Move x pixels in any direction
        (2) Cannot move , for a maximum of x * 2 pixels in any direction
        """
        delta = 64
        
        if self.walking:
            if self.direction == 0:
                if int(self.position[1]) >= int(self.center_position[1] + self.delta):
                    self.position[1] = int(self.center_position[1] + self.delta)
                    self.stop()
            elif self.direction == 1:
                if int(self.position[0]) >= int(self.center_position[0] + self.delta):
                    self.position[0] = int(self.center_position[0] + self.delta)
                    self.stop()
            elif self.direction == 2:
                if int(self.position[1]) <= int(self.center_position[1] - self.delta):
                    self.position[1] = int(self.center_position[1] - self.delta)
                    self.stop()
            elif self.direction == 3:
                if int(self.position[0]) <= int(self.center_position[0] - self.delta):
                    self.position[0] = int(self.center_position[0] - self.delta)
                    self.stop()
        
        else:
            num = randint(0,3)
            #   Move down
            if num == 0:
                self.vel = vec(0, self.speed)
                self.direction = 0
                self.row = 0
            #   Move right
            elif num == 1:
                self.vel = vec(self.speed, 0)
                self.direction = 1
                self.row = 1
            #   Move up
            elif num == 2:
                self.vel = vec(0, -self.speed)
                self.direction = 2
                self.row = 2
            #   Move left
            elif num == 3:
                self.vel = vec(-self.speed, 0)
                self.direction = 3
                self.row = 3

            self.walking = True


    
class Ice_Boner(Boner):
    """A Boner wielding Ice powers"""
    def __init__(self, position=vec(0,0)):
        super().__init__(position, file_name="ice_boner.png",
                         hp=40, type=Skeletal_Ice)

class Fire_Boner(Boner):
    """A Boner wielding Fire powers"""
    def __init__(self, position=vec(0,0)):
        super().__init__(position, file_name="fire_boner.png",
                         hp=40, fps=16, type=Skeletal_Fire)



#   ====   Avian Enemies   ====   #
class Flapper(Enemy):
    """Small flying enemies"""
    def __init__(self, position=vec(0, 0), row = 0, type = Avian):
        super().__init__(position, "flapper.png",
                         nFrames=6, fps=12,
                         max_hp = 5, hp = 5,
                         type=type, push_player=False)
        self.row = row

        self.damage_pallet = {
        }

        self.movement_frames = 8
        self.frame_counter = 0
        self.set_damage_pallet()

    def get_hit_box(self):
        return pygame.Rect(self.position[0] + 2, self.position[1] + 4, 12, 8)
    
    def get_drop(self):
        return Heart(vec(self.position[0] + self.image.get_width()//2, self.position[1]))
    
    def get_money(self):
        return Buck(vec(self.position[0] + self.image.get_width()//2, self.position[1]))

    def update_movement(self, seconds, player):
        """
        Each frame or every x frames:
        (1) -> 20% chance: Move in any direction
        (2) -> 40% Stop
        (3) -> 40% Keep moving same direction
        """
        if self.frame_counter == self.movement_frames:
            self.frame_counter = 0
            num1 = randint(1,5)

            #   Change directions (40%)
            if num1 == 1 or num1 == 2:
                num = randint(0,7)
                #   Move down
                if num == 0:
                    self.vel = vec(0, self.speed)
                    self.direction = 0
                #   Move right
                elif num == 1:
                    self.vel = vec(self.speed, 0)
                    self.direction = 1
                #   Move up
                elif num == 2:
                    self.vel = vec(0, -self.speed)
                    self.direction = 2
                #   Move left
                elif num == 3:
                    self.vel = vec(-self.speed, 0)
                    self.direction = 3

                #   Move top-left
                elif num == 4:
                    self.vel = vec(-self.speed // 2, -self.speed // 2)
                #   Move top-right
                elif num == 5:
                    self.vel = vec(self.speed // 2, -self.speed // 2)
                #   Move bottom-left
                elif num == 6:
                    self.vel = vec(self.speed // 2, -self.speed // 2)
                #   Move bottom-right
                elif num == 7:
                    self.vel = vec(self.speed // 2, self.speed // 2)

            #   Keep same direction (60%)
            elif num1 == 3 or num1 == 4:
                pass
                
            #   Stop (20%)
            elif num1 == 5:
                self.vel = vec(0,0)
            
        else:
            self.frame_counter += 1


class Fire_Flapper(Flapper):
    """Small flying enemies"""
    def __init__(self, position=vec(0, 0)):
        super().__init__(position, row=1, type=Avian_Fire)

class Ice_Flapper(Flapper):
    """Small flying enemies"""
    def __init__(self, position=vec(0, 0)):
        super().__init__(position, row=2, type=Avian_Ice)

class Thunder_Flapper(Flapper):
    """Small flying enemies"""
    def __init__(self, position=vec(0, 0)):
        super().__init__(position, row=3, type=Avian_Thunder)

class Gale_Flapper(Flapper):
    """Small flying enemies"""
    def __init__(self, position=vec(0, 0)):
        super().__init__(position, row=4, type=Avian_Wind)


class BetaFlapper(Enemy):
    """Faster, more durable flappers that dodge attacks and dash at you"""
    def __init__(self, position=vec(0, 0), type = Avian):
        super().__init__(position, "betaflapper.png",
                         nFrames=6, fps=16,
                         max_hp = 15, hp = 15,
                         type=type, use_pallet = True,
                         push_player=False)

        #   Easy Pallet Swap for elemental flappers
        self.pallet = {
            #   Eye Color
            (248, 0, 0) : (248, 0, 0),

            #   Body Color
            (148, 67, 0) : (148, 67, 0),
            (110, 49, 0) : (110, 49, 0),
            (61, 28, 0) : (61, 28, 0)
        }

        self.frame_counter = 0
        self.movement_frames = 8

    def get_hit_box(self):
        return pygame.Rect(self.position[0] + 2, self.position[1] + 4, 12, 8)
    
    def get_drop(self):
        n = randint(0, 2)
        if n == 0:
            return BigHeart(vec(self.position[0] + self.image.get_width()//2, self.position[1]))
        return Heart(vec(self.position[0] + self.image.get_width()//2, self.position[1]))
    
    def get_money(self):
        n = randint(0, 3)
        if n == 3:
            return Buck_R(vec(self.position[0] + self.image.get_width()//2, self.position[1]))
        return Buck_B(vec(self.position[0] + self.image.get_width()//2, self.position[1]))

    def update_movement(self, seconds, player=None):
        Flapper.update_movement(self, seconds, player)


class Fire_BetaFlapper(BetaFlapper):
    """Faster, more durable flappers that dodge attacks and dash at you"""
    def __init__(self, position=vec(0, 0)):
        super().__init__(position, type=Avian_Fire)

        #   Easy Pallet Swap for elemental flappers
        self.pallet = {
            #   Eye Color
            (248, 0, 0) : (248, 183, 0),

            #   Body Color
            (148, 67, 0) : (238, 67, 0),
            (110, 49, 0) : (176, 49, 0),
            (61, 28, 0) : (99, 27, 0)
        }

    
#   ====   Reptillian Enemies   ====   #
class Stinger(Enemy):
    """
    Has a hitbox and a sting box.
    Stings the player if it enters the sting box
    """
    
    def __init__(self, position=vec(0,0)):
        super().__init__(position, "stinger.png",
                         nFrames=11, fps=8,
                         nRows = 2,
                         max_hp=30, hp=30,
                         pre_loaded=True,
                         type=Reptillian)

        # self.damage_pallet = {
        #      (153, 229, 80, 255) : (255, 0, 0, 255),
        #      (106, 190, 48, 255) : (116, 9, 5, 255),
        #      (55, 148, 110, 255) : (100, 30, 30, 255),
        #      (251, 224, 115, 255) : (250, 30, 30, 255),
        #      (75, 105, 47, 255) : (142, 11, 11, 255)
        # }
        self.add_state("sting", 0, 1, 3, 8)
        self.load_images()
        self.set_damage_pallet()
        self.set_heal_pallet()
        self.set_image()



    
    def get_hit_box(self):
        return pygame.Rect(self.position[0] + 33, self.position[1] + 17, 7,17)
    
    def get_sting_box(self):
        return pygame.Rect(self.position[0] + 42, self.position[1] + 6, 37, 43)
    
    def get_drop(self):
        return Heart(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))
    
    def get_money(self):
        return Buck(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))
    
    def draw(self, drawSurface, drawHitbox=False, use_camera=True):
        #   Draw sting box for testing
        # pygame.draw.rect(drawSurface, (255,0,0), self.get_sting_box())
        
        return super().draw(drawSurface, drawHitbox, use_camera)

    def update(self, seconds, player=None):
        super().update(seconds, player)
        #   Check if the player is inside the sting rect    #
        if self.current_state == "idle":
            if self.get_sting_box().colliderect(player.getCollisionRect()):
                self.set_state("sting")
        
        elif self.current_state == "sting":
            if not self.get_sting_box().colliderect(player.getCollisionRect()):
                self.set_state("idle")



#   ====   Non-elemental Enemies   ====   #
class Slimer(Enemy):
    """A sentient mass of slime. Gross.
    These guys always drop 1 Buck. When at full health, they drop more."""
    def __init__(self, position=vec(0,0), direction = 1, speed = 50, hp = 10,
                 fps = 8, use_pallet = False):
        super().__init__(position, "gremlin.png",
                         nFrames=6, fps=fps,
                         max_hp = hp, hp = hp,
                         use_pallet=use_pallet,
                         speed = speed,
                         type=Non)
        self.direction = direction
        self.row = self.direction

        self.motion_timer = 0.0
        self.motion_tick = 1.0
        self.moving = False

        

        self.set_image()
        self.set_damage_pallet()

    def get_hit_box(self):
        newRect = pygame.Rect(0,0,12,34)
        newRect.left = int(self.position[0]+3)
        newRect.top = int(self.position[1]+1)
        return newRect
    
    def get_drop(self):
            return Buck(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))
        
    def get_money(self):
        return Buck_B(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))

    def update_movement(self, seconds, player):
        if not self.moving:
            if self.direction == 1:
                self.vel[0] = self.speed
            elif self.direction == 3:
                self.vel[0] = -self.speed
            self.moving = True

        else:
            self.motion_timer += seconds
            if self.motion_timer >= self.motion_tick:
                self.motion_timer = 0.0
                self.moving = False

                if self.direction == 1:
                    self.direction = 3

                elif self.direction == 0:
                    self.direction = 2

                elif self.direction == 2:
                    self.direction = 0

                elif self.direction == 3:
                    self.direction = 1

                self.row = self.direction
                self.set_image()
                self.vel = vec(0,0)

class Slimer_Blue(Slimer):
    def __init__(self, position=vec(0, 0), direction=1):
        super().__init__(position, direction,
                         hp=15, use_pallet=True)
        self.pallet = {
            #   Main Body
            (28,58,0): (28, 1, 58),
            (49, 102, 0): (49, 1, 101),
            (71, 148, 0): (71, 7, 145),

            #   Eyes
            # (255, 41, 41): None,
            # (148, 0, 0): None,

            #   Mouth / Teeth
            # (58, 0, 0): None,
            # (247, 218, 218): None,
        }

    def get_drop(self):
        num = randint(1,3)
        #   33% chance to drop $10
        if num == 1:
            return Buck_R(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))

        #   66% chance to drop $5
        return Buck_B(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))
            
    def get_money(self):
        num = randint(1,3)
        #   66% chance to drop $10
        if num == 1 or num == 2:
            return Buck_R(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))

        #   33% chance to drop $5
        return Buck_B(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))


class Slimer_Poison(Slimer):
    """Slimers that inflict poison damage on you"""
    def __init__(self, position=vec(0, 0), direction=1):
        super().__init__(position, direction,
                         hp=15, use_pallet=True, speed = 30)
        self.pallet = {
            #   Main Body
            (28,58,0): (48, 1, 58),
            (49, 102, 0): (97, 1, 101),
            (71, 148, 0): (145, 7, 133),

            #   Eyes
            (255, 41, 41): (148, 145, 0),
            (148, 0, 0): (246, 255, 41),

            #   Mouth / Teeth
            (58, 0, 0): (63, 61, 61),
            (247, 218, 218): (255, 122, 122),
        }

    def get_drop(self):
        num = randint(1,3)
        #   33% chance to drop $5
        if num == 1:
            return Buck_B(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))

        #   66% chance to drop $10
        return Buck_R(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))
                
    def get_money(self):
        #   Always drop $10
        return Buck_R(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))

class Slimer_Fast(Slimer):
    """Slimers that move quick"""
    def __init__(self, position=vec(0, 0), direction=1):
        super().__init__(position, direction,
                         fps=16,
                         hp=20, use_pallet=True, speed = 90)
        self.pallet = {
            #   Main Body
            (28,58,0): (58, 53, 1),
            (49, 102, 0): (130, 127, 0),
            (71, 148, 0): (188, 184, 4),
        }

    def get_drop(self):
        num = randint(1,3)
        #   33% chance to drop $5
        if num == 1:
            return Buck_B(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))

        #   66% chance to drop $10
        return Buck_R(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))
                    
    def get_money(self):
        #   Always drop $10
        return Buck_R(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))
    



class Blamer(Enemy):
    def __init__(self, position=vec(0, 0), file_name = "blamer.png",
                    type = Phantom, hp = 5, speed = 20,
                    fps = 8, direction = 0):
        super().__init__(position, file_name,
                            nFrames=3, fps=fps,
                            max_hp = hp, hp = hp,
                            type=type, speed=speed,
                            push_player=False)

        #   Movement data   #
        self.center_position = self.position.copy()
        self.delta = 16
        self.direction = direction
        self.motion_tick = 0
        self.motion_delta = 8
        self.visible_frames = 120
        self.invisible_frames = 200
        self.frame_counter = 0
        self.alpha = 0
        self.set_alpha(0)

        #   States  #
        self.visible = False
        self.transitioning = False

        self.set_damage_pallet()
        # self.damage_pallet = {
        #      (240, 240, 217, 255) : (255, 0, 0, 255),
        #      (210, 75, 70, 255) : (116, 9, 5, 255)
        # }

    def handle_player_collision(self, other):
        return self.visible and (not self.transitioning)

    def collides_with_projectile(self, proj):
        if (not self.visible) or self.transitioning:
            return False

        if proj.type == Non:
            return False
        return super().collides_with_projectile(proj)

    def set_next_pos(self, player):
        """Appear on top of the player and attack them"""
        pos = player.position.copy()
        self.position = vec(pos[0] - 16, pos[1] - 6)

    def update_movement(self, seconds, player):
        """Randomly render the ghost just barely visible when he is invisible"""
        #   Move and disappear
        if self.visible:
            if self.transitioning:
                self.alpha -= 5
                if self.alpha <= 0:
                    self.set_alpha(0)
                    self.alpha = 0
                    self.visible = False
                    self.transitioning = False
                else:
                    self.set_alpha(self.alpha)
            else:
                if self.direction == 0:
                    if self.motion_tick == self.motion_delta:
                        self.direction = 2
                        self.motion_tick = 0
                    else:
                        self.position[1] += 1

                elif self.direction == 2:
                    if self.motion_tick == self.motion_delta:
                        self.direction = 0
                        self.motion_tick = 0
                    else:
                        self.position[1] -= 1

                self.motion_tick += 1
            self.frame_counter += 1
            if self.frame_counter == self.visible_frames:
                self.transitioning = True
                self.frame_counter = 0

        #   Appear
        else:
            if self.transitioning:
                self.alpha += 12
                if self.alpha >= 230:
                    self.alpha = 230
                    self.set_alpha(230)
                    self.transitioning = False
                    self.visible = True
                else:
                    self.set_alpha(self.alpha)
            else:
                self.frame_counter += 1
                if self.frame_counter == self.invisible_frames:
                    self.transitioning = True
                    self.frame_counter = 0
                    self.set_next_pos(player)


        



#   ====   Bosses   ====   #
class AlphaFlapper(Enemy):
    def __init__(self, position = vec(0,0), file_name = "alphaflapper.png",
                 type=Avian, hp=50):
        super().__init__(position, file_name,
                         nFrames = 6, fps=16,
                         max_hp=hp, hp=hp,
                         speed = 50,
                         type=type)

        self.ignore_collision = True

    def get_drop(self):
        return GreenHeart(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))
    
    def get_money(self):
        return Buck(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))

class IceAlphaFlapper(AlphaFlapper):
    def __init__(self, position = vec(0,0)):
        super().__init__(position, "alphaflapper_ice.png",
                         Avian_Ice, hp=50)




class LavaKnight(Enemy):
    def __init__(self, position=vec(0,0), fall = False, boss = True):
        """
        Position of shadow does not move unless
        the knight moves its position.
        Moving its position is not the same as
        jumping up or down.
        """
        super().__init__(position, "knight.png",
                         nFrames=1, fps=16,
                         max_hp=100, hp=100, speed=0,
                         name="Lava Knight", id=[],
                         type=Fire)
        
        #   Behaves differently as a boss   #
        self.boss = boss
        
        
        #   Timers and Counters #
        self.startup_timer = 0.0
        self.jumpTimer = 0.5
        self.fall_timer = 0.0 #timer for off screen
        self.cold_timer = 0.0
        self.max_cold_time = 5.0
        self.freezeCounter = 10 #Once this gets to zero, it becomes vulnerable to Bombofauns
        self.maxCount = 10 #The maximum integer the freezeCount can be
        self.vibration_tick = 0


        #   State Booleans  #
        self.initializing = True
        self.starting = False
        self.shaking = False
        self.moving = False #   done with animation
        self.respawning = False
        self.falling = False
        self.desperate = False #    True if final phase is active

        self.jumpingUp = False
        self.jumpingDown = False
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False

        self.frozen = False
        self.vulnerable = False #   Able to be frozen
        self.cold = False # Able to be blown up
        self.dying = False

        self.pause = True # ??


        #   Drawing Instructions    #
        self.drawn = False
        self.shadow = Animated(vec(self.position[0], self.position[1]), "knight.png", (4,0))
        self.shadow.frame = 4
        self.currentRow = 0


        #   Player Targeting    #
        self.targetPos = vec(0,0)
        self.xVals = [] #   list of possible positions in the collisionRect
        self.yVals = []
        self.objects = [] # list of enemies to spawn


        #   Set the image   #
        self.set_image()


    def set_objects(self):
        self.objects = [
            # FireBall(vec(self.position[0]-8, self.position[1]), 2),
            # FireBall(vec(self.position[0]+32, self.position[1]), 4),
            # FireBall(vec(self.position[0]+32, self.position[1]+32), 0),
            # FireBall(vec(self.position[0]-8, self.position[1]+32), 5)
        ]

    def reset_objects(self):
        self.spawning = False
    
    def set_position(self, vector):
        vector2 = vec(vector[0], vector[1])
        self.position = vector
        self.shadow.position = vector2

    def reset(self):
        self.frozen = False
        self.starting = False
        self.vibration_tick = 0
        self.startup_timer = 0.0
        self.fall_timer = 0.0 #timer for off screen
        self.shaking = False #vibrating bool
        self.moving = False #done with animation
        self.respawning = False
        self.falling = False
        self.targetPos = vec(0,0)
        self.desperate = False #True if final phase is active
        self.hp = self.maxHp
        self.jumpingUp = False
        self.jumpingDown = False
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False
        self.frozen = False
        self.jumpTimer = 0.5
        self.pause = True
        self.freezeCounter = self.maxCount #Once this gets to zero, it becomes vulnerable to Bombofauns
        self.cold = False #Able to be blown up
        self.cold_timer = 0.0
        self.vulnerable = False #Able to be frozen
        self.iframeTimer = 0.0
        self.shadow.frame = 4
        self.xVals = [] #list of possible positions in the collisionRect
        self.yVals = []
        self.animation_timer = 0.0
        self.frameTime = 0.05
        self.frame = 3
        self.currentRow = 0
        self.initializing = True
        self.objects = []
        self.dying = False
        self.setImage()
        self.set_position(vec(RESOLUTION[0]//2-16, RESOLUTION[1]//2-16))

    #override
    def hurt(self, damage, setHit = True):
        self.hit = setHit
        self.hp -= damage
        self.injury = damage
        if self.desperate:
            if self.hp <= 0:
                self.dying = True
                self.ignoreCollision = True
            else:
                SoundManager.getInstance().playLowSFX("enemyhit.wav", volume=0.5)

        elif self.hp <= 0:
            self.desperate = True
            self.max_cold_time = 2.0
            self.hp = 25
            self.unsetCold()
        else:
            SoundManager.getInstance().playLowSFX("enemyhit.wav", volume=0.5)
        

    def bounce(self, other):
        if not self.cold and not self.falling and not self.respawning:
            self.fullStop()
            self.respawning = True
    
    def startRespawn(self):
        SoundManager.getInstance().playSFX("big_jump.wav")
        self.fullStop()
        self.ignoreCollision = True
        self.respawning = True
        self.top = True

    def fullStop(self):
        self.stop()
        self.jumpingUp = False
        self.jumpingDown = False
        self.jumpTimer = 0.0

    def stop(self):
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False

    def setCold(self):
        self.cold = True
        self.movingDown = False
        self.movingUp = False
        self.movingLeft = False
        self.movingRight = False
        self.row = 4
        self.currentRow = 4
        self.frame = 0
        self.setImage()
    
    def unsetCold(self):
        self.cold_timer = 0.0
        self.cold = False
        self.vulnerable = False
        self.freezeCounter = self.maxCount
        self.fullStop()
        self.respawning = True
        self.top = True
        self.row = 0
        self.currentRow = 0
        self.frame = 0
        self.frameTime = 0.05
        self.setImage()
    
    def stopMotion(self, position):
        self.setCollisionRange()
        if int(position[1]) in self.yVals:
            self.movingUp = False
            self.movingDown = False
        if int(position[0]) in self.xVals:
            self.movingRight = False
            self.movingLeft = False

    def getCollisionRect(self):
        return pygame.Rect((self.position[0], self.position[1]+8), (32,24))
    def getStartupRect(self):
        return pygame.Rect((self.position[0]-200, self.position[1]+32), (400, 24))
    
    def getShadowRect(self):
        return pygame.Rect((self.shadow.position[0] + 7, self.shadow.position[1] + 27), (19,5))
    
    def setImage(self):
        self.image = SpriteManager.getInstance().getSprite("knight.png", (self.frame, self.row))
    
    def incrementFrame(self):
        self.frame += 1
        self.frame %= 3

    def draw(self, drawSurface):
        super().draw(drawSurface, False)
    
    def drawTop(self, drawSurface):
        self.shadow.draw(drawSurface)
        super().draw(drawSurface)

    """
    Only damage player when on the ground
    """
    def handlePlayerCollision(self, player):
        if self.ignoreCollision or self.dying:
            return False
        else:
            return True
    
    def knockBack(self, other):
        ##Calculate side method is messed up.
        ##Properties of left and right are inversed
        side = self.calculateSide(other)
        if side == "left":
            self.setActualPos(0, False, 10)
        elif side == "top":
            self.setActualPos(1, True, 10)
        elif side == "right":
            self.setActualPos(0, True, 10)
        elif side == "bottom":
            self.setActualPos(1, False, 10)

    def handleCollision(self, other=None):
        if self.cold:
            if other.id == "bombo":
                #self.knockBack(other)
                self.hurt(other.damage)
                if not self.dying and self.cold_timer >= self.max_cold_time:
                    
                    self.unsetCold()
            return
        
        if not self.ignoreCollision:
            if self.vulnerable and other.id == "blizz":
                self.row = 5
                self.vulnerable = False
                self.freezeCounter -= 1
                self.frameTime += 0.05
                if self.freezeCounter <= 0:
                    self.setCold()
                    SoundManager.getInstance().playSFX("freeze.wav")
                else:
                    SoundManager.getInstance().playLowSFX("enemyhit.wav", volume=0.5)
                    if self.freezeCounter == 3:
                        self.currentRow = 3
                        self.setImage()
                    elif self.freezeCounter == 5:
                        self.currenRow = 2
                        self.setImage()
                    elif self.freezeCounter == 8:
                        self.currentRow = 1
                        self.setImage()
                    else:
                        pass
    
    def setTargetPos(self, position):
        if self.respawning:
            self.targetPos = vec(int(position[0]-8), int(position[1]-8))
        else:
            self.targetPos = vec(int(position[0]), int(position[1]+16))

    def setCollisionRange(self):
        self.xVals = []
        self.yVals = []
        pos = self.getShadowRect().topleft
        for i in range(19):
            self.xVals.append(pos[0] + i)
        for i in range(5):
            self.yVals.append(pos[1] + i)
        
        
    """
    Sets the position of the shadow and the knight
    """
    def setActualPos(self, axis = 0, add = True, value = 1, seconds = -1):
        if seconds == -1:
            if add:
                self.position[axis] += value
                self.shadow.position[axis] += value
            else:
                self.position[axis] -= value
                self.shadow.position[axis] -= value
        else:
            if add:
                self.vel[axis] = 200
            else:
                self.vel[axis] = -200
            self.position += self.vel * seconds
    """
    The knight chooses which direction 
    to move based on the player's position.

    position -> player's current position
    """
    def setDirection(self, position):
        if self.cold:
            return
        
        if int(position[0]) < int(self.position[0] + 16):
            self.movingLeft = True
            self.movingRight = False
        
        elif int(position [0]) > int(self.position[0] + 16):
            self.movingRight = True
            self.movingLeft = False

        if int(position[1]) < int(self.position[1] + 32):
            self.movingUp = True
            self.movingDown = False
        
        elif int(position [1]) > int(self.position[1] + 32):
            self.movingDown = True
            self.movingUp = False
    
    
    """
    Begin to fall down and crush the player
    """
    def crush(self):
        self.vel = vec(0,0)
        self.jumpingUp = False
        self.jumpingDown = True
        self.jumpTimer = 0.0
        

    def update(self, seconds, player = None):
        if player:
            position = player.position.copy()


        if self.cold:
            self.cold_timer += seconds

        ##Death Animation
        if self.dying:
            if self.startup_timer >= 1.0:
                if self.startup_timer >= 3.0:
                    if self.frame == 4:
                        self.startup_timer += seconds
                        if self.startup_timer >= 3.1:
                            self.dead = True
                            SoundManager.getInstance().playLowSFX("enemydies.wav", volume=0.2)
                    else:
                        self.animation_timer += seconds
                        if self.animation_timer >= 0.1:
                            self.animation_timer = 0.0
                            self.frame += 1
                            self.setImage()
                else:
                    self.startup_timer += seconds
                    if self.vibration_tick == 0:
                        self.setActualPos(0, True)
                        self.vibration_tick += 1
                        SoundManager.getInstance().playSFX("LA_Rock_Push.wav")
                    elif self.vibration_tick == 1:
                        self.setActualPos(0, False)
                        self.vibration_tick += 1
                    elif self.vibration_tick == 2:
                        self.setActualPos(0, False)
                        self.vibration_tick += 1
                    elif self.vibration_tick == 3:
                        self.setActualPos(0, True)
                        self.vibration_tick = 0
            else:
                self.startup_timer += seconds
            return

        ##Startup Animation
        if not self.moving:
            if self.starting:
                if not self.shaking:
                    self.startup_timer += seconds
                    if self.startup_timer >= 0.2:
                        self.startup_timer = 0.0
                        self.shaking = True
                else:
                    if self.startup_timer >= 2:
                        self.vibration_tick = 0
                        SoundManager.getInstance().stopSFX("LA_Rock_Push.wav")
                        self.frame = 0
                        self.setImage()
                        self.startup_timer += seconds
                        if self.startup_timer >= 3:
                            self.moving = True
                            self.startup_timer = 0.0
                    else:
                        self.startup_timer += seconds
                        if self.vibration_tick == 0:
                            SoundManager.getInstance().playSFX("LA_Rock_Push.wav")
                            self.setActualPos(0, True)
                            self.vibration_tick += 1
                        elif self.vibration_tick == 1:
                            self.setActualPos(0, False)
                            self.vibration_tick += 1
                        elif self.vibration_tick == 2:
                            self.setActualPos(0, False)
                            self.vibration_tick += 1
                        elif self.vibration_tick == 3:
                            self.setActualPos(0, True)
                            self.vibration_tick = 0
                        return
                return
            elif self.getStartupRect().collidepoint(position):
                self.starting = True

        else:
            
            #   Regular Animation Routine    #
            if not self.cold and self.frame < 3:
                self.animation_timer += seconds
                if not self.vulnerable:
                    if self.animation_timer >= 0.01:
                        self.animation_timer = 0.0
                        self.incrementFrame()
                        self.setImage()
                else: 
                    if self.animation_timer > 1 / self.fps:
                        self.animation_timer = 0.0
                        self.incrementFrame()
                        self.animation_timer -= 1 / self.fps
                        self.set_image()
                        self.setImage()
                        
            if self.initializing:
                return
            ##I-frame update
            if self.moving and not self.vulnerable:
                self.i_frame_counter += 1
                if self.i_frame_counter >= 20:
                    self.vulnerable = True
                    self.i_frame_counter = 0
                    self.row = self.currentRow
                    self.setImage()

            ##Respawn off screen
            if self.respawning and not self.pause:
                if self.falling:
                    ##Shadow reappears
                    if self.top:
                        if self.shadow.frame == 4:
                            self.fall_timer += seconds
                            ##Falling down
                            if self.fall_timer >= 0.2:
                                self.position[1] += 12
                                ##Crashed
                                if self.position[1] >= self.targetPos[1]:
                                    SoundManager.getInstance().stopAllSFX()                            
                                    SoundManager.getInstance().playSFX("crash.wav")
                                    self.position[1] = self.targetPos[1]
                                    self.falling = False
                                    self.top = False
                                    self.fall_timer = 0.0
                                    self.respawning = False
                                    self.pause = True
                                    if self.desperate:
                                        self.spawning = True
                                        self.set_objects()
                        ##Decrement shadow frame
                        else:
                            self.shadow.frame -= 1
                            self.shadow.image = SpriteManager.getInstance().getSprite("knight.png", (self.shadow.frame, 0))

                    ##Off screen, ready to set target
                    else:
                        self.fall_timer += seconds
                        if self.fall_timer >= 1.0:
                            self.fall_timer = 0.0
                            self.setTargetPos(position)
                            self.shadow.position = self.targetPos
                            self.position[0] = self.targetPos[0]
                            self.shadow.position[0] = self.targetPos[0]
                            self.top = True
                
                ##Jumping up  
                else:
                    self.position[1] -= 4
                    if self.position[1] + 32 <= -64:
                        self.shadow.frame += 1
                        self.shadow.frame %= 7
                        if self.shadow.frame == 0:
                            self.shadow.frame = 6
                            self.top = False
                            self.falling = True
                        self.shadow.image = SpriteManager.getInstance().getSprite("knight.png", (self.shadow.frame, 0))
                return
            
            
            
            ##Mid air movement
            if not self.pause:
                ##Jumping up
                self.jumpTimer += seconds
                if self.jumpingUp:
                    self.ignoreCollision = True
                    if self.position[1] <= self.shadow.position[1]-8:
                        self.setCollisionRange()
                        ##Player inside collision rect (able to be crushed)
                        if self.getCollisionRect().collidepoint((position[0]+8, position[1])):
                            self.crush()
                        
                        if self.jumpTimer >= 0.5 or (self.targetPos[0] in self.xVals and self.targetPos[1] in self.yVals):
                            self.crush()
                            
                        else:
                            if self.targetPos[1] < self.yVals[0]:
                                self.setActualPos(1, False, 2)
                            elif self.targetPos[1] > self.yVals[-1]:
                                self.setActualPos(1, True, 2)
                            
                            if self.targetPos[0] < self.xVals[0]:
                                self.setActualPos(0, False, 2)
                            elif self.targetPos[0] > self.xVals[-1]:
                                self.setActualPos(0, True, 2)

                        if self.cold:
                            if self.jumpTimer >= 0.1:
                                self.jumpingUp = False
                                self.jumpingDown = True
                                self.jumpTimer = 0.0
                    else:
                        self.position[1] -= 2

                    
                
                ##Falling down
                elif self.jumpingDown:
                    self.ignoreCollision = True
                    if self.cold:
                        self.position[1] += 6
                    else:
                        self.position[1] += 4
                    if self.position[1] >= self.shadow.position[1]:
                        SoundManager.getInstance().stopAllSFX()
                        SoundManager.getInstance().playSFX("crash.wav")
                        self.position[1] = self.shadow.position[1]
                        self.pause = True
                        self.top = False
                        self.jumpingDown = False
                        self.jumpTimer = 0.0
                        return

            ##Ground (no movement)
            else:
                self.ignoreCollision = False
                self.jumpTimer += seconds
                if self.jumpTimer >= 0.8:
                    self.jumpTimer = 0.0
                    self.pause = False
                    if self.desperate:
                        if self.cold:
                            self.setTargetPos(position)
                            SoundManager.getInstance().playSFX("big_jump.wav")
                            self.top = True
                            self.jumpingUp = True
                        else:
                            self.startRespawn()
                    else:
                        self.setTargetPos(position)
                        SoundManager.getInstance().playSFX("big_jump.wav")
                        self.top = True
                        self.jumpingUp = True