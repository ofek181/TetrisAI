from tetris.game import Game


def main():
    play = True  # play or train a neural network
    is_player_human = True  # a human is playing or an algorithm
    set_audio = True  # set audio on/off

    if play:
        game = Game()
        game.play(set_audio)
    else:
        pass


if __name__ == '__main__':
    main()
