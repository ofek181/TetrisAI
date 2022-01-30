from enum import Enum


class DisplayConsts:
    FPS = 30
    SCREEN_WIDTH = 500
    SCREEN_HEIGHT = 600
    FONT_COLOR = (255, 255, 255)
    LINE_FONT = (50, 50, 50)
    LINE_WIDTH = 10
    FONT_SIZE = 80
    WINNER_SIZE = 90
    FONT_TYPE = '8-Bit-Madness'


# class AudioConsts:
#     HIT_AUDIO = os.path.join(local_dir_audio, 'hit.wav')
#     SCORE_AUDIO = os.path.join(local_dir_audio, 'score.wav')


class PieceConsts:
    PIECE_SIZE = 10
    # TODO add colors


class GameConsts:
    MAX_SCORE = 1000000


class Action(Enum):
    NO_ACTION = 0
    MOVE_UP = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    MOVE_RIGHT = 4
    QUIT = 9




