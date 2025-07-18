from . import (Drawable, Animated, Heart, BigHeart, 
                Buck, FireShard, GreenHeart, Buck_B, Buck_R, Bombodrop, LargeBombo, GiantBombo)
from .weapons import *
from .types import *

from utils import SoundManager, SpriteManager, SCALE, RESOLUTION, vec
from random import randint
import pygame

from abc import abstractmethod

#   -----   Engine  -----   #
#   Each frame, the Engine performs (3) Tasks.
#   (1) Draw
#   (2) Handle Events and Collision
#   (3) Upate the world
#
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
#   - 





#   -----   Enemies -----   #
#
#   --- Ids --- #
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
#   
#   *enemy.getDrop()* returns the item(s) the enemy drops
#
#
#   ---------------------   #
#
#   ----- Bosses -----  #
#
#   (1) Light Cloaker
#   Flag: 100/200
#   Type: Light
#   Area: Wavering Grotto
#   Gimmick: Teleport to 4 different locations
#
#
#   (2) Alpha Flapper
#   Flag: 101/201
#   Type: Non-Elemental
#   Area: Chapel Hall
#   Gimmick: Gets faster the more you damage it
#
#
#   (3) Smiler
#   Flag: 102/202
#   Type: Phantom
#   Area: Stardust Quarry
#   Gimmick: "Do you wanna know my real name? It's John." *Dies*
#
#
#   (4) Lava Knight
#   Flag: 103/203
#   Type: Fire
#   Area: Scorching Fields
#   Gimmick: Launch up off screen and fall on the player. 2 phases
#
#
#   (5) Robert (Round 1)
#   Flag: 104/204
#   Type: Skeletal
#   Area: ???
#   Gimmick: Extremely sturdy, but slow as hell. Faces one direction
#   and tosses endless bones at you.


class State(object):
    def __init__(file_name, row, nFrames):
        return


    

class Enemy(Drawable):
    def __init__(self, position=vec(0,0), fileName="",
                 frame=0, row=0, nFrames=1, fps=16,
                 max_hp = 5, hp=5, speed=50,
                 name = "", id = [], type=0,
                 top = False, i_frames = 20):
        
        #   Enemy Identification    #
        self.id = id
        self.name = name

        #   Animation Data  #
        self.fileName = fileName
        self.animation_timer = 0.0
        self.nFrames = nFrames
        self.fps = fps
        self.frame = frame
        self.row = row
        self.image = None
        self.set_image()

        #   Color Pallet Dictionary #
        ##  Each color is mapped to a damage color  ##
        self.pallet = {

        }

        #   Draw Instructions   #
        self.drawn = False # The enemy has been drawn
        self.top = False # The enemy is drawn at the top layer

        #   State Data  #
        self.current_state = "idle"

        ##  Set animation data per state in the following format:
        ##  [start_frame, row, nFrames, fps]
        self.states = {
            "idle":[self.frame, self.row, self.nFrames, self.fps]
        }

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
        self.hit = False
        self.dead = False
        self.dying = False
        self.frozen = False # If True, movement is halted; not a status effect
        self.i_frames = i_frames
        self.i_frame_counter = 0
        self.damaged = False # True if I-frames are active
        self.ignore_pallet = False # True if 0 damage dealt but still want I-frames

    #   ----- Getters and Setters ----- #
    def set_image(self) -> None:
        """Set the enemy's image before drawing"""
        self.image = SpriteManager.getInstance().getEnemy(self.fileName, (self.row, self.frame))

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

    @abstractmethod
    def get_drop(self):
        return
    
    @abstractmethod
    def get_money(self):
        return
    
    def play_hurt_sound(self, damage):
        if damage == 0:
            return
        elif damage < 0:
            return
        elif self.hp > 0: 
            SoundManager.getInstance().playLowSFX("enemyhit.wav", volume=0.5)
        else:
            self.dead = True
            SoundManager.getInstance().playLowSFX("enemydies.wav", volume=0.2)

    #   ----- Collision Detection ----- #
    def bounds_safety(self) -> bool:
        return False
    
    def collides_with_block(self, block) -> bool:
        """Determine whether or not to handle block collision"""
        return False

    def collides_with_projectile(self, proj) -> bool:
        """Determine whether or not to handle projectile collision."""
        return self.get_hit_box().colliderect(proj.getCollisionRect())

    def handle_player_collision(self, player) -> bool:
        """Determine whether or not to handle player collison"""
        return False
    
    def handle_projectile_collision(self, proj) -> None:
        """Handle collision with a projectile"""
        #   I-Frame Checker #
        if self.damaged:
            return
        
        #   Calculate Damage based on Types  #
        other_type = proj.type.NAME
        damage = proj.damage

        #   Check Resistance    #
        if other_type in self.type.RESISTANCE:
            damage = damage // self.type.RES_FACTOR

        #   Check Weakness  #
        elif other_type in self.type.WEAKNESS:
            damage *= self.type.WEAK_FACTOR

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

        #   Play a sound effect #
        self.play_hurt_sound(damage)

        #   Start I-Frames  #
        self.damaged = True
        if damage == 0:
            self.ignore_pallet = True

    def handle_collision(self, other) -> None:
        """Handle collision with another object"""
        return
    
    #   ----- Drawing ----- #
    def draw(self, drawSurface, drawHitbox=False, use_camera=True) -> None:
        #   Draw I-Frames   #
        if self.damaged and not self.ignore_pallet:
            temp_image = self.image.copy()

            temp_image.lock()
            for x in range(temp_image.get_width()):
                for y in range(temp_image.get_height()):
                    #   Set the color accroding to the enemy's pallet   #
                    color = temp_image.get_at((x, y))

                    for c in self.pallet:
                        if color == c:
                            temp_image.set_at((x, y), self.pallet[c])
                            
                    


            temp_image.unlock()
            drawSurface.blit(temp_image, self.position)
        else:
            super().draw(drawSurface, drawHitbox, use_camera)
        # self.drawn = True
    

    #   ----- Updating -----    #
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
        if self.damaged:
            self.i_frame_counter += 1
            if self.i_frame_counter == self.i_frames:
                self.i_frame_counter = 0
                self.damaged = False
                self.ignore_pallet = False

        #   Update Position #
        self.position += self.vel * seconds

    

class Test_Boner(Enemy):
    def __init__(self, position=vec(0, 0)):
        super().__init__(position, "boner.png",
                         nFrames=6, fps=12,
                         max_hp = 2_000, hp = 2_000,
                         type=Skeletal)

        self.pallet = {
             (240, 240, 217, 255) : (255, 0, 0, 255),
             (210, 75, 70, 255) : (116, 9, 5, 255)
        }
        
    def get_hit_box(self):
        return pygame.Rect(self.position[0] + 2, self.position[1] + 1, 14, 26)
    
    def get_drop(self):
        return Heart(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))
    
    def get_money(self):
        return Buck(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))
    

class Boner(Enemy):
    def __init__(self, position=vec(0, 0)):
        super().__init__(position, "boner.png",
                         nFrames=6, fps=8,
                         max_hp = 20, hp = 20,
                         type=Skeletal)

        self.pallet = {
             (240, 240, 217, 255) : (255, 0, 0, 255),
             (210, 75, 70, 255) : (116, 9, 5, 255)
        }

    def get_hit_box(self):
        return pygame.Rect(self.position[0] + 2, self.position[1] + 1, 14, 26)
    
    def get_drop(self):
        return Heart(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))
    
    def get_money(self):
        return Buck(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))


class Ice_Boner(Enemy):
    def __init__(self, position=vec(0,0)):
        super().__init__(position, "ice_boner.png",
                         nFrames=6, fps=8,
                         max_hp=40, hp=40,
                         type=Skeletal_Ice)

        self.pallet = {
             (198, 240, 217, 255) : (255, 0, 0, 255),
             (70, 210, 201, 255) : (116, 9, 5, 255),
             (48, 152, 145, 255) : (116, 9, 5, 255)
        }
    
    def get_hit_box(self):
        return pygame.Rect(self.position[0] + 2, self.position[1] + 1, 14, 26)
    
    def get_drop(self):
        return Heart(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))
    
    def get_money(self):
        return Buck(vec(self.position[0] + self.image.get_width()//2, self.position[1] + self.image.get_height()//2))


class Stinger(Enemy):
    def __init__(self, position=vec(0,0)):
        """Has a hitbox and a sting box.
        Stings the player if it enters the sting box"""

        super().__init__(position, "stinger.png",
                         nFrames=11, fps=8,
                         max_hp=30, hp=30,
                         type=Reptillian)

        self.pallet = {
             (153, 229, 80, 255) : (255, 0, 0, 255),
             (106, 190, 48, 255) : (116, 9, 5, 255),
             (55, 148, 110, 255) : (100, 30, 30, 255),
             (251, 224, 115, 255) : (250, 30, 30, 255),
             (75, 105, 47, 255) : (142, 11, 11, 255)
        }

        self.add_state("sting", 0, 1, 3, 8)

    
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