export type Difficulty = 'Easy' | 'Medium' | 'Hard' | 'Expert';

export type Algorithm = 'backtracking' | 'ac3_mrv' | 'forward_checking' | 'simulated_annealing';

export interface SudokuGrid {
  puzzle: number[][];
  difficulty: Difficulty;
  num_cells_filled: number;
}

export interface SolveMetrics {
  time_ms: number;
  states_explored: number;
  backtracks: number;
  optimality: boolean;
}

export interface SolveStep {
  cell: [number, number];
  value: number;
  state: number[][];
}

export interface SolveResult {
  success: boolean;
  algorithm: Algorithm;
  solution: number[][];
  metrics: SolveMetrics;
  steps: SolveStep[];
}

export interface ComparisonResult {
  success: boolean;
  results: SolveResult[];
  winner: Algorithm;
  analysis: string;
}
