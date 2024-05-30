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

from WTypes import *
from WObject import WObject

class TTarget(WObject):
    
    # private
    __targetType: int = 0
    
    def __init__(self):
        super().__init__()
        self._gameManager.registerTarget(self)
        self.__setInitialPosition()
        
    def __setInitialPosition(self):
        self.pos = WPair

class TSpeedup(TTarget):
    def __init__(self):
        super().__init__()
        self.objType = 3

class TSpeedDown(TTarget):
    def __init__(self):
        super().__init__()
        self.objType = 4

class TFeverTime(TTarget):
    def __init__(self):
        super().__init__()
        self.objType = 5
