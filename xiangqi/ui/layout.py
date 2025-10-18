#Hàm định nghĩa bố cục giao diện người dùng
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple
from xiangqi.core.constants import BOARD_FILES, BOARD_RANKS

@dataclass(slots=True)
class Layout:
    win_w: int = 800
    win_h: int = 900
    margin: int = 40 # Lề
    red_at_bottom: bool = True  # rank 0 ở dưới
    sidebar_w: int = 0  # Chiều rộng thanh bên

    # Computed fields
    cell: int = field(init=False)
    origin_x: int = field(init=False)
    origin_y: int = field(init=False)


    # Tính toán các giá trị phụ thuộc
    def __post_init__(self) -> None:
        # Tính kích thước cửa sổ, trừ lề
        usable_w = self.win_w - 2 * self.margin - self.sidebar_w
        usable_h = self.win_h - 2 * self.margin

        # Kích thước ô vuông
        cell_w = usable_w / (BOARD_FILES - 1)
        cell_h = usable_h / (BOARD_RANKS - 1)
        self.cell = int(min(cell_w, cell_h))

        # Kích thước lưới thực tế: 8 khoảng ngang, 9 khoảng dọc
        grid_w = self.cell * (BOARD_FILES - 1)
        grid_h = self.cell * (BOARD_RANKS - 1)
        self.origin_x = self.margin + (usable_w - grid_w) // 2
        self.origin_y = (self.win_h - grid_h) // 2

    # Đổi từ (file, rank) sang pixel (tọa độ góc trên bên trái ô vuông)
    def square_to_px(self, file_: int, rank: int) -> Tuple[int, int]:
        x = self.origin_x + file_ * self.cell
        y = self.origin_y + (BOARD_RANKS - 1 - rank) * self.cell if self.red_at_bottom else self.origin_y + rank * self.cell
        return x, y
    
    # Trả về hình chữ nhật (x, y, w, h) để vẽ quân cờ, căn giữa ô vuông
    def piece_rect_centered(self, file_: int, rank: int, scale: float = 0.84) -> Tuple[int, int, int, int]:
        cx, cy = self.square_to_px(file_, rank)
        size = int(self.cell * scale)
        return (cx - size // 2, cy - size // 2, size, size)

    # Đổi pixel (x, y) sang (file, rank) nếu click gần giao điểm trong bán kính snap_radius*cell
    def px_to_square(self, x: int, y: int, snap_radius: float = 0.45):
        """
        Đổi pixel -> (file, rank) nếu click gần giao điểm trong bán kính snap_radius*cell.
        Trả về None nếu click ngoài lưới/xa tâm.
        """
        fx = (x - self.origin_x) / self.cell
        ry = (y - self.origin_y) / self.cell
        if self.red_at_bottom:
            ry = (BOARD_RANKS - 1) - ry
        cf = round(fx)
        cr = round(ry)
        if not (0 <= cf < BOARD_FILES and 0 <= cr < BOARD_RANKS):
            return None
        cx, cy = self.square_to_px(cf, cr)
        dx, dy = x - cx, y - cy
        if (dx * dx + dy * dy) ** 0.5 <= self.cell * snap_radius:
            return (cf, cr)
        return None