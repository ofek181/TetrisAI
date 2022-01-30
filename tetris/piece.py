from consts import PieceConsts


class Piece:
    """
        A class to implement the different piece's shapes of the game and their rotations.
        Tetriminos:
            0 - S - Green
            1 - Z - Red
            2 - I - Cyan
            3 - O - Yellow
            4 - J - Blue
            5 - L - Orange
            6 - T - Purple
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
    """

    def __init__(self, x_pos: int, y_pos: int, idx: int) -> None:
        """
            Constructs all the necessary attributes for the Piece object.
        """
        self.x = x_pos
        self.y = y_pos
        self.shape = PieceConsts.shapes[idx]
        self.rotation = 0
        self.color = PieceConsts.colors[idx]

    def rotate(self):
        """
            Rotates the piece by increasing the rotation index by 1 % the amount of variations the shape has.
        """
        self.rotation = (self.rotation + 1) % len(self.shape)

    def decode_shape(self):
        encoded_shape = self.shape[self.rotation]
        positions = []

        for column_idx, column in enumerate(encoded_shape):
            values = list[column]
            for row_idx, row in enumerate(values):
                if row == '0':
                    positions.append((self.x + row_idx, self.y + column_idx))
