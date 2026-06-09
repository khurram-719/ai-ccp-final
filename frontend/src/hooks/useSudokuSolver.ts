import { useState } from 'react';
import { SudokuGrid, SolveResult, ComparisonResult, Algorithm, Difficulty } from '../types';

// In production the Flask backend is served from the same origin under `/api`
// (see root vercel.json). Override locally via VITE_API_URL if needed.
const API_URL = import.meta.env.VITE_API_URL ?? '/api';

export function useSudokuSolver() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generatePuzzle = async (difficulty: Difficulty): Promise<SudokuGrid | null> => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ difficulty })
      });

      if (!response.ok) throw new Error('Failed to generate puzzle');

      const data = await response.json();
      if (!data.success) throw new Error(data.error);

      return data;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      setError(message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  const solvePuzzle = async (puzzle: number[][], algorithm: Algorithm, includeSteps: boolean = false): Promise<SolveResult | null> => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/solve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ puzzle, algorithm, include_steps: includeSteps })
      });

      if (!response.ok) throw new Error('Failed to solve puzzle');

      const data = await response.json();
      if (!data.success) throw new Error(data.error);

      return data;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      setError(message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  const compareSolvers = async (puzzle: number[][], algorithms: Algorithm[]): Promise<ComparisonResult | null> => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_URL}/compare`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ puzzle, algorithms })
      });

      if (!response.ok) throw new Error('Failed to compare solvers');

      const data = await response.json();
      if (!data.success) throw new Error(data.error);

      return data;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unknown error';
      setError(message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    error,
    generatePuzzle,
    solvePuzzle,
    compareSolvers
  };
}
