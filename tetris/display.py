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
        draw_grid(grid):
         Draws the tetris' grid.
        display_next_piece(self, positions, color):
         Displays the upcoming piece.
        display_score(self, score):
         Displays the score of the game.
        draw_screen(self, grid, positions, color, score):
         Displays a single frame of the game.
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

    def display_next_piece(self, positions: list, color: tuple):
        """
            Displays the upcoming shape.
        """
        font = pygame.font.SysFont(DisplayConsts.FONT, DisplayConsts.FONT_SIZE)
        label = font.render('Next Shape:', True, DisplayConsts.FONT_COLOR)
        top_left_x = int(DisplayConsts.TOP_LEFT_X + DisplayConsts.PLAY_WIDTH * 1.2)
        top_left_y = DisplayConsts.TOP_LEFT_Y + DisplayConsts.FONT_SIZE * 2
        bs = DisplayConsts.BLOCK_SIZE

        for loc in positions:
            pos_x = top_left_x + loc[0] * bs
            pos_y = top_left_y + loc[1] * bs
            pygame.draw.rect(self.window, color, (pos_x, pos_y, bs, bs), 0)
            pygame.draw.line(self.window, DisplayConsts.GRID_COLOR, (pos_x, pos_y), (pos_x + bs, pos_y))
            pygame.draw.line(self.window, DisplayConsts.GRID_COLOR, (pos_x, pos_y + bs), (pos_x + bs, pos_y + bs))
            pygame.draw.line(self.window, DisplayConsts.GRID_COLOR, (pos_x, pos_y), (pos_x, pos_y + bs))
            pygame.draw.line(self.window, DisplayConsts.GRID_COLOR, (pos_x + bs, pos_y), (pos_x + bs, pos_y + bs))

        self.window.blit(label, (top_left_x, top_left_y - 2 * bs))

    def display_score(self, score: int):
        """
            Displays the current game score.
        """
        font = pygame.font.SysFont(DisplayConsts.FONT, DisplayConsts.FONT_SIZE)
        txt = font.render('Score: ', True, DisplayConsts.FONT_COLOR)
        scr = font.render(str(score), True, DisplayConsts.FONT_COLOR)
        top_left_x = int(DisplayConsts.TOP_LEFT_X + DisplayConsts.PLAY_WIDTH * 1.2)
        top_left_y = int(DisplayConsts.TOP_LEFT_Y * 5)
        self.window.blit(txt, (top_left_x, top_left_y))
        self.window.blit(scr, (top_left_x + 100, top_left_y))

    def draw_game_over(self, score: int, highest_score: int) -> None:
        font = pygame.font.SysFont(DisplayConsts.FONT, DisplayConsts.FONT_SIZE)
        txt1 = font.render('Game over', True, DisplayConsts.FONT_COLOR)
        scr = font.render('Score: ' + str(score), True, DisplayConsts.FONT_COLOR)
        highest_scr = font.render('Highest Score: ' + str(highest_score), True, DisplayConsts.FONT_COLOR)
        txt2 = font.render('Press Space to continue', True, DisplayConsts.FONT_COLOR)
        display_x = DisplayConsts.TOP_LEFT_X + DisplayConsts.PLAY_WIDTH // 2 - DisplayConsts.FONT_SIZE // 2
        display_y = DisplayConsts.TOP_LEFT_Y + DisplayConsts.PLAY_HEIGHT // 2 - DisplayConsts.FONT_SIZE * 5
        buff = 60

        self.window.fill(DisplayConsts.BLACK)
        self.window.blit(txt1, (display_x, display_y))
        self.window.blit(txt2, (display_x, display_y + int(buff * 0.8)))
        self.window.blit(scr, (display_x, display_y + buff * 3))
        self.window.blit(highest_scr, (display_x, display_y + int(buff * 3.8)))

        pygame.display.update()

    def draw_screen(self, grid: list, positions: list, color: tuple, score: int) -> None:
        """
            Implements a frame of the game.
        """
        self.window.fill(DisplayConsts.BLACK)
        self.draw_grid(grid)
        self.display_next_piece(positions, color)
        self.display_score(score)

        pygame.time.Clock().tick(DisplayConsts.FPS)
        pygame.display.update()


