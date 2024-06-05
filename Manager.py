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

from Controller import *
from TTarget import THalf
from WTypes import *

# Singleton
class GameManager:

    # public
    local_player = None
    deltaTime: float = 0.0
    loopCount = 0
    gameMap = [[0 for i in range(36)] for j in range(64)] # 1: 플레이어 몸통, 2: 플레이어가 향하는 방향 9칸, 3: 먹이
    assets = {}
    
    # private
    __instance = None
    
    __fpsClock = None
    __displaySurf = None
    __basicFont = None
    __nameFont = None

    __fps = 360
    __cellSize: int = 0
    __name = ""
    __screenSize = None
    __screenWidth: int = 1920 # screenWidth(1280 : 1920 : 2560 : 3840) = mag_ratio(2:3:4:6) = cell_size(20:30:40:60)
    __screenHeight: int = 1080
    __mag_ratio = 3

    __newTargetInterval = 2000 # milliseconds
    __newTargetRemain = 0
    
    __objects = []
    __targets = []
    __controllers = []

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        # load in memory
        GameManager.assets["target_normal"] = pygame.image.load("assets/target_normal.png")
        GameManager.assets["target_half"] = pygame.image.load("assets/target_half.png")
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

    def createNewTarget(self, _type = None, _coord = None):
        from TTarget import TNormal, TSpeedUp, TSpeedDown, TFeverTime
        
        if _coord is not None:
            if _coord[0] < 0 or _coord[0] > 63 or _coord[1] < 0 or _coord[1] > 35:
                return
            _pos = _coord * self.__cellSize
        else:
            _pos = None
            
        if _type is not None:
            if _type == 0:
                TNormal(_coord = _coord, _pos = _pos)
            elif _type == 1:
                TSpeedUp(_coord = _coord, _pos = _pos)
            elif _type == 2:
                TSpeedDown(_coord = _coord, _pos = _pos)
            elif _type == 3:
                TFeverTime(_coord = _coord, _pos = _pos)
            elif _type == 4:
                THalf(_coord = _coord, _pos = _pos)
            return
        
        _rnd = random.randint(0, 99)
        if _rnd < 10:
            THalf(_coord = _coord, _pos = _pos)
            return
        if _rnd < 50: # 40%
            TNormal(_coord = _coord, _pos = _pos)
            return
        if _rnd < 80: # 30%
            TSpeedUp(_coord = _coord, _pos = _pos)
            return
        if _rnd < 95: # 15%
            TSpeedDown(_coord = _coord, _pos = _pos)
            return
        TFeverTime(_coord = _coord, _pos = _pos) # 5%

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
        self.__nameFont = pygame.font.Font('freesansbold.ttf', 8 * self.__mag_ratio)
        self.__basicFont = pygame.font.Font('freesansbold.ttf', 9 * self.__mag_ratio)
        pygame.display.set_caption('Wormy by T.Y.KIM')

    def beginLoop(self):
        _controller = SingleController()
        _controller.name = self.__name
        self.__controllers.append(_controller)
        self.__controllers.append(AIController())
        #self.__controllers.append(AIController())
        #self.__controllers.append(AIController())
        self.__mainLoop()
    
    # private
    def __mainLoop(self):
        while True:
            _events = pygame.event.get()
            for event in _events:
                if event.type == QUIT:
                    self.__terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.__terminate()
                        
            self.loopCount += 1

            if self.__newTargetRemain <= 0 and len(self.__targets) < 30:
                self.createNewTarget()
                self.__newTargetRemain = self.__newTargetInterval
            self.__newTargetRemain -= self.deltaTime

            for controller in self.__controllers:
                controller.controllerUpdate(_events)

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
                if obj.drawLayer == 0:
                    obj.draw(self.__displaySurf)
                    
            for obj in self.__objects:
                if obj.drawLayer == 1:
                    obj.draw(self.__displaySurf)

            for obj in self.__objects:
                if obj.drawLayer == 2:
                    obj.draw(self.__displaySurf)

            self.__drawName()
            self.__drawUI()
            
            if self.local_player.controller.isGameOver:
                self.__showGameOverScreen()
            
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
    
    def __showGameOverScreen(self):
        gameOverFont = pygame.font.Font('freesansbold.ttf', 75 * self.__mag_ratio)
        gameSurf = gameOverFont.render('Game', True, RED)
        overSurf = gameOverFont.render('Over', True, RED)
        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()
        gameRect.midtop = (self.__screenWidth / 2, 5 * self.mag_ratio)
        overRect.midtop = (self.__screenWidth / 2, gameRect.height + 20 * self.__mag_ratio)

        self.__displaySurf.blit(gameSurf, gameRect)
        self.__displaySurf.blit(overSurf, overRect)
        self.__drawPressKeyMsg()

    def __drawPressKeyMsg(self):
        pressKeySurf = self.__basicFont.render('Press SPACE to resurrect.', True, DARKGRAY)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (self.__screenWidth / 2 - 120, self.__screenHeight / 2)
        self.__displaySurf.blit(pressKeySurf, pressKeyRect)
    
    def __drawUI(self):
        i = 0
        for controller in self.__controllers:
            _str = "Name: " + controller.name + ", Length: " + str(controller.puppet.getLen) + ", Speed: " + str(controller.puppet.speed)
            if controller.puppet.isFeverTime:
                _str += ", FEVER TIME!"
        
            UISurf = self.__basicFont.render(_str, True, WHITE)
            UIRect = UISurf.get_rect()
            UIRect.topleft = (10 * self.__mag_ratio, 10 * self.__mag_ratio + i * 10 * self.__mag_ratio)
            i += 1
            BgRect = pygame.Rect(UIRect.left - 5 * self.__mag_ratio, UIRect.top, UIRect.width + 10 * self.__mag_ratio, UIRect.height)
            self.__drawRectAlpha(self.__displaySurf, (0, 0, 0, 128), BgRect)
            self.__displaySurf.blit(UISurf, UIRect)
    
    def __drawName(self):
        for controller in self.__controllers:
            if controller.puppet == self.local_player:
                color = GREEN
            else:
                color = WHITE
            UISurf = self.__nameFont.render(controller.name, True, color)
            UIRect = UISurf.get_rect()
            UIRect.center = (controller.puppet.pos + WPair(self.__cellSize // 2, -8 * self.__mag_ratio)).toTuple()
            BgRect = pygame.Rect(UIRect.left - 2 * self.__mag_ratio, UIRect.top, UIRect.width + 4 * self.__mag_ratio, UIRect.height)
            self.__drawRectAlpha(self.__displaySurf, (0, 0, 0, 64), BgRect)
            self.__displaySurf.blit(UISurf, UIRect)
    
    def __drawRectAlpha(self, surface, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)

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

    @property
    def controllers(self):
        return self.__controllers
    
class OptionManager:

    # public
    isFirstPlay = True
    
    # private
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
                    "name": "Player" + str(random.randint(100, 999)),
                    "screenWidth" : 1920,
                    "screenHeight" : 1080
                }
                json.dump(self.__option, f, indent = '\t')
        
        self.__ctx.parseOption(self.__option) 
    
    # public
    def updateOption(self, key: str, data):
        self.__option[key] = data
        with open('Options.json', 'w') as f:
            json.dump(self.__option, f, indent = '\t')
        
        self.__ctx.parseOption(self.__option)
    
    def getOption(self, key: str):
        return self.__option[key]
    
    def isValidOption(self, key: str, data):
        
        assert key in ("screenWidth", "name"), 'Invalid key error in OptionManager.isValidOption'
        
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