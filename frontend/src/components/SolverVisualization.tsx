import { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw } from 'lucide-react';
import { SolveResult } from '../types';
import { PuzzleGrid } from './PuzzleGrid';

interface SolverVisualizationProps {
  result: SolveResult;
  puzzle: number[][];
}

export function SolverVisualization({ result, puzzle }: SolverVisualizationProps) {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  const steps = result.steps || [];
  const currentState = steps.length > 0 ? steps[currentStepIndex].state : result.solution;

  useEffect(() => {
    if (!isPlaying) return;

    const timer = setTimeout(() => {
      if (currentStepIndex < steps.length - 1) {
        setCurrentStepIndex(currentStepIndex + 1);
      } else {
        setIsPlaying(false);
      }
    }, 100);

    return () => clearTimeout(timer);
  }, [isPlaying, currentStepIndex, steps.length]);

  const handlePlayPause = () => {
    if (steps.length === 0) return;
    setIsPlaying(!isPlaying);
  };

  const handleReset = () => {
    setCurrentStepIndex(0);
    setIsPlaying(false);
  };

  return (
    <div className="flex flex-col gap-6">
      <div className="flex justify-center">
        <PuzzleGrid
          puzzle={puzzle}
          currentState={currentState}
          showSolution={steps.length === 0}
        />
      </div>

      {steps.length > 0 && (
        <div className="flex flex-col gap-4">
          <div className="flex gap-3 items-center justify-center">
            <button
              onClick={handlePlayPause}
              className="px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95 flex items-center gap-2 font-semibold shadow-lg shadow-blue-500/50"
            >
              {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              {isPlaying ? 'Pause' : 'Play'}
            </button>
            <button
              onClick={handleReset}
              className="px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95 border border-white/20 flex items-center gap-2 font-semibold"
            >
              <RotateCcw className="w-4 h-4" />
              Reset
            </button>
            <span className="text-sm text-cyan-300 bg-white/5 px-3 py-2 rounded-lg border border-white/10">
              Step {currentStepIndex + 1} of {steps.length}
            </span>
          </div>

          <input
            type="range"
            min="0"
            max={steps.length - 1}
            value={currentStepIndex}
            onChange={(e) => {
              setCurrentStepIndex(parseInt(e.target.value));
              setIsPlaying(false);
            }}
            className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer accent-cyan-500"
          />
        </div>
      )}

      <div className="bg-gradient-to-br from-white/10 to-white/5 p-5 rounded-xl border border-white/20">
        <h4 className="font-bold mb-4 text-lg text-cyan-300 flex items-center gap-2">
          📊 Performance Metrics
        </h4>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="bg-white/5 p-3 rounded-lg border border-white/10">
            <span className="text-gray-300">⏱️ Time Taken</span>
            <div className="font-bold text-cyan-300 mt-1 text-lg">{result.metrics.time_ms.toFixed(2)} ms</div>
          </div>
          <div className="bg-white/5 p-3 rounded-lg border border-white/10">
            <span className="text-gray-300">🔍 States Explored</span>
            <div className="font-bold text-emerald-300 mt-1 text-lg">{result.metrics.states_explored}</div>
          </div>
          <div className="bg-white/5 p-3 rounded-lg border border-white/10">
            <span className="text-gray-300">↩️ Backtracks</span>
            <div className="font-bold text-orange-300 mt-1 text-lg">{result.metrics.backtracks}</div>
          </div>
          <div className="bg-white/5 p-3 rounded-lg border border-white/10">
            <span className="text-gray-300">✨ Optimal</span>
            <div className="font-bold mt-1 text-lg">
              <span className={result.metrics.optimality ? 'text-green-400' : 'text-red-400'}>
                {result.metrics.optimality ? '✓ Yes' : '✗ No'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
