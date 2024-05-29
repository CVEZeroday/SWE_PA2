"""
/********************************************/
/*     Copyrights (C) 2024 CVE_zeroday.     */
/*          All rights reserved.            */
/********************************************/
/*      File Name: CClientPlayer.py         */
/*   Created by CVE_zeroday on 28.05.2024   */
/*               (T.Y.Kim)                  */
/********************************************/
"""

from WTypes import *
from CPlayer import CPlayer

# class defining player who is not played by host user
class CClientPlayer(CPlayer):
    def __init__(self, _pos: WPair = None, _scale: WPair = None, _coord: WPair = None):
        super().__init__(_pos, _scale, _coord)