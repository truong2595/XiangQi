
BOARD_FILES = 9  # files (cột)
BOARD_RANKS = 10   # ranks (hàng)
FILE_LETTERS = "ABCDEFGHI"

# Palace (files 3..5, ranks khác nhau theo màu)
PALACE_FILES = (3, 4, 5)
PALACE_RANKS_RED = (0, 1, 2)
PALACE_RANKS_BLACK = (7, 8, 9)

# River: ranh giữa rank 4 và 5
RIVER_DIVIDER = 4  # rank <=4: phía RED; rank >=5: phía BLACK

# Khởi tạo (file, rank, color, type)
# (Có thể thay bằng load từ FEN tùy chỉnh sau)
INITIAL_PIECES = [
    # RED back rank
    (0, 0, "red",   "chariot"),
    (1, 0, "red",   "horse"),
    (2, 0, "red",   "elephant"),
    (3, 0, "red",   "advisor"),
    (4, 0, "red",   "general"),
    (5, 0, "red",   "advisor"),
    (6, 0, "red",   "elephant"),
    (7, 0, "red",   "horse"),
    (8, 0, "red",   "chariot"),
    # RED cannons
    (1, 2, "red",   "cannon"),
    (7, 2, "red",   "cannon"),
    # RED soldiers
    (0, 3, "red",   "soldier"),
    (2, 3, "red",   "soldier"),
    (4, 3, "red",   "soldier"),
    (6, 3, "red",   "soldier"),
    (8, 3, "red",   "soldier"),
    # BLACK back rank
    (0, 9, "black", "chariot"),
    (1, 9, "black", "horse"),
    (2, 9, "black", "elephant"),
    (3, 9, "black", "advisor"),
    (4, 9, "black", "general"),
    (5, 9, "black", "advisor"),
    (6, 9, "black", "elephant"),
    (7, 9, "black", "horse"),
    (8, 9, "black", "chariot"),
    # BLACK cannons
    (1, 7, "black", "cannon"),
    (7, 7, "black", "cannon"),
    # BLACK soldiers
    (0, 6, "black", "soldier"),
    (2, 6, "black", "soldier"),
    (4, 6, "black", "soldier"),
    (6, 6, "black", "soldier"),
    (8, 6, "black", "soldier"),
]

# Offsets di chuyển cơ bản
ADVISOR_OFFSETS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
GENERAL_OFFSETS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
ELEPHANT_OFFSETS = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
ELEPHANT_EYE_MAP = {  # offset -> ô “mắt” phải trống
    (-2, -2): (-1, -1),
    (-2,  2): (-1,  1),
    ( 2, -2): ( 1, -1),
    ( 2,  2): ( 1,  1),
}
HORSE_OFFSETS = [
    (-2, -1), (-2, 1), (2, -1), (2, 1),
    (-1, -2), (1, -2), (-1, 2), (1, 2),
]
# Map từ delta cuối -> ô chân phải trống
HORSE_LEG_MAP = {
    (-2, -1): (-1, 0),
    (-2,  1): (-1, 0),
    ( 2, -1): ( 1, 0),
    ( 2,  1): ( 1, 0),
    (-1, -2): (0, -1),
    ( 1, -2): (0, -1),
    (-1,  2): (0,  1),
    ( 1,  2): (0,  1),
}

# Hướng tiến của tốt (giả sử RED đi tăng rank, BLACK giảm rank; tùy bạn thống nhất)
SOLDIER_FORWARD = {
    "red": 1,
    "black": -1,
}

# Giá trị quân (AI sơ bộ)
PIECE_VALUES = {
    "general": 10000,
    "advisor": 20,
    "elephant": 20,
    "horse": 45,
    "chariot": 90,
    "cannon": 50,
    "soldier": 10,
}

# Mapping file index -> ký tự (CLI / notation)
FILE_LETTERS = "abcdefghi"