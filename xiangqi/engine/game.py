# Hàm định nghĩa lớp Game quản lý trạng thái ván cờ
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Tuple

from xiangqi.core.board import Board
from xiangqi.core.moves import Move
from xiangqi.core.enums import PieceColor, GameResult
from xiangqi.rules.validators import generate_legal_moves
from xiangqi.rules.check import is_in_check


@dataclass(slots=True)
class _HistoryItem:
    move: Move
    # snapshot để undo
    piece_id: int
    from_pos: Tuple[int, int]
    captured_id: Optional[int]


class Game:
    """
    Quản lý trạng thái ván cờ:
    - board: trạng thái bàn cờ
    - turn: lượt hiện tại (RED bắt đầu)
    - history: stack để undo
    - result: kết quả (None nếu chưa kết thúc)
    """

    __slots__ = ("board", "turn", "_history", "result")

    def __init__(self, start_color: PieceColor = PieceColor.RED) -> None:
        self.board = Board(setup=True)
        self.turn: PieceColor = start_color
        self._history: List[_HistoryItem] = []
        self.result: Optional[GameResult] = None

    # ---------------- Queries ----------------

    # Hàm sinh nước đi hợp lệ cho lượt hiện tại
    def legal_moves(self) -> List[Move]:
        if self.result is not None:
            return []
        return generate_legal_moves(self.board, self.turn)

    # Kiểm tra bên hiện tại có bị chiếu không
    def is_in_check_current(self) -> bool:
        return is_in_check(self.board, self.turn)

    # Kiểm tra ván đã kết thúc chưa
    def is_checkmate(self) -> bool:
        if self.result is not None:
            return self.result in (GameResult.RED_WINS, GameResult.BLACK_WINS)
        if self.legal_moves():
            return False
        return self.is_in_check_current()

    # Kiểm tra kết quả, nếu còn nước đi thì không phải stalemate
    def is_stalemate(self) -> bool:
        if self.result is not None:
            return self.result == GameResult.DRAW
        if self.legal_moves():
            return False
        return not self.is_in_check_current()

    # ---------------- Apply / Undo ----------------

    # Áp dụng một nước đi
    def apply_move(self, move: Move, validate: bool = True) -> None:
        """
        Áp dụng một nước đi.
        - Nếu validate=True: chỉ chấp nhận move thuộc legal_moves() (so sánh theo tọa độ).
        - Cập nhật lịch sử để có thể undo.
        Sau khi đi xong, kiểm tra checkmate/stalemate và cập nhật result nếu ván kết thúc.
        """
        if self.result is not None:
            raise ValueError("Game already finished")

        # Nếu validate, kiểm tra move có hợp lệ không, phải thuộc legal_moves()
        if validate:
            lm = self.legal_moves()
            if not any(self._same_coords(m, move) for m in lm):
                raise ValueError("Move is not legal")

        piece = self.board.piece_at(move.from_file, move.from_rank)
        if piece is None:
            raise ValueError("No piece at source square")
        if piece.color is not self.turn:
            raise ValueError("Moving the wrong side")

        # Thực thi
        captured = self.board.move_piece(piece, move.to_file, move.to_rank)

        # Lưu history
        self._history.append(
            _HistoryItem(
                move=move,
                piece_id=piece.id,
                from_pos=(move.from_file, move.from_rank),
                captured_id=(captured.id if captured else None),
            )
        )

        # Đổi lượt
        self.turn = PieceColor.BLACK if self.turn is PieceColor.RED else PieceColor.RED

        # Cập nhật kết quả nếu ván kết thúc
        self._update_result_after_move()

    def undo(self) -> None:
        """
        Hoàn tác nước đi cuối.
        """
        if not self._history:
            return
        h = self._history.pop()

        # Lấy lại piece và captured
        piece = self._piece_by_id(h.piece_id)
        captured = self._piece_by_id(h.captured_id) if h.captured_id is not None else None

        # Undo di chuyển
        self.board.undo_move_piece(piece, h.from_pos[0], h.from_pos[1], captured)

        # Đổi lượt lại
        self.turn = PieceColor.BLACK if self.turn is PieceColor.RED else PieceColor.RED

        # Xóa kết quả (tiếp tục ván)
        self.result = None

    # ---------------- Convenience ----------------

    def apply_coords(self, from_file: int, from_rank: int, to_file: int, to_rank: int, validate: bool = True) -> None:
        """
        Tiện ích: áp dụng nước đi bằng tọa độ.
        """
        mv = Move(from_file, from_rank, to_file, to_rank)
        self.apply_move(mv, validate=validate)

    # ---------------- Internal helpers ----------------

    def _update_result_after_move(self) -> None:
        """
        Sau khi vừa đổi lượt (self.turn = bên tiếp theo), kiểm tra:
        - Nếu bên tới lượt không còn nước đi
            - Đang bị chiếu -> đối phương thắng
            - Không bị chiếu -> hòa (stalemate)
        """
        next_color = self.turn
        moves = generate_legal_moves(self.board, next_color)
        if moves:
            self.result = None
            return

        in_check_next = is_in_check(self.board, next_color)
        if in_check_next:
            # Người vừa đi thắng
            winner = PieceColor.RED if next_color is PieceColor.BLACK else PieceColor.BLACK
            self.result = GameResult.RED_WINS if winner is PieceColor.RED else GameResult.BLACK_WINS
        else:
            self.result = GameResult.DRAW
    
    # Lấy piece theo id
    def _piece_by_id(self, pid: int):
        for p in self.board.pieces:
            if p.id == pid:
                return p
        raise KeyError(f"Piece id not found: {pid}")
    
    # So sánh hai nước đi có cùng tọa độ không
    @staticmethod
    def _same_coords(a: Move, b: Move) -> bool:
        return (
            a.from_file == b.from_file
            and a.from_rank == b.from_rank
            and a.to_file == b.to_file
            and a.to_rank == b.to_rank
        )