from enum import Enum

class Seat(Enum):
    South = 0
    North = 1
    West = 2
    East = 3
    
class Trump(Enum):
    No = 0
    Spdaes = 1
    Hearts = 2
    Diamonds = 3
    Clubs = 4
    
def getTricks(seat: Seat, trump: Trump, tricks: str):
    return tricks.split()[seat.value*5+trump.value]