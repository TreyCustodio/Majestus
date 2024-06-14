import pygame
"""
This file represents controllers
"""

class Xbox(object):
    def __init__(self, value=None):
        self.value = value
        self.name = ""
    
    def setValue(self, value):
        self.value = value
        self.value.init()
        self.name = self.value.get_name()