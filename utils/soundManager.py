"""
A Singleton Sound Manager class
Author: Liz Matthews, 2/17/2024

Provides on-demand loading of sounds and music for a pygame program.

"""

import pygame
import os

class SoundManager(object):
    """A singleton factory class to create and store sounds and music on demand."""
    
    _INSTANCE = None
    
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._SM()
        
        return cls._INSTANCE
    
    # Do not directly instantiate this class!
    class _SM(object):
        """An internal SoundManager class to contain the actual code."""
        
        _SFX_FOLDER = "sounds"
        _MUSIC_FOLDER = "music"
        
        def __init__(self):
            self.BGMs = {}
            self.dict = {}
            self.currentlyPlaying = None
        
        def playBGM(self, name):
            if self.currentlyPlaying:
                pygame.mixer.music.stop()
            self.currentlyPlaying = name
            pygame.mixer.music.load(os.path.join(SoundManager._SM._MUSIC_FOLDER,
                                                 name))        
            pygame.mixer.music.play(-1)
        
        def fadeoutBGM(self, fadeoutAmount=1000):
            pygame.mixer.music.fadeout(fadeoutAmount)
            self.currentlyPlaying = None
        
        def playSFX(self, name, loops=0):
            if name not in self.dict:
                self._loadSFX(name)
            return self.dict[name].play(loops)
        
        def playLowSFX(self, name, volume = 0.5, loops=0):
            if name not in self.dict:
                fullname = os.path.join(SoundManager._SM._SFX_FOLDER, name)
                sound = pygame.mixer.Sound(fullname)
                #print(sound.get_volume())
                sound.set_volume(volume)
                self.dict[name] = sound
            return self.dict[name].play(loops)
        
        def _loadSFX(self, name):
            """Loads a sound from a file."""
            fullname = os.path.join(SoundManager._SM._SFX_FOLDER, name)
            sound = pygame.mixer.Sound(fullname)
                
            self.dict[name] = sound
        
        def stopSFX(self, name):
            if name in self.dict:
                self.dict[name].stop()

        def playOnce(self, name):
            if name in self.dict:
                return
            else:
                self.playSFX(name)

        def stopAllSFX(self):
            for song, player in self.dict.items():
                if song.endswith(".wav"):
                    player.stop()
