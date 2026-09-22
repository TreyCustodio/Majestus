from gameObjects import *
"""
Map Data for Wavering Grotto

~Your hopes and dreams sink into the moist sand beneath your feet...~
~But your mind and heart force them back to the surface...~
"""

class Template(MajestusEngine):
    """(WIP) Template for constructing new rooms"""
    def __init__(self):
        super().__init__(enemies= [],
                         bgm = "03", room_dir = "tut_1",
                         roomId=0)
        self.trigger1 = None
        self.doors = []

    def load_blocks(self):
        return

    def trigger_collision(self, trigger_id):
        return

    def load_progress(self):
        return

    def create_doors(self):
        return


    
class Wavering_1(MajestusEngine):
    """New version of the first room"""
    def __init__(self):
        super().__init__(enemies = [Boner(vec(16*8, 16*2)),
                                    Boner(vec(16*9, 16*2)),
                                    Boner(vec(16*10, 16*2))
                                    ],
                         bgm="03", room_dir="tut_1",
                         roomId=4
                        )

        self.trigger1 = Trigger(door = 2, id=1)
        self.doors = [2]

    def load_blocks(self):
        self.blocks.append(self.trigger1)
        self.createSquare()

    def trigger_collision(self, trigger_id):
        if trigger_id == 1:
            self.transport(Wavering_2, position=vec(16*28, 16*11), keepBGM=True)

    def load_progress(self):
        return
    
    def create_doors(self):
        self.set_doors("square")




class Wavering_2(MajestusEngine):
    """New version of the first room"""
    def __init__(self):
        super().__init__(size = vec(608, 208),
                         enemies = [Slimer(vec(16*7, 16*5 + 8)),
                                    Slimer(vec(16*21, 16*5 + 8)),
                                    Slimer(vec(16*14, 16*5 + 8)),

                                    Boner(vec(16*8, 16*2)),
                                    Boner(vec(16*9, 16*2)),
                                    Boner(vec(16*10, 16*2))
                                    ],
                         bgm="03", room_dir="tut_2",
                         roomId=5
                        )
        
        self.triggers = [
            Trigger(vec(16*27,208-2), width=48, id=1),
            Trigger(vec(16*8,-14), width=48, id=2),
            Trigger(vec(16*27, -14), width = 48, id=3)
        ]
        self.doors = [1,2,4,7,6]

    def load_blocks(self):
        self.blocks = self.triggers + self.blocks
        self.createHorizontal()

    def trigger_collision(self, trigger_id):
        if trigger_id == 1:
            self.transport(Wavering_1, position_int=2, keepBGM=True)
        elif trigger_id == 2:
            self.transport(Wavering_3, vec(16*9, 16*18), keepBGM=True)
        elif trigger_id == 3:
            self.transport(Wavering_Shop, position_int=0, keepBGM=True)

    def load_progress(self):
        return
    
    def create_doors(self):
        self.set_doors("square")




class Wavering_Shop(MajestusEngine):
    """New version of the first room"""
    def __init__(self):
        super().__init__(
                        # size = vec(304, 320),
                         enemies = [Boner(vec(16*8, 16*2)),
                                    Boner(vec(16*9, 16*2)),
                                    Boner(vec(16*10, 16*2))
                                    ],
                         bgm="03", room_dir="tut_shop",
                         roomId=6
                        )

        self.doors = [0]
        self.triggers = [
            Trigger(vec(16*8,206), width=48, id=1),
        ]

    def load_blocks(self):
        self.blocks = self.triggers + self.blocks
        self.createSquare()
        for i in range(3,10):
            self.blocks.append(IBlock(vec(16*i, 16*4)))
            self.blocks.append(IBlock(vec(16*i + (16*7), 16*4)))

    def trigger_collision(self, trigger_id):
        if trigger_id == 1:
            self.transport(Wavering_2, vec(16*28, 16), keepBGM=True)

    def load_progress(self):
        return
    
    def create_doors(self):
        self.set_doors("square")






class Wavering_3(MajestusEngine):
    """New version of the first room"""
    def __init__(self):
        super().__init__(size = vec(304, 320),
                         enemies = [Boner(vec(16*8, 16*2)),
                                    Boner(vec(16*9, 16*2)),
                                    Boner(vec(16*10, 16*2))
                                    ],
                         bgm="03", room_dir="tut_3",
                         roomId=7
                        )

        self.doors = [0,2,1]
        self.triggers = [
            Trigger(vec(16*8, self.size[1]-2), width=48, id = 1),
            Trigger(vec(16*8, -14), width=48, id = 2),
            Trigger(vec(16*18 + 14, 16*5), height=48, id = 3)
        ]

    def load_blocks(self):
        self.blocks = self.triggers + self.blocks
        self.createVertical()

    def trigger_collision(self, trigger_id):
        if trigger_id == 1:
            self.transport(Wavering_2, position_int=2, keepBGM=True)
        elif trigger_id == 2:
            return
            self.transport(Entrance, vec(16*9,16*9), keepBGM=False)
        elif trigger_id == 3:
            self.transport(Wavering_4, position_int=3, keepBGM=True)

    def load_progress(self):
        return
    
    def create_doors(self):
        self.set_doors("vertical")





class Wavering_4(MajestusEngine):
    """New version of the first room"""
    def __init__(self):
        super().__init__(enemies = [Boner(vec(16*8, 16*2)),
                                    Boner(vec(16*9, 16*2)),
                                    Boner(vec(16*10, 16*2))
                                    ],
                         bgm="03", room_dir="tut_4",
                         roomId=8
                        )

        self.doors = [3]
        self.triggers = [
            Trigger(vec(-14, 16*5), height=48, id = 1)
        ]

    def load_blocks(self):
        self.blocks = self.triggers + self.blocks
        self.createSquare()

    def trigger_collision(self, trigger_id):
        if trigger_id == 1:
            self.transport(Wavering_3, vec(16*17, 16*6), keepBGM=True)

    def load_progress(self):
        return
    
    def create_doors(self):
        self.set_doors("square")