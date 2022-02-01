from tetris.piece import Piece
from tetris.screen import Screen
from tetris.display import Display
import pygame


def test():
    # __________________________________________________
    # Piece Tests
    # __________________________________________________
    # piece1 = Piece(100, 200, 0)
    # for _ in range(3):
    #     print(piece1.get_random_shape())
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
    # Logic Tests
    # __________________________________________________
    # logic = Screen()
    # piece = Piece(0, 2, 3)
    # print(logic.grid)
    # print(len(logic.grid[3]))
    # print(len(logic.grid[:][:]))
    # print(len(logic.grid[0]))
    # for i in range(10):
    #     logic.taken_positions[(i, 0)] = (255, 255, 255)
    #     logic.taken_positions[(i, 2)] = (200, 5, 5)
    # logic.taken_positions[(0, 1)] = (1, 1, 1)
    # logic.taken_positions[(1, 1)] = (2, 2, 2)
    # # logic.taken_positions[(0, 3)] = (3, 3, 3)
    # logic.update_grid()
    # print(logic.taken_positions)
    # pos = piece.decode_shape()
    # print(logic.is_collision(pos, piece.color))
    # print(logic.taken_positions)
    # print(logic.grid)
    # filled_rows = logic.is_row_filled()
    # logic.clear_filled_rows(filled_rows)
    # print(logic.grid)
    # logic.update_grid()
    # print(logic.grid)
    # __________________________________________________
    # Display Tests
    # __________________________________________________
    display = Display()
    screen = Screen()
    piece1 = Piece(5, 5, 6)
    piece2 = Piece(3, 3, 2)
    positions1 = piece1.decode_shape()
    positions2 = piece2.decode_shape()
    for pos in positions1:
        screen.taken_positions[pos] = piece1.color
    screen.update_grid()
    while 1:
        display.draw_grid(screen.grid)
        display.display_next_piece(positions2, piece2.color)
        display.display_score(1000)
        pygame.display.update()


if __name__ == '__main__':
    test()
