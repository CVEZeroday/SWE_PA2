"""
/********************************************/
/*     Copyrights (C) 2024 CVE_zeroday.     */
/*          All rights reserved.            */
/********************************************/
/*        File Name: Controller.py          */
/*   Created by CVE_zeroday on 25.05.2024   */
/*               (T.Y.Kim)                  */
/********************************************/
"""

import random

from WTypes import *

class Controller:
    
    # public
    puppet = None
    isGameOver: bool = False
    controllerType = None # Single: 0, Host: 1, Network: 2, AI: 3
    
    name = ''
    uid = 0
    
    # protected
    _gameManager = None
    
    def __init__(self):
        from Manager import GameManager
        self._gameManager = GameManager()
    
    # public
    def spawn(self):
        from CPlayer import CPlayer
        _ret = self.__setInitialPosition()
        self.puppet = CPlayer(_pos = _ret[0], _coord = _ret[1], _direction = _ret[2])
        self.puppet.controller = self
        self.isGameOver = False

    def controllerUpdate(self, _events):
        pass

    def getDirection(self):
        pass

    # private
    def __setInitialPosition(self):
        zero_indices = [(i, j) for i, row in enumerate(self._gameManager.gameMap) for j, value in enumerate(row) if value == 0]

        if zero_indices:
            _tmp = random.choice(zero_indices)
            _coord = WPair(_tmp[0], _tmp[1])
            _pos = _coord * self._gameManager.cellSize
        else:
            _coord = WPair(0, 0)
            _pos = _coord * self._gameManager.cellSize
        
        if _coord[0] < 32:
            _direction = WPair(1, 0)
        else:
            _direction = WPair(-1, 0)
        
        return _pos, _coord, _direction

class AIController(Controller):
    
    # private
    __context = 0 # 0: 먹이, 1: 공격, 2: 회피

    __min_target_dist = None
    __min_target_coord = None
    
    __min_player_dist = None
    __min_player_coord = None
    __target_player_head = None
    
    __prev_coord = None
    __delay = 500 # 0.5초 후 ai 작동 시작
    
    def __init__(self):
        super().__init__()
        self.controllerType = 3
        self.name = "Bot " + str(random.randint(100, 999))
        self.spawn()
        self.__prev_coord = self.puppet.coord
        
    # public
    def controllerUpdate(self, _events):
        
        if self.__delay > 0:
            self.__delay -= self._gameManager.deltaTime
            return
        else:
            self.__delay = 0
        
        super().controllerUpdate(_events)
        if self.isGameOver:
            self.__delay = 500
            self.spawn()
            return
        self.__processContext()
    
    def getDirection(self):
        
        if self.__delay > 0:
            return
        
        super().getDirection()
        _tmp = self.__processOutput()
        if _tmp != self.puppet.direction:
            self.puppet.move(_tmp)

    # private
    def __processContext(self):
        # context setting
        self.__min_target_dist = 100
        self.__min_target_coord = None
        for _target in self._gameManager.targets:
            _tmp = self.puppet.coord.distance(_target.coord)
            if _tmp < self.__min_target_dist:
                self.__min_target_dist = _tmp
                self.__min_target_coord = _target.coord
        
        self.__min_player_dist = 100
        self.__min_player_coord = None
        for controller in self._gameManager.controllers:
            if controller == self:
                continue
            _tmp = self.puppet.coord.distance(controller.puppet.coord)
            if _tmp < self.__min_player_dist:
                self.__min_player_dist = _tmp
                self.__min_player_coord = controller.puppet.coord
                self.__target_player_head = controller.puppet

        if self.__min_player_coord is None:
            self.__context = 0
            return
        
        if self.__min_target_coord is None:
            self.__context = 1
        elif self.__min_target_dist <= 2:
            self.__context = 0
        elif self.__min_player_dist <= 10:
            if self.__target_player_head.speed > self.puppet.speed:
                self.__context = 2
            elif self.__target_player_head.speed == self.puppet.speed:
                if self.__min_player_dist <= 5:
                    self.__context = 2
                else:
                    self.__context = 0
            else:
                self.__context = 1
        else:
            self.__context = 0
    
    def __processOutput(self):
        if self.__context == 0:
            return self.__directionToward(self.__min_target_coord)
        elif self.__context == 1:
            return self.__directionToward(self.__min_player_coord + self.__target_player_head.direction * 3)
        elif self.__context == 2:
            return self.__directionFrom(self.__min_player_coord)
    
    def __directionToward(self, _target_coord):
        _curr = self.puppet.coord
        _available = []
        for _direction in (WPair(1, 0), WPair(-1, 0), WPair(0, 1), WPair(0, -1)):
            _tmp = _curr + _direction
            if 0 <= _tmp[0] <= 63 and 0 <= _tmp[1] <= 35:
                if self._gameManager.gameMap[_tmp[0]][_tmp[1]] != 1:
                    _available.append(_direction)
        
        _min_direction = WPair(1, 0)
        _min_distance = 100
        for _direction in _available:
            _tmp = _curr + _direction
            _tmp_dist = _tmp.distance(_target_coord)
            if _tmp_dist < _min_distance:
                _min_distance = _tmp_dist
                _min_direction = _direction
        
        return _min_direction

    def __directionFrom(self, _target_coord):
        _curr = self.puppet.coord
        _available = []
        for _direction in (WPair(1, 0), WPair(-1, 0), WPair(0, 1), WPair(0, -1)):
            _tmp = _curr + _direction
            if 0 <= _tmp[0] <= 63 and 0 <= _tmp[1] <= 35:
                if self._gameManager.gameMap[_tmp[0]][_tmp[1]] != 1:
                    _available.append(_direction)

        _max_direction = WPair(1, 0)
        _max_distance = 0
        for _direction in _available:
            _tmp = _curr + _direction
            _tmp_dist = _tmp.distance(_target_coord)
            if _tmp_dist > _max_distance:
                _max_distance = _tmp_dist
                _max_direction = _direction

        return _max_direction

class SingleController(Controller):
    def __init__(self):
        super().__init__()
        self.controllerType = 0
        self.spawn()

    # public
    def spawn(self):
        super().spawn()
        self._gameManager.local_player = self.puppet

    def controllerUpdate(self, _events):
        super().controllerUpdate(_events)

        for event in _events:
            if event.type == KEYDOWN:
                if event.key in KEY_LEFT:
                    self.puppet.move(WPair(-1, 0))
                if event.key in KEY_UP:
                    self.puppet.move(WPair(0, -1))
                if event.key in KEY_RIGHT:
                    self.puppet.move(WPair(1, 0))
                if event.key in KEY_DOWN:
                    self.puppet.move(WPair(0, 1))
                if event.key in KEY_RESURRECT:
                    if self.isGameOver:
                        self.spawn()


"""
!!! NOT IMPLEMENTED YET !!!
"""
class HostController(Controller):
    def __init__(self):
        super().__init__()
        self.controllerType = 1

class NetworkController(Controller):
    def __init__(self):
        super().__init__()
        self.controllerType = 2
        
    def controllerUpdate(self, _events):
        super().controllerUpdate(_events)
        for event in _events:
            if event.type == KEYDOWN:
                if event.key in KEY_LEFT:
                    pass
                if event.key in KEY_UP:
                    pass
                if event.key in KEY_RIGHT:
                    pass
                if event.key in KEY_DOWN:
                    pass
