#Hàm vẽ bàn cờ và quân cờ lên bề mặt pygame
from __future__ import annotations
from typing import Tuple
import pygame
from xiangqi.core.constants import BOARD_FILES, BOARD_RANKS, FILE_LETTERS
from xiangqi.core.board import Board
from xiangqi.core.enums import PieceColor
from xiangqi.ui.layout import Layout

Color = Tuple[int, int, int]
BG = (230, 200, 140)
GRID = (80, 60, 30)
RIVER_BG = (210, 180, 120)
PALACE_LINE = (100, 80, 40)

def draw_board(surface: pygame.Surface, layout: Layout) -> None:
    surface.fill(BG)
    ox, oy, cell = layout.origin_x, layout.origin_y, layout.cell
    # Ngang (10 hàng)
    for i in range(10):
        y = oy + i * cell
        x0 = ox
        x1 = ox + (9 - 1) * cell
        pygame.draw.line(surface, GRID, (x0, y), (x1, y), 2)

    river_split_rank = 4  # Chia sông ở hàng 4..5

    # Dọc (9 cột)
    for f in range(9):
        x = ox + f * cell
        y0 = oy
        y1 = oy + (10 - 1) * cell
        if f in (0, 8):
            pygame.draw.line(surface, GRID, (x, y0), (x, y1), 2)
        else:
            pygame.draw.line(surface, GRID, (x, y0), (x, oy + river_split_rank * cell), 2)
            pygame.draw.line(surface, GRID, (x, oy + (river_split_rank + 1) * cell), (x, y1), 2)
    # Sông
    river_rect = pygame.Rect(ox + 2, oy + river_split_rank * cell + 2, (9 - 1) * cell - 2, cell - 2)
    pygame.draw.rect(surface, RIVER_BG, river_rect, 0)
    # Cung
    def pt(f: int, r: int): return layout.square_to_px(f, r)
    pygame.draw.line(surface, PALACE_LINE, pt(3, 0), pt(5, 2), 2)
    pygame.draw.line(surface, PALACE_LINE, pt(5, 0), pt(3, 2), 2)
    pygame.draw.line(surface, PALACE_LINE, pt(3, 9), pt(5, 7), 2)
    pygame.draw.line(surface, PALACE_LINE, pt(5, 9), pt(3, 7), 2)

def draw_pieces(surface: pygame.Surface, board: Board, images, layout: Layout) -> None:
    for p in board.pieces:
        if p.captured:
            continue
        rect = layout.piece_rect_centered(p.file, p.rank, scale=0.84)
        img = images.get((p.color, p.type))
        if img is None:
            cx, cy = layout.square_to_px(p.file, p.rank)
            radius = int(layout.cell * 0.4)
            color = (200, 40, 40) if p.color is PieceColor.RED else (40, 40, 40)
            pygame.draw.circle(surface, (240, 240, 220), (cx, cy), radius)
            pygame.draw.circle(surface, (80, 80, 80), (cx, cy), radius, 2)
            pygame.draw.circle(surface, color, (cx, cy), max(2, radius // 8))
        else:
            surface.blit(img, rect)

def draw_file_labels(surface: pygame.Surface, layout, font: pygame.font.Font, letters: str = FILE_LETTERS) -> None:
    ox, oy, cell = layout.origin_x, layout.origin_y, layout.cell
    y_bottom = oy + (BOARD_RANKS - 1) * cell + int(cell * 0.55)
    # nếu cần cả phía trên, có thể thêm y_top
    for f in range(BOARD_FILES):
        x = ox + f * cell
        ch = letters[f] if f < len(letters) else str(f)
        surf = font.render(ch, True, (60, 60, 60))
        rect = surf.get_rect(center=(x, y_bottom))
        surface.blit(surf, rect)

def draw_rank_labels(surface: pygame.Surface, layout, font: pygame.font.Font) -> None:
    ox, cell = layout.origin_x, layout.cell
    x_left  = ox - int(cell * 0.70)
    for r in range(BOARD_RANKS):
        # dùng layout.square_to_px để lấy đúng tọa độ Y theo hướng red_at_bottom
        _, y = layout.square_to_px(0, r)
        label = str(r)  # nếu muốn 1..10: label = str(r + 1)
        surf = font.render(label, True, (60, 60, 60))
        rect_l = surf.get_rect(center=(x_left, y))
        surface.blit(surf, rect_l)

def render(surface: pygame.Surface, board: Board, images, layout: Layout) -> None:
    draw_board(surface, layout)
    draw_pieces(surface, board, images, layout)