import random
from typing import List, Tuple
from .constraint_satisfaction import ConstraintSatisfaction

class PuzzleGenerator:
    """Generates valid, uniquely-solvable Sudoku puzzles."""

    def __init__(self):
        self.csp = ConstraintSatisfaction()

    def generate(self, difficulty: str) -> List[List[int]]:
        """Generate a puzzle of specified difficulty."""
        # Create a complete, valid grid
        complete_grid = self._generate_complete_grid()

        # Determine target number of cells to remove based on difficulty
        difficulty_map = {
            'Easy': (35, 40),
            'Medium': (30, 34),
            'Hard': (25, 29),
            'Expert': (20, 24)
        }

        if difficulty not in difficulty_map:
            difficulty = 'Medium'

        min_cells, max_cells = difficulty_map[difficulty]
        target_filled = random.randint(min_cells, max_cells)

        # Remove cells while maintaining uniqueness
        puzzle = [row[:] for row in complete_grid]
        cells_to_remove = 81 - target_filled

        removed_count = 0
        attempts = 0
        max_attempts = 1000

        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)

        for row, col in cells:
            if removed_count >= cells_to_remove or attempts >= max_attempts:
                break

            if puzzle[row][col] == 0:
                continue

            backup = puzzle[row][col]
            puzzle[row][col] = 0

            # Check if puzzle still has unique solution
            if self._has_unique_solution(puzzle):
                removed_count += 1
            else:
                puzzle[row][col] = backup

            attempts += 1

        return puzzle

    def _generate_complete_grid(self) -> List[List[int]]:
        """Generate a complete, valid Sudoku grid."""
        grid = [[0] * 9 for _ in range(9)]

        def fill_grid():
            for row in range(9):
                for col in range(9):
                    if grid[row][col] == 0:
                        # Get candidates and shuffle
                        candidates = list(self.csp.get_candidates(grid, row, col))
                        random.shuffle(candidates)

                        for num in candidates:
                            grid[row][col] = num
                            if fill_grid():
                                return True
                            grid[row][col] = 0

                        return False
            return True

        fill_grid()
        return grid

    def _has_unique_solution(self, puzzle: List[List[int]], max_solutions: int = 2) -> bool:
        """Check if puzzle has exactly one solution."""
        grid = [row[:] for row in puzzle]
        solutions = []

        def solve():
            if len(solutions) >= max_solutions:
                return False

            for row in range(9):
                for col in range(9):
                    if grid[row][col] == 0:
                        candidates = self.csp.get_candidates(grid, row, col)
                        if not candidates:
                            return False

                        for num in candidates:
                            grid[row][col] = num
                            if solve():
                                pass
                            grid[row][col] = 0

                        return False

            solutions.append([row[:] for row in grid])
            return True

        solve()
        return len(solutions) == 1

    def validate_puzzle(self, puzzle: List[List[int]]) -> Tuple[bool, str]:
        """Validate that a puzzle is valid and solvable."""
        # Check grid structure
        if len(puzzle) != 9 or any(len(row) != 9 for row in puzzle):
            return False, "Invalid grid dimensions"

        # Check cell values
        for row in puzzle:
            for val in row:
                if not isinstance(val, int) or val < 0 or val > 9:
                    return False, "Invalid cell values"

        # Check validity with current state
        if not self.csp.is_valid_sudoku(puzzle):
            return False, "Puzzle violates Sudoku constraints"

        # Check uniqueness
        if not self._has_unique_solution(puzzle):
            return False, "Puzzle does not have unique solution"

        return True, "Valid puzzle"
