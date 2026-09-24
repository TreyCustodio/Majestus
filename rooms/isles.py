from gameObjects import *
"""
Map Data for Frigid Isles

~
~
"""



class Frigid_1(MajestusEngine):
    def __init__(self):
        super().__init__(enemies = [],
                            bgm = "08", room_dir = "frigid_1",
                            roomId = 1)
        self.bgm = "08"

        # self.ignoreClear = True
        # self.max_enemies = 0
        # self.enemyPlacement = 0
        # self.background = Level("frost_1.png")
        # self.doors = [0]
        # self.toChapel = Trigger(door = 0)
        # #self.trigger1 = Trigger(door = 0)
        # self.torch1 = Torch((COORD[7][5]), lit = False)
        # self.torch2 = Torch((COORD[11][5]), lit = False)

        # self.chest = Chest(COORD[9][3], text = SPEECH["david"])
        # self.spawning.append(self.chest)
        # self.weightedSwitch = WeightedSwitch((16*9,16*8))
        # self.switches.append(self.weightedSwitch)
        # self.blockP = PushableBlock((16*6,16*8))
        # self.david = David(COORD[9][6], boss = True)
        # #self.david.hp = 1
        # self.portal = Portal(COORD[9][6], 1)
        # self.torches.append(self.torch1)
        # self.torches.append(self.torch2)

    def load_blocks(self):
        self.createSquare()

    def trigger_collision(self, trigger_id):
        if trigger_id == 1:
            return
            self.transport(Wavering_2, position=vec(16*28, 16*11), keepBGM=True)

    def load_progress(self):
        self.display_text("You're a bitch.\n")
        return
    
    def load_doors(self):
        self.set_doors("square")
