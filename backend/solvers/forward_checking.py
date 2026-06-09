from typing import List, Dict, Set, Optional
from modules.constraint_satisfaction import ConstraintSatisfaction
from modules.performance_tracker import PerformanceTracker

class ForwardCheckingSolver:
    """Constraint propagation: Forward checking with domain reduction."""

    def __init__(self):
        self.csp = ConstraintSatisfaction()
        self.tracker = PerformanceTracker()
        self.domains = {}

    def solve(self, puzzle: List[List[int]], track_steps: bool = False) -> Optional[List[List[int]]]:
        """Solve puzzle using forward checking."""
        grid = [row[:] for row in puzzle]
        self.tracker.reset()
        self.tracker.start()

        # Initialize domains
        self._initialize_domains(grid)

        if self._backtrack_with_fc(grid, track_steps):
            self.tracker.stop()
            return grid
        else:
            self.tracker.stop()
            return None

    def _initialize_domains(self, grid: List[List[int]]):
        """Initialize domain for each cell."""
        self.domains = {}
        for row in range(9):
            for col in range(9):
                if grid[row][col] != 0:
                    self.domains[(row, col)] = {grid[row][col]}
                else:
                    self.domains[(row, col)] = self.csp.get_candidates(grid, row, col)

    def _backtrack_with_fc(self, grid: List[List[int]], track_steps: bool = False) -> bool:
        """Backtrack with forward checking."""
        # Find unassigned variable with minimum remaining values (MRV heuristic)
        unassigned = None
        min_domain = 10

        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    domain_size = len(self.domains[(row, col)])
                    if domain_size == 0:
                        return False
                    if domain_size < min_domain:
                        min_domain = domain_size
                        unassigned = (row, col)

        if unassigned is None:
            return True

        row, col = unassigned
        self.tracker.increment_states()

        # Try each value in domain
        for num in sorted(self.domains[(row, col)]):
            if self.csp.is_valid_placement(grid, row, col, num):
                grid[row][col] = num

                if track_steps:
                    self.tracker.record_step((row, col), num, grid)

                # Save current domains
                saved_domains = self._save_domains()

                # Forward check
                if self._forward_check(grid, row, col):
                    if self._backtrack_with_fc(grid, track_steps):
                        return True

                    self.tracker.increment_backtracks()

                # Restore domains
                self._restore_domains(saved_domains)
                grid[row][col] = 0

        return False

    def _forward_check(self, grid: List[List[int]], row: int, col: int) -> bool:
        """Check if assignment is forward-compatible."""
        assigned_value = grid[row][col]
        peers = self.csp.get_peers(row, col)

        for peer_row, peer_col in peers:
            if grid[peer_row][peer_col] == 0:
                self.domains[(peer_row, peer_col)].discard(assigned_value)
                if len(self.domains[(peer_row, peer_col)]) == 0:
                    return False

        return True

    def _save_domains(self) -> Dict:
        """Save current domains state."""
        return {k: v.copy() for k, v in self.domains.items()}

    def _restore_domains(self, saved_domains: Dict):
        """Restore domains to saved state."""
        self.domains = {k: v.copy() for k, v in saved_domains.items()}

    def get_metrics(self):
        """Get performance metrics."""
        return self.tracker.get_metrics()

    def get_steps(self):
        """Get solving steps for visualization."""
        return self.tracker.steps
