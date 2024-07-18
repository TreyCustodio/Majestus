import pygame
"""
This file represents controllers
"""

"""
Dictionary for gamecube actions
"""
GAMECUBE = {
        "interact": 2,
        "shoot": 0,
        "element": 3,
        "pause": 9,
        "skip": 1
    }

ACTIONS = {
    "interact": False,
    "shoot": False,
    "element": False,
    "pause": False,
    "skip": False,
    "motion": False
}

class InputManager(object):
    def getPressed(event, action: str):
        if action == "motion":
            return event.type == pygame.JOYAXISMOTION
        return event.type == pygame.JOYBUTTONDOWN and event.button == GAMECUBE[action]

    def getUnpressed(event, action: str):
        return event.type == pygame.JOYBUTTONUP and event.button == GAMECUBE[action]

class Xbox(object):
    def __init__(self, value=None):
        self.value = value
        self.name = ""
    
    def setValue(self, value):
        self.value = value
        self.value.init()
        self.name = self.value.get_name()

class Gamecube(object):
    def __init__(self, value=None):
        self.value = value
        self.name = ""