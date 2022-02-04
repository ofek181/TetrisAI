import pygame
from consts import AudioConsts


class Audio:
    """
        A class to implement the audio of the game.
        ----------------------------
        Methods
        ----------------------------
        clear():
         Play a sound when lines are cleared.
        game_over():
         Play a sound when game is over.
        theme():
         Play the theme of the game.
    """

    @staticmethod
    def clear() -> None:
        """
            Play a sound when lines are cleared.
        """
        pygame.mixer.init()
        channel = pygame.mixer.Channel(0)
        sound = pygame.mixer.Sound(AudioConsts.CLEAR)
        channel.play(sound)

    @staticmethod
    def game_over() -> None:
        """
            Play a sound when game is over.
        """
        pygame.mixer.init()
        channel = pygame.mixer.Channel(1)
        sound = pygame.mixer.Sound(AudioConsts.GAMEOVER)
        channel.play(sound)

    @staticmethod
    def theme() -> None:
        """
            Play the theme of the game.
        """
        pygame.mixer.init()
        channel = pygame.mixer.Channel(1)
        sound = pygame.mixer.Sound(AudioConsts.THEME)
        pygame.mixer.Sound.set_volume(sound, 0.25)
        channel.play(sound, loops=-1)

