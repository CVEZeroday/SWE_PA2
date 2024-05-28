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

from Manager import GameManager
from WTypes import WPair

class WObject:
    pos = None
    coord = None
    scale = None
     
    objType = -1 # objType 0: playerHead, 1: playerBody, 2: playerBodyPivot 3: speedUp, 4: speedDown, 5: fever time, 6: wormhole entry, 7: wormhole exit

    drawLayer = 0 # 클수록 위에 그려짐. 0, 1, 2
    
    # protected
    _gameManager = GameManager()
    _objImage = None
    _objImageSize = None
    
    
    def __init__(self, _pos: WPair = None, _scale: WPair = None, _coord: WPair = None):
       
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
       
        self._objImage = pygame.image.load("./assets/apple.png")
        self._objImageSize = (WPair(self._objImage.get_width(), self._objImage.get_height()).normalize() * self.scale *
                              (10 * self._gameManager.mag_ratio))
        self._objImage = pygame.transform.scale(self._objImage, self._objImageSize.toTuple())
        
        #print(WPair(self._objImage.get_width(), self._objImage.get_height()))
        
        self._gameManager.registerObject(self)

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