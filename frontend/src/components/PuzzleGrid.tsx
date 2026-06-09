import React from 'react';

interface PuzzleGridProps {
  puzzle: number[][];
  solution?: number[][];
  currentState?: number[][];
  onCellChange?: (row: number, col: number, value: number) => void;
  showSolution?: boolean;
  isEditable?: boolean;
}

export function PuzzleGrid({
  puzzle,
  solution,
  currentState,
  onCellChange,
  showSolution = false,
  isEditable = false
}: PuzzleGridProps) {
  const displayGrid = currentState || solution || puzzle;

  const getCellClass = (row: number, col: number): string => {
    const baseClass = 'w-11 h-11 border flex items-center justify-center font-bold text-sm transition-all duration-200';
    const isOriginal = puzzle[row][col] !== 0;
    const isSolved = solution && solution[row][col] !== 0 && puzzle[row][col] === 0;

    let classes = baseClass;

    // Bold borders for 3x3 boxes
    if ((row + 1) % 3 === 0) classes += ' border-b-2';
    if ((col + 1) % 3 === 0) classes += ' border-r-2';

    if (isOriginal) {
      classes += ' bg-gradient-to-br from-slate-700 to-slate-800 text-cyan-300 border-white/30 cursor-default shadow-md';
    } else if (isSolved) {
      classes += ' bg-gradient-to-br from-emerald-900 to-teal-900 text-emerald-300 border-white/40 shadow-lg shadow-emerald-500/30 hover:shadow-emerald-500/50';
    } else {
      classes += ' bg-gradient-to-br from-slate-800 to-slate-900 text-white border-white/20 hover:bg-slate-700 hover:border-cyan-400 hover:shadow-lg hover:shadow-cyan-500/20';
    }

    return classes;
  };

  const handleCellChange = (row: number, col: number, value: string) => {
    if (!isEditable || puzzle[row][col] !== 0) return;

    const numValue = value === '' ? 0 : parseInt(value);
    if (numValue >= 0 && numValue <= 9) {
      onCellChange?.(row, col, numValue);
    }
  };

  return (
    <div className="inline-block border-2 border-white/40 rounded-lg overflow-hidden shadow-2xl shadow-cyan-500/20 hover:shadow-cyan-500/40 transition-shadow duration-300">
      {displayGrid.map((row, rowIdx) => (
        <div key={rowIdx} className="flex">
          {row.map((cell, colIdx) => (
            <input
              key={`${rowIdx}-${colIdx}`}
              type="text"
              maxLength={1}
              value={cell === 0 ? '' : cell}
              onChange={(e) => handleCellChange(rowIdx, colIdx, e.target.value)}
              disabled={!isEditable || puzzle[rowIdx][colIdx] !== 0}
              className={getCellClass(rowIdx, colIdx)}
            />
          ))}
        </div>
      ))}
    </div>
  );
}
