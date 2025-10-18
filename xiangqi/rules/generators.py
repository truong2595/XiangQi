# Hàm sinh nước đi giả cho từng loại quân (không kiểm tra chiếu)

from __future__ import annotations
from typing import List, Iterable
from xiangqi.core.board import Board
from xiangqi.core.piece import Piece
from xiangqi.core.moves import Move
from xiangqi.core.enums import PieceType, PieceColor
from xiangqi.core.constants import (
    BOARD_FILES, BOARD_RANKS,
    PALACE_FILES, PALACE_RANKS_RED, PALACE_RANKS_BLACK,
    RIVER_DIVIDER,
    ADVISOR_OFFSETS, GENERAL_OFFSETS,
    ELEPHANT_OFFSETS, ELEPHANT_EYE_MAP,
    HORSE_OFFSETS, HORSE_LEG_MAP,
    SOLDIER_FORWARD,
)

# ----------------- Helpers cơ bản -----------------
# Kiểm tra ô có nằm trong bàn cờ không
def in_bounds(f: int, r: int) -> bool:
    return 0 <= f < BOARD_FILES and 0 <= r < BOARD_RANKS
# Kiểm tra ô có nằm trong cung không
def in_palace(f: int, r: int, color: PieceColor) -> bool:
    if f not in PALACE_FILES:
        return False
    return r in (PALACE_RANKS_RED if color is PieceColor.RED else PALACE_RANKS_BLACK)
# Kiểm tra nước đi của tượng có hợp lệ không
def elephant_target_ok(rank: int, color: PieceColor) -> bool:
    # Tượng không vượt sông
    return rank <= RIVER_DIVIDER if color is PieceColor.RED else rank > RIVER_DIVIDER

def soldier_crossed_river(rank: int, color: PieceColor) -> bool:
    return rank > RIVER_DIVIDER if color is PieceColor.RED else rank <= RIVER_DIVIDER

# ----------------- Chariot -----------------
def gen_chariot_moves(board: Board, piece: Piece) -> List[Move]:
    moves: List[Move] = []
    f, r = piece.file, piece.rank
    for df, dr in ((1,0), (-1,0), (0,1), (0,-1)):
        nf, nr = f + df, r + dr
        while in_bounds(nf, nr):
            target = board.piece_at(nf, nr)
            if target is None:
                moves.append(Move(f, r, nf, nr))
            else:
                if target.color is not piece.color:
                    moves.append(Move(f, r, nf, nr, captured_id=target.id))
                break
            nf += df
            nr += dr
    return moves

# ----------------- Cannon -----------------
def gen_cannon_moves(board: Board, piece: Piece) -> List[Move]:
    moves: List[Move] = []
    f, r = piece.file, piece.rank
    for df, dr in ((1,0), (-1,0), (0,1), (0,-1)):
        nf, nr = f + df, r + dr
        # Phase 1: trượt
        while in_bounds(nf, nr):
            target = board.piece_at(nf, nr)
            if target is None:
                moves.append(Move(f, r, nf, nr))
                nf += df; nr += dr
                continue
            # gặp màn
            nf += df; nr += dr
            break
        # Phase 2: tìm quân đầu tiên sau màn để ăn
        while in_bounds(nf, nr):
            target = board.piece_at(nf, nr)
            if target:
                if target.color is not piece.color:
                    moves.append(Move(f, r, nf, nr, captured_id=target.id))
                break
            nf += df; nr += dr
    return moves

# ----------------- Horse -----------------
def gen_horse_moves(board: Board, piece: Piece) -> List[Move]:
    moves: List[Move] = []
    f, r = piece.file, piece.rank
    for df, dr in HORSE_OFFSETS:
        leg_df, leg_dr = HORSE_LEG_MAP[(df, dr)]
        lf, lr = f + leg_df, r + leg_dr
        if not in_bounds(lf, lr) or board.piece_at(lf, lr):
            continue  # chân bị chặn
        nf, nr = f + df, r + dr
        if not in_bounds(nf, nr):
            continue
        target = board.piece_at(nf, nr)
        if target is None or target.color is not piece.color:
            moves.append(Move(f, r, nf, nr, captured_id=target.id if target else None))
    return moves

# ----------------- Elephant -----------------
def gen_elephant_moves(board: Board, piece: Piece) -> List[Move]:
    moves: List[Move] = []
    f, r = piece.file, piece.rank
    for df, dr in ELEPHANT_OFFSETS:
        eye_df, eye_dr = ELEPHANT_EYE_MAP[(df, dr)]
        eye_f, eye_r = f + eye_df, r + eye_dr
        if not in_bounds(eye_f, eye_r) or board.piece_at(eye_f, eye_r):
            continue  # mắt bị chặn
        nf, nr = f + df, r + dr
        if not in_bounds(nf, nr) or not elephant_target_ok(nr, piece.color):
            continue
        target = board.piece_at(nf, nr)
        if target is None or target.color is not piece.color:
            moves.append(Move(f, r, nf, nr, captured_id=target.id if target else None))
    return moves

# ----------------- Advisor -----------------
def gen_advisor_moves(board: Board, piece: Piece) -> List[Move]:
    moves: List[Move] = []
    f, r = piece.file, piece.rank
    for df, dr in ADVISOR_OFFSETS:
        nf, nr = f + df, r + dr
        if not in_bounds(nf, nr) or not in_palace(nf, nr, piece.color):
            continue
        target = board.piece_at(nf, nr)
        if target is None or target.color is not piece.color:
            moves.append(Move(f, r, nf, nr, captured_id=target.id if target else None))
    return moves

# ----------------- General -----------------
def gen_general_moves(board: Board, piece: Piece) -> List[Move]:
    moves: List[Move] = []
    f, r = piece.file, piece.rank
    for df, dr in GENERAL_OFFSETS:
        nf, nr = f + df, r + dr
        if not in_bounds(nf, nr) or not in_palace(nf, nr, piece.color):
            continue
        target = board.piece_at(nf, nr)
        if target is None or target.color is not piece.color:
            moves.append(Move(f, r, nf, nr, captured_id=target.id if target else None))
    # Nước đối phương thẳng tướng
    opp = _find_opponent_general(board, piece.color)
    if opp and opp.file == f and _file_clear(board, f, r, opp.rank):
        moves.append(Move(f, r, opp.file, opp.rank, captured_id=opp.id))
    return moves

# ----------------- Soldier -----------------
def gen_soldier_moves(board: Board, piece: Piece) -> List[Move]:
    moves: List[Move] = []
    f, r = piece.file, piece.rank
    # Dùng SOLDIER_FORWARD dict (chuỗi value của PieceColor là "red"/"black")
    forward = SOLDIER_FORWARD[piece.color.value]
    nf, nr = f, r + forward
    if in_bounds(nf, nr):
        target = board.piece_at(nf, nr)
        if target is None or target.color is not piece.color:
            moves.append(Move(f, r, nf, nr, captured_id=target.id if target else None))
    if soldier_crossed_river(r, piece.color):
        for df in (-1, 1):
            nf = f + df
            nr = r
            if not in_bounds(nf, nr):
                continue
            target = board.piece_at(nf, nr)
            if target is None or target.color is not piece.color:
                moves.append(Move(f, r, nf, nr, captured_id=target.id if target else None))
    return moves

# ----------------- Dispatcher ----------------
# Sinh nước đi giả cho quân cụ thể
def generate_pseudo_moves(board: Board, piece: Piece) -> List[Move]:
    if piece.captured:
        return []
    t = piece.type
    if t is PieceType.CHARIOT:
        return gen_chariot_moves(board, piece)
    if t is PieceType.CANNON:
        return gen_cannon_moves(board, piece)
    if t is PieceType.HORSE:
        return gen_horse_moves(board, piece)
    if t is PieceType.ELEPHANT:
        return gen_elephant_moves(board, piece)
    if t is PieceType.ADVISOR:
        return gen_advisor_moves(board, piece)
    if t is PieceType.GENERAL:
        return gen_general_moves(board, piece)
    if t is PieceType.SOLDIER:
        return gen_soldier_moves(board, piece)
    return []

# Sinh tất cả nước đi giả cho một màu cụ thể
def generate_all_pseudo_moves(board: Board, color: PieceColor) -> List[Move]:
    out: List[Move] = []
    for p in board.all_active_pieces(color):
        out.extend(generate_pseudo_moves(board, p))
    return out

# Sinh tất cả nước đi giả cho một màu cụ thể (dùng yield) để tiết kiệm bộ nhớ
def iter_pseudo_moves(board: Board, color: PieceColor) -> Iterable[Move]:
    for p in board.all_active_pieces(color):
        for mv in generate_pseudo_moves(board, p):
            yield mv

# ----------------- Internal helpers -----------------
# Tìm tướng đối phương
def _find_opponent_general(board: Board, my: PieceColor) -> Piece | None:
    opp = PieceColor.RED if my is PieceColor.BLACK else PieceColor.BLACK
    for p in board.all_active_pieces(opp):
        if p.type is PieceType.GENERAL:
            return p
    return None

# Kiểm tra file có trống không giữa hai rank
def _file_clear(board: Board, file_: int, r1: int, r2: int) -> bool:
    lo, hi = sorted((r1, r2))
    for rank in range(lo + 1, hi):
        if board.piece_at(file_, rank):
            return False
    return True