import { Algorithm } from '../types';

interface AlgorithmSelectorProps {
  selectedAlgorithm: Algorithm;
  onAlgorithmChange: (algorithm: Algorithm) => void;
  disabled?: boolean;
  competitive?: boolean;
}

const algorithmInfo = {
  backtracking: {
    name: 'Backtracking',
    description: '🔄 Uninformed DFS - Exhaustive tree search',
    icon: '📊'
  },
  ac3_mrv: {
    name: 'AC-3 + MRV',
    description: '🎯 Constraint propagation + heuristics',
    icon: '⚡'
  },
  forward_checking: {
    name: 'Forward Checking',
    description: '✅ Domain reduction during search',
    icon: '🔗'
  },
  simulated_annealing: {
    name: 'Simulated Annealing',
    description: '🌡️ Local search with probabilistic jumps',
    icon: '🔥'
  }
};

export function AlgorithmSelector({
  selectedAlgorithm,
  onAlgorithmChange,
  disabled = false,
  competitive = false
}: AlgorithmSelectorProps) {
  const algorithms: Algorithm[] = ['backtracking', 'ac3_mrv', 'forward_checking', 'simulated_annealing'];

  return (
    <div className="flex flex-col gap-4">
      {competitive ? (
        <div className="text-sm text-gray-300 bg-white/5 p-3 rounded-lg border border-white/10">
          🏆 Competitive mode will run all algorithms and compare their performance
        </div>
      ) : (
        <div className="grid grid-cols-2 gap-2">
          {algorithms.map((algo) => (
            <button
              key={algo}
              onClick={() => onAlgorithmChange(algo)}
              disabled={disabled}
              className={`p-3 rounded-lg transition-all duration-200 transform hover:scale-105 active:scale-95 ${
                selectedAlgorithm === algo
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-blue-500/50'
                  : 'bg-white/10 text-gray-300 hover:bg-white/20 border border-white/20'
              } disabled:opacity-50 disabled:cursor-not-allowed disabled:scale-100 font-medium`}
            >
              <div className="text-lg mb-1">{algorithmInfo[algo].icon}</div>
              {algorithmInfo[algo].name}
            </button>
          ))}
        </div>
      )}

      {!competitive && (
        <div className="text-xs text-gray-300 bg-white/5 p-3 rounded-lg border border-white/10 flex items-start gap-2">
          <span className="text-base mt-0.5">💡</span>
          <span>{algorithmInfo[selectedAlgorithm].description}</span>
        </div>
      )}
    </div>
  );
}
