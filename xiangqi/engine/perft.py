# Hàm thực hiện perft cho Xiangqi, đếm số node ở độ sâu nhất định
# Chỉ dùng trong mục đích kiểm tra và phát triển engine
# Có thể bỏ qua khi chạy UI hoặc chơi bình thường
from __future__ import annotations

from typing import List, Tuple

from xiangqi.engine.game import Game
from xiangqi.core.moves import Move


def perft(game: Game, depth: int) -> int:
    """
    Đếm số node ở độ sâu 'depth' từ trạng thái hiện tại.
    Depth=0 trả về 1 (đếm chính node hiện tại).
    """
    if depth == 0:
        return 1

    nodes = 0
    moves = game.legal_moves()
    for mv in moves:
        game.apply_move(mv, validate=False)
        nodes += perft(game, depth - 1)
        game.undo()
    return nodes


def perft_divide(game: Game, depth: int) -> List[Tuple[str, int]]:
    """
    Trả về danh sách (move_str, nodes) cho từng nước ở ply 1.
    """
    results: List[Tuple[str, int]] = []
    for mv in game.legal_moves():
        game.apply_move(mv, validate=False)
        n = perft(game, depth - 1)
        game.undo()
        results.append((move_to_str(mv), n))
    return results


def move_to_str(m: Move) -> str:
    """
    Chuỗi đơn giản cho move theo tọa độ: ffrr->ttrr (vd: 00->01).
    Điều chỉnh nếu bạn có ký hiệu riêng.
    """
    return f"{m.from_file}{m.from_rank}->{m.to_file}{m.to_rank}"


if __name__ == "__main__":
    # Chạy nhanh: python -m xiangqi.engine.perft 2
    import sys

    d = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    g = Game()
    total = perft(g, d)
    print(f"perft({d}) = {total}")
    for s, n in perft_divide(g, d):
        print(f"{s}: {n}")