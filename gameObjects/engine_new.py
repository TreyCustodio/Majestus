import pygame
from math import ceil
from UI import EventManager, ACTIONS
from utils import SpriteManager
from . import (Drawable, HudImageManager, HudButtons, Slash, Blizzard, HealthBar, ElementIcon, EnergyBar, Blessing, Torch, AmmoBar, Fade, Drop, Heart, Player, Enemy, NonPlayer, Sign, Chest, Key, Geemer, Switch, 
               WeightedSwitch, DamageIndicator, LightSwitch, TimedSwitch, LockedSwitch, Block, IBlock, Trigger,
               PushableBlock, LockBlock, Bullet, Sword, Clap, Slash, Flapper, Number,
               Tile, Portal, Buck, Boulder, Map, BossHealth,
               Shadow, Walls, Floor, Camera, Highlight, ShopDisplay, Name)

from utils import SoundManager, vec, RESOLUTION, SPEECH, ICON, INV, COORD, FLAGS, EQUIPPED, UPSCALED, INTRO, SHORTCUTS, ACTIVE_SHORTCUT


class AbstractEngine(object):

    def __init__(self, room_dir = "", use_camera = False, room_size = vec(*RESOLUTION)):
        return
    
    def handle_event(self, )