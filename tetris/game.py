import random
import pygame
from tetris.interface import ABCGame
from tetris.piece import Piece
from tetris.screen import Screen
from tetris.display import Display
from consts import GameConsts


class Game(ABCGame):
    """
            A class to implement the Tetris game.
            ----------------------------
            Attributes
            ----------------------------
           ////////////////////////////
            ----------------------------
            Methods
            ----------------------------
            __init__(self):
             Constructs all the necessary attributes for the Game object.
             /////////////////////////////////////////
        """

    def __init__(self) -> None:
        """
            Constructs all the necessary attributes for the Game object.
        """
        self.display = Display()
        self.screen = Screen()
        self.current_shape_idx, self.next_shape_idx = random.randint(0, 6), random.randint(0, 6)
        self.score = 0

    def _is_game_over(self):
        pass

    def play(self):
        current_piece = Piece(5, 0, self.current_shape_idx)
        next_piece = Piece(3, 3, self.next_shape_idx)

        clock = pygame.time.Clock()
        run = True
        get_next_piece = False
        speed = GameConsts.STARTING_SPEED
        delta = 0
        level = 0

        while run:
            clock.tick()
            delta += clock.get_rawtime()
            level += clock.get_rawtime()

            self.screen.update_grid()
            next_positions = next_piece.decode_shape()

            if level > GameConsts.TIME:
                if speed > GameConsts.MAX_SPEED:  # smaller speed is faster
                    speed -= GameConsts.INC
                level = 0

            if delta > speed:
                current_piece.y += 1
                if not self.screen.is_valid_rotation(current_piece.decode_shape()):
                    current_piece.y -= 1
                    get_next_piece = True
                delta = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    run = False
                    pygame.display.quit()
                    quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not self.screen.is_valid_rotation(current_piece.decode_shape()):
                            current_piece.x += 1

                    elif event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not self.screen.is_valid_rotation(current_piece.decode_shape()):
                            current_piece.x -= 1

                    elif event.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if not self.screen.is_valid_rotation(current_piece.decode_shape()):
                            current_piece.y -= 1
                            get_next_piece = True

                    elif event.key == pygame.K_UP:
                        current_piece.rotate()
                        if not self.screen.is_valid_rotation(current_piece.decode_shape()):
                            current_piece.unrotate()

            if get_next_piece:
                for pos in current_piece.decode_shape():
                    self.screen.taken_positions[pos] = current_piece.color
                self.current_shape_idx = self.next_shape_idx
                self.next_shape_idx = random.randint(0, 6)
                current_piece = Piece(5, 0, self.current_shape_idx)
                next_piece = Piece(3, 3, self.next_shape_idx)
                get_next_piece = False

                self.screen.clear_filled_rows(self.screen.is_row_filled())

            for loc in current_piece.decode_shape():
                if loc[1] >= 0:
                    self.screen.grid[loc[1]][loc[0]] = current_piece.color

            if self.screen.is_game_over():
                # TODO implement game over
                print("game over")

            self.display.draw_screen(self.screen.grid, next_positions, next_piece.color, self.score)
