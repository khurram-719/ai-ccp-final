from flask import Blueprint, request, jsonify
from solvers.backtracking import BacktrackingSolver
from solvers.ac3_mrv import AC3MRVSolver
from solvers.forward_checking import ForwardCheckingSolver
from solvers.simulated_annealing import SimulatedAnnealingSolver

comparison_bp = Blueprint('comparison', __name__, url_prefix='/api')

SOLVERS = {
    'backtracking': BacktrackingSolver,
    'ac3_mrv': AC3MRVSolver,
    'forward_checking': ForwardCheckingSolver,
    'simulated_annealing': SimulatedAnnealingSolver
}

@comparison_bp.route('/compare', methods=['POST'])
def compare():
    """Run all algorithms on same puzzle and compare performance."""
    data = request.get_json()
    puzzle = data.get('puzzle')
    algorithms = data.get('algorithms', list(SOLVERS.keys()))

    if not puzzle or len(puzzle) != 9 or any(len(row) != 9 for row in puzzle):
        return jsonify({
            'success': False,
            'error': 'Invalid puzzle format'
        }), 400

    results = []
    winner = None
    best_time = float('inf')

    try:
        for algo_name in algorithms:
            if algo_name not in SOLVERS:
                continue

            solver = SOLVERS[algo_name]()
            solution = solver.solve(puzzle, track_steps=False)

            metrics = solver.get_metrics()
            time_ms = metrics['time_ms']

            result = {
                'algorithm': algo_name,
                'success': solution is not None,
                'metrics': metrics
            }

            if solution is not None:
                result['solution'] = solution
                if time_ms < best_time:
                    best_time = time_ms
                    winner = algo_name

            results.append(result)

        analysis = _generate_analysis(results, winner)

        return jsonify({
            'success': True,
            'results': results,
            'winner': winner,
            'analysis': analysis
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def _generate_analysis(results: list, winner: str) -> str:
    """Generate analysis of algorithm performance comparison."""
    if not results:
        return "No results to analyze"

    successful = [r for r in results if r['success']]
    if not successful:
        return "No algorithms successfully solved the puzzle"

    # Calculate speedups
    winner_time = next(r['metrics']['time_ms'] for r in results if r['algorithm'] == winner)

    analysis_parts = []
    analysis_parts.append(f"{winner} was the fastest solver.")

    for result in results:
        if result['algorithm'] != winner and result['success']:
            slowdown = result['metrics']['time_ms'] / winner_time
            analysis_parts.append(
                f"{result['algorithm']} was {slowdown:.1f}x slower, "
                f"exploring {result['metrics']['states_explored']} states vs "
                f"{next(r['metrics']['states_explored'] for r in results if r['algorithm'] == winner)}"
            )

    return " ".join(analysis_parts)
