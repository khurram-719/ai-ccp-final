import time
from typing import Dict, Any, List

class PerformanceTracker:
    """Tracks performance metrics during puzzle solving."""

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.states_explored = 0
        self.backtracks = 0
        self.steps = []
        self.is_running = False

    def start(self):
        """Start tracking time."""
        self.start_time = time.time()
        self.is_running = True

    def stop(self):
        """Stop tracking time."""
        self.end_time = time.time()
        self.is_running = False

    def increment_states(self, count: int = 1):
        """Increment states explored counter."""
        if self.is_running:
            self.states_explored += count

    def increment_backtracks(self, count: int = 1):
        """Increment backtracks counter."""
        if self.is_running:
            self.backtracks += count

    def record_step(self, cell: tuple, value: int, state: List[List[int]]):
        """Record a solving step for visualization."""
        self.steps.append({
            'cell': cell,
            'value': value,
            'state': [row[:] for row in state]  # Deep copy
        })

    def get_time_ms(self) -> float:
        """Get elapsed time in milliseconds."""
        if self.start_time is None:
            return 0.0
        end = self.end_time if self.end_time else time.time()
        return (end - self.start_time) * 1000

    def get_metrics(self) -> Dict[str, Any]:
        """Get all tracked metrics."""
        return {
            'time_ms': self.get_time_ms(),
            'states_explored': self.states_explored,
            'backtracks': self.backtracks,
            'optimality': True
        }

    def reset(self):
        """Reset all metrics."""
        self.start_time = None
        self.end_time = None
        self.states_explored = 0
        self.backtracks = 0
        self.steps = []
        self.is_running = False
