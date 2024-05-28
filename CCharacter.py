"""
/********************************************/
/*     Copyrights (C) 2024 CVE_zeroday.     */
/*          All rights reserved.            */
/********************************************/
/*        File Name: CCharacter.py          */
/*   Created by CVE_zeroday on 24.05.2024   */
/*               (T.Y.Kim)                  */
/********************************************/
"""

from Manager import GameManager
from WObject import WObject
from WTypes import *


# class defining character, this class implements moving mechanism of object
class CCharacter(WObject):
    
    # public
    id: int = 0
    direction: WPair = None
    speed = 8 # coord/s
    
    def __init__(self, _pos: WPair = None, _scale: WPair = None, _coord: WPair = None):
        super().__init__(_pos, _scale, _coord)
        self.direction = WPair(1, 0)
    
    # public
    # TODO: 부드럽게 이동하는거 구현
    
    def earlyUpdate(self):
        super().earlyUpdate()
        if self.direction[0] > 0 or self.direction[1] > 0:
            self.coord = self.pos.round() // self._gameManager.cellSize
        if self.direction[0] < 0 or self.direction[1] < 0:
            self.coord = (self.pos.round() - self.direction * self._gameManager.cellSize) // self._gameManager.cellSize
        # coord는 object 전체가 이동을 완료하면 바뀜
        
    def update(self):
        super().update()
        
    def lateUpdate(self):
        super().lateUpdate()
        self.pos = self.pos + (self.direction * (self._gameManager.deltaTime * 0.001 * self.speed * self._gameManager.cellSize))
        #print("pos: {}".format(str(self.pos)))

# class defining body components
class CCharacterComponent(CCharacter):
    
    # public
    head = None
    id: int = -1 # component id
    
    pivot = None # CCharacterComponent or CPlayer
    
    def __init__(self, _head, _id: int, _pos: WPair, _scale: WPair, _coord: WPair):
        assert _id >= 1, "Unknown error on CCharacterComponent.__init__: id of CCharacterComponent is 0"
        super().__init__(_pos, _scale, _coord)
        self.head = _head
        self.id = _id
        self.pivot = self.head.pivots[-1]
        self.objType = 1
        
        #print("_pos: " + str(_pos) + "pos of __prev: " + str(self.__prev.pos))
    
    def earlyUpdate(self):
        super().earlyUpdate()
        
    def update(self):
        #print(self.coord)
        super().update()
        if self.coord == self.pivot.coord:
            if self.pivot != self.head:
                self.pivot = self.pivot.prev
                self.direction = (self.pivot.pos - self.pos).normalize2()
                
                _tmp = self._gameManager.cellSize
                self.pos = ((self.pos + _tmp // 2) // _tmp) * _tmp
                
                if self.head.getLen - 1 == self.id: # if CCharacterComponent is tail
                    self.head.removePivot() # remove last pivot
                
        self.speed = self.head.speed
        
        #print(self.head.pos - self.pos)
        #print("component: " + str(self.pos))
    def lateUpdate(self):
        super().lateUpdate()
        if self.head.components[self.id - 1].direction == self.direction:
            _tmp = self.head.components[self.id - 1].pos - self.pos
            if (_tmp[0] == 0 or _tmp[1] == 0) and _tmp != self.direction * self._gameManager.cellSize:
                self.pos = self.head.components[self.id - 1].pos - (self.direction * self._gameManager.cellSize)
        self.__setObjImage()
        
    def __setObjImage(self):
        if self.head.getLen - 1 == self.id:
            if self.direction == WPair(1, 0):
                self._objImage = GameManager.assets["tail_left"]
            elif self.direction == WPair(-1, 0):
                self._objImage = GameManager.assets["tail_right"]
            elif self.direction == WPair(0, 1):
                self._objImage = GameManager.assets["tail_up"]
            elif self.direction == WPair(0, -1):
                self._objImage = GameManager.assets["tail_down"]
        else:
            if self.direction[1] == 0:
                self._objImage = GameManager.assets["body_horizontal"]
            elif self.direction[0] == 0:
                self._objImage = GameManager.assets["body_vertical"]
            
class CCharacterPivot(WObject):
    
    # public
    head = None
    prev = None
    
    __pivotType = -1 # 0 : bottom-left, 1 : bottom-right, 2 : top-left, 3 : top-right
    
    def __init__(self, _head, _pivotType: int, _pos: WPair = None, _scale: WPair = None, _coord: WPair = None):
        super().__init__(_pos, _scale, _coord)
        self.head = _head
        self.__pivotType = _pivotType
        self.objType = 2
        self.prev = self.head
        #print("pivot: " + str(self.coord))
        
        self.drawLayer += 1
        
        if self.__pivotType == 0:
            self._objImage = GameManager.assets["body_bottomleft"]
        elif self.__pivotType == 1:
            self._objImage = GameManager.assets["body_bottomright"]
        elif self.__pivotType == 2:
            self._objImage = GameManager.assets["body_topleft"]
        elif self.__pivotType == 3:
            self._objImage = GameManager.assets["body_topright"]
        
    def lateUpdate(self):
        super().lateUpdate()