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
        display:
         an attribute to represent the display of the game.
        screen:
         an attribute to represent the screen and logic of the game.
        current_shape_idx:
         the current piece's shape.
        next_shape_idx:
         the next piece's shape.
        score:
         current score of the game.
        ----------------------------
        Methods
        ----------------------------
        __init__(self):
         Constructs all the necessary attributes for the Display object.
        play(self, is_player_human, audio)
         Main loop of the game. Containing all the logic and implementations for Tetris.
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
        """
            Main loop of the game. Containing all the logic and implementations for Tetris.
        """
        # initiate objects and variables
        current_piece = Piece(5, 0, self.current_shape_idx)
        next_piece = Piece(3, 3, self.next_shape_idx)

        clock = pygame.time.Clock()
        run = True
        get_next_piece = False
        down_key_press = False
        check_collision = False
        speed = GameConsts.STARTING_SPEED
        down_key_refresh_rate = GameConsts.DOWN_KEY_REFRESH
        delta = 0
        delta_down_key = 0
        level = 0

        handler = EventHandler()
        if audio:
            Audio.theme()

        # main loop of the game
        while run:
            # use time for the changing the difficulty and speed of the game.
            clock.tick()
            delta += clock.get_rawtime()
            delta_down_key += clock.get_rawtime()
            level += clock.get_rawtime()
            next_positions = next_piece.decode_shape()

            self.screen.update_grid()

            # decrease the spawn time of new pieces as the game progresses.
            if level > GameConsts.TIME:
                if speed > GameConsts.MAX_SPEED:
                    speed -= GameConsts.INC
                level = 0

            # if a user doesnt press down_key then gravity occurs.
            if delta > speed and down_key_press:
                current_piece.y += 1
                if not self.screen.is_valid_rotation(current_piece.decode_shape()):
                    current_piece.y -= 1
                    check_collision = True
                delta = 0

            # the user can press the down key but we need to make sure the pieces doesnt fall immediately.
            if delta_down_key > down_key_refresh_rate:
                down_key_press = True
                delta_down_key = 0

            # handle the different user's actions during the game.
            event = handler.handle_events()

            if event == consts.Action.DOWN and down_key_press:
                current_piece.y += 1
                down_key_press = False
                if not self.screen.is_valid_rotation(current_piece.decode_shape()):
                    current_piece.y -= 1
                    check_collision = True

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

            # check for collisions with ground or other pieces.
            # important the case where at the start of the frame the piece was in a collided positions
            # but a user's input made it so that it now in a valid position
            # in that case, get_next_piece needs to be False because a collision did not occur.
            if check_collision:
                current_piece.y += 1
                # checks for collisions with other pieces
                for pos in current_piece.decode_shape():
                    if pos in self.screen.taken_positions:
                        get_next_piece = True

                # checks for collisions with the ground
                if not get_next_piece:
                    if current_piece.y >= GameConsts.GRID_HEIGHT:
                        if not self.screen.is_valid_rotation(current_piece.decode_shape()):
                            get_next_piece = True

                current_piece.y -= 1
                check_collision = False

            # handles the event of a collision and gets a new piece into the grid.
            if get_next_piece:
                for pos in current_piece.decode_shape():
                    self.screen.taken_positions[pos] = current_piece.color
                self.current_shape_idx = self.next_shape_idx
                next_idx = random.randint(0, 6)
                while self.current_shape_idx == next_idx:
                    next_idx = random.randint(0, 6)
                self.next_shape_idx = next_idx
                current_piece = Piece(5, 0, self.current_shape_idx)
                next_piece = Piece(3, 3, self.next_shape_idx)
                get_next_piece = False

                rows = self.screen.is_row_filled()
                if len(rows) > 0:
                    Audio.clear()
                self.screen.clear_filled_rows(rows)
                self.score += self.screen.get_score(len(rows))

            # checks if the current score is greater than the highest score and saves it.
            highest_score = self.screen.update_highest_score(self.score)

            # checks if the user lost and handles the game over screen and audio.
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
                self.play(is_player_human, audio)

            # refreshes the display with respect to the FPS of the game.
            self.display.draw_screen(self.screen.grid, next_positions, next_piece.color, self.score)
