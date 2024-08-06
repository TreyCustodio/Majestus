import pygame
"""
A module for managing events
in the pygame event queue
"""

"""
RT -> select which attack to put on RT. Or have it set to element or arrow
"""

"""
Dictionaries
"""
## Specifies which actions are on and off
ACTIONS = {
    "interact": False, #Talking/interacting with objects
    "run":False,
    "shoot": False, #Shooting your ranged weapon
    "element": False, #Attacking with your element
    "pause": False, #Pause / Start
    "map": False, #Map / Select
    "special": "shoot",
    "target": False,
    "target_left":False,
    "target_right":False,
    "motion": False, #Movement
    "motion_axis": 0,
    "motion_value": 0,
    "down": False,
    "right": False,
    "up": False,
    "left": False,
    "down_r": False,
    "right_r": False,
    "up_r": False,
    "left_r": False,
}

##  Gives the button for each GAMECUBE action
GAMECUBE = {
        "interact": 2, #A
        "run": 2,
        "shoot": 0, #Y
        "element": 3, #B
        "pause": 9, #Start
        "map": 1, #X
        "target": 4 #X
    }

##  Gives the button for each SWITCH action
SWITCH = {
        "interact": 0, #A
        "run": 0,
        "shoot": 3, #Y
        "element": 1, #B
        "pause": 6, #Start
        "map": 4, #X
        "target": 4, #Axis 4, 1.0 -> down, -1.0 -> up
        "target_left":9,
        "target_right":10
    }

##  Gives the button for each KEYBOARD action
KEY = {
        "interact": pygame.K_z,
        "run": pygame.K_z,
        "shoot": pygame.K_x,
        "element": pygame.K_c,
        "pause": pygame.K_RETURN,
        "map": pygame.K_SPACE,
        "down":pygame.K_DOWN,
        "right":pygame.K_RIGHT,
        "up":pygame.K_UP,
       "left":pygame.K_LEFT,
       "target": pygame.K_LSHIFT
    }



"""
Classes
"""


class EventManager(object):
    """
    Singleton class that manages each event in the pygame event queue
    and decides how to affect the game based on the event.

    In higher level classes, event handling is done as follows:
    1. Checking if the desired action is activated by calling Actions["action"]
    and performing the action without deactivating it (action stays on as long as button held without pressing another).
    2. Checking if the desired action is activated, performing it, and deactivating it
    by calling performAction("action") -> Interactions, Pausing
    """
    _INSTANCE = None

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._EM()
        return cls._INSTANCE
    

    class _EM(object):
        def __init__(self):
            self.readyToFetch = True
            self.controller = "key"
            self.deadZone = 0.5

            self.cursorReady = False
            self.eventBufferTimer = 0.0
            self.updating = True
        
        def readyToUpdate(self):
            return self.updating
        
        def toggleFetching(self):
            self.readyToFetch = not self.readyToFetch
        
        def startTransition(self):
            pygame.event.clear()
        
        def endTransition(self):
            pygame.event.clear()
        
        def buffCursor(self):
            self.cursorReady = False

        def getCursorReady(self):
            return self.cursorReady
         
        def setJoystick(self):
            ##Set up joystick
            joysticks = pygame.joystick.get_count()
            for i in range(joysticks):
                joystick = pygame.joystick.Joystick(i)
                print(joystick.get_name())
                if joystick.get_name() == "Generic USB Joystick":
                    self.controller = "Gamecube"
                    pygame.joystick.Joystick(i).init()
                elif joystick.get_name() == "Nintendo Switch Pro Controller":
                    self.controller = "Switch"
                    pygame.joystick.Joystick(i).init()
                
        
        def removeJoystick(self, id):
            self.controller = "key"
        
        """
        If the action is activated, the action
        is deactivated and the function returns True
        False otherwise
        """
        def performAction(self, action: str):
            if ACTIONS[action]:
                ACTIONS[action] = False
                return True
            else:
                return False
        
        def setSpecial(self, action: str):
            ACTIONS["special"] = action

        ##Handle each event
        def handleEvents(self, engine):
            if self.readyToFetch:
                ##Handle events in the queue
                for event in pygame.event.get():
                    #if event.type != pygame.JOYAXISMOTION:
                    #print(event)
                    ##Quit game
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    
                    
                        

                    ##  Controller plugged
                    if event.type == pygame.JOYDEVICEADDED:
                        self.setJoystick()
                        return
                    elif event.type == pygame.JOYDEVICEREMOVED:
                        self.removeJoystick(event.instance_id)
                        return

                    ##  Window manipulation
                    if event.type == pygame.WINDOWMOVED or event.type == pygame.WINDOWLEAVE or not pygame.mouse.get_focused():
                        self.updating = False
                        if engine.state == "game":
                            if engine.game.player:
                                engine.game.player.stop()
                            
                            engine.state.pause()
                        pygame.event.clear()
                        return
                    elif not self.updating:
                        self.updating = True
                    
                    ##  Controller inputs
                    #Gamecube
                    if self.controller == "Gamecube":
                        if event.type == pygame.JOYBUTTONDOWN:
                            ACTIONS["interact"] = event.button == GAMECUBE["interact"]
                            ACTIONS["run"] = event.button == GAMECUBE["run"]
                            ACTIONS["shoot"] = event.button == GAMECUBE["shoot"]
                            if event.button == GAMECUBE["element"]:
                                ACTIONS["element"] = True
                            ACTIONS["pause"] = event.button == GAMECUBE["pause"]
                            ACTIONS["map"] = event.button == GAMECUBE["map"]
                            if event.button == GAMECUBE["target"]:
                                ACTIONS["target"] = True

                        elif event.type == pygame.JOYBUTTONUP:
                            button = event.button
                            if button == GAMECUBE["interact"]:
                                ACTIONS["interact"] = False
                            elif button == GAMECUBE["run"]:
                                ACTIONS["run"] = False
                            elif button == GAMECUBE["shoot"]:
                                ACTIONS["shoot"] = False
                            elif button == GAMECUBE["element"]:
                                ACTIONS["element"] = False
                            elif button == GAMECUBE["pause"]:
                                ACTIONS["pause"] = False
                            elif button == GAMECUBE["map"]:
                                ACTIONS["map"] = False
                            elif button == GAMECUBE["target"]:
                                ACTIONS["target"] = False

                        elif event.type == pygame.JOYAXISMOTION:
                            if event.value <= self.deadZone:
                                ACTIONS["motion"] = False
                            ACTIONS["motion"] = True
                            ACTIONS["motion_axis"] = event.axis
                            ACTIONS["motion_value"] = event.value
                            if event.axis == 1:
                                ##Upwards
                                if event.value < 0:
                                    if event.value < -self.deadZone:
                                        ACTIONS["up"] = True
                                        ACTIONS["down"] = False
                                    else:
                                        ACTIONS["up"] = False
                                        ACTIONS["down"] = False
                                
                                ##Downwards
                                elif event.value > 0:
                                    if event.value > self.deadZone:
                                        ACTIONS["down"] = True
                                        ACTIONS["up"] = False
                                    else:
                                        ACTIONS["down"] = False
                                        ACTIONS["up"] = False
                                
                                else:
                                    ACTIONS["up"] = False
                                    ACTIONS["down"] = False
                          

                            elif event.axis == 0:
                                ##Leftwards
                                if event.value < 0:
                                    if event.value < -self.deadZone:
                                        ACTIONS["left"] = True
                                        ACTIONS["right"] = False
                                    else:
                                        ACTIONS["left"] = False
                                        ACTIONS["right"] = False
                                
                                ##Rightwards
                                elif event.value > 0:
                                    if event.value > self.deadZone:
                                        ACTIONS["right"] = True
                                        ACTIONS["left"] = False
                                    else:
                                        ACTIONS["right"] = False
                                        ACTIONS["left"] = False

                                else:
                                    ACTIONS["left"] = False
                                    ACTIONS["right"] = False

                            
                
                    #Switch
                    elif self.controller == "Switch":
                        if event.type == pygame.JOYBUTTONDOWN:
                            ACTIONS["interact"] = event.button == SWITCH["interact"]
                            ACTIONS["run"] = event.button == SWITCH["run"]
                            ACTIONS["shoot"] = event.button == SWITCH["shoot"]
                            ACTIONS["pause"] = event.button == SWITCH["pause"]
                            ACTIONS["map"] = event.button == SWITCH["map"]
                            ACTIONS["target_left"] = event.button == SWITCH["target_left"]
                            ACTIONS["target_right"] = event.button == SWITCH["target_right"]
                            if event.button == SWITCH["element"]:
                                ACTIONS["element"] = True
                        elif event.type == pygame.JOYBUTTONUP:
                            button = event.button
                            if button == SWITCH["interact"]:
                                ACTIONS["interact"] = False
                            elif button == SWITCH["run"]:
                                ACTIONS["run"] = False
                            elif button == SWITCH["shoot"]:
                                ACTIONS["shoot"] = False
                            elif button == SWITCH["element"]:
                                ACTIONS["element"] = False
                            elif button == SWITCH["pause"]:
                                ACTIONS["pause"] = False
                            elif button == SWITCH["map"]:
                                ACTIONS["map"] = False
                            elif button == SWITCH["target_left"]:
                                ACTIONS["target_left"] = False
                            elif button == SWITCH["target_right"]:
                                ACTIONS["target_right"] = False

                        elif event.type == pygame.JOYAXISMOTION:
                            if event.axis == 4:
                                #print(event)
                                if event.value >= self.deadZone:
                                    ACTIONS["target"] = True
                                else:
                                    ACTIONS["target"] = False
                            if event.axis == 5:
                                #print(event)
                                if event.value >= self.deadZone:
                                    ACTIONS[ACTIONS["special"]] = True
                                else:
                                    ACTIONS[ACTIONS["special"]] = False
                            else:
                                if event.value <= self.deadZone:
                                    ACTIONS["motion"] = False
                                ACTIONS["motion"] = True
                                ACTIONS["motion_axis"] = event.axis
                                ACTIONS["motion_value"] = event.value
                                if event.axis == 1:
                                    ##Upwards
                                    if event.value < 0:
                                        if event.value < -self.deadZone:
                                            ACTIONS["up"] = True
                                            ACTIONS["down"] = False
                                        else:
                                            ACTIONS["up"] = False
                                            ACTIONS["down"] = False
                                    
                                    ##Downwards
                                    elif event.value > 0:
                                        if event.value > self.deadZone:
                                            ACTIONS["down"] = True
                                            ACTIONS["up"] = False
                                        else:
                                            ACTIONS["down"] = False
                                            ACTIONS["up"] = False
                                    
                                    else:
                                        ACTIONS["up"] = False
                                        ACTIONS["down"] = False
                            

                                elif event.axis == 0:
                                    ##Leftwards
                                    if event.value < 0:
                                        if event.value < -self.deadZone:
                                            ACTIONS["left"] = True
                                            ACTIONS["right"] = False
                                        else:
                                            ACTIONS["left"] = False
                                            ACTIONS["right"] = False
                                    
                                    ##Rightwards
                                    elif event.value > 0:
                                        if event.value > self.deadZone:
                                            ACTIONS["right"] = True
                                            ACTIONS["left"] = False
                                        else:
                                            ACTIONS["right"] = False
                                            ACTIONS["left"] = False

                                    else:
                                        ACTIONS["left"] = False
                                        ACTIONS["right"] = False

                                if event.axis == 3:
                                    ##Upwards
                                    if event.value < 0:
                                        if event.value < -0.65:
                                            ACTIONS["up_r"] = True
                                            ACTIONS["down_r"] = False
                                        else:
                                            ACTIONS["up_r"] = False
                                            ACTIONS["down_r"] = False
                                    
                                    ##Downwards
                                    elif event.value > 0:
                                        if event.value > 0.65:
                                            ACTIONS["down_r"] = True
                                            ACTIONS["up_r"] = False
                                        else:
                                            ACTIONS["down_r"] = False
                                            ACTIONS["up_r"] = False
                                    
                                    else:
                                        ACTIONS["up_r"] = False
                                        ACTIONS["down_r"] = False
                            

                                elif event.axis == 2:
                                    ##Leftwards
                                    if event.value < 0:
                                        if event.value < -0.65:
                                            ACTIONS["left_r"] = True
                                            ACTIONS["right_r"] = False
                                        else:
                                            ACTIONS["left_r"] = False
                                            ACTIONS["right_r"] = False
                                    
                                    ##Rightwards
                                    elif event.value > 0:
                                        if event.value > 0.65:
                                            ACTIONS["right_r"] = True
                                            ACTIONS["left_r"] = False
                                        else:
                                            ACTIONS["right_r"] = False
                                            ACTIONS["left_r"] = False

                                    else:
                                        ACTIONS["left_r"] = False
                                        ACTIONS["right_r"] = False
                    #Keyboard
                    elif self.controller == "key":
                        if event.type == pygame.KEYDOWN:
                            key = event.key
                            ACTIONS["interact"] = key == KEY["interact"]
                            ACTIONS["shoot"] = key == KEY["shoot"]
                            ACTIONS["element"] = key == KEY["element"]
                            ACTIONS["pause"] = key == KEY["pause"]
                            ACTIONS["map"] = key == KEY["map"]
                            if key == KEY["target"]:
                                ACTIONS["target"] = True
                            ##Movement
                            if key == KEY["down"]:
                                ACTIONS["down"] = True
                            elif key == KEY["up"]:
                                ACTIONS["up"] = True
                            elif key == KEY["right"]:
                                ACTIONS["right"] = True
                            elif key == KEY["left"]:
                                ACTIONS["left"] = True
         

                        elif event.type == pygame.KEYUP:
                            key = event.key
                            if key == KEY["interact"]:
                                ACTIONS["interact"] = False
                            elif key == KEY["shoot"]:
                                ACTIONS["shoot"] = False
                            elif key == KEY["element"]:
                                ACTIONS["element"] = False
                            elif key == KEY["pause"]:
                                ACTIONS["pause"] = False
                            elif key == KEY["map"]:
                                ACTIONS["map"] = False
                            elif key == KEY["down"]:
                                ACTIONS["down"] = False
                            elif key == KEY["up"]:
                                ACTIONS["up"] = False
                            elif key == KEY["right"]:
                                ACTIONS["right"] = False
                            elif key == KEY["left"]:
                                ACTIONS["left"] = False
                            elif key == KEY["target"]:
                                ACTIONS["target"] = False
                    
                    
                    ##Move menu cursors
                    #engine.moveMenuCursor()
                    ##Handle collision
                
                    
                    
                    
                engine.handleCollision()
                engine.handleEvent()
        

        def updateBuffer(self, seconds):
            if not self.cursorReady:
                self.eventBufferTimer += seconds
                if self.eventBufferTimer >= 0.15:
                    self.cursorReady = True
                    self.eventBufferTimer = 0.0