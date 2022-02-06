import torch
import torch.nn as nn
import torch.nn.functional
from consts import GameConsts

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class DeepQNetwork(nn.Module):
    """
        A class to implement the DQN model using the standard way in pytorch __init__ and forward.
    """
    def __init__(self):
        """
            Implements the architecture of the model.
        """
        super(DeepQNetwork, self).__init__()

        # convolutional layers
        self.conv1 = nn.Conv2d(1, 8, kernel_size=(2, 2), stride=(1, 1))
        self.bn1 = nn.BatchNorm2d(8)
        self.conv2 = nn.Conv2d(8, 16, kernel_size=(2, 2), stride=(1, 1))
        self.bn2 = nn.BatchNorm2d(16)

        # compute linear input
        def conv2d_size_out(size, kernel_size=2, stride=2):
            return (size - (kernel_size - 1) - 1) // stride + 1

        convw = conv2d_size_out(conv2d_size_out(GameConsts.GRID_WIDTH))
        convh = conv2d_size_out(conv2d_size_out(GameConsts.GRID_HEIGHT))
        input_size = convw * convh * 16

        # 2 dense layers and output layer
        self.linear1 = nn.Linear(input_size, 128)
        self.linear2 = nn.Linear(input_size, 10)
        self.output = nn.Linear(input_size, 4)

    def forward(self, x):
        """
            Implements the forward pass of the neural network.
        """
        x = x.to(device)
        x = nn.functional.relu(self.bn1(self.conv1(x)))
        x = nn.functional.relu(self.bn2(self.conv2(x)))
        x = nn.functional.relu(self.bn1(self.linear1(x)))
        x = nn.functional.relu(self.bn1(self.linear2(x)))
        return self.output(x.view(x.size(0), -1))
