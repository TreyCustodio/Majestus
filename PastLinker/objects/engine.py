import pygame
import gc
from . import Drawable, Animated, Walker, Sniper
from UI import SoundManager, WordManager, EventManager
from utils import RESOLUTION, FLOOR

class Engine:
    """
    The Engine drives the game.
    Each frame, it draws the game in its current state,
    handles input from the user,
    and updates the objects in the game.
    """


##  ----------------------------------------------- ##
                ##  Initialization   ##

    def __init__(self, spawnRate=200):
        """
        Initialize the engine's relevant
        variables and objects.
        """
        #   States
        self.inTitle = True
        self.inGame = False
        self.paused = False
        self.dead = False
        self.hurting = False
        self.sniping = False
        self.upgradeReady = True
        self.spawnReady = True
        self.wipe_on = False
        self.wipe_off = False

        #   Timers and Counters
        self.iFrames = 0
        self.frameCounter = 0
        self.spawnRate = spawnRate
        self.maxEnemies = 20
        self.spawnTimer = 0.0
        self.snipeTimer = 10.0
        self.flashTimer = 0.0
        self.wipe_alpha = 0
        self.flash_alpha = 200
        

        #   Drawable Objects
        self.title_text = pygame.font.SysFont("Garamond", 36).render("War And Keys", False, (200,0,0))
        self.title = pygame.font.SysFont("Garamond", 16).render("Press any button", False, (255,255,255))
        
        self.background = pygame.Rect((0,0), (RESOLUTION[0], RESOLUTION[1]))
        self.floor = pygame.Rect((0,RESOLUTION[1] - FLOOR), (RESOLUTION[0], 1))
        self.flash = Drawable((0,0), "black.png")
        self.flash.image = pygame.transform.scale(self.flash.image, RESOLUTION)
        self.flash.image.set_alpha(self.flash_alpha)
        self.pauseImage = Animated((RESOLUTION[0]//2 - 60//2, RESOLUTION[1]//2 - 16//2), "pause.png", nFrames=1)

        self.player = Animated((0, RESOLUTION[1] - (FLOOR + 16)), "player.png", nFrames=6)
        
        #   Hp and Damage
        self.hp = 100
        self.hpBar = pygame.Rect(1,1, self.hp, 16)
        self.hpOutline = pygame.Rect(0,0, self.hp+2, 16+2)
        self.damage = 0
        self.damageY = self.player.position[1] - 24

        #   Lists
        self.enemies = [] # List containing the enemies
        self.keyBuffer = [] # List containing the player's current string



##  ----------------------------------------------- ##
            ##  Auxillaury Routines   ##

    def pause(self):
        """
        Pause the game.
        """
        self.playSFX("pause.wav")
        self.paused = True
    
    def resume(self):
        """
        Resume the game.
        """
        self.playSFX("pause.wav")
        self.paused = False
        self.flash_alpha = 200
        self.flash.image.set_alpha(200)
        self.flashTImer = 0.0
    
    def backSpace(self):
        """
        Delete the last character
        in the player's current string.
        """
        if len(self.keyBuffer) > 0:
            del self.keyBuffer[-1]

    def spawn(self, force = False):
        #   Max length is 11
        """
        Spawn an enemy.
        Param force -> Ignores spawnReady and the length of self.enemies
        and forces an enemy to spawn.
        """
        if force or (self.spawnReady and (len(self.enemies) < self.maxEnemies)):
            if self.sniping:
                e = Walker(WordManager.getCommon(True), (255,255,70))
            else:
                e = Walker(WordManager.getCommon())
            self.enemies.append(e)
            self.frameCounter = 0
            self.spawnReady = False
    
    def spawnSniper(self):
        """
        Spawn a sniper upgrade.
        """
        e = Sniper()
        self.enemies.append(e)
        self.upgradeReady = False

    def playSFX(self, fileName):
        """
        Play a sound effect.
        """
        SoundManager.getInstance().playSFX(fileName)

    def startGame(self):
        """
        Start the game.
        """
        self.playSFX("pause.wav")
        #SoundManager.getInstance().playBGM("01_Relax-my-eyes.mp3")
        self.inTitle = False
        self.inGame = True
    
    def hurt(self, damage):
        """
        Hurt the player.
        """
        if not self.hurting:
            self.damageY = self.player.position[1] - 24
            self.hp -= damage
            self.hpBar = pygame.Rect(1,1,self.hp, 16)
            self.hurting = True



    ##  ----------------------------------------------- ##
                    ##  Event Handling   ##

    def handleKey(self):
        """
        Handles key presses obtained
        from the user.
        """
        if self.paused:
            return
        
        elif self.inGame:
            if WordManager.DIFFICULTY == None:
                WordManager.setDifficulty("easy")

            if EventManager.backspace_ready:
                self.backSpace()
                EventManager.buffBackspace()

            for key in EventManager.queue:
                if len(self.keyBuffer) == 0:
                        self.playSFX("text_1.wav")
                        self.keyBuffer.append(chr(key).upper())
                else:
                    self.playSFX("text_1.wav")
                    self.keyBuffer.append(chr(key))

                del EventManager.queue[0]

    
    def submitString(self):
        """
        Try to damage an enemy
        using the player's current string.
        """
        for e in self.enemies:
            if e.string == ''.join(self.keyBuffer):
                if e.type == "snipe":
                    self.playSFX("text_2.wav")
                    self.snipe()
                    e.kill()
                else:
                    self.playSFX("text_2.wav")
                    e.kill()
                    self.spawn()
                self.keyBuffer = []
                return
        self.playSFX("text_3.wav")

    def snipe(self):
        """
        Initiate the sniper powerup.
        All enemies can now be
        killed with 1 key press.
        """
        self.sniping = True
        for e in self.enemies:
            e.string = e.string[0]
            e.color = (255,255,70)

        

    ##  ----------------------------------------------- ##
                    ##  Drawing   ##

    def draw(self, drawSurf):
        """
        Blit all the drawable objects
        to the drawSurf.
        """
        if self.inTitle:
            #   Name of the game
            drawSurf.blit(self.title_text, (RESOLUTION[0] // 2 - self.title_text.get_width() // 2, RESOLUTION[1] // 2 - self.title_text.get_height() * 1.5))
            #   Press any button
            drawSurf.blit(self.title, (RESOLUTION[0] // 2 - self.title.get_width() // 2, RESOLUTION[1] // 2 - self.title.get_height() // 2))
        
        elif self.inGame:
            #   Background
            self.drawBackground(drawSurf)
            
            #   Floor
            self.drawFloor(drawSurf)
            
            #   Enemies
            for e in self.enemies:
                e.draw(drawSurf)

            #   Player
            self.player.draw(drawSurf)
            text = pygame.font.SysFont("Garamond", 24).render(''.join(self.keyBuffer), False, (255,255,255))
            
            text_box = pygame.Rect((self.player.position[0] + 8, self.player.position[1] - 24), ())
            drawSurf.blit(text, (self.player.position[0] + 8, self.player.position[1] - 24))

            pygame.draw.rect(drawSurf, (255,255,255), self.hpOutline, 1)
            pygame.draw.rect(drawSurf, (0,255,0), self.hpBar)
            
            if self.hurting:
                self.drawDamage(drawSurf)

            #   Pause
            if self.paused:
                self.flash.draw(drawSurf)
                self.pauseImage.draw(drawSurf)

    def drawBackground(self, drawSurf):
        """
        Draw the background image.
        """
        pygame.draw.rect(drawSurf, (0,0,0), self.background)

    def drawFloor(self, drawSurf):
        """
        Draw the floor image.
        """
        pygame.draw.rect(drawSurf, (255,255,255), self.floor)

    def drawDamage(self, drawSurf):
        """
        Draw red damage numbers.
        """
        text = pygame.font.SysFont("Garamond", 24).render("-"+str(self.damage), False, (255,50,50))
        drawSurf.blit(text, (self.player.position[0] + 8, self.damageY))

    def drawWipe(self, drawSurf):
        """
        Draw black over the entire screen.
        Used for smooth fadeouts.
        """
        return
        #pygame.draw.rect(drawSurf, pygame.Color(0,0,0,0), self.background)


    ##  ----------------------------------------------- ##
                    ##  Updating    ##

    def update(self, seconds):
        #   Update Death
        if self.dead:
            return
        
        if self.inGame:
            if self.paused:
                self.pauseImage.update(seconds)
                self.flashTimer += seconds
                if self.flashTimer >= 0.5:
                    self.flashTimer = 0.0
                    if self.flash_alpha == 150:
                        self.flash_alpha = 200
                        self.flash.image.set_alpha(self.flash_alpha)
                    else:
                        self.flash_alpha = 150
                        self.flash.image.set_alpha(self.flash_alpha)
                return
            
            #   Update Player
            self.player.update(seconds)

            #   Update I-frames
            if self.hurting:
                self.iFrames += 1
                self.damageY -= 1
                if self.iFrames == 30:
                    self.iFrames = 0
                    self.hurting = False
                    self.damage = 0
                    self.damageY = 0
            
            #   Update Enemies
            damage = 0
            if self.enemies:
                for e in self.enemies:
                    if e.dead:
                        del self.enemies[self.enemies.index(e)]
                    else:
                       e.update(seconds)
                       #    Check if enemy is attacking the player
                       if e.position[0] <= self.player.position[0] + self.player.getSize()[0]:
                           e.kill()
                           damage = e.getDamage()
                           self.hurt(damage)
                           self.damage = damage

            #   Spawn Enemies
            if not self.spawnReady:
                self.spawnTimer += seconds
                if self.spawnTimer >= 0.0:
                    self.spawnTimer = 0.0
                    self.spawnReady = True

            self.frameCounter += 1
            if not self.sniping and self.upgradeReady and self.frameCounter == 5:
                self.spawnSniper()
            else:
                if self.frameCounter >= self.spawnRate:
                    self.spawn()
            
            #   Update Snipe Timer
            if self.sniping:
                self.snipeTimer -= seconds
                if self.snipeTimer <= 0.0:
                    self.snipeTimer = 10.0
                    self.sniping = False


        