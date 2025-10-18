#Hàm định nghĩa lớp Piece đại diện cho quân cờ
from dataclasses import dataclass
from .enums import PieceColor, PieceType

@dataclass(slots=True)
class Piece:
    id: int
    color: PieceColor
    type: PieceType
    file: int  # 0..8
    rank: int  # 0..9
    captured: bool = False