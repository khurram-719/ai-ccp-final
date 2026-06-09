import random
import math
from typing import List, Optional
from modules.constraint_satisfaction import ConstraintSatisfaction
from modules.performance_tracker import PerformanceTracker
from solvers.backtracking import BacktrackingSolver

class SimulatedAnnealingSolver:
    """Local search: Simulated annealing starting from complete assignment."""

    def __init__(self):
        self.csp = ConstraintSatisfaction()
        self.tracker = PerformanceTracker()
        self.initial_temp = 200.0
        self.cooling_rate = 0.998
        self.min_temp = 0.01
        self.max_iterations = 50000
        self.max_restarts = 30
        self.use_fallback = True

    def solve(self, puzzle: List[List[int]], track_steps: bool = False) -> Optional[List[List[int]]]:
        """Solve puzzle using simulated annealing."""
        self.tracker.reset()
        self.tracker.start()
        # Prepare fixed positions (clues)
        fixed = {(r, c) for r in range(9) for c in range(9) if puzzle[r][c] != 0}

        best_grid = None
        best_violations = float('inf')

        # Try multiple random restarts to escape local minima
        for attempt in range(self.max_restarts):
            grid = self._generate_initial_state(puzzle)
            current_violations = self.csp.count_violations(grid)
            if current_violations < best_violations:
                best_violations = current_violations
                best_grid = [row[:] for row in grid]

            current_temp = self.initial_temp
            iterations = 0

            while current_temp > self.min_temp and iterations < self.max_iterations:
                self.tracker.increment_states()

                # Box-aware neighbor: choose two mutable cells in same row, preferring box-conflicting pairs
                row_idx = random.randint(0, 8)
                mutable_cols = [c for c in range(9) if (row_idx, c) not in fixed]
                
                if len(mutable_cols) < 2:
                    current_temp *= self.cooling_rate
                    iterations += 1
                    continue

                # Choose two columns: prefer swaps that reduce box violations
                if len(mutable_cols) >= 3 and random.random() < 0.7:
                    # Greedy: pick the pair with most box conflicts
                    col1, col2 = self._best_box_swap_pair(grid, row_idx, mutable_cols)
                else:
                    col1, col2 = random.sample(mutable_cols, 2)

                # Record energy before swap
                prev_violations = current_violations

                # Apply swap
                grid[row_idx][col1], grid[row_idx][col2] = grid[row_idx][col2], grid[row_idx][col1]

                # Compute new energy
                new_violations = self.csp.count_violations(grid)
                delta = new_violations - prev_violations

                # Acceptance criterion: lower energy always accepted; worse accepted probabilistically
                accept = False
                if delta <= 0:
                    accept = True
                else:
                    try:
                        # Use adaptive cooling: penalize uphill moves more as temp drops
                        cooling_factor = 1.0 + (1.0 - current_temp / self.initial_temp) * 5.0
                        prob = math.exp(-delta * cooling_factor / current_temp)
                    except OverflowError:
                        prob = 0.0
                    if random.random() < prob:
                        accept = True

                if accept:
                    current_violations = new_violations
                    if current_violations < best_violations:
                        best_violations = current_violations
                        best_grid = [row[:] for row in grid]
                        if track_steps:
                            # record the swap as a step
                            self.tracker.record_step((row_idx, col1), grid[row_idx][col1], grid)

                        if best_violations == 0:
                            self.tracker.stop()
                            return best_grid
                else:
                    # Reject: swap back
                    grid[row_idx][col1], grid[row_idx][col2] = grid[row_idx][col2], grid[row_idx][col1]

                current_temp *= self.cooling_rate
                iterations += 1

            # end of iterations for this restart
            if best_violations == 0:
                self.tracker.stop()
                return best_grid

        # after all restarts
        self.tracker.stop()
        if best_violations == 0:
            return best_grid
        
        # Fallback to backtracking if SA fails
        if self.use_fallback and best_violations > 0:
            self.tracker.reset()
            self.tracker.start()
            fallback = BacktrackingSolver()
            result = fallback.solve(puzzle, track_steps=track_steps)
            self.tracker.stop()
            if result:
                return result
        
        return None

    def _generate_initial_state(self, puzzle: List[List[int]]) -> List[List[int]]:
        """Generate initial complete (but possibly invalid) state."""
        grid = [row[:] for row in puzzle]

        # For each row, fill empty cells with the missing numbers (so each row is a permutation 1-9)
        for r in range(9):
            fixed_nums = [grid[r][c] for c in range(9) if grid[r][c] != 0]
            missing = list(set(range(1, 10)) - set(fixed_nums))
            random.shuffle(missing)
            # Fill empty positions in this row
            for c in range(9):
                if grid[r][c] == 0:
                    grid[r][c] = missing.pop()

        return grid

    def _best_box_swap_pair(self, grid: List[List[int]], row_idx: int, mutable_cols: list) -> tuple:
        """Find the pair of columns in a row that would reduce box violations most if swapped."""
        best_delta = 0
        best_pair = (mutable_cols[0], mutable_cols[1])

        for i in range(len(mutable_cols)):
            for j in range(i + 1, len(mutable_cols)):
                col1, col2 = mutable_cols[i], mutable_cols[j]

                # Count box violations before and after swap
                box1_before = self._count_box_violations_at_cell(grid, row_idx, col1)
                box2_before = self._count_box_violations_at_cell(grid, row_idx, col2)

                # Swap
                grid[row_idx][col1], grid[row_idx][col2] = grid[row_idx][col2], grid[row_idx][col1]
                box1_after = self._count_box_violations_at_cell(grid, row_idx, col1)
                box2_after = self._count_box_violations_at_cell(grid, row_idx, col2)

                # Unswap
                grid[row_idx][col1], grid[row_idx][col2] = grid[row_idx][col2], grid[row_idx][col1]

                delta = (box1_before + box2_before) - (box1_after + box2_after)
                if delta > best_delta:
                    best_delta = delta
                    best_pair = (col1, col2)

        return best_pair

    def _count_box_violations_at_cell(self, grid: List[List[int]], row: int, col: int) -> int:
        """Count duplicate values in the 3x3 box containing (row, col)."""
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        val = grid[row][col]
        count = 0
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r, c) != (row, col) and grid[r][c] == val:
                    count += 1
        return count

    def get_metrics(self):
        """Get performance metrics."""
        return self.tracker.get_metrics()

    def get_steps(self):
        """Get solving steps for visualization."""
        return self.tracker.steps
