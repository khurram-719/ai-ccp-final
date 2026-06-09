import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { ComparisonResult } from '../types';

interface AnalyticsDashboardProps {
  comparison: ComparisonResult;
}

export function AnalyticsDashboard({ comparison }: AnalyticsDashboardProps) {
  const successfulResults = comparison.results.filter(r => r.success);

  if (successfulResults.length === 0) {
    return (
      <div className="text-center py-12 text-gray-300 bg-white/5 rounded-lg border border-white/10">
        <span className="text-3xl">🚫</span>
        <p className="mt-2">No successful solutions to compare</p>
      </div>
    );
  }

  const chartData = successfulResults.map(r => ({
    algorithm: r.algorithm.replace(/_/g, ' ').toUpperCase(),
    time: parseFloat(r.metrics.time_ms.toFixed(2)),
    states: r.metrics.states_explored,
    backtracks: r.metrics.backtracks
  }));

  const chartColors = {
    time: '#06b6d4',
    states: '#10b981',
    backtracks: '#f59e0b'
  };

  return (
    <div className="flex flex-col gap-6">
      <div className="bg-white/10 backdrop-blur-md p-6 rounded-2xl border border-white/20">
        <h3 className="text-xl font-bold mb-3 text-cyan-300 flex items-center gap-2">
          🏆 Winner: <span className="text-pink-300">{comparison.winner?.toUpperCase().replace(/_/g, ' ')}</span>
        </h3>
        <p className="text-gray-300 leading-relaxed">{comparison.analysis}</p>
      </div>

      <div className="bg-white/10 backdrop-blur-md p-6 rounded-2xl border border-white/20">
        <h3 className="text-lg font-bold mb-6 text-cyan-300 flex items-center gap-2">
          ⏱️ Execution Time (ms)
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey="algorithm" stroke="rgba(255,255,255,0.6)" />
            <YAxis stroke="rgba(255,255,255,0.6)" />
            <Tooltip 
              contentStyle={{ backgroundColor: 'rgba(15, 23, 42, 0.9)', border: '1px solid rgba(255,255,255,0.2)' }}
              labelStyle={{ color: '#06b6d4' }}
            />
            <Bar dataKey="time" fill={chartColors.time} radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white/10 backdrop-blur-md p-6 rounded-2xl border border-white/20">
        <h3 className="text-lg font-bold mb-6 text-emerald-300 flex items-center gap-2">
          🔍 States Explored
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey="algorithm" stroke="rgba(255,255,255,0.6)" />
            <YAxis stroke="rgba(255,255,255,0.6)" />
            <Tooltip 
              contentStyle={{ backgroundColor: 'rgba(15, 23, 42, 0.9)', border: '1px solid rgba(255,255,255,0.2)' }}
              labelStyle={{ color: '#10b981' }}
            />
            <Bar dataKey="states" fill={chartColors.states} radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white/10 backdrop-blur-md p-6 rounded-2xl border border-white/20">
        <h3 className="text-lg font-bold mb-6 text-orange-300 flex items-center gap-2">
          ↩️ Backtracks Performed
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey="algorithm" stroke="rgba(255,255,255,0.6)" />
            <YAxis stroke="rgba(255,255,255,0.6)" />
            <Tooltip 
              contentStyle={{ backgroundColor: 'rgba(15, 23, 42, 0.9)', border: '1px solid rgba(255,255,255,0.2)' }}
              labelStyle={{ color: '#f59e0b' }}
            />
            <Bar dataKey="backtracks" fill={chartColors.backtracks} radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white/10 backdrop-blur-md p-6 rounded-2xl border border-white/20">
        <h3 className="text-lg font-bold mb-6 text-purple-300">📊 Detailed Comparison</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-white/20">
                <th className="px-4 py-3 text-left text-cyan-300 font-bold">Algorithm</th>
                <th className="px-4 py-3 text-right text-emerald-300 font-bold">Time (ms)</th>
                <th className="px-4 py-3 text-right text-blue-300 font-bold">States</th>
                <th className="px-4 py-3 text-right text-orange-300 font-bold">Backtracks</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/10">
              {chartData.map((row, idx) => (
                <tr
                  key={row.algorithm}
                  className={`transition-all duration-200 hover:bg-white/10 ${
                    row.algorithm === comparison.winner?.toUpperCase().replace(/_/g, ' ')
                      ? 'bg-gradient-to-r from-yellow-500/20 to-yellow-500/5 border-l-2 border-yellow-400'
                      : ''
                  }`}
                >
                  <td className="px-4 py-3 font-bold text-white">
                    {idx === 0 && '🥇'} {idx === 1 && '🥈'} {idx === 2 && '🥉'} {row.algorithm}
                  </td>
                  <td className="px-4 py-3 text-right font-mono text-cyan-300">{row.time.toFixed(2)}</td>
                  <td className="px-4 py-3 text-right font-mono text-emerald-300">{row.states}</td>
                  <td className="px-4 py-3 text-right font-mono text-orange-300">{row.backtracks}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
