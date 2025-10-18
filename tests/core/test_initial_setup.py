from xiangqi.core.board import Board
from xiangqi.core.enums import PieceType, PieceColor

def test_total_piece_count():
    b = Board()
    assert len(b.pieces) == 32, "Phải có đúng 32 quân"

def test_each_side_has_general():
    b = Board()
    reds = [p for p in b.pieces if p.type is PieceType.GENERAL and p.color is PieceColor.RED]
    blacks = [p for p in b.pieces if p.type is PieceType.GENERAL and p.color is PieceColor.BLACK]
    assert len(reds) == 1 and len(blacks) == 1, "Mỗi bên đúng 1 tướng"

def test_soldier_count():
    b = Board()
    assert sum(1 for p in b.pieces if p.type is PieceType.SOLDIER) == 10, "Tổng 10 tốt"

def test_advisor_count():
    b = Board()
    assert sum(1 for p in b.pieces if p.type is PieceType.ADVISOR) == 4, "Mỗi bên 2 sĩ"

def test_elephant_count():
    b = Board()
    assert sum(1 for p in b.pieces if p.type is PieceType.ELEPHANT) == 4

def test_horse_count():
    b = Board()
    assert sum(1 for p in b.pieces if p.type is PieceType.HORSE) == 4

def test_rook_or_chariot_count():
    b = Board()
    # Nếu bạn dùng CHARIOT thay vì ROOK đổi tên tương ứng
    names = {p.type.name for p in b.pieces}
    target_name = "ROOK" if "ROOK" in names else "CHARIOT"
    assert sum(1 for p in b.pieces if p.type.name == target_name) == 4

# ...existing code...
def test_cannon_count():
    b = Board()
    assert sum(1 for p in b.pieces if p.type is PieceType.CANNON) == 4  # tổng 4 pháo
# ...existing code...
def test_cannon_each_side():
    b = Board()
    red = sum(1 for p in b.pieces if p.type is PieceType.CANNON and p.color is PieceColor.RED)
    black = sum(1 for p in b.pieces if p.type is PieceType.CANNON and p.color is PieceColor.BLACK)
    assert red == 2 and black == 2
# ...existing code...

def test_initial_general_positions():
    b = Board()
    # Tướng đỏ file 4 rank 0 ; tướng đen file 4 rank 9 (theo quy ước hiện tại)
    assert any(p.type is PieceType.GENERAL and p.color is PieceColor.RED and (p.file, p.rank) == (4, 0) for p in b.pieces)
    assert any(p.type is PieceType.GENERAL and p.color is PieceColor.BLACK and (p.file, p.rank) == (4, 9) for p in b.pieces)

def test_no_duplicate_piece_ids():
    b = Board()
    ids = [p.id for p in b.pieces]
    assert len(ids) == len(set(ids)), "ID quân không được trùng"

def test_all_pieces_on_board_grid_match():
    b = Board()
    # Mỗi quân chưa bị ăn phải đúng vị trí trên grid
    for p in b.pieces:
        if not p.captured:
            # Có thể None nếu grid lệch
            from_grid = b.piece_at(p.file, p.rank)
            assert from_grid is p, f"Grid lệch cho piece id={p.id}"