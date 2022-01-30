import pygame
from consts import DisplayConsts


class Display:
    """
        A class to implement the display of the game.
        ----------------------------
        Attributes
        ----------------------------
        screen : pygame object
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
    def __init__(self):
        """
            Constructs all the necessary attributes for the Display object.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((DisplayConsts.SCREEN_WIDTH, DisplayConsts.SCREEN_HEIGHT))

    def display_next_piece(self, piece: Piece):
        """
            Displays the upcoming shape.
        """
        pass

    def display_score(self, score: int):
        """
            Displays the current game score.
        """
        pass

    def draw_screen(self, piece: Piece, next_piece: Piece, score: int):
        """
            Implements the animation of the falling piece.
                Parameters:
                    piece : current piece played.
                    next_piece: upcoming piece.
                    score: score of left player.
        """
        pass


