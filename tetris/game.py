import random
import pygame
from time import sleep

import consts
from tetris.interface import ABCGame
from tetris.piece import Piece
from tetris.screen import Screen
from tetris.display import Display
from tetris.event_handler import EventHandler
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
        side_key_press = False
        down_key_press = False
        speed = GameConsts.STARTING_SPEED
        left_right_key_refresh_rate = GameConsts.LEFT_RIGHT_KEY_REFRESH
        down_key_refresh_rate = GameConsts.DOWN_KEY_REFRESH
        delta = 0
        delta_side_key = 0
        delta_down_key = 0
        level = 0

        handler = EventHandler()

        while run:
            clock.tick()
            delta += clock.get_rawtime()
            delta_side_key += clock.get_rawtime()
            delta_down_key += clock.get_rawtime()
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

            if delta_side_key > left_right_key_refresh_rate:
                side_key_press = True
                delta_side_key = 0
            if delta_down_key > down_key_refresh_rate:
                down_key_press = True
                delta_down_key = 0

            event = handler.handle_events()

            if event == consts.Action.DOWN and down_key_press:
                current_piece.y += 1
                down_key_press = False
                if not self.screen.is_valid_rotation(current_piece.decode_shape()):
                    current_piece.y -= 1
                    get_next_piece = True

            if event == consts.Action.UP:
                current_piece.rotate()
                if not self.screen.is_valid_rotation(current_piece.decode_shape()):
                    current_piece.unrotate()

            if event == consts.Action.RIGHT and side_key_press:
                current_piece.x += 1
                side_key_press = False
                if not self.screen.is_valid_rotation(current_piece.decode_shape()):
                    current_piece.x -= 1

            if event == consts.Action.LEFT and side_key_press:
                current_piece.x -= 1
                side_key_press = False
                if not self.screen.is_valid_rotation(current_piece.decode_shape()):
                    current_piece.x += 1

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

                # TODO implement score

                # TODO make the game prettier

            self.display.draw_screen(self.screen.grid, next_positions, next_piece.color, self.score)
