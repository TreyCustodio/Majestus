from . import Drawable
from utils import SpriteManager
from UI import EventManager

"""
Author - Trey Custodio
This files helps to manage different
button Icons based on what controller
the player is using
"""

### Icon Classes    ###
"""
Abstract Icon class.
Child classes represent button Icons
to be displayed in-game.
"""
class AbstractIcon(Drawable):
    def __init__(self, position):
        self.position = position
        self.frame = 0
        self.row = 0
        self.nFrames = 4
        self.framesPerSecond = 16
        self.frameTimer = 0.0
    

"""
Interact button
"""
class InteractIcon(AbstractIcon):
    def __init__(self, position):
        super().__init__(position)
        self.image = IconManager.getIcon("interact")
        self.id = "interact"

"""
Element button
"""
class ElemIcon(AbstractIcon):
    def __init__(self, position):
        super().__init__(position)
        self.image = IconManager.getIcon("element")
        self.id = "element"

"""
Shoot button
"""
class ShootIcon(AbstractIcon):
    def __init__(self, position):
        super().__init__(position)
        self.image = IconManager.getIcon("shoot")
        self.id = "shoot"

"""
Right Trigger
"""
class ShortcutIcon(AbstractIcon):
    def __init__(self, position):
        super().__init__(position)
        self.image = IconManager.getIcon("shortcut")
        self.id = "shortcut"

"""
Left Trigger
"""
class TargetIcon(AbstractIcon):
    def __init__(self, position):
        super().__init__(position)
        self.image = IconManager.getIcon("target")
        self.id = "target"

"""
Left Bumper
"""
class LeftIcon(AbstractIcon):
    def __init__(self, position):
        super().__init__(position)
        self.image = IconManager.getIcon("shortcut_left")
        self.id = "shortcut_left"

"""
Right Bumper
"""
class RightIcon(AbstractIcon):
    def __init__(self, position):
        super().__init__(position)
        self.image = IconManager.getIcon("shortcut_right")
        self.id = "shortcut_right"

"""
Control Stick
Arrows if using keys, otherwise the same for all controllers.
"""
class StickIcon(AbstractIcon):
    def __init__(self, position):
        super().__init__(position)
        self.image = IconManager.getIcon("stick")
        self.id = "stick"


### Icon Manager Class  ###

class IconManager(object):

    """
    Returns the Surface object representing the icon image (in white box).

    key (not capitalized), Switch, Gamecube, Xbox, Ps5
    """
    #Static
    def getIcon(button: str = ""):
        controller = EventManager.getInstance().getController()
        if controller == "Switch":
            if button == "interact":
                return SpriteManager.getInstance().getSprite("z.png", (0,0))
            elif button == "shoot":
                return SpriteManager.getInstance().getSprite("z.png", (0,0))
            if button == "element":
                return SpriteManager.getInstance().getSprite("z.png", (0,0))
        else:
            return SpriteManager.getInstance().getSprite("z.png", (0,1))
    
    def getButton(button : str = ""):
        """
        Returns the surface object representing the button image.
        """
        ##  Get Y (Row)
        controller = EventManager.getInstance().getController()
        if controller == "Switch":
            y = 4
        else:
            y = 5

        ##  Get X (Column)
        if button == "interact":
            x = 0
        elif button == "element":
            x = 1
        elif button == "shoot":
            x = 2
        elif button == "shortcut_left":
            x = 6
        elif button == "shortcut_right":
            x = 7
        elif button == "shortcut_trigger":
            x = 5

        
        return SpriteManager.getInstance().getSprite("buttons.png", (x,y))


    """
    Animate Icon images.
    @param icon -> the icon object to animate. Will be a child of AbstractIcon.
    """
    def update(icon, seconds = 0.0):
        controller = EventManager.getInstance().getController()
        icon.frameTimer += seconds
        if icon.frameTimer > 1/ icon.framesPerSecond:
            icon.frame += 1
            icon.frame %= icon.nFrames
            icon.frameTimer -= 1/icon.framesPerSecond
            if icon.id == "interact":
                if controller == "Switch":
                    icon.image = SpriteManager.getInstance().getSprite("z.png", (icon.frame, 0))
                else:
                    icon.image = SpriteManager.getInstance().getSprite("z.png", (icon.frame, 1))
