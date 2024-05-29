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

class Controller:
    
    target = None
    def __init__(self, target):
        self.target = target

class AIController(Controller):
    def __init__(self, target):
        super().__init__(target)

class NetworkController(Controller):
    def __init__(self, target):
        super().__init__(target)