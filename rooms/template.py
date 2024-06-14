class Template(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Thun_1()
      
        return cls._INSTANCE
    
    class _Temp(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "fire.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("test.png")
            self.trigger1 = Trigger(door = 0)

        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           
        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                self.enemyCollision(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Room, 0, keepBGM=True)
                    else:
                        self.player.handleCollision(b)