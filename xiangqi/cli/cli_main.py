from __future__ import annotations
import argparse
from typing import Dict, Tuple

from xiangqi.engine.game import Game
from xiangqi.core.enums import PieceType, PieceColor
from xiangqi.core.board import Board
from xiangqi.core.moves import Move

SYMBOLS: Dict[Tuple[PieceColor, PieceType], str] = {
    (PieceColor.RED,   PieceType.CHARIOT): "R",
    (PieceColor.BLACK, PieceType.CHARIOT): "r",
    (PieceColor.RED,   PieceType.HORSE):   "H",
    (PieceColor.BLACK, PieceType.HORSE):   "h",
    (PieceColor.RED,   PieceType.ELEPHANT):"E",
    (PieceColor.BLACK, PieceType.ELEPHANT):"e",
    (PieceColor.RED,   PieceType.ADVISOR): "A",
    (PieceColor.BLACK, PieceType.ADVISOR): "a",
    (PieceColor.RED,   PieceType.GENERAL): "K",
    (PieceColor.BLACK, PieceType.GENERAL): "k",
    (PieceColor.RED,   PieceType.CANNON):  "C",
    (PieceColor.BLACK, PieceType.CANNON):  "c",
    (PieceColor.RED,   PieceType.SOLDIER): "P",
    (PieceColor.BLACK, PieceType.SOLDIER): "p",
}

def board_ascii(board: Board) -> str:
    # rank 9 (trên) xuống 0 (dưới), file 0..8 trái->phải
    rows = []
    for r in range(9, -1, -1):
        cells = []
        for f in range(9):
            p = board.piece_at(f, r)
            if p and not p.captured:
                cells.append(SYMBOLS[(p.color, p.type)])
            else:
                cells.append(".")
        rows.append(f"{r:>2} " + " ".join(cells))
    footer = "   " + " ".join(str(f) for f in range(9))
    return "\n".join(rows + [footer])

def cmd_loop() -> None:
    g = Game()
    print("XiangQi CLI. Lệnh: show | moves f r | move f r tf tr | undo | turn | result | perft d | help | quit")
    print(board_ascii(g.board))
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        parts = line.split()
        cmd = parts[0].lower()

        try:
            if cmd in ("q", "quit", "exit"):
                break
            elif cmd in ("h", "help"):
                print("Lệnh: show | moves f r | move f r tf tr | undo | turn | result | perft d | quit")
            elif cmd == "show":
                print(board_ascii(g.board))
            elif cmd == "turn":
                print("Turn:", g.turn.value)
            elif cmd == "result":
                print("Result:", g.result)
            elif cmd == "moves":
                if len(parts) != 3:
                    print("Cú pháp: moves f r"); continue
                f, r = int(parts[1]), int(parts[2])
                p = g.board.piece_at(f, r)
                if not p or p.captured:
                    print("Không có quân ở ô này"); continue
                ms = [m for m in g.legal_moves() if m.from_file == f and m.from_rank == r]
                for m in ms:
                    print(f"{m.from_file}{m.from_rank}->{m.to_file}{m.to_rank}")
                print(f"{len(ms)} nước")
            elif cmd == "move":
                if len(parts) != 5:
                    print("Cú pháp: move f r tf tr"); continue
                f, r, tf, tr = map(int, parts[1:5])
                mv = Move(f, r, tf, tr)
                g.apply_move(mv, validate=True)
                print(board_ascii(g.board))
                if g.result:
                    print("Kết thúc:", g.result)
            elif cmd == "undo":
                g.undo()
                print(board_ascii(g.board))
            elif cmd == "perft":
                if len(parts) != 2:
                    print("Cú pháp: perft depth"); continue
                from xiangqi.engine.perft import perft
                d = int(parts[1])
                n = perft(g, d)
                print(f"perft({d}) = {n}")
            else:
                print("Lệnh không hợp lệ. Gõ 'help'.")
        except Exception as e:
            print("Lỗi:", e)

def main() -> None:
    parser = argparse.ArgumentParser(prog="xiangqi-cli", description="XiangQi CLI")
    parser.add_argument("--repl", action="store_true", help="Mở chế độ tương tác")
    parser.add_argument("--perft", type=int, help="Chạy perft ở độ sâu D")
    args = parser.parse_args()

    if args.repl or args.perft is None:
        cmd_loop()
    else:
        g = Game()
        from xiangqi.engine.perft import perft
        print(perft(g, args.perft))

if __name__ == "__main__":
    main()