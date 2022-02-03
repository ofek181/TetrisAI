import pygame
from consts import Action


class EventHandler:
    """
        A static class to implement the event handler of the game.
        Methods
        ----------------------------
        handle_events() -> int:
         a function to handle the left user events during the game run time.
    """

    @staticmethod
    def handle_events() -> Action:
        """
        Handles the user's inputs during the game.
        Returns
            The action ID accordingly:
            DOWN -  0
            UP -    1
            LEFT -  2
            RIGHT - 3
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                return Action.UP
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                return Action.RIGHT
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                return Action.LEFT

        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            return Action.DOWN

