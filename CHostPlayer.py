"""
/********************************************/
/*     Copyrights (C) 2024 CVE_zeroday.     */
/*          All rights reserved.            */
/********************************************/
/*        File Name: CHostPlayer.py         */
/*   Created by CVE_zeroday on 24.05.2024   */
/*               (T.Y.Kim)                  */
/********************************************/
"""

from WTypes import *
from CPlayer import CPlayer

# class defining player who is played by host user
class CHostPlayer(CPlayer):
    def __init__(self, _pos: WPair, _scale: WPair, _coord: WPair = None):
       super().__init__(_pos, _scale, _coord)
