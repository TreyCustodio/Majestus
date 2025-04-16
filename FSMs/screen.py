from . import AbstractGameFSM

class State(object):
    def __init__(self, state=""):
        self.state = state
    
    def to(self, state):
        self.state = state
        return self.state

class ScreenManagerFSM(object):
    mainMenu = State()
    game     = State()
    paused   = State()
    textBox = State()
    intro = State()
    
    toIntro = mainMenu.to(intro)
    toGame = intro.to(game)
    speak =  game.to(textBox) | textBox.to(game) 
    speakP = paused.to(textBox) | textBox.to(paused) # Paused -> Textbox or Textbox -> Paused
    speakI = intro.to(textBox) | textBox.to(intro) # Intro -> Text or Text -> Intro
    pause = game.to(paused) | paused.to(game) | \
            mainMenu.to.itself(internal=True)
    toMain = game.to(mainMenu) | paused.to(mainMenu)
    startGame = mainMenu.to(game)
    quitGame  = game.to(mainMenu) | \
                paused.to.itself(internal=True)
    
    def isInGame(self):
        return self == "game" or self == "paused"
    
    def on_enter_game(self):
        pass
        #self.obj.game.link.updateMovement()
    