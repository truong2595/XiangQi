# Hàm sinh nước đi hợp lệ (loại bỏ tự chiếu)
from __future__ import annotations

from typing import List, Tuple, Optional

from xiangqi.core.board import Board
from xiangqi.core.moves import Move
from xiangqi.core.enums import PieceColor
from xiangqi.rules.generators import generate_all_pseudo_moves
from xiangqi.rules.check import is_in_check


def _apply(board: Board, move: Move) -> Tuple:
    """
    Áp dụng tạm 1 nước đi lên board.
    Trả về snapshot để hoàn tác: (piece, (from_file, from_rank), captured_piece_or_None)
    """
    piece = board.piece_at(move.from_file, move.from_rank)
    if piece is None:
        return (None, (0, 0), None)  # không hợp lệ, caller sẽ bỏ qua
    from_pos = (piece.file, piece.rank)
    captured = board.move_piece(piece, move.to_file, move.to_rank)
    return (piece, from_pos, captured)


def _undo(board: Board, snapshot: Tuple) -> None:
    """
    Hoàn tác theo snapshot từ _apply.
    """
    piece, (from_f, from_r), captured = snapshot
    if piece is None:
        return
    board.undo_move_piece(piece, from_f, from_r, captured)


def generate_legal_moves(board: Board, color: PieceColor) -> List[Move]:
    """
    Sinh danh sách nước hợp lệ: pseudo moves lọc theo tự chiếu (và cả 'flying general').
    """
    legal: List[Move] = []
    for mv in generate_all_pseudo_moves(board, color):
        snap = _apply(board, mv)
        # Loại nước để lại tướng mình bị chiếu
        if not is_in_check(board, color):
            legal.append(mv)
        _undo(board, snap)
    return legal