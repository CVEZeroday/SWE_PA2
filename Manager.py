"""
/********************************************/
/*     Copyrights (C) 2024 CVE_zeroday.     */
/*          All rights reserved.            */
/********************************************/
/*          File Name: Manager.py           */
/*   Created by CVE_zeroday on 24.05.2024   */
/*               (T.Y.Kim)                  */
/********************************************/

Some code is from 
# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

"""

import json, os, random, pygame
from pygame.locals import *

from WTypes import *

# Singleton
class GameManager:

    local_player = None

    # public
    deltaTime: float = 0.0

    # private
    __instance = None
    
    __fpsClock = None
    __displaySurf = None
    __basicFont = None

    __fps = 360
    __cellSize: int = 0
    __name = ""
    __screenSize = None
    __screenWidth: int = 1920 # screenWidth(1280 : 1920 : 2560 : 3840) = mag_ratio(2:3:4:6) = cell_size(20:30:40:60)
    __screenHeight: int = 1080
    __mag_ratio = 3

    __newTargetInterval = 3000 # milliseconds
    __newTargetRemain = 0
    
    __objects = []
    __targets = []
    
    gameMap = [[0 for i in range(36)] for j in range(64)] # 1: 플레이어 몸통, 2: 플레이어가 향하는 방향 9칸, 3: 먹이
    
    assets = {}

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        # load in memory
        GameManager.assets["target_normal"] = pygame.image.load("assets/target_normal.png")
        GameManager.assets["target_speedUp"] = pygame.image.load("assets/target_speedUp.png")
        GameManager.assets["target_speedDown"] = pygame.image.load("assets/target_speedDown.png")
        GameManager.assets["target_feverTime"] = pygame.image.load("assets/target_feverTime.png")
        GameManager.assets["body_bottomleft"] = pygame.image.load("assets/body_bottomleft.png")
        GameManager.assets["body_bottomright"] = pygame.image.load("assets/body_bottomright.png")
        GameManager.assets["body_horizontal"] = pygame.image.load("assets/body_horizontal.png")
        GameManager.assets["body_topleft"] = pygame.image.load("assets/body_topleft.png")
        GameManager.assets["body_topright"] = pygame.image.load("assets/body_topright.png")
        GameManager.assets["body_vertical"] = pygame.image.load("assets/body_vertical.png")
        GameManager.assets["head_down"] = pygame.image.load("assets/head_down.png")
        GameManager.assets["head_up"] = pygame.image.load("assets/head_up.png")
        GameManager.assets["head_left"] = pygame.image.load("assets/head_left.png")
        GameManager.assets["head_right"] = pygame.image.load("assets/head_right.png")
        GameManager.assets["tail_down"] = pygame.image.load("assets/tail_down.png")
        GameManager.assets["tail_up"] = pygame.image.load("assets/tail_up.png")
        GameManager.assets["tail_left"] = pygame.image.load("assets/tail_left.png")
        GameManager.assets["tail_right"] = pygame.image.load("assets/tail_right.png")

    # public

    def registerObject(self, _object):
        self.__objects.append(_object)

    def removeObject(self, _object):
        self.__objects.remove(_object)

    def createNewTarget(self):
        from TTarget import TNormal, TSpeedUp, TSpeedDown, TFeverTime
        _rnd = random.randint(0, 99)
        if _rnd < 50: # 50%
            TNormal()
            return
        if _rnd < 80: # 30%
            TSpeedUp()
            return
        if _rnd < 95: # 15%
            TSpeedDown()
            return
        TFeverTime() # 5%

    def registerTarget(self, _target):
        self.__targets.append(_target)
        
    def removeTarget(self, _target):
        self.__targets.remove(_target)
    
    def getScreenSize(self):
        return self.__screenSize
    
    def parseOption(self, _option):
        #self.__fps = _option["fps"]
        self.__name = _option["name"]
        self.__screenSize = WPair(_option["screenWidth"], _option["screenHeight"]).toInt()
        self.__screenWidth, self.__screenHeight = self.__screenSize[0], self.__screenSize[1]
        self.__mag_ratio = self.__screenWidth // 640
        self.__cellSize = 10 * self.__mag_ratio
        
    def initPygame(self):
        pygame.init()
        self.__fpsClock = pygame.time.Clock()
        self.__displaySurf = pygame.display.set_mode(self.__screenSize.toTuple())
        self.__basicFont = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('Wormy')

    def beginLoop(self):
        self.__mainLoop()
    
    # private
    def __mainLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.__terminate()
                    if event.key == K_SPACE:
                        for obj in self.__objects:
                            if obj.objType == 0:
                                obj.addComponent()
                    if event.key == K_a:
                        for obj in self.__objects:
                            if obj.objType == 0:
                                obj.debug_CCharacter_1(0)
                    if event.key == K_w:
                        for obj in self.__objects:
                            if obj.objType == 0:
                                obj.debug_CCharacter_1(1)
                    if event.key == K_d:
                        for obj in self.__objects:
                            if obj.objType == 0:
                                obj.debug_CCharacter_1(2)
                    if event.key == K_s:
                        for obj in self.__objects:
                            if obj.objType == 0:
                                obj.debug_CCharacter_1(3)
                    if event.key == K_r:
                        self.local_player.isGameOver = False
                    if event.key == K_q:
                        for obj in self.__objects:
                            if obj.objType == 0:
                                obj.speed -= 1
                    if event.key == K_e:
                        for obj in self.__objects:
                            if obj.objType == 0:
                                obj.speed += 1
                    
                    if event.key == K_z:
                        #for i in range(64):
                            #print(self.gameMap[i])
                        self.createNewTarget()
            
            if self.local_player.isGameOver:
                break

            # ================ debug end ====================

            if self.__newTargetRemain <= 0:
                self.createNewTarget()
                self.__newTargetRemain = self.__newTargetInterval
            self.__newTargetRemain -= self.deltaTime

            for obj in self.__objects:
                if obj.objType == 0:
                    obj.checkGameOver()
            
            for obj in self.__objects:
                obj.earlyUpdate()
            
            for obj in self.__objects:
                obj.update()

            self.__displaySurf.fill(BG_1)
            self.__drawGrid()
            
            for obj in self.__objects:
                obj.lateUpdate()
            
            for obj in self.__objects:
                if obj.drawLayer == 0 and obj.visible:
                    obj.draw(self.__displaySurf)
                    
            for obj in self.__objects:
                if obj.drawLayer == 1 and obj.visible:
                    obj.draw(self.__displaySurf)

            for obj in self.__objects:
                if obj.drawLayer == 2 and obj.visible:
                    obj.draw(self.__displaySurf)
            
            pygame.display.update()
            self.deltaTime = self.__fpsClock.tick(self.__fps)
    
    
    def __terminate(self):
        pygame.quit()
        exit(0)

    def __drawGrid(self):
        for x in range(0, self.__screenWidth, self.__cellSize):  # draw vertical lines
            pygame.draw.line(self.__displaySurf, DARKGRAY, (x, 0), (x, self.__screenHeight))
        for y in range(0, self.__screenHeight, self.__cellSize):  # draw horizontal lines
            pygame.draw.line(self.__displaySurf, DARKGRAY, (0, y), (self.__screenWidth, y))

    @property
    def cellSize(self):
        return self.__cellSize

    @property
    def mag_ratio(self):
        return self.__mag_ratio

    @property
    def objects(self):
        return self.__objects
    
    @property
    def targets(self):
        return self.__targets
    
    """
    def __showStartScreen(self):
        titleFont = pygame.font.Font('freesansbold.ttf', 100)
        titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
        titleSurf2 = titleFont.render('Wormy!', True, GREEN)

        degrees1 = 0
        degrees2 = 0
        while True:
            self.__displaySurf.fill(BLACK)
            rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
            rotatedRect1 = rotatedSurf1.get_rect()
            rotatedRect1.center = (self.__screenWidth / 2, self.__screenHeight / 2)
            self.__displaySurf.blit(rotatedSurf1, rotatedRect1)

            rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
            rotatedRect2 = rotatedSurf2.get_rect()
            rotatedRect2.center = (self.__screenWidth / 2, self.__screenHeight / 2)
            self.__displaySurf.blit(rotatedSurf2, rotatedRect2)

            self.__drawPressKeyMsg()

            if self.__checkForKeyPress():
                pygame.event.get()  # clear event queue
                return
            pygame.display.update()
            self.__fpsClock.tick(self.__fps)
            degrees1 += 3  # rotate by 3 degrees each frame
            degrees2 += 7  # rotate by 7 degrees each frame
    def __drawPressKeyMsg(self):
        pressKeySurf = self.__basicFont.render('Press a key to play.', True, DARKGRAY)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (self.__screenWidth - 200, self.__screenHeight - 30)
        self.__displaySurf.blit(pressKeySurf, pressKeyRect)

    def __checkForKeyPress(self):
        if len(pygame.event.get(QUIT)) > 0:
            self.__terminate()

        keyUpEvents = pygame.event.get(KEYUP)
        if len(keyUpEvents) == 0:
            return None
        if keyUpEvents[0].key == K_ESCAPE:
            self.__terminate()
        return keyUpEvents[0].key
    """
    """
    def __showGameOverScreen(self):
        gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
        gameSurf = gameOverFont.render('Game', True, WHITE)
        overSurf = gameOverFont.render('Over', True, WHITE)
        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()
        gameRect.midtop = (self.__screenWidth / 2, 10)
        overRect.midtop = (self.__screenWidth / 2, gameRect.height + 10 + 25)

        self.__displaySurf.blit(gameSurf, gameRect)
        self.__displaySurf.blit(overSurf, overRect)
        self.__drawPressKeyMsg()
        pygame.display.update()
        pygame.time.wait(500)
        self.__checkForKeyPress()  # clear out any key presses in the event queue

        while True:
            if self.__checkForKeyPress():
                pygame.event.get()  # clear event queue
                return
    """
    
class OptionManager:

    isFirstPlay = True
    
    __option = None
    __ctx = None
    
    def __init__(self, _ctx: GameManager):
        self.__ctx = _ctx
        
        if os.path.isfile('Options.json'):
            self.isFirstPlay = False
            with open('Options.json', 'r') as f:
                self.__option = json.load(f)
        else:
            self.isFirstPlay = True
            with open('Options.json', 'w') as f:
                self.__option = {
                    "fps" : 60,
                    "name": "player" + str(random.randint(100, 999)),
                    "screenWidth" : 1920,
                    "screenHeight" : 1080
                }
                json.dump(self.__option, f, indent = '\t')
        
        self.__ctx.parseOption(self.__option) 
        
    def updateOption(self, key: str, data):
        self.__option[key] = data
        with open('Options.json', 'w') as f:
            json.dump(self.__option, f, indent = '\t')
        
        self.__ctx.parseOption(self.__option)
    
    def getOption(self, key: str):
        return self.__option[key]
    
    def isValidOption(self, key: str, data):
        
        assert key in ("fps", "screenWidth", "name"), 'Invalid key error in OptionManager.isValidOption'
        
        if key == "fps":
            if type(data) != int:
                return False
            if data not in (30, 60, 144, 240):
                return False
            
            return True
        
        if key == "screenWidth":
            if type(data) != int:
                return False
            if data not in (1280, 1920, 2560, 3840):
                return False
            
            return True
        
        if key == "name":
            if len(data) < 2 or len(data) > 10:
                return False
            
            return True