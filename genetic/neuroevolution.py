import random
import pygame
import genetic_nn
import sys
import pickle
import math
from time import sleep
from random import randrange
from tetris.api import Environment
from consts import GameConsts, Action

global generation


class NeatAI:
    """
        A class implementing the NEAT algorithm on Tetris.
        ----------------------------
    # TODO finish docstring
    """
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
            balls.append(Ball(x_vel=random.randint(1, 4), y_vel=randrange(-2, 2)))
            paddles.append(Paddle(x_pos=50, y_pos=DisplayConsts.SCREEN_HEIGHT//2))
            genes.append(genome)

        # game loop for each generation
        while len(balls) > 0:
            # game display and event handling
            display.draw_training(static_paddle=static_paddle, paddles=paddles, balls=balls)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

            # move the balls and check collisions
            for index, ball in enumerate(balls):
                ball.move()
                new_vel = Physics.calc_ball_velocity(ball, paddles[index], static_paddle)
                ball.x_vel, ball.y_vel = new_vel.x_vel, new_vel.y_vel

            # remove paddle and ball if the ball is out of screen
            for index, ball in enumerate(balls):
                if ball.x_pos <= 0:
                    genes[index].fitness -= 5
                    neural_networks.pop(index)
                    genes.pop(index)
                    balls.pop(index)
                    paddles.pop(index)

            # reinforce the winning paddles for each living frame
            for index, paddle in enumerate(paddles):
                genes[index].fitness += 0.1
                output = neural_networks[index].activate((balls[index].x_vel, balls[index].y_vel,
                                                         balls[index].x_pos, balls[index].y_pos,
                                                         paddle.x_pos, paddle.y_pos))

                # move paddle up
                if output[0] >= 0.5:
                    paddle.move(-paddle.y_vel)

                # move paddle down
                if output[0] <= -0.5:
                    paddle.move(paddle.y_vel)

                # do nothing
                if -0.5 < output[0] < 0.5:
                    continue

    @staticmethod
    def test(config_path, genome_path="pongAI/winner.pkl"):
        """
            Loads the winner network and runs the flappy bird game
            :param
                config_file: location of config file.
                genome_path: winner network.
            :return:
                None
            """
        # Load NEAT config
        config = genetic_nn.config.Config(genetic_nn.DefaultGenome, genetic_nn.DefaultReproduction, genetic_nn.DefaultSpeciesSet,
                                          genetic_nn.DefaultStagnation, config_path)

        # Unpickle saved winner
        with open(genome_path, "rb") as f:
            genome = pickle.load(f)

        # initialization
        ball = Ball()
        ai_paddle = Paddle(x_pos=50, y_pos=DisplayConsts.SCREEN_HEIGHT // 2)
        human_paddle =  Paddle(x_pos=DisplayConsts.SCREEN_WIDTH - 50,
                               y_pos=DisplayConsts.SCREEN_HEIGHT // 2)
        ai_score = 0
        human_score = 0
        display = Display()
        neural_network = genetic_nn.nn.FeedForwardNetwork.create(genome, config)

        while True:
            # game display and event handling
            display.draw_objects(paddle_left=ai_paddle, paddle_right=human_paddle,
                                 ball=ball, score_left=ai_score, score_right=human_score)

            # move human paddle
            human_action = EventHandler.handle_right_events()
            if human_action == Action.MOVE_UP:
                human_paddle.move(-human_paddle.y_vel)
            if human_action == Action.MOVE_DOWN:
                human_paddle.move(human_paddle.y_vel)

            # quit the game if needed
            if human_action == Action.QUIT:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

            # move ai paddle
            output = neural_network.activate((ball.x_vel, ball.y_vel,
                                              ball.x_pos, ball.y_pos,
                                              ai_paddle.x_pos, ai_paddle.y_pos))
            # ai move paddle up
            if output[0] >= 0.5:
                ai_paddle.move(-ai_paddle.y_vel)

            # move paddle down
            if output[0] <= -0.5:
                ai_paddle.move(ai_paddle.y_vel)

            # accelerate the ball if action occurred for the first time
            if human_action != Action.NO_ACTION:
                if ball.x_vel == 0 and ball.y_vel == 0:
                    direction = randrange(start=-1, stop=1)
                    ball.x_vel = math.copysign(BallConsts.BALL_STARTING_VELOCITY_X, direction)

            # move the ball
            ball.move()

            # check for intersections
            new_vel = Physics.calc_ball_velocity(ball=ball, paddle_left=ai_paddle, paddle_right=human_paddle)
            ball.x_vel, ball.y_vel = new_vel.x_vel, new_vel.y_vel

            # if ai scored
            if Physics.is_score(ball)[0]:
                ai_score += 1
                ball = Ball()
                ai_paddle = Paddle(x_pos=50, y_pos=DisplayConsts.SCREEN_HEIGHT // 2)
                human_paddle = Paddle(x_pos=DisplayConsts.SCREEN_WIDTH - 50,
                                      y_pos=DisplayConsts.SCREEN_HEIGHT // 2)
            # if human scored
            if Physics.is_score(ball)[1]:
                human_score += 1
                ball = Ball()
                ai_paddle = Paddle(x_pos=50, y_pos=DisplayConsts.SCREEN_HEIGHT // 2)
                human_paddle = Paddle(x_pos=DisplayConsts.SCREEN_WIDTH - 50,
                                      y_pos=DisplayConsts.SCREEN_HEIGHT // 2)

            # check if game is over
            if human_score == GameConsts.MAX_SCORE:
                display.show_winner("Human wins!")
                sleep(3)
                break

            if ai_score == GameConsts.MAX_SCORE:
                display.show_winner("AI wins!")
                sleep(3)
                break

    @staticmethod
    def train(config_file):
        """
            Runs the NEAT algorithm to learn how to play flappy bird.
            :param
                config_file: location of config file
            :return:
                saves the defined winner in a pkl file
            """
        global generation
        generation = 0
        # Load configuration.
        config = genetic_nn.Config(genetic_nn.DefaultGenome, genetic_nn.DefaultReproduction,
                                   genetic_nn.DefaultSpeciesSet, genetic_nn.DefaultStagnation,
                                   config_file)

        # Create the population, which is the top-level object for a NEAT run.
        p = genetic_nn.Population(config)

        # Add a stdout reporter to show progress in the terminal.
        p.add_reporter(genetic_nn.StdOutReporter(True))
        stats = genetic_nn.StatisticsReporter()
        p.add_reporter(stats)

        # Run for up to 100 generations.
        winner = p.run(NeatAI.eval_genomes, 100)

        with open("pongAI/winner.pkl", "wb") as f:
            pickle.dump(winner, f)
            f.close()

        # Display the winning genome.
        print('\nBest genome:\n{!s}'.format(winner))


