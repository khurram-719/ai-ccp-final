from typing import List, Dict, Set, Tuple, Optional
from modules.constraint_satisfaction import ConstraintSatisfaction
from modules.performance_tracker import PerformanceTracker

class AC3MRVSolver:
    """Informed search: Arc Consistency 3 with MRV and Degree heuristics."""

    def __init__(self):
        self.csp = ConstraintSatisfaction()
        self.tracker = PerformanceTracker()
        self.domains = {}

    def solve(self, puzzle: List[List[int]], track_steps: bool = False) -> Optional[List[List[int]]]:
        """Solve puzzle using AC-3 + MRV."""
        grid = [row[:] for row in puzzle]
        self.tracker.reset()
        self.tracker.start()

        # Initialize domains
        self._initialize_domains(grid)

        # Run AC-3
        if not self._ac3(grid):
            self.tracker.stop()
            return None

        # Backtrack with MRV heuristic
        if self._backtrack_mrv(grid, track_steps):
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

    def _ac3(self, grid: List[List[int]]) -> bool:
        """Arc Consistency 3 algorithm."""
        queue = []

        # Build constraint queue (arcs between all pairs of peers)
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    peers = self.csp.get_peers(row, col)
                    for peer in peers:
                        if grid[peer[0]][peer[1]] == 0:
                            queue.append(((row, col), peer))
                            queue.append((peer, (row, col)))

        while queue:
            (xi, xj) = queue.pop(0)

            if self._revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    return False

                for peer in self.csp.get_peers(xi[0], xi[1]):
                    if peer != xj and grid[peer[0]][peer[1]] == 0:
                        queue.append((peer, xi))

        return True

    def _revise(self, xi: Tuple[int, int], xj: Tuple[int, int]) -> bool:
        """Revise domain of Xi relative to Xj."""
        revised = False

        to_remove = set()
        for x in self.domains[xi]:
            # Check if Xi=x is supported by some value in Xj's domain
            if not any(y in self.domains[xj] for y in range(1, 10) if y != x):
                to_remove.add(x)

        if to_remove:
            self.domains[xi] -= to_remove
            revised = True

        return revised

    def _backtrack_mrv(self, grid: List[List[int]], track_steps: bool = False) -> bool:
        """Backtrack with MRV and Degree heuristics."""
        # Find unassigned variable with minimum remaining values
        unassigned = self._select_unassigned_variable(grid)

        if unassigned is None:
            return True

        row, col = unassigned
        self.tracker.increment_states()

        # Order domain values by least constraining value heuristic
        domain_values = sorted(self.domains[(row, col)])

        for num in domain_values:
            if self.csp.is_valid_placement(grid, row, col, num):
                grid[row][col] = num

                if track_steps:
                    self.tracker.record_step((row, col), num, grid)

                # Save domains
                saved_domains = self._save_domains()

                # Update domains
                self.domains[(row, col)] = {num}

                # Run AC-3 on updated domains
                valid = True
                queue = []
                for peer in self.csp.get_peers(row, col):
                    if grid[peer[0]][peer[1]] == 0:
                        queue.append((peer, (row, col)))

                while queue and valid:
                    xi, xj = queue.pop(0)
                    if self._revise(xi, xj):
                        if len(self.domains[xi]) == 0:
                            valid = False
                        else:
                            for peer in self.csp.get_peers(xi[0], xi[1]):
                                if peer != xj and grid[peer[0]][peer[1]] == 0:
                                    queue.append((peer, xi))

                if valid:
                    if self._backtrack_mrv(grid, track_steps):
                        return True

                    self.tracker.increment_backtracks()

                # Restore domains
                self._restore_domains(saved_domains)
                grid[row][col] = 0

        return False

    def _select_unassigned_variable(self, grid: List[List[int]]) -> Optional[Tuple[int, int]]:
        """Select unassigned variable using MRV + Degree heuristic."""
        best_cell = None
        min_domain = 10
        max_degree = -1

        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    domain_size = len(self.domains[(row, col)])

                    if domain_size == 0:
                        return (row, col)

                    # MRV: prefer cell with smallest domain
                    if domain_size < min_domain:
                        min_domain = domain_size
                        best_cell = (row, col)
                        max_degree = self._count_unassigned_peers(grid, row, col)
                    # Degree heuristic: break ties by counting unassigned peers
                    elif domain_size == min_domain:
                        degree = self._count_unassigned_peers(grid, row, col)
                        if degree > max_degree:
                            max_degree = degree
                            best_cell = (row, col)

        return best_cell

    def _count_unassigned_peers(self, grid: List[List[int]], row: int, col: int) -> int:
        """Count unassigned peers (for degree heuristic)."""
        count = 0
        for peer_row, peer_col in self.csp.get_peers(row, col):
            if grid[peer_row][peer_col] == 0:
                count += 1
        return count

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
