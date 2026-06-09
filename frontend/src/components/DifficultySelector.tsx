import { Difficulty } from '../types';

interface DifficultySelectorProps {
  selectedDifficulty: Difficulty;
  onDifficultyChange: (difficulty: Difficulty) => void;
  disabled?: boolean;
}

export function DifficultySelector({
  selectedDifficulty,
  onDifficultyChange,
  disabled = false
}: DifficultySelectorProps) {
  const difficulties: Difficulty[] = ['Easy', 'Medium', 'Hard', 'Expert'];
  
  const difficultyColors = {
    Easy: 'from-green-400 to-emerald-500',
    Medium: 'from-yellow-400 to-orange-500',
    Hard: 'from-orange-400 to-red-500',
    Expert: 'from-red-500 to-pink-600'
  };

  return (
    <div className="flex gap-3 flex-wrap">
      {difficulties.map((difficulty) => (
        <button
          key={difficulty}
          onClick={() => onDifficultyChange(difficulty)}
          disabled={disabled}
          className={`px-4 py-2 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105 active:scale-95 ${
            selectedDifficulty === difficulty
              ? `bg-gradient-to-r ${difficultyColors[difficulty]} text-white shadow-lg shadow-${difficulty.toLowerCase()}-500/50`
              : 'bg-white/10 text-gray-300 hover:bg-white/20 border border-white/20'
          } disabled:opacity-50 disabled:cursor-not-allowed disabled:scale-100`}
        >
          {difficulty}
        </button>
      ))}
    </div>
  );
}
