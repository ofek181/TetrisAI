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

    def __init__(self) -> None:
        """
            Constructs all the necessary attributes for the Piece object.
        """
        self.grid = [[GameConsts.GRID_COLOR for x in range(GameConsts.GRID_WIDTH)]
                     for y in range(GameConsts.GRID_HEIGHT)]
        self.taken_positions = {}

    def update_grid(self) -> None:
        """
            creates the tetris puzzle grid.
            for every row and column, check if the position is taken already and input the piece color into the grid.
        """
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if (x, y) in self.taken_positions:
                    color = self.taken_positions[(x, y)]
                    self.grid[y][x] = color
                else:
                    self.grid[y][x] = GameConsts.GRID_COLOR

    def is_row_filled(self) -> list:
        """
            checks for if the entire row is filled so the tetris game can clear it.
        """
        counter = 0
        filled_rows = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if (x, y) in self.taken_positions:
                    counter += 1
                    if counter == len(self.grid[x]):
                        filled_rows.append(y)
            counter = 0
        return filled_rows

    def clear_filled_rows(self, filled_rows: list) -> None:
        """
            clear a row if the said row is already filled.
            take down all following rows by 1 for each deleted row
        """
        filled_rows.sort(reverse=True)
        for y in filled_rows:
            for x in range(len(self.grid[y])):
                del self.taken_positions[(x, y)]
            for next_y in range(y + 1, len(self.grid)):
                for next_x in range(len(self.grid[next_y])):
                    if (next_x, next_y) in self.taken_positions:
                        self.taken_positions[(next_x, next_y - 1)] = self.taken_positions[(next_x, next_y)]
                        del self.taken_positions[(next_x, next_y)]
