import os
from consts import GameConsts


class Screen:
    """
        A class to implement the screen object with respect to tetris' rule system.
        ----------------------------
        Attributes
        ----------------------------
        grid: list
         2dim list representing the tetris grid
        taken positions: dictionary
         dict representing all the taken tetris positions and their colors (eg. (1, 1) = (255, 255, 255))
        ----------------------------
        Methods
        ----------------------------
        __init__(self):
         Constructs all the necessary attributes for the Piece object.
        update_grid(self):
         Updates the tetris puzzle grid.
        is_row_filled(self):
         Checks if an entire row is filled.
        clear_filled_rows(self, filled_rows):
         clears filled rows.
        is_game_over(self):
         Checks if a player lost.
        is_valid_rotation(self, positions):
         Checks if you can rotate the piece in the current position it is in.
        is_collision(self, position, color):
         Checks if a collision occurred and adds the collided piece to the taken positions dict.
        get_score(n):
         Updates the game's score according to tetris' scoring system.
        update_highest_score(score):
         Writes the highest score to a file and returns it.
    """

    def __init__(self) -> None:
        """
            Constructs all the necessary attributes for the Piece object.
        """
        self.grid = [[GameConsts.GRID_FILL for x in range(GameConsts.GRID_WIDTH)]
                     for y in range(GameConsts.GRID_HEIGHT)]
        self.taken_positions = {}

    def update_grid(self) -> None:
        """
            updates the tetris puzzle grid.
            for every row and column, check if the position is taken already and input the piece color into the grid.
        """
        self.grid = [[GameConsts.GRID_FILL for x in range(GameConsts.GRID_WIDTH)]
                     for y in range(GameConsts.GRID_HEIGHT)]

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if (x, y) in self.taken_positions:
                    color = self.taken_positions[(x, y)]
                    self.grid[y][x] = color

    def is_row_filled(self) -> list:
        """
            checks if an entire row is filled so the tetris game can clear it.
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
        filled_rows.sort()
        for y in filled_rows:
            for x in range(len(self.grid[y])):
                del self.taken_positions[(x, y)]

        for row in filled_rows:
            for y in range(row, -1, -1):
                for x in range(len(self.grid[y])):
                    if (x, y) in self.taken_positions:
                        self.taken_positions[(x, y + 1)] = self.taken_positions.pop((x, y))

    def is_game_over(self) -> bool:
        """
            checks if the game is over.
        """
        for position in self.taken_positions:
            x, y = position
            if y <= 0:
                return True
        return False

    def is_valid_rotation(self, positions: list) -> bool:
        """
            checks if you can rotate the piece.
        """
        valid = [[(x, y) for x in range(GameConsts.GRID_WIDTH) if self.grid[y][x] == GameConsts.GRID_FILL]
                 for y in range(GameConsts.GRID_HEIGHT)]
        flatten_valid = [item for sublist in valid for item in sublist]
        for loc in positions:
            if loc not in flatten_valid:
                if loc[1] >= 0:
                    return False
        return True

    @staticmethod
    def get_score(n: int) -> int:
        """
            Updates the score of the game.
            40 - 1 line
            100 - 2 lines
            300 - 3 lines
            1200 - 4 lines
        """
        score = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}
        return score[n]

    @staticmethod
    def update_highest_score(score: int) -> int:
        """
             Writes the highest score to a file.
        """
        local_dir = os.path.dirname(__file__)
        path_parent = os.path.dirname(local_dir)
        config_path = os.path.join(path_parent, 'highscore.txt')

        with open(config_path, 'r') as file:
            lines = file.readlines()
            highest_score = int(lines[0].strip())

        with open(config_path, 'w') as file:
            if score > highest_score:
                file.write(str(score))
                return score
            else:
                file.write(str(highest_score))
                return highest_score
