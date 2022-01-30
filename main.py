import pygame
import pygame_menu
from consts import DisplayConsts


def main():
    pygame.init()
    surface = pygame.display.set_mode((DisplayConsts.SCREEN_WIDTH, DisplayConsts.SCREEN_HEIGHT))
    # tetris = Tetris()
    menu = pygame_menu.Menu('Tetris', DisplayConsts.SCREEN_WIDTH, DisplayConsts.SCREEN_HEIGHT,
                            theme=pygame_menu.themes.THEME_DARK)
    # menu.add.button('Play', AI.test)
    # menu.add.button('Test', AI.train)
    # menu.add.button('Train', tetris.run_game)
    menu.add.button('Exit', pygame_menu.events.EXIT)
    menu.mainloop(surface)


if __name__ == '__main__':
    main()
