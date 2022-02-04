from enum import Enum
import os
local_dir_audio = os.path.join(os.path.dirname(__file__), "audio")

class AudioConsts:
    CLEAR = os.path.join(local_dir_audio, 'Clear.wav')
    GAMEOVER = os.path.join(local_dir_audio, 'Gameover.wav')
    THEME = os.path.join(local_dir_audio, 'Theme.mp3')


class DisplayConsts:
    FPS = 30
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    PLAY_WIDTH = 250
    PLAY_HEIGHT = PLAY_WIDTH * 2
    BLOCK_SIZE = PLAY_WIDTH // 10
    TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 8
    TOP_LEFT_Y = (SCREEN_HEIGHT - PLAY_HEIGHT) // 2
    GRID_COLOR = (200, 200, 200)
    FONT = 'comicsans'
    FONT_SIZE = 30
    FONT_COLOR = (220, 220, 220)
    BLACK = (0, 0, 0)


class GameConsts:
    GRID_WIDTH = 10
    GRID_HEIGHT = 20
    GRID_FILL = (20, 20, 20)
    STARTING_SPEED = 350
    TIME = 4000
    DOWN_KEY_REFRESH = 20
    MAX_SPEED = 100
    INC = 2


class Action(Enum):
    DOWN = 0
    UP = 1
    RIGHT = 2
    LEFT = 3


class PieceConsts:
    PIECE_SIZE = 10
    GREEN = (114, 203, 59)
    RED = (255, 50, 19)
    CYAN = (0, 190, 200)
    YELLOW = (255, 213, 0)
    BLUE = (3, 65, 174)
    ORANGE = (255, 151, 28)
    PURPLE = (128, 0, 128)

    S = [['.....',
          '.....',
          '..00.',
          '.00..',
          '.....'],
         ['.....',
          '.0...',
          '.00..',
          '..0..',
          '.....']]

    Z = [['.....',
          '.....',
          '.00..',
          '..00.',
          '.....'],
         ['.....',
          '...0.',
          '..00.',
          '..0..',
          '.....']]

    I = [['.....',
          '.0...',
          '.0...',
          '.0...',
          '.0...'],
         ['.....',
          '0000.',
          '.....',
          '.....',
          '.....']]

    O = [['.....',
          '.....',
          '.00..',
          '.00..',
          '.....']]

    J = [['.....',
          '.0...',
          '.000.',
          '.....',
          '.....'],
         ['.....',
          '..00.',
          '..0..',
          '..0..',
          '.....'],
         ['.....',
          '.....',
          '.000.',
          '...0.',
          '.....'],
         ['.....',
          '..0..',
          '..0..',
          '.00..',
          '.....']]

    L = [['.....',
          '...0.',
          '.000.',
          '.....',
          '.....'],
         ['.....',
          '..0..',
          '..0..',
          '..00.',
          '.....'],
         ['.....',
          '.....',
          '.000.',
          '.0...',
          '.....'],
         ['.....',
          '.00..',
          '..0..',
          '..0..',
          '.....']]

    T = [['.....',
          '..0..',
          '.000.',
          '.....',
          '.....'],
         ['.....',
          '..0..',
          '..00.',
          '..0..',
          '.....'],
         ['.....',
          '.....',
          '.000.',
          '..0..',
          '.....'],
         ['.....',
          '..0..',
          '.00..',
          '..0..',
          '.....']]

    shapes = [S, Z, I, O, J, L, T]
    colors = [GREEN, RED, CYAN, YELLOW, BLUE, ORANGE, PURPLE]




