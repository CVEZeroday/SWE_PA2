"""
/********************************************/
/*     Copyrights (C) 2024 CVE_zeroday.     */
/*          All rights reserved.            */
/********************************************/
/*           File Name: Debug.py            */
/*   Created by CVE_zeroday on 26.05.2024   */
/*               (T.Y.Kim)                  */
/********************************************/
"""

isDebugMode: bool = True

def debug_func(fn):
    if isDebugMode:
        def func_wrapper(*args, **kwargs):
            fn(*args, **kwargs)
    else:
        def func_wrapper(*args, **kwargs):
            pass
    
    return func_wrapper