"""
!!! NOT IMPLEMENTED YET !!!
/********************************************/
/*     Copyrights (C) 2024 CVE_zeroday.     */
/*          All rights reserved.            */
/********************************************/
/*         File Name: NNetwork.py           */
/*   Created by CVE_zeroday on 24.05.2024   */
/*               (T.Y.Kim)                  */
/********************************************/
"""

# Network 구현 계획
# Client 측은 position, direction 업데이트만
# Host 측에서 전부 계산

import socket, threading
from WTypes import *

class NClient:
    
    # private
    __tcp_sock = None
    __udp_sock = None
    __conn_id = -1
    
    def __init__(self, addr, port):
        self.__tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__tcp_sock.connect((addr, port))
        
        self.__udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class NServer:

    # public
    max_conn_count = 5
    
    # private
    __listening_sock = None
    __listening_thrd = None
    __loop_thrd = None
    
    __tcp_socks = []
    __tcp_socks_lock = None
    __udp_socks = []
    
    __conn_count = 0
    
    def __init__(self, port):
        self.__tcp_socks_lock = threading.Lock()
        self.__listening_thrd = threading.Thread(target = self.__listening_thrd_manage_new_connection, args = port)
        self.__listening_thrd.start()
        
        self.__loop_thrd = threading.Thread(target = self.__loop_thrd_main)
    
    # public
    def start(self):
        pass
        
    # private
    def __listening_thrd_manage_new_connection(self, port):
        while True:
            self.__listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__listening_sock.bind(('', port))
            self.__listening_sock.listen()
            
            self.__tcp_socks_lock.acquire()
            self.__tcp_socks.append(self.__listening_sock)
            self.__handshake(self.__listening_sock)
            self.__tcp_socks_lock.release()
    
    def __handshake(self, _sock):
        data = _sock.recv(HANDSHAKE_CLIENT_SIZE)
        
        
    
    def __loop_thrd_main(self):
        while True:
            pass