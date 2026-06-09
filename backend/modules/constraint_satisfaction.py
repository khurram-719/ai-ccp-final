from typing import Set, List, Tuple, Dict

class ConstraintSatisfaction:
    """CSP utilities for Sudoku solving."""

    @staticmethod
    def get_peers(row: int, col: int) -> Set[Tuple[int, int]]:
        """Get all peers (cells that share constraints) with given cell."""
        peers = set()

        # Row peers
        for c in range(9):
            if c != col:
                peers.add((row, c))

        # Column peers
        for r in range(9):
            if r != row:
                peers.add((r, col))

        # Box peers (3x3)
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r, c) != (row, col):
                    peers.add((r, c))

        return peers

    @staticmethod
    def get_box(row: int, col: int) -> Tuple[int, int]:
        """Get the 3x3 box index for a cell."""
        return (3 * (row // 3), 3 * (col // 3))

    @staticmethod
    def is_valid_placement(grid: List[List[int]], row: int, col: int, num: int) -> bool:
        """Check if placing num at (row, col) is valid."""
        # Check row
        if num in grid[row]:
            return False

        # Check column
        if num in [grid[r][col] for r in range(9)]:
            return False

        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if grid[r][c] == num:
                    return False

        return True

    @staticmethod
    def get_candidates(grid: List[List[int]], row: int, col: int) -> Set[int]:
        """Get valid candidate values for a cell."""
        if grid[row][col] != 0:
            return set()

        candidates = set(range(1, 10))

        # Remove values in row
        candidates -= set(grid[row])

        # Remove values in column
        candidates -= set(grid[r][col] for r in range(9))

        # Remove values in 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                candidates.discard(grid[r][c])

        return candidates

    @staticmethod
    def get_empty_cells(grid: List[List[int]]) -> List[Tuple[int, int]]:
        """Get all empty cells in the grid."""
        empty = []
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    empty.append((r, c))
        return empty

    @staticmethod
    def is_complete(grid: List[List[int]]) -> bool:
        """Check if grid is completely filled."""
        for row in grid:
            if 0 in row:
                return False
        return True

    @staticmethod
    def is_valid_sudoku(grid: List[List[int]]) -> bool:
        """Check if current grid state violates constraints."""
        # Check rows
        for row in grid:
            non_zero = [x for x in row if x != 0]
            if len(non_zero) != len(set(non_zero)):
                return False

        # Check columns
        for col in range(9):
            non_zero = [grid[row][col] for row in range(9) if grid[row][col] != 0]
            if len(non_zero) != len(set(non_zero)):
                return False

        # Check boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                non_zero = []
                for r in range(box_row, box_row + 3):
                    for c in range(box_col, box_col + 3):
                        if grid[r][c] != 0:
                            non_zero.append(grid[r][c])
                if len(non_zero) != len(set(non_zero)):
                    return False

        return True

    @staticmethod
    def count_violations(grid: List[List[int]]) -> int:
        """Count constraint violations in the grid (for local search)."""
        violations = 0
        seen = set()

        # Count duplicate values in each row
        for row in grid:
            seen.clear()
            for val in row:
                if val != 0:
                    if val in seen:
                        violations += 1
                    seen.add(val)

        # Count duplicate values in each column
        for col in range(9):
            seen.clear()
            for row in range(9):
                val = grid[row][col]
                if val != 0:
                    if val in seen:
                        violations += 1
                    seen.add(val)

        # Count duplicate values in each box
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                seen.clear()
                for r in range(box_row, box_row + 3):
                    for c in range(box_col, box_col + 3):
                        val = grid[r][c]
                        if val != 0:
                            if val in seen:
                                violations += 1
                            seen.add(val)

        return violations
