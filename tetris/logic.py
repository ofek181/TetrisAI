from consts import GameConsts


class Logic:
    """
        A class to implement the logic object with respect to tetris' rule system.
        ----------------------------
        Attributes
        ----------------------------
        x_pos: int
         x position of the piece
        y_pos: int
         y position of the piece
        shape: list
         a list containing all the shapes and rotations of the piece objects.
        rotation: int
         current rotation of the piece, affecting the shape of it. between 0-3.
        color: list
         a list containing the colors of the different shapes according to the tetris color scheme.
        ----------------------------
        Methods
        ----------------------------
        __init__(self, x_pos, y_pos, idx):
         Constructs all the necessary attributes for the Piece object.
        rotate(self):
         Rotates the piece.
        decode_shape(self):
         Decodes the encoded positions into actual x,y positions.
    """

    def __init__(self):
        """
            Constructs all the necessary attributes for the Piece object.
        """
        self.grid = [[GameConsts.GRID_COLOR for _ in range(GameConsts.GRID_WIDTH)]
                     for _ in range(GameConsts.GRID_HEIGHT)]
        self.taken_positions = {}

    def update_grid(self):
        """
            creates the tetris puzzle grid.
            for every row and column, check if the position is taken already and input the piece color into the grid.
        """
        for column in range(len(self.grid)):
            for row in range(len(self.grid[column])):
                if (row, column) in self.taken_positions:
                    color = self.taken_positions[(row, column)]
                    self.grid[column][row] = color

    def is_row_cleared(self):
        counter = 0
        cleared_rows = []
        for column in range(len(self.grid)):
            for row in range(len(self.grid[column])):
                if (row, column) in self.taken_positions:
                    counter += 1
                    if counter == len(self.grid[row]):
                        cleared_rows.append(column)
            counter = 0
        return cleared_rows
