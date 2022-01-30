from abc import ABC, abstractmethod


class Game(ABC):
    """
        Game interface for future use.
    """
    @abstractmethod
    def play(self):
        """
            Future main loop of the game.
        """
        pass

    @abstractmethod
    def _is_game_over(self):
        """
            Checks for game over state.
        """
        pass

    @abstractmethod
    def _calc_frame(self):
        """
            Calculates a single frame of the game.
        """
        pass
