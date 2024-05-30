"""
/********************************************/
/*     Copyrights (C) 2024 CVE_zeroday.     */
/*          All rights reserved.            */
/********************************************/
/*          File Name: CPlayer.py           */
/*   Created by CVE_zeroday on 24.05.2024   */
/*               (T.Y.Kim)                  */
/********************************************/
"""

from collections import deque

from Manager import GameManager
from CCharacter import CCharacter, CCharacterComponent, CCharacterPivot
from WTypes import WPair

from Debug import *

# class defining playable character / head component, this class process input data and move character
class CPlayer(CCharacter):
    
    __len = 1
    __components = []
    __pivots = []

    direction_buf: deque = None
    
    # private
    __prev_coord = None
    __buffer_max_size = 3
    
    isGameOver: bool = True
    
    def __init__(self, _pos: WPair = None, _scale: WPair = None, _coord: WPair = None):
        super().__init__(_pos, _scale, _coord)
        self.__components.append(self)
        self.__pivots.append(self)
        self.objType = 0
        self.__prev_coord = self.coord
        self.direction_buf = deque()
        
        self.isGameOver = False
        
        self.addComponent()
        
        self.debug_CCharacter()

    @debug_func
    def debug_CCharacter(self):
        self.direction_buf.append(WPair(1, 0))

    @debug_func
    def debug_CCharacter_1(self, a):
        if a == 0:
            self.direction_buf.appendleft(WPair(-1, 0))
        elif a == 1:
            self.direction_buf.appendleft(WPair(0, -1))
        elif a == 2:
            self.direction_buf.appendleft(WPair(1, 0))
        elif a == 3:
            self.direction_buf.appendleft(WPair(0, 1))

        if len(self.direction_buf) > 1:
            if self.direction_buf[0] == self.direction_buf[1]:
                self.direction_buf.popleft()

    @property
    def components(self):
        return self.__components
    
    @property
    def pivots(self):
        return self.__pivots
    
    @property
    def getLen(self):
        return self.__len
    
    def addComponent(self):
        component = CCharacterComponent(self, self.__len, self.__components[-1].pos + self.__components[-1].direction * (-1 * self._gameManager.cellSize), self.scale, self.__components[-1].coord + self.direction * -1)
        component.direction = self.__components[-1].direction
        self.__len += 1
        self.__components.append(component)
        
        
    def removeComponent(self, _id):
        self.__components[_id].delete()
        del self.__components[_id]
        
    def addPivot(self, _oldDirection, _newDirection):
        
        if ((_oldDirection == WPair(1, 0) and _newDirection == WPair(0, 1))
            or (_oldDirection == WPair(0, -1) and _newDirection == WPair(-1, 0))):
           _pivotType = 0
        if ((_oldDirection == WPair(0, -1) and _newDirection == WPair(1, 0))
            or (_oldDirection == WPair(-1, 0) and _newDirection == WPair(0, 1))):
            _pivotType = 1
        if ((_oldDirection == WPair(1, 0) and _newDirection == WPair(0, -1))
            or (_oldDirection == WPair(0, 1) and _newDirection == WPair(-1, 0))):
            _pivotType = 2
        if ((_oldDirection == WPair(0, 1) and _newDirection == WPair(1, 0))
            or (_oldDirection == WPair(-1, 0) and _newDirection == WPair(0, -1))):
            _pivotType = 3

        pivot = CCharacterPivot(self, _pivotType, self.pos, self.scale, self.coord)
        if len(self.__pivots) > 1:
            self.__pivots[1].prev = pivot
        self.__pivots.insert(1, pivot)
        
        for component in self.__components[1:]:
            if component.pivot == self:
                component.pivot = pivot

    def removePivot(self):
        self.__pivots[-1].delete()
        del self.__pivots[-1]
        
    def earlyUpdate(self):
        super().earlyUpdate()
    
    def update(self):
        super().update()
        
        while len(self.direction_buf) > self.__buffer_max_size:
            self.direction_buf.pop()

        if self.__prev_coord != self.coord:
            while self.direction_buf:
                _newDirection = self.direction_buf.pop()
                if self.direction != _newDirection:
                    _oldDirection = self.direction
                    self.direction = _newDirection
                    
                    _cellSize = self._gameManager.cellSize
                    self.pos = ((self.pos + _cellSize // 2) // _cellSize) * _cellSize
                    self.addPivot(_oldDirection, _newDirection)
                    break
            

        self.__prev_coord = self.coord
        #print("CPlayer: "+ str(self.pos))
    
    def lateUpdate(self):
        super().lateUpdate()
        print(self.isGameOver)
        self.__setObjImage()
        
    def checkGameOver(self):
        for _object in self._gameManager.objects:
            if _object.objType == 1 and _object.id != 1:
                if _object.coord == self.coord:
                    self.isGameOver = True
                    return
        
        if self.coord[0] < 0 or self.coord[1] < 0:
            self.isGameOver = True
            return
        if self.coord[0] > 64 or self.coord[1] > 36:
            self.isGameOver = True
            return
    
    def delete(self):
        super().delete()
        for component in self.__components:
            del component # free components
    
    def __setObjImage(self):
        if self.direction == WPair(1, 0):
            self._objImage = GameManager.assets["head_right"]
        elif self.direction == WPair(-1, 0):
            self._objImage = GameManager.assets["head_left"]
        elif self.direction == WPair(0, 1):
            self._objImage = GameManager.assets["head_down"]
        elif self.direction == WPair(0, -1):
            self._objImage = GameManager.assets["head_up"]


