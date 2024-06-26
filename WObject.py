"""
/********************************************/
/*     Copyrights (C) 2024 CVE_zeroday.     */
/*          All rights reserved.            */
/********************************************/
/*         File Name: WObject.py            */
/*   Created by CVE_zeroday on 24.05.2024   */
/*               (T.Y.Kim)                  */
/********************************************/
"""

import pygame

from WTypes import WPair

class WObject:
    
    # public
    pos = None
    coord = None
    scale = None
     
    objType = -1 # objType 0: playerHead, 1: playerBody, 2: playerBodyPivot, 3: normal target, 4: speedUp, 5: speedDown, 6: fever time

    objId: int = 0

    drawLayer = 0 # 클수록 위에 그려짐. 0, 1, 2
    visible: bool = True
    
    # protected
    _gameManager = None
    _objImage = None
    _objImageSize = None
    
    
    def __init__(self, _pos: WPair = None, _scale: WPair = None, _coord: WPair = None):
        from Manager import GameManager
        self._gameManager = GameManager()

        if _pos is not None:
            self.pos = _pos
        else:
            self.pos = WPair(0, 0)
       
        if _scale is not None:
            self.scale = _scale
        else:
            self.scale = WPair(1, 1)
        
        if _coord is not None:
            self.coord = _coord
        else:
           self.coord = WPair(0, 0)
       
        self.objId = WObject.objId
        WObject.objId += 1
       
        self._objImage = pygame.image.load("./assets/target_speedUp.png")
        self._objImageSize = (WPair(self._objImage.get_width(), self._objImage.get_height()).normalize() * self.scale *
                              (10 * self._gameManager.mag_ratio))
        self._objImage = pygame.transform.scale(self._objImage, self._objImageSize.toTuple())
        
        self._gameManager.registerObject(self)

    # public
    def draw(self, _displaySurf: pygame.Surface):
        self._objImageSize = (WPair(self._objImage.get_width(), self._objImage.get_height()).normalize() * self.scale *
                              (10 * self._gameManager.mag_ratio))
        self._objImage = pygame.transform.scale(self._objImage, self._objImageSize.toTuple())
        _displaySurf.blit(self._objImage, self.pos.toTuple())
    
    def updateImageSize(self):
        self._objImageSize = (WPair(self._objImage.get_width(), self._objImage.get_height()).normalize() * self.scale *
                              (10 * self._gameManager.mag_ratio))
    
    def earlyUpdate(self):
        pass
    
    def update(self):
        pass
    
    def lateUpdate(self):
        pass
    
    def delete(self):
        self._gameManager.removeObject(self)
        del self