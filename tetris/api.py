import random

from tetris.piece import Piece
from tetris.screen import Screen
from tetris.display import Display
from consts import GameConsts, Action


class Environment:
    """
        A class to implement the environment of the Tetris game.
    """
    def __init__(self) -> None:
        """
            Constructs all the necessary attributes for the Game object.
        """
        self.display = Display()
        self.screen = Screen()
        self.current_shape_idx, self.next_shape_idx = random.randint(0, 6), random.randint(0, 6)
        while self.current_shape_idx == self.next_shape_idx:
            self.next_shape_idx = random.randint(0, 6)
        self.score = 0
        self.game_over = False

        self.current_piece = Piece(5, 0, self.current_shape_idx)
        self.next_piece = Piece(3, 3, self.next_shape_idx)

    def reset(self) -> None:
        """
            Resets the environment
        """
        self.__init__()
        self.play()

    def get_state(self) -> tuple[list, int]:
        """
            returns a wXh matrix of 1s and 0s, 1 if there is a tetrimino and 0 if not.
            also returns the next piece shape.
        """
        state = [[0 for _ in range(GameConsts.GRID_WIDTH)] for _ in range(GameConsts.GRID_HEIGHT)]

        for y in range(len(self.screen.grid)):
            for x in range(len(self.screen.grid[y])):
                if self.screen.grid[y][x] != GameConsts.GRID_FILL:
                    state[y][x] = 1

        return state, self.next_shape_idx

    def step(self, action) -> None:
        """
            Step function where the user (AI) can enter an action of play.
        """
        if action == Action.UP:
            self.current_piece.rotate()
            if not self.screen.is_valid_rotation(self.current_piece.decode_shape()):
                self.current_piece.unrotate()

        if action == Action.LEFT:
            self.current_piece.x += 1
            if not self.screen.is_valid_rotation(self.current_piece.decode_shape()):
                self.current_piece.x -= 1

        if action == Action.RIGHT:
            self.current_piece.x -= 1
            if not self.screen.is_valid_rotation(self.current_piece.decode_shape()):
                self.current_piece.x += 1

    def play(self):
        get_next_piece = False
        self.screen.update_grid()

        # implements gravity.
        self.current_piece.y += 1
        if not self.screen.is_valid_rotation(self.current_piece.decode_shape()):
            self.current_piece.y -= 1

        for loc in self.current_piece.decode_shape():
            if loc[1] >= 0:
                self.screen.grid[loc[1]][loc[0]] = self.current_piece.color

        # check for collisions with ground or other pieces.
        self.current_piece.y += 1
        for pos in self.current_piece.decode_shape():
            if pos in self.screen.taken_positions:
                get_next_piece = True

        if not get_next_piece:
            if self.current_piece.y >= GameConsts.GRID_HEIGHT:
                if not self.screen.is_valid_rotation(self.current_piece.decode_shape()):
                    get_next_piece = True
        self.current_piece.y -= 1

        # handles the event of a collision and gets a new piece into the grid.
        if get_next_piece:
            for pos in self.current_piece.decode_shape():
                self.screen.taken_positions[pos] = self.current_piece.color
            self.current_shape_idx = self.next_shape_idx
            next_idx = random.randint(0, 6)
            while self.current_shape_idx == next_idx:
                next_idx = random.randint(0, 6)
            self.next_shape_idx = next_idx
            self.current_piece = Piece(5, 0, self.current_shape_idx)
            self.next_piece = Piece(3, 3, self.next_shape_idx)

            rows = self.screen.is_row_filled()
            self.screen.clear_filled_rows(rows)
            self.score += self.screen.get_score(len(rows))

        # # checks if the current score is greater than the highest score and saves it.
        # highest_score = self.screen.update_highest_score(self.score)

        # checks if the user lost and handles the game over screen and audio.
        if self.screen.is_game_over():
            self.game_over = True
            # self.reset()

        # refreshes the display with respect to the FPS of the game.
        self.display.draw_screen(self.screen.grid, self.next_piece.decode_shape(),
                                 self.next_piece.color, self.score)
