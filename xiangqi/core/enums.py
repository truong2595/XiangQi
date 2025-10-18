# Hàm liệt kê các enum dùng trong Xiangqi
from enum import Enum

class PieceColor(Enum):
    RED = "red"
    BLACK = "black"

class PieceType(Enum):
    GENERAL = "general"
    ADVISOR = "advisor"
    ELEPHANT = "elephant"
    HORSE = "horse"
    CHARIOT = "chariot"
    CANNON = "cannon"
    SOLDIER = "soldier"

class GameResult(Enum):
    RED_WINS = "red_wins"
    BLACK_WINS = "black_wins"
    DRAW = "draw"