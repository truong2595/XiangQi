# Hàm vẽ thanh bên hiển thị danh sách nước đi
from __future__ import annotations
from typing import List, Optional, Tuple
import pygame
from xiangqi.core.moves import Move
from xiangqi.ui.layout import Layout
from xiangqi.core.constants import FILE_LETTERS

PANEL_BG = (245, 245, 245)
PANEL_TEXT = (20, 20, 20)
PANEL_TITLE = (80, 80, 80)
SEPARATOR = (200, 200, 200)

# Vẽ danh sách nước đi vào thanh bên
def _fmt_sq(f: int, r: int) -> str:
    # file -> chữ (A..I), rank giữ nguyên số
    ch = FILE_LETTERS[f] if 0 <= f < len(FILE_LETTERS) else str(f)
    return f"{ch}{r}"

# Định dạng nước đi thành chuỗi hiển thị
def _fmt_move(m: Move) -> str:
    # Chỉ in nước đi theo định dạng: E2->E3
    return f"{_fmt_sq(m.from_file, m.from_rank)}->{_fmt_sq(m.to_file, m.to_rank)}"

# Lấy danh sách Move từ lịch sử Game
def _history_moves(game) -> List[Move]:
    # Lấy danh sách Move từ lịch sử Game (đọc _history nếu chưa có API công khai)
    if hasattr(game, "_history"):
        return [h.move for h in game._history]  # type: ignore[attr-defined]
    return []

# Vẽ danh sách nước đi vào thanh bên
def draw_move_list(surface: pygame.Surface, layout: Layout, game, font: pygame.font.Font) -> None:
    if layout.sidebar_w <= 0:
        return
    panel_x = layout.win_w - layout.sidebar_w
    panel_rect = pygame.Rect(panel_x, 0, layout.sidebar_w, layout.win_h)
    pygame.draw.rect(surface, PANEL_BG, panel_rect)
    pygame.draw.line(surface, SEPARATOR, (panel_x, 0), (panel_x, layout.win_h), 1)

    title = font.render("Moves", True, PANEL_TITLE)
    surface.blit(title, (panel_x + 12, 12))

    moves = _history_moves(game)
    rows: List[Tuple[int, Optional[Move], Optional[Move]]] = []
    for i in range(0, len(moves), 2):
        m_red: Optional[Move] = moves[i]
        m_black: Optional[Move] = moves[i + 1] if i + 1 < len(moves) else None
        rows.append((i // 2 + 1, m_red, m_black))

    line_h = font.get_linesize()
    top = 40
    visible = max(0, (layout.win_h - top - 8) // line_h)
    start = max(0, len(rows) - visible)

    x_no = panel_x + 12
    x_red = panel_x + 62
    x_blk = panel_x + 142

    for idx in range(start, len(rows)):
        y = top + (idx - start) * line_h
        no, mr, mb = rows[idx]
        surface.blit(font.render(f"{no:>2}.", True, PANEL_TEXT), (x_no, y))
        if mr:
            m = mr if isinstance(mr, Move) else mr[0]  # hỗ trợ cả dạng (Move, pid) nếu bạn dùng
            surface.blit(font.render(_fmt_move(m), True, (180, 30, 30)), (x_red, y))
        if mb:
            m = mb if isinstance(mb, Move) else mb[0]
            surface.blit(font.render(_fmt_move(m), True, (30, 30, 30)), (x_blk, y))