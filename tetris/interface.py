from abc import ABC, abstractmethod


class ABCGame(ABC):
    """
        Game interface for future use.
    """
    @abstractmethod
    def play(self):
        """
            Future main loop of the game.
        """
        pass
