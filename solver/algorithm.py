from tetris.api import Environment
from consts import GameConsts


class Ai:
    """
        A class to deterministically approximate a solution for a tetris board.
    """
    def __init__(self) -> None:
        """
            Constructs all the necessary attributes for the Ai object.
        """
        self.tetris = Environment()

    @staticmethod
    def check_intersection(positions: list, grid: list) -> bool:
        """
            checks if you can rotate the piece.
        """
        valid = [[(x, y) for x in range(GameConsts.GRID_WIDTH) if grid[y][x] == GameConsts.GRID_FILL]
                 for y in range(GameConsts.GRID_HEIGHT)]
        flatten_valid = [item for sublist in valid for item in sublist]
        for loc in positions:
            if loc not in flatten_valid:
                if loc[1] >= 0:
                    return False
        return True

    def simulate_drop(self, x: int, rotation: int) -> list:
        """
            Simulates a drop of a piece.
        """
        simulated_grid = self.tetris.screen.grid
        current_piece = self.tetris.current_piece
        current_piece.x = x
        current_piece.rotation = rotation

        while not self.check_intersection(current_piece.decode_shape(), simulated_grid):
            current_piece.y += 1
        current_piece.y -= 1

        for pos in current_piece.decode_shape():
            simulated_grid[pos[1]][pos[0]] = current_piece.color

        return simulated_grid

    @staticmethod
    def check_height(simulated_grid: list) -> int:
        """
            Checks the height of the new tower simulated by the drop function.
            height = Grid_Height is the best value possible.
            height = 0 is the worst value possible.
        """
        max_height = GameConsts.GRID_HEIGHT

        for x in range(len(simulated_grid[0])):
            height_in_column = GameConsts.GRID_HEIGHT
            for y in range(len(simulated_grid)):
                if simulated_grid[y][x] != GameConsts.GRID_FILL:
                    height_in_column = y
                    continue

            if height_in_column < max_height:
                max_height = height_in_column

        return max_height

    @staticmethod
    def check_holes(simulated_grid: list) -> int:
        """
            Checks the number of holes after a simulated drop.
            holes = 0 is the best value possible.
        """
        holes = 0

        for x in range(len(simulated_grid[0])):
            found = False
            for y in range(len(simulated_grid)):
                if simulated_grid[y][x] != GameConsts.GRID_FILL:
                    found = True

                if found:
                    if simulated_grid[y][x] == GameConsts.GRID_FILL:
                        holes += 1

        return holes

    @staticmethod
    def check_bumpiness(simulated_grid: list) -> int:
        """
            Checks to see the bumpiness of the grid.
            bumpiness = 0 is the best value possible.
        """
        heights = [GameConsts.GRID_HEIGHT] * GameConsts.GRID_WIDTH
        bumpiness = 0

        for x in range(len(simulated_grid[0])):
            for y in range(len(simulated_grid)):
                if simulated_grid[y][x] != GameConsts.GRID_FILL:
                    heights.append(y)
                    continue

        for idx, height in enumerate(heights[:-1]):
            next_height = heights[idx + 1]
            diff = abs(height - next_height)
            bumpiness += diff

        return bumpiness

    @staticmethod
    def compute_score_for_move(max_height: int, holes: int, bumpiness: int) -> int:
        """
        Computes the score of a single move based on the maximum height, holes and bumpiness it leaves.
            :param max_height: we need to maximize this parameter (higher height means lower value)
            :param holes: we need to minimize this parameters (a lot of holes are bad)
            :param bumpiness: we need to minimize this (greater bumpiness is bad)
            :return: score function of a single move, higher score value means a better move
                     score = grid.height is the best score possible.
        """
        score = max_height - holes - bumpiness
        return score

    def choose_best_action(self) -> None:
        """
            Chooses the best action based on amount of holes and height.
        """
        pass

    def solve_puzzle(self) -> None:
        """
            solves for the best position of a single piece
        """
        pass


