from tetris.piece import Piece


def test():
    # Piece object Tests
    # __________________________________________________
    piece1 = Piece(100, 200, 0)
    # piece2 = Piece(100, 200, 1000)
    # piece3 = Piece(100, 200, -2)
    tmp = piece1.decode_shape()
    piece1.rotate()
    print(tmp)
    tmp = piece1.decode_shape()
    piece1.rotate()
    print(tmp)
    tmp = piece1.decode_shape()
    print(tmp)
    # __________________________________________________


if __name__ == '__main__':
    test()
