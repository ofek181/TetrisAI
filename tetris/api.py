import random
import numpy

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
        self.ungrabbed_bag = [0, 1, 2, 3, 4, 5, 6]
        self.current_shape_idx = self.seven_bag()
        self.next_shape_idx = self.seven_bag()
        self.score = 0
        self.game_over = False

        self.current_piece = Piece(5, 0, self.current_shape_idx)
        self.next_piece = Piece(3, 3, self.next_shape_idx)
        self.get_next_piece = False

    def seven_bag(self) -> int:
        if len(self.ungrabbed_bag) == 0:
            self.ungrabbed_bag = [0, 1, 2, 3, 4, 5, 6]
        shape = random.choice(self.ungrabbed_bag)
        self.ungrabbed_bag.remove(shape)
        return shape

    def reset(self, fps) -> None:
        """
            Resets the environment
        """
        self.__init__()
        self.play(Action.IDLE, fps)

    def get_state(self) -> numpy.ndarray:
        """
            returns a vector of 1s and 0s, 1 if there is a tetrimino and 0 if not.
            appended with the the next piece' shape.
        """
        state = [[0 for _ in range(GameConsts.GRID_WIDTH)] for _ in range(GameConsts.GRID_HEIGHT)]

        for y in range(len(self.screen.grid)):
            for x in range(len(self.screen.grid[y])):
                if self.screen.grid[y][x] != GameConsts.GRID_FILL:
                    state[y][x] = 1

        return numpy.asarray(state)

    def get_data(self) -> list:
        state = [[0 for _ in range(GameConsts.GRID_WIDTH)] for _ in range(GameConsts.GRID_HEIGHT)]

        for y in range(len(self.screen.grid)):
            for x in range(len(self.screen.grid[y])):
                if self.screen.grid[y][x] != GameConsts.GRID_FILL:
                    state[y][x] = 1

        flat_list = []
        for sublist in state:
            for item in sublist:
                flat_list.append(item)

        flat_list.append(self.current_shape_idx)
        flat_list.append(self.current_piece.y)
        flat_list.append(self.current_piece.x)
        flat_list.append(self.current_piece.rotation)
        flat_list.append(self.next_shape_idx)

        return flat_list

    def _step(self, action) -> None:
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

        if action == Action.IDLE:
            pass

    def play(self, action: Action, fps: int, disable_graphics: bool = False) -> None:
        self.get_next_piece = False
        self.screen.update_grid()

        # implements gravity.
        self.current_piece.y += 1
        if not self.screen.is_valid_rotation(self.current_piece.decode_shape()):
            self.current_piece.y -= 1

        self._step(action)

        for loc in self.current_piece.decode_shape():
            if loc[1] >= 0:
                self.screen.grid[loc[1]][loc[0]] = self.current_piece.color

        # check for collisions with ground or other pieces.
        self.current_piece.y += 1
        for pos in self.current_piece.decode_shape():
            if pos in self.screen.taken_positions:
                self.get_next_piece = True

        if not self.get_next_piece:
            for pos in self.current_piece.decode_shape():
                if pos[1] >= GameConsts.GRID_HEIGHT:
                    self.get_next_piece = True
        self.current_piece.y -= 1

        # handles the event of a collision and gets a new piece into the grid.
        if self.get_next_piece:
            for pos in self.current_piece.decode_shape():
                self.screen.taken_positions[pos] = self.current_piece.color
            self.current_shape_idx = self.next_shape_idx
            self.next_shape_idx = self.seven_bag()
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
        if not disable_graphics:
            self.display.draw_screen(self.screen.grid, self.next_piece.decode_shape(),
                                     self.next_piece.color, self.score, fps)
