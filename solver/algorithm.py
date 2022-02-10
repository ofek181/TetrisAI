import pygame
from copy import copy
from time import sleep
from tetris.api import Environment
from consts import GameConsts, Action


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
    def check_valid_position(positions: list, grid: list) -> bool:
        """
            checks for intersections.
        """
        valid = [[(x, y) for x in range(GameConsts.GRID_WIDTH) if grid[y][x] == GameConsts.GRID_FILL]
                 for y in range(GameConsts.GRID_HEIGHT)]
        flatten_valid = [item for sublist in valid for item in sublist]
        for loc in positions:
            if loc not in flatten_valid:
                if loc[1] >= 0:
                    return False
                if loc[0] > GameConsts.GRID_WIDTH or loc[0] < 0:
                    return False
        return True

    @staticmethod
    def update_grid(taken_positions: dict) -> list:
        """
            updates the tetris puzzle grid.
            for every row and column, check if the position is taken and input the piece color into the grid.
        """
        simulated_grid = [[GameConsts.GRID_FILL for _ in range(GameConsts.GRID_WIDTH)]
                          for _ in range(GameConsts.GRID_HEIGHT)]

        for y in range(len(simulated_grid)):
            for x in range(len(simulated_grid[y])):
                if (x, y) in taken_positions:
                    simulated_grid[y][x] = taken_positions[(x, y)]

        return simulated_grid

    def simulate_drop(self, x: int, rotation: int) -> tuple:
        """
            Simulates a drop of a piece.
        """
        simulated_grid = copy(self.tetris.screen.grid)
        current_piece = copy(self.tetris.current_piece)
        simulated_taken = copy(self.tetris.screen.taken_positions)
        current_piece.x = x
        current_piece.y = 0
        current_piece.rotation = rotation
        out = False

        for pos in current_piece.decode_shape():
            if pos[0] < 0 or pos[0] > GameConsts.GRID_WIDTH:
                out = True

        if not out:
            while self.check_valid_position(current_piece.decode_shape(), simulated_grid):
                current_piece.y += 1
            current_piece.y -= 1
        else:
            return simulated_taken, out

        for pos in current_piece.decode_shape():
            simulated_taken[pos] = current_piece.color

        return simulated_taken, out

    @staticmethod
    def get_height_of_column(x_pos: int, positions: dict):
        """
            returns the height of a single column.
        """
        for y in range(GameConsts.GRID_HEIGHT):
            if (x_pos, y) in positions:
                return y
        return GameConsts.GRID_HEIGHT

    @staticmethod
    def check_height(simulated_taken: dict) -> int:
        """
            Checks the height of the new tower simulated by the drop function.
            height = 0 is the best value possible.
        """
        height = GameConsts.GRID_HEIGHT
        for pos in simulated_taken:
            if pos[1] < height:
                height = pos[1]

        max_height = GameConsts.GRID_HEIGHT - (height + 1)
        return max_height

    @staticmethod
    def check_holes(simulated_taken: dict) -> int:
        """
            Checks the number of holes after a simulated drop.
            holes = 0 is the best value possible.
        """
        holes = 0

        for x in range(GameConsts.GRID_WIDTH):
            height = Ai.get_height_of_column(x, simulated_taken)
            idx = 0
            while height + idx < GameConsts.GRID_HEIGHT:
                if (x, height + idx) not in simulated_taken:
                    holes += 1
                idx += 1

        return holes

    @staticmethod
    def check_bumpiness(simulated_taken: dict) -> int:
        """
            Checks to see the bumpiness of the grid.
            bumpiness = 0 is the best value possible.
        """
        heights = []
        bumpiness = 0

        for x in range(GameConsts.GRID_WIDTH):
            h = Ai.get_height_of_column(x, simulated_taken)
            heights.append(h)

        for x in range(GameConsts.GRID_WIDTH - 1):
            bumpiness += abs(heights[x] - heights[x + 1])

        return bumpiness

    @staticmethod
    def check_pillars(simulated_taken: dict) -> int:
        """
            Checks to see the number of pillars in the grid.
            pillar = height difference >= 2
        """
        heights = []
        pillars = 0

        for x in range(GameConsts.GRID_WIDTH):
            h = Ai.get_height_of_column(x, simulated_taken)
            heights.append(h)

        for x in range(GameConsts.GRID_WIDTH - 1):
            if heights[x] - heights[x + 1] >= 2:
                pillars += 1

        return pillars

    @staticmethod
    def check_lines(simulated_taken: dict) -> int:
        """
            Checks to see the number of lines that will be cleared.
        """
        lines = 0
        for y in range(GameConsts.GRID_HEIGHT):
            count = 0
            for x in range(GameConsts.GRID_WIDTH):
                if (x, y) in simulated_taken:
                    count += 1
                if count == GameConsts.GRID_WIDTH:
                    lines += 1

        return lines

    @staticmethod
    def compute_cost_for_move(max_height: int, holes: int, bumpiness: int, pillars: int, lines: int) -> float:
        """
        Computes the score of a single move based on the maximum height, holes and bumpiness it leaves.
            :param max_height: we need to minimize this parameter.
            :param holes: we need to minimize this parameters.
            :param bumpiness: we need to minimize this.
            :param pillars: we need to minimize the amount of pillars.
            :param lines: we need to maximize the amount of lines cleared.
            :return: cost function of a single move, the move with the lowest cost is the best move.
        """
        a, b, c, d, e = 0.5, 5, 0.25, 1.5, -6
        cost = a * max_height + b * holes + c * bumpiness + d * pillars + e * lines
        return cost

    def best_final_state(self) -> tuple:
        """
            Calculates the best final state based on the state with the lowest cost.
        """
        min_cost = float('inf')
        best_state = 0, 0
        for rotation in range(len(self.tetris.current_piece.shape)):
            for x in range(GameConsts.GRID_WIDTH):
                simulated_taken, out = self.simulate_drop(x, rotation)
                if not out:
                    height = self.check_height(simulated_taken)
                    holes = self.check_holes(simulated_taken)
                    bumpiness = self.check_bumpiness(simulated_taken)
                    pillars = self.check_pillars(simulated_taken)
                    lines = self.check_lines(simulated_taken)
                    cost = self.compute_cost_for_move(height, holes, bumpiness, pillars, lines)
                    if cost < min_cost:
                        best_state = x, rotation
                        min_cost = cost
        return best_state

    def solve_puzzle(self) -> None:
        """
            solves for the best position of a single piece
        """
        fps = 10
        self.tetris.reset(fps)
        desired_x_pos, desired_rotation = self.best_final_state()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.display.quit()
                    quit()
            if desired_x_pos > self.tetris.current_piece.x:
                action = Action.LEFT
            elif desired_x_pos < self.tetris.current_piece.x:
                action = Action.RIGHT
            elif desired_rotation != self.tetris.current_piece.rotation:
                action = Action.UP
            else:
                action = Action.IDLE

            self.tetris.play(action, fps)

            if self.tetris.get_next_piece:
                desired_x_pos, desired_rotation = self.best_final_state()

            if self.tetris.game_over:
                self.tetris.display.draw_game_over(self.tetris.score, "AI")
                sleep(1)
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                            pygame.display.quit()
                            quit()


def main():
    ai = Ai()
    ai.solve_puzzle()


if __name__ == '__main__':
    main()
