from xiangqi.core.board import Board

def test_board_constructs():
    b = Board()
    assert len(b.pieces) == 32