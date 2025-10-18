from __future__ import annotations
from typing import List, Optional
from .piece import Piece
from .enums import PieceColor, PieceType
from .constants import INITIAL_PIECES, BOARD_FILES, BOARD_RANKS

class Board:
    """
    Quản lý danh sách quân và truy vấn ô.
    Không sinh nước đi tại đây.
    """

    __slots__ = ("pieces", "_grid")

    def __init__(self, setup: bool = True) -> None:
        self.pieces: List[Piece] = []
        # _grid[file][rank] = index vào self.pieces hoặc -1
        self._grid: List[List[int]] = [[-1 for _ in range(BOARD_RANKS)] for _ in range(BOARD_FILES)]
        if setup:
            self._setup_initial()

    def _setup_initial(self) -> None:
        pid = 0
        for f, r, color_str, type_str in INITIAL_PIECES:
            color = PieceColor(color_str)
            ptype = PieceType(type_str)
            piece = Piece(id=pid, color=color, type=ptype, file=f, rank=r)
            self.pieces.append(piece)
            self._grid[f][r] = pid
            pid += 1

    def piece_at(self, file: int, rank: int) -> Optional[Piece]:
        if 0 <= file < BOARD_FILES and 0 <= rank < BOARD_RANKS:
            idx = self._grid[file][rank]
            if idx >= 0:
                return self.pieces[idx]
        return None

    def move_piece(self, piece: Piece, to_file: int, to_rank: int) -> Optional[Piece]:
        """
        Di chuyển quân; trả về quân bị ăn (nếu có).
        Không kiểm tra hợp lệ (việc đó ở rules/validators).
        """
        # Xử lý capture
        captured: Optional[Piece] = self.piece_at(to_file, to_rank)
        if captured and not captured.captured:
            captured.captured = True
            self._grid[captured.file][captured.rank] = -1

        # Cập nhật vị trí quân
        self._grid[piece.file][piece.rank] = -1
        piece.file = to_file
        piece.rank = to_rank
        self._grid[to_file][to_rank] = piece.id
        return captured

    def undo_move_piece(self, piece: Piece, from_file: int, from_rank: int, captured: Optional[Piece]) -> None:
        """
        Hoàn tác di chuyển (dùng cho undo hoặc giả lập).
        """
        self._grid[piece.file][piece.rank] = -1
        piece.file = from_file
        piece.rank = from_rank
        self._grid[from_file][from_rank] = piece.id
        if captured:
            captured.captured = False
            self._grid[captured.file][captured.rank] = captured.id

    def all_active_pieces(self, color: Optional[PieceColor] = None):
        for p in self.pieces:
            if not p.captured and (color is None or p.color is color):
                yield p