#Hàm nạp ảnh assets quân cờ
from __future__ import annotations
import pathlib
from typing import Dict, Tuple, Iterable, Optional
import pygame
from xiangqi.core.enums import PieceType, PieceColor

# Gốc assets, tạo đường đẫn tuyệt đối đến assets
ASSETS_DIR = pathlib.Path(__file__).resolve().parents[2] / "assets"

# Map type -> tên file trong bộ English/Chinese
NAME_EN = {
    PieceType.CHARIOT: "Rook",
    PieceType.HORSE: "Horse",
    PieceType.ELEPHANT: "Elephant",
    PieceType.ADVISOR: "Advisor",
    PieceType.GENERAL: "King",    # General = King trong asset
    PieceType.CANNON: "Cannon",
    PieceType.SOLDIER: "Pawn",
}
# Chinese bộ này cũng dùng English tên file (Chinese-Rook-Red.png, Chinese-King-Red.png, ...)
NAME_CN = NAME_EN

ABBREV = {
    PieceType.CHARIOT: "XE",
    PieceType.HORSE: "MÃ",
    PieceType.ELEPHANT: "TG",
    PieceType.ADVISOR: "SĨ",
    PieceType.GENERAL: "TG",
    PieceType.CANNON: "PH",
    PieceType.SOLDIER: "TT",
}

def _color_dir(color: PieceColor) -> str:
    return "Red" if color is PieceColor.RED else "Black"

def _candidate_paths(color: PieceColor, ptype: PieceType, preferred_theme: Optional[str]) -> Iterable[pathlib.Path]:
    # Thứ tự thử: preferred_theme (nếu có) -> English -> Chinese
    order = []
    if preferred_theme in ("English", "Chinese"):
        order.append(preferred_theme)
    order.extend([t for t in ("English", "Chinese") if t != preferred_theme])

    for theme in order:
        name = (NAME_EN if theme == "English" else NAME_CN)[ptype]
        fname = f"{theme}-{name}-{_color_dir(color)}.png"
        yield ASSETS_DIR / "Pieces" / theme / _color_dir(color) / fname

def _load_or_fallback(size: int, color: PieceColor, ptype: PieceType, preferred_theme: Optional[str]) -> pygame.Surface:
    # Thử lần lượt các path ứng viên
    for path in _candidate_paths(color, ptype, preferred_theme):
        if path.exists():
            img = pygame.image.load(str(path)).convert_alpha()
            return pygame.transform.smoothscale(img, (size, size))
    # Fallback vẽ tròn + chữ nếu không tìm thấy ảnh
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    import pygame.gfxdraw as gfx
    col = (200, 40, 40) if color is PieceColor.RED else (40, 40, 40)
    gfx.filled_circle(surf, size // 2, size // 2, size // 2 - 2, (240, 240, 220))
    gfx.aacircle(surf, size // 2, size // 2, size // 2 - 2, (80, 80, 80))
    font = pygame.font.SysFont("arial", max(14, size // 4), bold=True)
    text = font.render(ABBREV[ptype], True, col)
    rect = text.get_rect(center=(size // 2, size // 2))
    surf.blit(text, rect)
    return surf

def load_piece_images(cell_size: int, preferred_theme: Optional[str] = None) -> Dict[Tuple[PieceColor, PieceType], pygame.Surface]:
    """
    Nạp ảnh quân theo cấu trúc:
      assets/Pieces/{English|Chinese}/{Red|Black}/{Theme}-{Name}-{Color}.png
    preferred_theme: "English" | "Chinese" | None (auto thử English rồi Chinese)
    """
    images: Dict[Tuple[PieceColor, PieceType], pygame.Surface] = {}
    size = int(cell_size * 0.8)
    for color in (PieceColor.RED, PieceColor.BLACK):
        for ptype in PieceType:
            images[(color, ptype)] = _load_or_fallback(size, color, ptype, preferred_theme)
    return images