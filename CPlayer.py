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
from WTypes import *

from Debug import *

# class defining playable character / head component, this class process input data and move character
class CPlayer(CCharacter):
    
    # public
    direction_buf: deque = None
    controller = None
    
    # private
    __len = 1
    __components = None
    __pivots = None
    
    __buffer_max_size = 3

    __feverTimeSpeed = 4
    __feverTimeMaxLength = 7000 # milliseconds
    __feverTimeRemain = 0
    
    __baseSpeed = None
    
    __halfTarget = 0

    def __init__(self, _pos: WPair = None, _scale: WPair = None, _coord: WPair = None, _direction: WPair = None):
        super().__init__(_pos, _scale, _coord)
        if _direction is not None:
            self.direction = _direction 
        self.__components = []
        self.__pivots = []
        self.__components.append(self)
        self.__pivots.append(self)
        self.objType = 0
        self.direction_buf = deque()
        self.drawLayer = 1
        self.__baseSpeed = self.speed
        self.addComponent()
        self.debug_CCharacter()

    # public
    def move(self, _direction):
        self.direction_buf.appendleft(_direction)
        if len(self.direction_buf) > 1:
            if self.direction_buf[0] == self.direction_buf[1]:
                self.direction_buf.popleft()
    
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
        
        self.__updateFeverTime()
        self.__checkAndUpdateDirection()
        
        self._prev_coord = self.coord
    
    def lateUpdate(self):
        super().lateUpdate()
        self.__checkTarget()
        self.__setObjImage()
        
    def gameOver(self):
        self.controller.isGameOver = True
        self.delete()
    
    def checkGameOver(self):
        for _controller in self._gameManager.controllers: # 타인과의 충돌 검사
            if _controller == self.controller:
                continue
            for _component in _controller.puppet.components:
                if _component.coord == self.coord:
                    if _component.id == 0: # 머리끼리 충돌하면 더 짧은 쪽이 죽음 (같으면 둘다 죽음)
                        if _component.getLen < self.__len:
                            _controller.puppet.gameOver()
                        elif _component.getLen > self.__len:
                            self.gameOver()
                        else:
                            _controller.puppet.gameOver()
                            self.gameOver()
                    else:
                        self.gameOver()
                    return
        
        for _component in self.__components[1:]: # 자신과의 충돌 검사
            if _component.coord == self.coord and _component.id != 1:
                self.gameOver()
                return
        
        if self.coord[0] < 0 or self.coord[1] < 0:
            self.gameOver()
            return
        if self.coord[0] > 63 or self.coord[1] > 35:
            self.gameOver()
            return
    
    def delete(self):
        for component in self.__components[1:]:
            component.delete()
        for pivot in self.__pivots[1:]:
            pivot.delete()
        super().delete()
    
    # private
    def __setObjImage(self):
        if self.direction == WPair(1, 0):
            self._objImage = GameManager.assets["head_right"]
        elif self.direction == WPair(-1, 0):
            self._objImage = GameManager.assets["head_left"]
        elif self.direction == WPair(0, 1):
            self._objImage = GameManager.assets["head_down"]
        elif self.direction == WPair(0, -1):
            self._objImage = GameManager.assets["head_up"]
    
    def __checkTarget(self):
        for target in self._gameManager.targets:
            if target.coord == self.coord:
                target.delete()
                if target.objType == 7:
                    if self.__feverTimeRemain > 0:
                        self.__halfTarget += 2
                    else:
                        self.__halfTarget += 1
                    if self.__halfTarget % 2 == 0:
                        self.addComponent()
                else:
                    self.addComponent()
                    if self.__feverTimeRemain > 0:
                        self.addComponent()

                if target.objType == 4:
                    if self.__baseSpeed <= 14: # 최대속도 16
                        self.__baseSpeed += 2
                elif target.objType == 5:
                    if self.__baseSpeed >= 8: # 최저속도 6
                        self.__baseSpeed -= 2
                elif target.objType == 6:
                    self.__feverTimeRemain = self.__feverTimeMaxLength
    
    def __updateFeverTime(self):
        if self.__feverTimeRemain > 0:
            self.speed = self.__baseSpeed + self.__feverTimeSpeed
            self.__feverTimeRemain -= self._gameManager.deltaTime
        else:
            self.speed = self.__baseSpeed
            self.__feverTimeRemain = 0
            
    def __checkAndUpdateDirection(self):
        while len(self.direction_buf) > self.__buffer_max_size:
            self.direction_buf.pop()

        if self._prev_coord != self.coord:
            
            self.controller.getDirection()

            while self.direction_buf:
                _newDirection = self.direction_buf.pop()
                if self.direction != _newDirection and self.direction * -1 != _newDirection:
                    _oldDirection = self.direction
                    self.direction = _newDirection

                    _cellSize = self._gameManager.cellSize
                    self.pos = ((self.pos + _cellSize // 2) // _cellSize) * _cellSize
                    self.addPivot(_oldDirection, _newDirection)

                    for i in range(1, 10):
                        _tmp = self._prev_coord + _oldDirection * i
                        if _tmp[0] > 63 or _tmp[0] < 0 or _tmp[1] > 35 or _tmp[1] < 0:
                            break
                        self._gameManager.gameMap[_tmp[0]][_tmp[1]] = 0

                    break

            if 63 >= self.coord[0] >= 0 and 35 >= self.coord[1] >= 0:
                self._gameManager.gameMap[self.coord[0]][self.coord[1]] = 1
            for i in range(1, 10): # 머리 포함 10칸 스폰 금지
                _tmp = (self.coord + self.direction * i).toInt()
                if _tmp[0] > 63 or _tmp[0] < 0 or _tmp[1] > 35 or _tmp[1] < 0:
                    break
                self._gameManager.gameMap[_tmp[0]][_tmp[1]] = 2

    @property
    def components(self):
        return self.__components

    @property
    def pivots(self):
        return self.__pivots

    @property
    def getLen(self):
        return self.__len

    @property
    def isFeverTime(self):
        return self.__feverTimeRemain > 0
    
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
