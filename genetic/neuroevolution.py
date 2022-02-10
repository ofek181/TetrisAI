import os
import neat
import pygame
import sys
import pickle
from time import sleep
from operator import itemgetter
from tetris.api import Environment
from consts import GameConsts, Action

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
global generation


class NeatAI:
    """
        A class implementing the NEAT algorithm on Tetris.
        ----------------------------
    """
    @staticmethod
    def helper_reward_positive(state) -> int:
        reward = 0
        state = state.tolist()
        for line in state:
            max_1 = 1
            count = 0
            for idx in range(len(line) - 1):
                item = line[idx]
                item_next = line[idx + 1]
                if item == 1 and item_next == 1:
                    max_1 += 1
                    if max_1 > count:
                        count = max_1
                else:
                    max_1 = 1
            if count > 8:
                reward += 4
            elif count > 7:
                reward += 3
            elif count > 6:
                reward += 2
            elif count > 5:
                reward += 1
        return reward

    @staticmethod
    def eval_genomes(genomes, config):
        """
            Evaluates all genome of tetris by pre defined fitness.
            :param
                 genomes: each genome includes a list of connection genes.
                 config: the NEAT config file.
            :return:
                None
        """
        # initialize parameters
        global generation
        generation += 1
        neural_networks = []
        tetris = []
        genes = []
        for genome_id, genome in genomes:
            genome.fitness = 0
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            neural_networks.append(network)
            tetris.append(Environment())
            genes.append(genome)

        # game loop for each generation
        while len(tetris) > 0:
            # game display and event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

            # handle game over
            for idx, game in enumerate(tetris):
                if game.game_over:
                    genes[idx].fitness -= 100
                    neural_networks.pop(idx)
                    genes.pop(idx)
                    tetris.pop(idx)

            # reinforce the winning environments for each living frame
            for idx, game in enumerate(tetris):
                genes[idx].fitness += 0.01
                genes[idx].fitness += game.screen.get_score(len(game.screen.is_row_filled()))

                output = neural_networks[idx].activate(game.get_data())

                index, element = max(enumerate(output), key=itemgetter(1))
                if idx == 0:
                    game.play(Action(index), 1000, False)
                else:
                    game.play(Action(index), 1000, True)

    @staticmethod
    def test(config_path, genome_path=ROOT_DIR+"\\winner.pickle"):
        """
            Loads the winner network and runs game.
            :param
                config_file: location of config file.
                genome_path: winner network.
            :return:
                None
        """
        # Load NEAT config
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation, config_path)

        # Unpickle saved winner
        with open(genome_path, "rb") as f:
            genome = pickle.load(f)

        # initialization
        tetris = Environment()
        neural_network = neat.nn.FeedForwardNetwork.create(genome, config)

        while True:
            # quit the game if needed
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.display.quit()
                    quit()

            output = neural_network.activate(tetris.get_data())
            index, element = max(enumerate(output), key=itemgetter(1))
            tetris.play(Action(index), 30)

            # check if game is over
            if tetris.game_over:
                print("game over")
                sleep(3)
                break

    @staticmethod
    def train(config_file):
        """
            Runs the NEAT algorithm to learn how to play.
            :param
                config_file: location of config file
            :return:
                saves the defined winner in a pkl file
        """
        global generation
        generation = 0
        # Load configuration.
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_file)

        # Create the population, which is the top-level object for a NEAT run.
        p = neat.Population(config)

        # Add a stdout reporter to show progress in the terminal.
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        # Run for up to 1000 generations.
        winner = p.run(NeatAI.eval_genomes, 10000)

        with open("winner.pickle", "wb") as f:
            pickle.dump(winner, f)
            f.close()

        # Display the winning genome.
        print('\nBest genome:\n{!s}'.format(winner))


