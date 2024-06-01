"""
/********************************************/
/*     Copyrights (C) 2024 CVE_zeroday.     */
/*          All rights reserved.            */
/********************************************/
/*         File Name: TTarget.py            */
/*   Created by CVE_zeroday on 24.05.2024   */
/*               (T.Y.Kim)                  */
/********************************************/
"""

import random
from WTypes import *
from WObject import WObject

class TTarget(WObject):
    
    # private
    __targetType: int = 0
    
    def __init__(self):
        super().__init__()
        self._gameManager.registerTarget(self)
        self.__setInitialPosition()

        self._gameManager.gameMap[self.coord[0]][self.coord[1]] = 3
        self.drawLayer = 0
        
    def __setInitialPosition(self):
        zero_indices = [(i, j) for i, row in enumerate(self._gameManager.gameMap) for j, value in enumerate(row) if value == 0]

        if zero_indices:
            _tmp = random.choice(zero_indices)
            self.coord = WPair(_tmp[0], _tmp[1])
            self.pos = self.coord * self._gameManager.cellSize

    def delete(self):
        super().delete()
        self._gameManager.removeTarget(self)
        self._gameManager.gameMap[self.coord[0]][self.coord[1]] = 0


class TNormal(TTarget):
    def __init__(self):
        super().__init__()
        self.objType = 3

        self._objImage = self._gameManager.assets["target_normal"]

class TSpeedUp(TTarget):
    def __init__(self):
        super().__init__()
        self.objType = 4

        self._objImage = self._gameManager.assets["target_speedUp"]

class TSpeedDown(TTarget):
    def __init__(self):
        super().__init__()
        self.objType = 5

        self._objImage = self._gameManager.assets["target_speedDown"]

class TFeverTime(TTarget):
    def __init__(self):
        super().__init__()
        self.objType = 6

        self._objImage = self._gameManager.assets["target_feverTime"]
