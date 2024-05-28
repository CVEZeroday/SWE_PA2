"""
/********************************************/
/*     Copyrights (C) 2024 CVE_zeroday.     */
/*          All rights reserved.            */
/********************************************/
/*           File Name: main.py             */
/*   Created by CVE_zeroday on 24.05.2024   */
/*               (T.Y.Kim)                  */
/********************************************/
"""
from Debug import *

from WTypes import WPair
from Manager import OptionManager, GameManager
from CPlayer import CPlayer

def main():
    gameManager = GameManager()
    optionManager = OptionManager(gameManager)
    
    if optionManager.isFirstPlay:
        print("게임 초기 설정을 시작합니다.\n아무 값도 입력하지 않거나 잘못된 형식이 입력된 경우 기본값으로 설정됩니다.\n")
        
        _input = input("FPS 값을 입력해주세요 (30, 60, 144, 240 중 입력, 기본값 60): ")
        if _input.isdecimal():
            _input = int(_input)
        
        if optionManager.isValidOption("fps", _input):
            optionManager.updateOption("fps", _input)
        else:
            print("잘못된 값이 입력되었습니다. 기본값으로 설정됩니다.")
        print("FPS값이 {}으로 설정되었습니다.\n".format(optionManager.getOption("fps")))
        
        _input = input("화면의 가로 크기 값을 입력해주세요. 비율은 16:9로 고정됩니다. (1280, 1920, 2560, 3840 중 입력, 기본값 1920): ") 
        if _input.isdecimal():
            _input = int(_input)
        
        if optionManager.isValidOption("screenWidth", _input):
            optionManager.updateOption("screenWidth", _input)
            optionManager.updateOption("screenHeight", _input * 9 / 16)
        else:
            print("잘못된 값이 입력되었습니다. 기본값으로 설정됩니다.")
        print("화면의 가로 크기 값이 {}으로 설정되었습니다.\n".format(optionManager.getOption("screenWidth")))

        _input = input("사용할 닉네임을 입력해주세요. (길이는 2~10자, 기본값 {}): ".format(optionManager.getOption("name")))
        if optionManager.isValidOption("name", _input):
            optionManager.updateOption("name", _input)
        else:
            print("잘못된 값이 입력되었습니다. 기본값으로 설정됩니다.")
        print("닉네임이 {}으로 설정되었습니다.\n".format(optionManager.getOption("name")))
    else:
        _input = input("게임을 시작하시려면 0을, 설정을 변경하시려면 1을 입력해주세요: ")
        if _input.isdecimal():
            _input = int(_input)
        else:
            _input = 0
            
        if _input == 1:
            while True:
                _input = input("변경할 설정을 골라주세요 (1: FPS, 2: 화면 가로 크기, 3: 닉네임, 4: 게임 시작): ")                
                if _input.isdecimal():
                    _input = int(_input)
                else:
                    _input = -1
                    
                if _input == 1:
                    while True:
                        _tmp = input("변경할 FPS값을 입력해주세요 (30, 60, 144, 240 중 입력): ")
                        if _tmp.isdecimal():
                            _tmp = int(_tmp)
                        
                        if optionManager.isValidOption("fps", _tmp):
                            optionManager.updateOption("fps", _tmp)
                            print("FPS값이 {}으로 설정되었습니다.\n".format(optionManager.getOption("fps")))
                            break
                        print("올바른 값을 입력해주세요.\n")
                elif _input == 2:
                    while True:
                        _tmp = input("변경할 화면 가로 크기 값을 입력해주세요 (1280, 1920, 2560, 3840 중 입력) : ")
                        if _tmp.isdecimal():
                            _tmp = int(_tmp)
                        if optionManager.isValidOption("screenWidth", _tmp):
                            optionManager.updateOption("screenWidth", _tmp)
                            optionManager.updateOption("screenHeight", _tmp * 9 / 16)
                            print("화면 가로 크기 값이 {}으로 설정되었습니다.\n".format(optionManager.getOption("screenWidth")))
                            break
                        print("올바른 값을 입력해주세요.\n")
                elif _input == 3:
                    while True:
                        _tmp = input("변경할 닉네임을 입력해주세요: ")
                        if optionManager.isValidOption("name", _tmp):
                            optionManager.updateOption("name", _tmp)
                            print("닉네임이 {}으로 설정되었습니다.\n".format(optionManager.getOption("name")))
                            break
                        print("올바른 값을 입력해주세요.\n")
                elif _input == 4:
                    break
                else:
                    print("올바른 값을 입력해주세요.\n")
    
    print("게임을 시작합니다.")
    debug_main()
    gameManager.initPygame()
    gameManager.beginLoop()
    
    print("게임을 종료합니다.")
    exit(0)

@debug_func
def debug_main():
    CPlayer(WPair(0, 0), WPair(1, 1), WPair(0, 0))
    

def debug():
    a = WPair(0, -1)
    b = WPair(1, 3)
    c = WPair(0, -1)
    d = WPair(1, 3)
    print(id(a))
    print(id(b))
    print(id(c))
    print(id(d))

if __name__ == '__main__':
    main()
    #debug()