from typing import List, Optional
from modules.constraint_satisfaction import ConstraintSatisfaction
from modules.performance_tracker import PerformanceTracker

class BacktrackingSolver:
    """Uninformed search: Standard depth-first backtracking."""

    def __init__(self):
        self.csp = ConstraintSatisfaction()
        self.tracker = PerformanceTracker()

    def solve(self, puzzle: List[List[int]], track_steps: bool = False) -> Optional[List[List[int]]]:
        """Solve puzzle using backtracking."""
        grid = [row[:] for row in puzzle]
        self.tracker.reset()
        self.tracker.start()

        if self._backtrack(grid, track_steps):
            self.tracker.stop()
            return grid
        else:
            self.tracker.stop()
            return None

    def _backtrack(self, grid: List[List[int]], track_steps: bool = False) -> bool:
        """Recursive backtracking function."""
        # Find next empty cell
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    self.tracker.increment_states()

                    # Try each digit
                    for num in range(1, 10):
                        if self.csp.is_valid_placement(grid, row, col, num):
                            grid[row][col] = num

                            if track_steps:
                                self.tracker.record_step((row, col), num, grid)

                            if self._backtrack(grid, track_steps):
                                return True

                            grid[row][col] = 0
                            self.tracker.increment_backtracks()

                    return False

        # All cells filled - solution found
        return True

    def get_metrics(self):
        """Get performance metrics."""
        return self.tracker.get_metrics()

    def get_steps(self):
        """Get solving steps for visualization."""
        return self.tracker.steps
