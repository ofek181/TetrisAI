import random
from collections import namedtuple, deque

Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))


class ReplayMemory:
    """
        Implementing experience replay memory for the DQN training.
        The memory stores the observations that the agent experiences. (s,a,s',r)
        By sampling from it randomly, we decorrelate the transitions.
    """
    def __init__(self, capacity):
        """
            Initiates the memory.
        """
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """
            Saves a transition (namedtuple).
        """
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        """
            Randomly samples from the memory.
        """
        return random.sample(self.memory, batch_size)

    def __len__(self):
        """
            Returns the length of the memory.
        """
        return len(self.memory)
