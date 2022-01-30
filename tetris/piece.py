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
        decode_shape(self):
         Decodes the encoded positions into actual x,y positions.
    """

    def __init__(self, x_pos: int, y_pos: int, idx: int) -> None:
        """
            Constructs all the necessary attributes for the Piece object.
        """
        self.x = x_pos
        self.y = y_pos

        try:
            self.shape = PieceConsts.shapes[idx]
            self.color = PieceConsts.colors[idx]
        except IndexError:
            print("Shape index must be between 0 - 6")
            exit(1)

        self.rotation = 0

    def rotate(self):
        """
            Rotates the piece by increasing the rotation index by 1 % the amount of variations the shape has.
        """
        self.rotation = (self.rotation + 1) % len(self.shape)

    def decode_shape(self):
        """
            Decodes the encoded piece's shape from the consts file into actual positions on screen.
        """
        encoded_shape = self.shape[self.rotation]
        positions = []
        x_offset, y_offset = 2, 4

        for column_idx, column in enumerate(encoded_shape):
            values = list[column]
            for row_idx, row in enumerate(column):
                if row == '0':
                    positions.append((self.x + row_idx, self.y + column_idx))

        for i, val in enumerate(positions):
            positions[i] = val[0] - x_offset, val[1] - y_offset

        return positions
