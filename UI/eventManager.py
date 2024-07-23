import pygame
"""
A module for managing events
in the pygame event queue
"""


"""
Dictionaries
"""
## Specifies which actions are on and off
ACTIONS = {
    "interact": False, #Talking/interacting with objects
    "shoot": False, #Shooting your ranged weapon
    "element": False, #Attacking with your element
    "pause": False, #Pause / Start
    "map": False, #Map / Select
    "motion": False, #Movement
    "motion_axis": 0,
    "motion_value": 0,
    "down": False,
    "right": False,
    "up": False,
    "left": False,
}

##  Gives the button for each GAMECUBE action
GAMECUBE = {
        "interact": 2,
        "shoot": 0,
        "element": 3,
        "pause": 9,
        "map": 1
    }

##  Gives the button for each KEYBOARD action
KEY = {
        "interact": pygame.K_z,
        "shoot": pygame.K_x,
        "element": pygame.K_c,
        "pause": pygame.K_RETURN,
        "map": pygame.K_LSHIFT,
        "down":pygame.K_DOWN,
        "right":pygame.K_RIGHT,
        "up":pygame.K_UP,
       "left":pygame.K_LEFT,
    }




"""
Classes
"""
class InputManager(object):
    """
    The duty of this class is to check if any available actions should
    be activated based on the most recent event.
    """
    def getPressed(event, action: str):
        """
        Returns true if an action is pressed
        """
        if action == "motion":
            ##True if joystick is being moved
            return event.type == pygame.JOYAXISMOTION
        
        #otherwise return true if a button is pressed and that button corresponds to the action
        return event.type == pygame.JOYBUTTONDOWN and event.button == GAMECUBE[action]

    def getUnpressed(event, action: str):
        #True if a button is released
        return event.type == pygame.JOYBUTTONUP and event.button == GAMECUBE[action]


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
            self. eventBufferTimer = 0.0
        
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
            
        ##Handle each event
        def handleEvents(self, engine):
            if self.readyToFetch:
               
                ##Handle events in the queue
                for event in pygame.event.get():
                    
                    ##Quit game
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    
                    ##  Window manipulation
                    if event.type == pygame.WINDOWMOVED:
                        if engine.state == "game":
                            if engine.game.player:
                                engine.game.player.stop()
                            engine.state.pause()
                        return

                    ##  Controller plugged
                    if event.type == pygame.JOYDEVICEADDED:
                        self.setJoystick()
                        return
                    elif event.type == pygame.JOYDEVICEREMOVED:
                        self.removeJoystick(event.instance_id)
                        return
                    
                    ##  Controller inputs
                    #Gamecube
                    if self.controller == "Gamecube":
                        if event.type == pygame.JOYBUTTONDOWN:
                            ACTIONS["interact"] = event.button == GAMECUBE["interact"]
                            ACTIONS["shoot"] = event.button == GAMECUBE["shoot"]
                            ACTIONS["element"] = event.button == GAMECUBE["element"]
                            ACTIONS["pause"] = event.button == GAMECUBE["pause"]
                            ACTIONS["map"] = event.button == GAMECUBE["map"]
                        
                        elif event.type == pygame.JOYBUTTONUP:
                            button = event.button
                            if button == GAMECUBE["interact"]:
                                ACTIONS["interact"] = False
                            elif button == GAMECUBE["shoot"]:
                                ACTIONS["shoot"] = False
                            elif button == GAMECUBE["element"]:
                                ACTIONS["element"] = False
                            elif button == GAMECUBE["pause"]:
                                ACTIONS["pause"] = False
                            elif button == GAMECUBE["map"]:
                                ACTIONS["map"] = False

                        elif event.type == pygame.JOYAXISMOTION:
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
                    
                    #Keyboard
                    elif self.controller == "key":
                        if event.type == pygame.KEYDOWN:
                            ACTIONS["interact"] = event.key == KEY["interact"]
                            ACTIONS["shoot"] = event.key == KEY["interact"]
                            ACTIONS["element"] = event.key == KEY["interact"]
                            ACTIONS["pause"] = event.key == KEY["interact"]
                            ACTIONS["map"] = event.key == KEY["interact"]

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
                    
                    
                    
                    ##Move menu cursors
                    #engine.moveMenuCursor()
                    ##Handle collision
                    engine.handleCollision()
                    
                    
                    
                
                engine.handleEvent()
        

        def updateBuffer(self, seconds):
            if not self.cursorReady:
                self.eventBufferTimer += seconds
                if self.eventBufferTimer >= 0.2:
                    self.cursorReady = True
                    self.eventBufferTimer = 0.0