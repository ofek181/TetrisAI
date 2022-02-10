import os
from neuroevolution import NeatAI


class Neat:
    """
        static class for implementing the train and test functions.
    """
    @staticmethod
    def train():
        """
            Determine path to configuration file. This path manipulation is
            here so that the script will run successfully regardless of the
            current working directory.
        """
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config-feedforward.txt')
        NeatAI.train(config_path)  # train

    @staticmethod
    def test():
        """
            Determine path to configuration file. This path manipulation is
            here so that the script will run successfully regardless of the
            current working directory.
        """
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config-feedforward.txt')
        NeatAI.test(config_path)  # test


def main():
    # Neat.train()
    Neat.test()


if __name__ == '__main__':
    main()



