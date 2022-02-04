import random
import pygame
from time import sleep

import consts
from tetris.interface import ABCGame
from tetris.piece import Piece
from tetris.screen import Screen
from tetris.display import Display
from tetris.event_handler import EventHandler
from tetris.sound import Audio
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

    def play(self, is_player_human: bool = True, audio: bool = True) -> None:
        current_piece = Piece(5, 0, self.current_shape_idx)
        next_piece = Piece(3, 3, self.next_shape_idx)

        clock = pygame.time.Clock()
        run = True
        get_next_piece = False
        down_key_press = False
        speed = GameConsts.STARTING_SPEED
        down_key_refresh_rate = GameConsts.DOWN_KEY_REFRESH
        delta = 0
        delta_down_key = 0
        level = 0

        handler = EventHandler()
        if audio:
            Audio.theme()

        while run:
            clock.tick()
            delta += clock.get_rawtime()
            delta_down_key += clock.get_rawtime()
            level += clock.get_rawtime()

            self.screen.update_grid()
            next_positions = next_piece.decode_shape()

            if level > GameConsts.TIME:
                if speed > GameConsts.MAX_SPEED:  # smaller speed is faster
                    speed -= GameConsts.INC
                level = 0

            if delta > speed and down_key_press:
                current_piece.y += 1
                if not self.screen.is_valid_rotation(current_piece.decode_shape()):
                    current_piece.y -= 1
                    get_next_piece = True
                delta = 0

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

            if event == consts.Action.RIGHT:
                current_piece.x += 1

                if not self.screen.is_valid_rotation(current_piece.decode_shape()):
                    current_piece.x -= 1

            if event == consts.Action.LEFT:
                current_piece.x -= 1
                if not self.screen.is_valid_rotation(current_piece.decode_shape()):
                    current_piece.x += 1

            for loc in current_piece.decode_shape():
                if loc[1] >= 0:
                    self.screen.grid[loc[1]][loc[0]] = current_piece.color

            if get_next_piece:
                for pos in current_piece.decode_shape():
                    self.screen.taken_positions[pos] = current_piece.color
                self.current_shape_idx = self.next_shape_idx
                self.next_shape_idx = random.randint(0, 6)
                current_piece = Piece(5, 0, self.current_shape_idx)
                next_piece = Piece(3, 3, self.next_shape_idx)
                get_next_piece = False

                rows = self.screen.is_row_filled()
                if len(rows) > 0:
                    Audio.clear()
                self.screen.clear_filled_rows(rows)
                self.score += self.screen.get_score(len(rows))

            highest_score = self.screen.update_highest_score(self.score)

            if self.screen.is_game_over():
                if audio:
                    Audio.game_over()

                if is_player_human:
                    self.display.draw_game_over(self.score, highest_score)
                    sleep(2)
                    action = False
                    while not action:
                        action = handler.handle_events_for_game_over()

                self.__init__()
                self.play(is_player_human)

            self.display.draw_screen(self.screen.grid, next_positions, next_piece.color, self.score)
