import pygame
from consts import DisplayConsts


class Display:
    """
        A class to implement the display of the game.
        ----------------------------
        Attributes
        ----------------------------
        window : pygame object
         an attribute to represent the screen of the game.
        ----------------------------
        Methods
        ----------------------------
        __init__(self):
         Constructs all the necessary attributes for the Display object.
        display_next_piece(self, piece):
         Displays the upcoming shape.
        display_score(self, score):
         Displays the score of the game.
        draw_screen(self, piece, next_piece, score):
         Uses pygame methods in order to display the ball and paddles.
    """
    def __init__(self) -> None:
        """
            Constructs all the necessary attributes for the Display object.
        """
        pygame.init()
        self.window = pygame.display.set_mode((DisplayConsts.SCREEN_WIDTH, DisplayConsts.SCREEN_HEIGHT))

    def draw_grid(self, grid) -> None:
        """
            Draws the tetris' grid.
        """
        top_left_x = DisplayConsts.TOP_LEFT_X
        top_left_y = DisplayConsts.TOP_LEFT_Y
        block_size = DisplayConsts.BLOCK_SIZE
        width = DisplayConsts.PLAY_WIDTH
        height = DisplayConsts.PLAY_HEIGHT

        for y in range(len(grid)):
            for x in range(len(grid[y])):
                pygame.draw.rect(self.window, grid[y][x],
                                 (top_left_x + x * block_size, top_left_y + y * block_size, block_size, block_size), 0)

        for y in range(len(grid) + 1):
            pygame.draw.line(self.window, DisplayConsts.GRID_COLOR,
                             (top_left_x,         top_left_y + y * block_size),
                             (top_left_x + width, top_left_y + y * block_size))
        for x in range(len(grid[0]) + 1):
            pygame.draw.line(self.window, DisplayConsts.GRID_COLOR,
                             (top_left_x + x * block_size, top_left_y),
                             (top_left_x + x * block_size, top_left_y + height))

        pygame.display.update()

    def display_next_piece(self, piece):
        """
            Displays the upcoming shape.
        """
        pass

    def display_score(self, score: int):
        """
            Displays the current game score.
        """
        pass

    def draw_screen(self, piece, next_piece, score: int):
        """
            Implements the animation of the falling piece.
                Parameters:
                    piece : current piece played.
                    next_piece: upcoming piece.
                    score: score of left player.
        """
        pass


