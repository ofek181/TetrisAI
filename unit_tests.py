from tetris.piece import Piece
from tetris.logic import Logic


def test():
    # __________________________________________________
    # Piece object Tests
    # __________________________________________________
    # piece1 = Piece(100, 200, 0)
    # piece2 = Piece(100, 200, 1000)
    # piece3 = Piece(100, 200, -2)
    # tmp = piece1.decode_shape()
    # piece1.rotate()
    # print(tmp)
    # tmp = piece1.decode_shape()
    # piece1.rotate()
    # print(tmp)
    # tmp = piece1.decode_shape()
    # print(tmp)
    # __________________________________________________
    # Logic object Tests
    # __________________________________________________
    logic = Logic()
    # print(logic.grid)
    # print(len(logic.grid[3]))
    # print(len(logic.grid[:][:]))
    # print(len(logic.grid[0]))
    for i in range(10):
        logic.taken_positions[(i, 3)] = (255, 255, 255)
        logic.taken_positions[(i, 5)] = (200, 5, 5)
    logic.update_grid()
    # print(logic.grid[:][3])
    print(logic.is_row_cleared())


if __name__ == '__main__':
    test()
