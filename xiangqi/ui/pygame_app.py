from __future__ import annotations
import sys, pathlib, pygame
# Thêm sys.path khi chạy file trực tiếp
ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from xiangqi.engine.game import Game
from xiangqi.ui.layout import Layout
from xiangqi.ui.assets import load_piece_images
from xiangqi.ui.renderer import render, draw_file_labels, draw_rank_labels
from xiangqi.ui.highlight import draw_highlights
from xiangqi.ui.sidebar import draw_move_list


def run() -> None:
    pygame.init()
    pygame.font.init()

    SIDEBAR_W = 260
    layout = Layout(win_w=600 + SIDEBAR_W, win_h=650, margin=50, red_at_bottom=True, sidebar_w=SIDEBAR_W)
    screen = pygame.display.set_mode((layout.win_w, layout.win_h))
    pygame.display.set_caption("XiangQi")

    game = Game()
    images = load_piece_images(layout.cell, preferred_theme="Chinese")  # hoặc "English"
    font = pygame.font.SysFont("consolas, courier new, arial", 18)

    selected = None
    cached_legal = game.legal_moves()

    clock = pygame.time.Clock()
    running = True

    def moves_from_selected(sel):
        if sel is None:
            return []
        sf, sr = sel
        return [m for m in cached_legal if m.from_file == sf and m.from_rank == sr]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    game.undo()
                    cached_legal = game.legal_moves()
                    selected = None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                sq = layout.px_to_square(*pos)
                if sq is None:
                    selected = None
                else:
                    f, r = sq
                    piece = game.board.piece_at(f, r)
                    ms = moves_from_selected(selected)
                    if selected is not None and any(m.to_file == f and m.to_rank == r for m in ms):
                        sf, sr = selected
                        try:
                            game.apply_coords(sf, sr, f, r, validate=True)
                            cached_legal = game.legal_moves()
                        except Exception:
                            pass
                        selected = None
                    else:
                        if piece and not piece.captured and piece.color is game.turn:
                            selected = (f, r)
                        else:
                            selected = None

        render(screen, game.board, images, layout)
        draw_file_labels(screen, layout, font)  # nhãn cột A..I
        draw_rank_labels(screen, layout, font)  # nhãn hàng 0..9
        draw_highlights(screen, layout, selected, moves_from_selected(selected))
        draw_move_list(screen, layout, game, font)

        pygame.display.set_caption(f"XiangQi - Turn: {game.turn.value} - Result: {game.result or 'playing'}")
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    run()