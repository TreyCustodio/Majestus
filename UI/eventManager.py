import pygame
"""
A module for managing events
in the pygame event queue
"""

class EventManager(object):

    _INSTANCE = None
    
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._EM()
        return cls._INSTANCE
    
    class _EM(object):
        def __init__(self):
            self.event = None
            self.readyToFetch = True
        
        def toggleFetching(self):
            self.readyToFetch = not self.readyToFetch
        
        def startTransition(self):
            #self.readyToFetch = True
            pygame.event.clear()
        
        def endTransition(self):
            pygame.event.clear()
            #print("A")
            #self.toggleFetching()
        
        def handleEvents(self, engine):
            
            for event in pygame.event.get():
                #print(event)
                
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    RUNNING = False

                    """ elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.display.toggle_fullscreen() """

                else:
                    #gameEngine.handleEvent(event)
                    result = engine.handleEvent(event)
                    if result == "exit":
                        RUNNING = False