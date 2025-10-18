# Kiểm tra chiếu và tướng đối mặt
from __future__ import annotations

from xiangqi.core.board import Board
from xiangqi.core.enums import PieceColor, PieceType
from xiangqi.rules.generators import generate_pseudo_moves


def find_general(board: Board, color: PieceColor):
    for p in board.all_active_pieces(color):
        if p.type is PieceType.GENERAL:
            return p
    return None


def is_in_check(board: Board, color: PieceColor) -> bool:
    """
    Trả về True nếu bên 'color' đang bị chiếu trong trạng thái board hiện tại.
    Dựa trên pseudo moves của đối phương (đã bao gồm 'flying general' trong generators).
    """
    general = find_general(board, color)
    if not general:
        return False  # không còn tướng => coi như không kiểm tra chiếu
    gx, gy = general.file, general.rank
    enemy = PieceColor.RED if color is PieceColor.BLACK else PieceColor.BLACK

    for p in board.all_active_pieces(enemy):
        for mv in generate_pseudo_moves(board, p):
            if mv.to_file == gx and mv.to_rank == gy:
                return True
    return False


def flying_general_exposed(board: Board) -> bool:
    """
    Hai tướng đối mặt (cùng file) và giữa hai tướng không có quân nào.
    Hỗ trợ debug/test; việc lọc nước bất hợp lệ đã được phủ bởi is_in_check khi validate.
    """
    red = find_general(board, PieceColor.RED)
    black = find_general(board, PieceColor.BLACK)
    if not red or not black:
        return False
    if red.file != black.file:
        return False
    file_ = red.file
    lo, hi = sorted((red.rank, black.rank))
    for r in range(lo + 1, hi):
        if board.piece_at(file_, r) is not None:
            return False
    return True