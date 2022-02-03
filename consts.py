from enum import Enum

# class AudioConsts:
#     HIT_AUDIO = os.path.join(local_dir_audio, 'hit.wav')
#     SCORE_AUDIO = os.path.join(local_dir_audio, 'score.wav')


class DisplayConsts:
    FPS = 60
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
    STARTING_SPEED = 400
    TIME = 4000
    LEFT_RIGHT_KEY_REFRESH = 100
    DOWN_KEY_REFRESH = 50
    MAX_SPEED = 50
    INC = 1


class Action(Enum):
    DOWN = 0
    UP = 1
    RIGHT = 2
    LEFT = 3


class PieceConsts:
    PIECE_SIZE = 10
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    CYAN = (0, 255, 255)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    ORANGE = (255, 127, 0)
    PURPLE = (128, 0, 128)

    S = [['.....',
          '.....',
          '..00.',
          '.00..',
          '.....'],
         ['.....',
          '..0..',
          '..00.',
          '...0.',
          '.....']]

    Z = [['.....',
          '.....',
          '.00..',
          '..00.',
          '.....'],
         ['.....',
          '..0..',
          '.00..',
          '.0...',
          '.....']]

    I = [['.....',
          '..0..',
          '..0..',
          '..0..',
          '..0..'],
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




