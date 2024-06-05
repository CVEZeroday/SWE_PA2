"""
/********************************************/
/*     Copyrights (C) 2024 CVE_zeroday.     */
/*          All rights reserved.            */
/********************************************/
/*          File Name: WTypes.py            */
/*   Created by CVE_zeroday on 24.05.2024   */
/*               (T.Y.Kim)                  */
/********************************************/
"""

from pygame.locals import *
import math
from ctypes import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 127, 0)
SILVER = (192, 192, 192)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
YELLOW = (255, 255, 0)

BG_1 = (176, 207, 87)
BG_2 = (182, 212, 94)

KEY_LEFT = (K_a, K_LEFT)
KEY_UP = (K_w, K_UP)
KEY_RIGHT = (K_d, K_RIGHT)
KEY_DOWN = (K_s, K_DOWN)
KEY_RESURRECT = (K_SPACE, 0)

class WPair:

    # public
    x = None
    y = None
    
    # private
    __known_instances = []
    __known_pairs = ((0,0), (0,1), (1,0), (-1,0), (0,-1), (-1,-1)) # This is for saving memory
    
    def __new__(cls, *args):
        if not cls.__known_instances:
            for pairs in cls.__known_pairs:
                _tmp = object.__new__(cls)
                _tmp.x = pairs[0]
                _tmp.y = pairs[1]
                cls.__known_instances.append(_tmp)
        
        for i in range(len(cls.__known_pairs)):
            if args == cls.__known_pairs[i]:
                return cls.__known_instances[i]
        
        return object.__new__(cls)
    
    def __init__(self, _x, _y): 
        if type(_x) == float or type(_y) == float:
            self.x = float(_x)
            self.y = float(_y)
        else:
            self.x = _x
            self.y = _y

    # public
    def toTuple(self):
        return (self.x, self.y)

    def toInt(self):
        return WPair(int(self.x), int(self.y))

    def toFloat(self):
        return WPair(float(self.x), int(self.y))

    def distance(self, other):
        assert type(other) == WPair, 'Type error in WPair.distance'
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def floor(self):
        return WPair(math.floor(self.x), math.floor(self.y))

    def round(self):
        return WPair(round(self.x), round(self.y))

    def normalize(self): # 절댓값의 최댓값이 1이 되도록 만듦

        _x: float = 0.0
        _y: float = 0.0

        if self.x == 0 and self.y == 0:
            return WPair(0, 0)
        if self.x == 0:
            return WPair(0, self.y / abs(self.y))
        if self.y == 0:
            return WPair(self.x / abs(self.x), 0)
        if self.x == self.y:
            return WPair(1, 1)

        ratio = abs(self.x / self.y)

        if abs(self.x) > abs(self.y):
            _x = self.x / ratio
            _y = self.y / ratio
        else:
            _x = self.x * ratio
            _y = self.y * ratio

        return WPair(_x, _y)

    def normalize2(self): # 방향을 x축 또는 y축 중 하나의 방향로 단순화함
        if abs(self.x) > abs(self.y):
            _x = 1 if self.x > 0 else (-1 if self.x < 0 else 0)
            _y = 0
        elif abs(self.x) < abs(self.y):
            _x = 0
            _y = 1 if self.y > 0 else (-1 if self.y < 0 else 0)
        else:
            _x = 0
            _y = 0

        return WPair(_x, _y)
    
    # operator overriding
    def __add__(self, other):
        assert type(other) in (WPair, int, float), 'Type error in WPair.__add__'
        if type(other) == WPair:
            return WPair(self.x + other.x, self.y + other.y)
        if type(other) == int or type(other) == float:
            return WPair(self.x + other, self.y + other)
    def __radd__(self, other):
        assert type(other) in (WPair, int, float), 'Type error in WPair.__radd__: type(self) == {0}, type(other) == {1}'.format(str(type(self)), str(type(other)))
        if type(other) == WPair:
            return WPair(self.x + other.x, self.y + other.y)
        if type(other) == int or type(other) == float:
            return WPair(self.x + other, self.y + other)
    
    def __sub__(self, other):
        assert type(other) in (WPair, int, float), 'Type error in WPair.__sub__'
        if type(other) == WPair:
            return WPair(self.x - other.x, self.y - other.y)
        if type(other) == int or type(other) == float:
            return WPair(self.x - other, self.y - other)
    
    def __mul__(self, other):
        assert type(other) in (WPair, int, float), 'Type error in WPair.__mul__'
        if type(other) == WPair:
            return WPair(self.x * other.x, self.y * other.y)
        if type(other) == int or type(other) == float:
            return WPair(self.x * other, self.y * other)
    
    def __floordiv__(self, other):
        return WPair(self.x // other, self.y // other)
    
    def __truediv__(self, other):
        return WPair(self.x / other, self.y / other)
    
    def __mod__(self, other):
        return WPair(self.x % other, self.y % other)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __getitem__(self, item):
        assert item in (0, 1), 'Access error in WPair.__getitem__'
        if item == 0:
            return self.x
        if item == 1:
            return self.y
    
    def __setitem__(self, key, value):
        assert key in (0, 1), 'Key error in WPair.__setitem__'
        if key == 0:
            self.x = value
        if key == 1:
            self.y = value 
    
    def __str__(self):
        return str(self.x) + ", " + str(self.y)
    
"""
!!! NOT IMPLEMENTED YET !!!
"""

HANDSHAKE_CLIENT_SIZE = 12
HANDSHAKE_SERVER_SIZE = 14
KEY_INPUT_DATA_SIZE = 4
GAME_EVENT_DATA_SIZE = 4
PLAYER_DATA_SIZE = 20
OBJECT_DATA_SIZE = 5
SESSION_EVENT_DATA_SIZE = 4
KEEP_ALIVE_SIZE = 1
POSITION_UPDATE_DATA_SIZE = 24

    
    # type 0 : handshaking (TCP)
    #   Packet Structure (S/C == 1)
    #   0 . | . | . | . 1 . | . | . | . 2 . | . | . | . 3 . | . | . | . 4
    #   +---------------------------------------------------------------+
    #   |S|    type     |      id       |          client_name          |
    #   +---------------------------------------------------------------+
    #   |                          client_name                          |
    #   +---------------------------------------------------------------+
    #   |                          client_name                          |
    #   +---------------------------------------------------------------+
    #   Packet Structure (S/C == 0)
    #   0 . | . | . | . 1 . | . | . | . 2 . | . | . | . 3 . | . | . | . 4
    #   +---------------------------------------------------------------+
    #   |S|    type     |    user_id    |          server_name          |
    #   +---------------------------------------------------------------+
    #   |                          server_name                          |
    #   +---------------------------------------------------------------+
    #   |                          server_name                          |
    #   +---------------------------------------------------------------+
    #   |  player_count |  object_count |                               |
    #   +---------------------------------------------------------------+
    # - S bit: 0 if Server, 1 if Client

def pack_handshaking_client(_id: int, client_name: str):
    packet = b''
    packet += (c_uint8(0b10000000))
    packet += c_uint8(_id)
    packet += bytes(client_name, 'utf-8')
    assert len(client_name) <= 10, "pack_handshaking_client: client_name must have length <= 10"
    while len(packet) < HANDSHAKE_CLIENT_SIZE:
        packet += c_uint8(0)
    return packet

def pack_handshaking_server(_user_id: int, server_name: str, player_count: int, object_count: int):
    packet = b''
    packet += (c_uint8(0))
    packet += c_uint8(_user_id)
    packet += bytes(server_name, 'utf-8')
    assert len(server_name) <= 10, "pack_handshaking_server: server_name must have length <= 10"
    while len(packet) < HANDSHAKE_SERVER_SIZE:
        packet += c_uint8(0)
    packet += c_uint16(player_count)
    packet += c_uint16(object_count)
    return packet

def unpack_handshaking(_bytes: bytes):
    if (_bytes[0] >> 7) == 1: # client
        _id = int(_bytes[1])
        _client_name = str(_bytes[2:12], 'utf-8')
        
        return _id, _client_name

    elif (_bytes[0] >> 7) == 0: # server
        _user_id = int(_bytes[1])
        _server_name = str(_bytes[2:12], 'utf-8')
        
        player_count = _bytes[12] + _bytes[13]
        player_count = c_uint16(player_count)
        player_count = int(player_count)
        
        object_count = _bytes[14] + _bytes[15]
        object_count = c_uint16(object_count)
        object_count = int(object_count)

        return _user_id, _server_name, player_count, object_count
    # type 1 : key_input data (TCP)
    #   Packet Structure
    #   0 . | . | . | . 1 . | . | . | . 2 . | . | . | . 3 . | . | . | . 4
    #   +---------------------------------------------------------------+
    #   |0|    type     |   client_id   |           key data            |
    #   +---------------------------------------------------------------+
    
    # type 2 : game event data (TCP)
    #   Packet Structure
    #   0 . | . | . | . 1 . | . | . | . 2 . | . | . | . 3 . | . | . | . 4
    #   +---------------------------------------------------------------+
    #   |0|    type     |   event_type  |          event_data           |
    #   +---------------------------------------------------------------+
    # event_type
    # 0: New Object
    # 1: Delete Object
    
    # type 3 : player data (TCP)
    #   Packet Structure
    #   0 . | . | . | . 1 . | . | . | . 2 . | . | . | . 3 . | . | . | . 4
    #   +---------------------------------------------------------------+
    #   |0|    type     |   player_id   |         player_name           |
    #   +---------------------------------------------------------------+
    #   |                          player_name                          |
    #   +---------------------------------------------------------------+
    #   |                          player_name                          |
    #   +---------------------------------------------------------------+
    #   |        component_count        |          pivot_count          |
    #   +---------------------------------------------------------------+
    #   |                           data_size                           |
    #   +---------------------------------------------------------------+
    #   |                            data~                              | # CCharacter, CCharacterComponent, CCharacterPivot 순서
    #   +---------------------------------------------------------------+
    #   |                             ...                               |
    #   +---------------------------------------------------------------+
    
    # type 4 : object data (TCP)
    #   Packet Structure
    #   0 . | . | . | . 1 . | . | . | . 2 . | . | . | . 3 . | . | . | . 4
    #   +---------------------------------------------------------------+
    #   |0|    type     |                   data_size                   |
    #   +---------------------------------------------------------------+
    #   |  data_size    |                     data~                     |
    #   +---------------------------------------------------------------+
    #   |                              ...                              |
    #   +---------------------------------------------------------------+
    
    # type 5 : session event data (TCP)
    #   Packet Structure
    #   0 . | . | . | . 1 . | . | . | . 2 . | . | . | . 3 . | . | . | . 4
    #   +---------------------------------------------------------------+
    #   |0|    type     |   event_type  |          event_data           |
    #   +---------------------------------------------------------------+
    
    # type 6 : keep-alive (TCP)
    #   Packet Structure
    #   0 . | . | . | . 1 . | . | . | . 2 . | . | . | . 3 . | . | . | . 4
    #   +---------------------------------------------------------------+
    #   |S|    type     |                                               |
    #   +---------------------------------------------------------------+
    
    # type 7 : position update data (UDP)
    #   Packet Structure
    #   0 . | . | . | . 1 . | . | . | . 2 . | . | . | . 3 . | . | . | . 4
    #   +---------------------------------------------------------------+
    #   |                          packet_size                          |
    #   +---------------------------------------------------------------+
    #   |                          position_x                           |
    #   +---------------------------------------------------------------+
    #   |                          position_x                           |
    #   +---------------------------------------------------------------+
    #   |                          position_y                           |
    #   +---------------------------------------------------------------+
    #   |                          position_y                           |
    #   +---------------------------------------------------------------+
    #   |dir bit|                       objId                           |
    #   +---------------------------------------------------------------+
    # - dir bit : 각각 2bit씩 4bit로 이루어짐, 00 == 0, 01 == 1, 11 == -1