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
        _OST_FOLDER = os.path.join("music", "ost")
        _MUSIC_FOLDER = "music"

        _VOICE_FOLDER = "sounds/voices"
        
        def __init__(self):
            self.ost = {} # "track number": [intro, loop, end]
            self.BGMs = {}
            self.dict = {}

            #   Channels    #
            pygame.mixer.set_reserved(5)
            self.bgm_channel = pygame.mixer.Channel(5)

            #   Booleans    #
            self.currently_playing = False # True if currently playing a track
            self.playing_intro = False # True if an intro to a track is playing
        
        def play_ost(self, name, has_intro = False, has_outro = False):
            """Play a track from the original soundtrack"""
            if name not in self.ost:
                self._load_ost(name, has_intro, has_outro)

            if has_intro:
                self.playing_intro = True
                self.currently_playing = name
                return self.bgm_channel.play(self.ost[name][0], 1)
            else:
                self.currently_playing = name
                return self.bgm_channel.play(self.ost[name][1], -1)


        def playBGM(self, name):
            if self.currently_playing:
                pygame.mixer.music.stop()
                
            self.currently_playing = name
            pygame.mixer.music.load(os.path.join(SoundManager._SM._MUSIC_FOLDER,
                                                 name))        
            pygame.mixer.music.play(-1)



        def fadeout_bgm(self, fadeoutAmount=1000):
            self.bgm_channel.fadeout(fadeoutAmount)
            self.currently_playing = None
        
    
        def playSFX(self, name, loops=0):
            if name not in self.dict:
                self._loadSFX(name)
            return self.dict[name].play(loops)
        
        
        def playVoice(self, name, loops=0):
            """
            Play and load a voice file from the voice directory
            """
            if name not in self.dict:
                self._loadVoice(name)
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
        
        
        def _load_ost(self, name, has_intro = False, has_outro = False):
            """Load up a track from the ost"""
            track_number = name
            fullname = os.path.join(SoundManager._SM._OST_FOLDER, name)

            if has_intro:
                name = fullname + "_intro.wav"
                intro = pygame.mixer.Sound(name)
            else:
                intro = None

            if has_outro:
                name = fullname + "_outro.wav"
                outro = pygame.mixer.Sound(name)
            else:
                outro = None

            name = fullname + "_loop.wav"
            loop = pygame.mixer.Sound(name)

            self.ost[track_number] = [intro, loop, outro]

        def _loadVoice(self, name):
            """
            Load a voice file from the voice directory
            """
            fullname = os.path.join(SoundManager._SM._VOICE_FOLDER, name)
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

        def update(self, seconds):
            if self.playing_intro:
                #   Transition to the track's loop after the intro finishes #
                if not self.bgm_channel.get_busy():
                    self.playing_intro = False
                    self.bgm_channel.play(self.ost[self.currently_playing][1], -1)