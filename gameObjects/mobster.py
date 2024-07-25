from utils import vec, SpriteManager, SoundManager
from UI import EventManager
from . import Drawable
"""
This file contains everything pertaining to
Monster Mobster.
"""


class MobsterEngine(object):
    """
    Main engine
    """
    def __init__(self, background_file = "background.png", bgm = "MSM_Castle.mp3"):
        self.background = SpriteManager.getInstance().getFx("mobster", background_file)
        self.bgm = bgm

        ##States
        self.in_speech = True
        self.ready_to_continue = False

    def initialize(self):
        SoundManager.getInstance().playBGM(self.bgm)

    def draw(self, drawSurf):
        drawSurf.blit(self.background, vec(0,0))

    def handleEvent(self):
        if self.in_speech:
            if self.ready_to_continue:
                pass
        else:
            pass

    def update(self, seconds):
        pass
