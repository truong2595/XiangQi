from __future__ import annotations
from typing import (
    Protocol, Iterable, Sequence, Optional, Callable,
    TypedDict, NewType, TYPE_CHECKING
)

File = int        # 0..8
Rank = int        # 0..9
Square = tuple[File, Rank]
PieceId = int

if TYPE_CHECKING:
    from .piece import Piece
    from .moves import Move
    from .board import Board
    from .enums import PieceColor

PieceSequence = Sequence["Piece"]
MoveSequence = Sequence["Move"]
EvaluateFn = Callable[["Board", "PieceColor"], int]
ZobristHash = NewType("ZobristHash", int)

class MoveDict(TypedDict, total=False):
    from_file: File
    from_rank: Rank
    to_file: File
    to_rank: Rank
    captured_id: Optional[PieceId]

class MoveProvider(Protocol):
    def legal_moves(self) -> Iterable["Move"]: ...