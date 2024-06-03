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
    __thrd = None # thread
    
    __tcp_socks = []
    __udp_socks = []
    
    __conn_count = 0
    
    def __init__(self, port):
        self.__thrd = threading.Thread(target = self.__mthrd_manage_new_connection, args = (port))
        self.__thrd.start()
    
    # public
    def start(self):
        pass
        
    # private
    def __mthrd_manage_new_connection(self, port):
        while True:
            self.__listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__listening_sock.bind(('', port))
            self.__listening_sock.listen()
            data = self.__listening_sock.recv(1024)