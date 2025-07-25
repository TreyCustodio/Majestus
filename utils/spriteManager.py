"""
A Singleton Sprite Manager class
Author: Liz Matthews, 7/21/2023

Provides on-demand loading of images for a pygame program.
Will load entire sprite sheets if given an offset.

"""

from pygame import display, image, Surface, Rect, SRCALPHA
from os.path import join

class SpriteManager(object):
   """A singleton factory class to create and store sprites on demand."""
   
   # The singleton instance variable
   _INSTANCE = None
   
   @classmethod
   def getInstance(cls):
      """Used to obtain the singleton instance"""
      if cls._INSTANCE == None:
         cls._INSTANCE = cls._SM()
      
      return cls._INSTANCE
   
   
      
   # Do not directly instantiate this class!
   class _SM(object):
      """An internal SpriteManager class to contain the actual code. Is a private class."""
      
      # Folder in which images are stored
      _IMAGE_FOLDER = "images"
      
      _ENEMY_FOLDER = join("images", "enemies")

      _ROOM_FOLDER = join("images", "levels")
      ## Note that windows OS will use "\\" while Linux OS will simply use "/"
      

      # Static information about the sprite sizes of particular image sheets.
      _SPRITE_SIZES = {"text_components.png":(16,16),"buttons.png":(20,16),"chars.png":(20,20), "rocker.png":(16,16),"shop_display.png":(176,64),"shop_items.png":(16,16),"lock.png":(48,48),"TextBox3.png":(244,68),"bone.png":(10,16),"boner.png":(18,28),"npc_boner.png":(18,28),"laser.png":(14,14), "gleemer.png":(18,32),"keys.png":(20,16),"gremlin_blue.png":(18,36),"freeze.png":(16,16),"target.png":(18,18),"firi.png":(18,30), "heart.png":(16,16),"npcBopper.png": (16,16), "Objects.png":(16,16), "element.png":(16,16), "Bullet.png":(16,16), "blizz.png":(32,32), "slash.png": (32,32),"TextBox.png": (244,32), "geemer.png": (22,18),
                       "TextBox2.png": (244,64), "indicator.png":(58,32),
                       "icon.png": (32,32), "blockP.png":(16,16), "fire.png":(18,18), "black.png": (304, 208), 
                       "bar.png":(16,16), "ammo.png": (16,16), "torch.png": (16,16), 
                       "blessing.png":(16,16), "thunder.png":(64,64), "gale.png": (18,18),
                       "energy.png":(16,32), "item.png":(16,16),
                       "bopper.png":(16,16), "flapper.png":(16,16), "dummy.png":(16,16), "david.png":(19,26), "thunderTiles.png":(16,16),
                       "portal.png":(16,16), "exclamation.png":(16,16), "z.png": (16,16), "fireIcon.png":(16,16),
                       "spinner.png":(32,32), "shotsfired.png":(18,18), "drops.png":(16,16),
                       "baller.png":(16,16), "barrier.png":(16,16), "pixels.png":(16,16), "map.png":(240,160),
                       "numbers.png":(16,16), "cursor.png":(16,16),
                       "mapRooms.png":(8,8), "light.png":(64,64),
                       "knight.png":(32,32), "bullshot.png":(32,32),
                       "shiver.png":(20,26), "shortcut.png":(32,32),
                       "gremlin.png":(18,36),"boulder.png":(32,32), "alphaflapper.png":(32,32), "fireball.png":(16,16), "bigcursor.png":(16*8, 32), "promptcursor.png":(36,32),
                       "stinger.png":(100,49), "ice_boner.png":(18,28)
      }
      
      # A default sprite size
      _DEFAULT_SPRITE = (18,26)
      
      # A list of images that require to be loaded with transparency
      _TRANSPARENCY = ["text_components.png","buttons.png", "chars.png", "rocker.png", "shop_display.png","shop_items.png","npc_boner.png","lock.png","TextBox3.png","bone.png","laser.png","gleemer.png","keys.png","freeze.png","target.png","firi.png","stardust.png","heart.png","walls.png","light_2.png","shadow.png","shadow_1.png","shadow_2.png","shadow_3.png","shadow_4.png","shadow_5.png","shadow_6.png","npcBopper.png", "boulder.png","ammo.png", "title_screen.png", "pointer.png", "portal.png", "Objects.png", "KeyCount.png", "numbers.png", "Bullet.png", "null.png", 
                       "icon.png", "TextBox.png", "TextBox2.png", "geemer.png", "item.png", "fire.png", "black.png", "blessing.png",
                       "thunder.png", "energy.png", "gale.png", "indicator.png",
                       "gremlin_blue.png", "boner.png", "david.png", "flapper.png", "gremlin.png", "dummy.png", "heater.png",#Enemies
                       "exclamation.png", "z.png", "fireIcon.png", "shotsfired.png", "drops.png",
                       "baller.png", "stunner.png", "mage.png", "barrier.png", "pixels.png",
                       "map.png", "mapRooms.png", "bar.png", "cursor.png",
                       "bopper.png", "stomper.png", "alphaflapper.png", "fireball.png", "bigcursor.png", "promptcursor.png",
                       "bullshot.png", "light.png", "shiver.png", "Pause.png", "shortcut.png", "stinger.png", "ice_boner.png"
                       ]
      
      # A list of images that require to be loaded with a color key
      _COLOR_KEY = ["Link.png", "Stalfos.png", "blizz.png", "slash.png", "spinner.png",
                    "knight.png", "Pause.png"]
      
      def __init__(self):
         # Stores the surfaces indexed based on file name
         # The values in _surfaces can be a single Surface
         #  or a two dimentional grid of surfaces if it is an image sheet
         self._surfaces = {}      
      
      def __getitem__(self, key):
         return self._surfaces[key]
   
      def __setitem__(self, key, item):
         self._surfaces[key] = item
      
      def getSize(self, fileName):
         spriteSize = SpriteManager._SM._SPRITE_SIZES.get(fileName,
                                             SpriteManager._SM._DEFAULT_SPRITE)
         return spriteSize
      
      def getSprite(self, fileName, offset=None, enemy = False):
         # If this sprite has not already been loaded, load the image from memory
         if fileName not in self._surfaces.keys():
            self._loadImage(fileName, offset != None)
         
         # If this is an image sheet, return the correctly offset sub surface
         if offset != None:
            return self[fileName][offset[1]][offset[0]]
         
         # Otherwise, return the sheet created
         return self[fileName]
      
      def getLevel(self, fileName):
         if fileName not in self._surfaces.keys():
            self._loadImage(fileName, level = True)
         return self[fileName]
      
      def getFx(self, room_dir, fileName, offset = None):
         if fileName not in self._surfaces.keys():
            self._loadFx(room_dir, fileName, offset != None)
         else:
            delattr
            self._loadFx(room_dir, fileName, offset != None)
         
         if offset != None:
            return self[fileName][offset[1]][offset[0]]
         return self[fileName]
      
      def getEnemy(self, fileName, offset: tuple):
         """Load an enemy sprite from the enemy directory"""
         if fileName not in self._surfaces.keys():
            self._loadImage(fileName, sheet = True, enemy = True)
         return self[fileName][offset[0]][offset[1]]
      
      def _loadImage(self, fileName, sheet=False, level = False, enemy = False):
         # Load the full image
         if level:
            fullImage = image.load(join(SpriteManager._SM._ROOM_FOLDER, fileName))
         elif enemy:
            fullImage = image.load(join(SpriteManager._SM._ENEMY_FOLDER, fileName))
         else:
            fullImage = image.load(join(SpriteManager._SM._IMAGE_FOLDER, fileName))
         
         self._loadRoutine(fullImage, fileName, sheet)
         
      def _loadFx(self, room_dir, fileName, sheet = False):
          effects_folder = join(SpriteManager._SM._ROOM_FOLDER, room_dir)
          fullImage = image.load(join(effects_folder, fileName))
          self._loadRoutine(fullImage, fileName, sheet, True)

      def _loadRoutine(self, fullImage, fileName, sheet = False, transparent = False):
         if not transparent:
            # Look up some information about the image to be loaded
            transparent = fileName in SpriteManager._SM._TRANSPARENCY
         colorKey = fileName in SpriteManager._SM._COLOR_KEY
         
         # Detect if a transparency is needed
         if transparent:
            fullImage = fullImage.convert_alpha()
         else:
            fullImage = fullImage.convert()
         
         # If the image to be loaded is an image sheet, split it up based on the sprite size
         if sheet:
               
            self[fileName] = []
            
            # Try to get the sprite size, use the default size if it is not stored
            spriteSize = self.getSize(fileName)

            # See how big the sprite sheet is
            sheetDimensions = fullImage.get_size()
            
            # Iterate over the entire sheet, increment by the sprite size
            for y in range(0, sheetDimensions[1], spriteSize[1]):
               self[fileName].append([])
               for x in range(0, sheetDimensions[0], spriteSize[0]):
                  
                  # If we need transparency
                  if transparent:
                     sprite = Surface(spriteSize, SRCALPHA, 32)
                  else:
                     sprite = Surface(spriteSize)
                  
                  sprite.blit(fullImage, (0,0), Rect((x,y), spriteSize))
                  
                  # If we need to set the color key
                  if colorKey:
                     sprite.set_colorkey(sprite.get_at((0,0)))
                  
                  # Add the sprite to the end of the current row
                  self[fileName][-1].append(sprite)
         else:
            # Not a sprite sheet, full image is what we wish to store
            self[fileName] = fullImage
               
            # If we need to set the color key
            if colorKey:
               self[fileName].set_colorkey(self[fileName].get_at((0,0)))
            
         