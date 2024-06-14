from . import Highlight, Animated
from utils import vec, SpriteManager, SoundManager, INV, EQUIPPED, COORD


class Map(object):
    """
    Represents a map for a specific area
    """
    _INSTANCE = None
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._Map()
        return cls._INSTANCE
    
    

    class _Map(object):
        
        
        def __init__(self):
            class Node(Animated):
                def __init__(self, position, offset=(0,0), flag = 0):
                    """
                    flags:
                    0 -> default, 1 -> boss, 2 -> incomplete/item, 3 -> special
                    """
                    ##Fix animation
                    
                    if flag == 0:
                        super().__init__(position, "mapRooms.png")
                        self.doorImage = SpriteManager.getInstance().getSprite("mapRooms.png", offset)
                        self.framesPerSecond = 4
                        self.nFrames = 6
                        self.clear = True

                    elif flag == 1:
                        super().__init__(position, "mapRooms.png", (0,7))
                        self.doorImage = SpriteManager.getInstance().getSprite("mapRooms.png", offset)
                        self.row = 7
                        self.framesPerSecond = 16
                        self.nFrames = 4
                        self.clear = False

                    elif flag == 2:
                        super().__init__(position, "mapRooms.png", (0,8))
                        self.doorImage = SpriteManager.getInstance().getSprite("mapRooms.png", offset)
                        self.row = 8
                        self.framesPerSecond = 4
                        self.nFrames = 6
                        self.clear = False
                    
                    elif flag == 3:
                        super().__init__(position, "mapRooms.png", (0,9))
                        self.doorImage = SpriteManager.getInstance().getSprite("mapRooms.png", offset)
                        self.row = 9
                        self.framesPerSecond = 4
                        self.nFrames = 6
                        self.clear = False
                    
                    elif flag == 4:
                        super().__init__(position, "mapRooms.png", (0,10))
                        self.doorImage = SpriteManager.getInstance().getSprite("mapRooms.png", offset)
                        self.row = 10
                        self.framesPerSecond = 4
                        self.nFrames = 6
                        self.clear = False
                    
                    elif flag == 5:
                        super().__init__(position, "mapRooms.png", (0,11))
                        self.doorImage = SpriteManager.getInstance().getSprite("mapRooms.png", offset)
                        self.row = 11
                        self.framesPerSecond = 4
                        self.nFrames = 6
                        self.clear = False

                    elif flag == 6:
                        super().__init__(position, "mapRooms.png", (0,12))
                        self.doorImage = SpriteManager.getInstance().getSprite("mapRooms.png", offset)
                        self.row = 12
                        self.framesPerSecond = 4
                        self.nFrames = 6
                        self.clear = False

                def clearRoom(self):
                    self.clear = True
                    self.row = 0

                def draw(self, drawSurf):
                    super().draw(drawSurf)
                    #print(self.doorImage)
                    drawSurf.blit(self.doorImage, self.position)
                
                def update(self, seconds):
                    super().update(seconds)
                    

            """
            Dictionary of dictionaries representing the rooms
            in each area.
            Follows typical elemental order
            0 -> entrance, 1-4 -> fire, ice, thunder, wind
            """
            self.rooms = {

                ##  Entrance    ##
                0:{
                 #Main route
                    0:Node((16*9+5, 16*9+2), (0,2)),
                    1:Node((16*9+5, 16*9-8), (0,4), flag = 2),
                    2:Node((16*9+5, 16*8-2), (2,6)),
                    3:Node((16*9+5, 16*8-12), (0,4)),
                    4:Node((16*9+5, 16*8-22), (2,1)),
                    5:Node((16*9+5, 16*8-32), (0,4)),
                    6:Node((16*9+5, 16*8-42), (3,2), flag=1),
                    7:Node((16*9-5, 16*8-22), (2,1)),
                    8:Node((16*9+15, 16*8-22), (2,1)),
                    
                    #Element rooms
                    20:Node((16*9-5, 16*8-12), (0,2), flag=3),
                    21:Node((16*9-5, 16*8-32), (3,2), flag=4),

                    22:Node((16*9+15, 16*8-12), (0,2), flag=5),
                    23:Node((16*9+15, 16*8-32), (3,2), flag=6),
                    #Geemer Town
                    9:Node((16*9-15, 16*8-2), (2,4)),
                    10:Node((16*9-15, 16*8-12), (3,2)),
                    11:Node((16*9-5, 16*8-2), (5, 4))
                },

                ##  Flame   ##
                1:{
                    0:None,
                    4:Node((16*9-5, 16*8-12), (3,2))
                }
                
            }
            self.mapNum = 0

            self.highlight = Highlight(self.rooms[EQUIPPED["area"]][EQUIPPED["room"]].position, flag=3)
            self.selectedPos = vec(self.highlight.position[0], self.highlight.position[1])

            self.image = SpriteManager.getInstance().getSprite("map.png", (0,0))
                
        def updateHighlight(self):
            if not INV["map"+str(self.mapNum)]:
                return
            self.mapNum = EQUIPPED["area"]
            self.highlight.position = self.rooms[EQUIPPED["area"]][EQUIPPED["room"]].position
            self.selectedPos = vec(self.highlight.position[0], self.highlight.position[1])

        def updateSelected(self):
            self.highlight.position = self.selectedPos

        def draw(self, drawSurf):
            """
            draw the rooms on the map
            mapNum:
            0 -> entrance, 1-4 -> elements
            """
            if not INV["map"+str(self.mapNum)]:
                mapImage = SpriteManager.getInstance().getSprite("map.png", (1,0))
                drawSurf.blit(mapImage, (32,24))
                return
            
            drawSurf.blit(self.image, (32,24))
            for key in self.rooms[self.mapNum]:
                self.rooms[self.mapNum][key].draw(drawSurf)
            
            if self.highlight.timer <= 0.1:
                self.highlight.draw(drawSurf)
            elif self.highlight.timer > 0.1 and self.highlight.timer <= 0.2:
                pass
            elif self.highlight.timer > 0.20:
                self.highlight.timer = 0
                
                self.highlight.draw(drawSurf)

        def update(self, seconds):
            if not INV["map"+str(self.mapNum)]:
                return
            for key in self.rooms[self.mapNum]:
                self.rooms[self.mapNum][key].update(seconds)
            
            self.highlight.updateFlashTimer(seconds)