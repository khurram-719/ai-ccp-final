import { useState } from 'react';
import { Zap, BarChart3, Brain, Sparkles } from 'lucide-react';
import { useSudokuSolver } from './hooks/useSudokuSolver';
import { PuzzleGrid } from './components/PuzzleGrid';
import { DifficultySelector } from './components/DifficultySelector';
import { AlgorithmSelector } from './components/AlgorithmSelector';
import { SolverVisualization } from './components/SolverVisualization';
import { AnalyticsDashboard } from './components/AnalyticsDashboard';
import type { Difficulty, Algorithm, SolveResult, ComparisonResult } from './types';

type Mode = 'puzzle' | 'solve' | 'competitive';

function App() {
  const [mode, setMode] = useState<Mode>('puzzle');
  const [difficulty, setDifficulty] = useState<Difficulty>('Medium');
  const [algorithm, setAlgorithm] = useState<Algorithm>('ac3_mrv');
  const [puzzle, setPuzzle] = useState<number[][] | null>(null);
  const [solveResult, setSolveResult] = useState<SolveResult | null>(null);
  const [comparisonResult, setComparisonResult] = useState<ComparisonResult | null>(null);

  const { loading, error, generatePuzzle, solvePuzzle, compareSolvers } = useSudokuSolver();

  const handleGeneratePuzzle = async () => {
    const generated = await generatePuzzle(difficulty);
    if (generated) {
      setPuzzle(generated.puzzle);
      setSolveResult(null);
      setComparisonResult(null);
      setMode('puzzle');
    }
  };

  const handleSolvePuzzle = async () => {
    if (!puzzle) return;
    const result = await solvePuzzle(puzzle, algorithm, true);
    if (result) {
      setSolveResult(result);
      setMode('solve');
    }
  };

  const handleCompare = async () => {
    if (!puzzle) return;
    const result = await compareSolvers(puzzle, ['backtracking', 'ac3_mrv', 'forward_checking', 'simulated_annealing']);
    if (result) {
      setComparisonResult(result);
      setMode('competitive');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      {/* Animated Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 -left-4 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
        <div className="absolute top-0 -right-4 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      {/* Header */}
      <header className="sticky top-0 z-50 backdrop-blur-md bg-white/10 border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4 group">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg blur opacity-75 group-hover:opacity-100 transition duration-300"></div>
                <div className="relative bg-slate-900 rounded-lg p-2">
                  <Brain className="w-8 h-8 text-cyan-400" />
                </div>
              </div>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
                  Sudoku AI Solver
                </h1>
                <p className="text-xs text-purple-300 mt-1">Powered by Advanced Search Algorithms</p>
              </div>
            </div>
            <Sparkles className="w-6 h-6 text-yellow-300 animate-pulse" />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Mode Tabs */}
        <div className="flex gap-2 mb-8 bg-white/5 backdrop-blur-md rounded-lg p-1 border border-white/10 w-fit mx-auto">
          {['puzzle', 'solve', 'competitive'].map((m) => (
            <button
              key={m}
              onClick={() => setMode(m as Mode)}
              disabled={m !== 'puzzle' && !puzzle}
              className={`px-6 py-3 rounded-md font-medium transition-all duration-200 flex items-center gap-2 ${
                mode === m
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white shadow-lg shadow-blue-500/50'
                  : 'text-gray-300 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed'
              }`}
            >
              {m === 'puzzle' && '🧩 Puzzle'}
              {m === 'solve' && '⚙️ Solve'}
              {m === 'competitive' && <><BarChart3 className="w-4 h-4" /> Compete</>}
            </button>
          ))}
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-500/20 backdrop-blur border border-red-500/50 rounded-lg text-red-200">
            ⚠️ {error}
          </div>
        )}

        {/* Puzzle Mode */}
        {mode === 'puzzle' && (
          <div className="bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl p-8 border border-white/20">
            <div className="flex items-center gap-3 mb-8">
              <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-emerald-400 to-teal-500 flex items-center justify-center">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <h2 className="text-3xl font-bold bg-gradient-to-r from-emerald-400 to-teal-300 bg-clip-text text-transparent">
                Generate Puzzle
              </h2>
            </div>

            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-200 mb-4">
                  Difficulty Level
                </label>
                <DifficultySelector
                  selectedDifficulty={difficulty}
                  onDifficultyChange={setDifficulty}
                  disabled={loading}
                />
              </div>

              <button
                onClick={handleGeneratePuzzle}
                disabled={loading}
                className="w-full px-6 py-4 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-bold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-emerald-500/50 disabled:shadow-none"
              >
                {loading ? '🔄 Generating Puzzle...' : '✨ Generate New Puzzle'}
              </button>

              {puzzle && (
                <div className="mt-8 pt-8 border-t border-white/10">
                  <h3 className="text-lg font-semibold text-cyan-300 mb-6">📋 Current Puzzle</h3>
                  <div className="flex justify-center bg-white/5 rounded-lg p-6 border border-white/10">
                    <PuzzleGrid puzzle={puzzle} />
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Single Solver Mode */}
        {mode === 'solve' && puzzle && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Left: Controls */}
            <div className="bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl p-8 border border-white/20">
              <div className="flex items-center gap-3 mb-8">
                <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-400 to-cyan-500 flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent">
                  Solve Puzzle
                </h2>
              </div>

              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-200 mb-4">
                    Select Algorithm
                  </label>
                  <AlgorithmSelector
                    selectedAlgorithm={algorithm}
                    onAlgorithmChange={setAlgorithm}
                    disabled={loading}
                  />
                </div>

                <button
                  onClick={handleSolvePuzzle}
                  disabled={loading}
                  className="w-full px-6 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white font-bold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-blue-500/50 disabled:shadow-none"
                >
                  {loading ? '🧠 Thinking...' : '⚡ Solve Puzzle'}
                </button>

                <div className="border-t border-white/10 pt-6">
                  <h3 className="text-lg font-semibold text-cyan-300 mb-6">📋 Original Puzzle</h3>
                  <div className="flex justify-center bg-white/5 rounded-lg p-4 border border-white/10">
                    <PuzzleGrid puzzle={puzzle} />
                  </div>
                </div>
              </div>
            </div>

            {/* Right: Results */}
            <div className="bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl p-8 border border-white/20">
              {solveResult ? (
                <div>
                  <div className="flex items-center gap-3 mb-8">
                    <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-purple-400 to-pink-500 flex items-center justify-center">
                      <Brain className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-300 bg-clip-text text-transparent">
                      Solution
                    </h3>
                  </div>
                  <SolverVisualization result={solveResult} puzzle={puzzle} />
                </div>
              ) : (
                <div className="text-center py-20">
                  <Sparkles className="w-12 h-12 text-purple-400 mx-auto mb-4 opacity-50" />
                  <p className="text-gray-300">Click "Solve Puzzle" to see results here</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Competitive Mode */}
        {mode === 'competitive' && puzzle && (
          <div className="space-y-6">
            <div className="bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl p-8 border border-white/20">
              <div className="flex items-center justify-between mb-8 flex-wrap gap-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-orange-400 to-red-500 flex items-center justify-center">
                    <BarChart3 className="w-6 h-6 text-white" />
                  </div>
                  <h2 className="text-3xl font-bold bg-gradient-to-r from-orange-400 to-red-300 bg-clip-text text-transparent">
                    Algorithm Showdown
                  </h2>
                </div>
                <button
                  onClick={handleCompare}
                  disabled={loading}
                  className="px-6 py-3 bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 text-white font-bold rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-orange-500/50"
                >
                  {loading ? '🔄 Running Competition...' : '🏁 Run Competition'}
                </button>
              </div>

              <div className="flex justify-center bg-white/5 rounded-lg p-6 border border-white/10">
                <PuzzleGrid puzzle={puzzle} />
              </div>
            </div>

            {comparisonResult && (
              <AnalyticsDashboard comparison={comparisonResult} />
            )}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/10 mt-12 backdrop-blur-md bg-white/5">
        <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
          <div className="flex flex-col items-center justify-center gap-3">
            <p className="text-sm text-gray-300">
              🚀 Sudoku AI Solver - Powered by Advanced Search Algorithms
            </p>
            <p className="text-xs text-gray-400">
              CSC202 Artificial Intelligence - Complex Computing Problem (CCP)
            </p>
          </div>
        </div>
      </footer>

      {/* CSS for animations */}
      <style>{`
        @keyframes blob {
          0%, 100% { transform: translate(0, 0) scale(1); }
          33% { transform: translate(30px, -50px) scale(1.1); }
          66% { transform: translate(-20px, 20px) scale(0.9); }
        }
        .animate-blob {
          animation: blob 7s infinite;
        }
        .animation-delay-2000 {
          animation-delay: 2s;
        }
        .animation-delay-4000 {
          animation-delay: 4s;
        }
      `}</style>
    </div>
  );
}

export default App;
