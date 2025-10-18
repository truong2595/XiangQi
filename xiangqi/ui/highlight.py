#Hàm vẽ hiệu ứng highlight trên bàn cờ
import pygame
from typing import Iterable, Tuple, Optional
from xiangqi.core.moves import Move
from xiangqi.ui.layout import Layout

def draw_highlights(surface: pygame.Surface,
                    layout: Layout,
                    selected: Optional[Tuple[int, int]],
                    moves: Iterable[Move]) -> None:
    # Ô đang chọn
    if selected is not None:
        f, r = selected
        cx, cy = layout.square_to_px(f, r)
        pygame.draw.circle(surface, (255, 215, 0), (cx, cy), int(layout.cell * 0.48), 3)

    # Nước hợp lệ từ ô đang chọn
    for mv in moves:
        cx, cy = layout.square_to_px(mv.to_file, mv.to_rank)
        if getattr(mv, "captured_id", None):
            # nước bắt: vòng đỏ
            pygame.draw.circle(surface, (0, 250, 0), (cx, cy), int(layout.cell * 0.36), 3)
        else:
            # nước đi thường: chấm xanh
            pygame.draw.circle(surface, (60, 160, 60), (cx, cy), int(layout.cell * 0.14), 0)