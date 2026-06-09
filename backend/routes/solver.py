from flask import Blueprint, request, jsonify
from solvers.backtracking import BacktrackingSolver
from solvers.ac3_mrv import AC3MRVSolver
from solvers.forward_checking import ForwardCheckingSolver
from solvers.simulated_annealing import SimulatedAnnealingSolver

solver_bp = Blueprint('solver', __name__, url_prefix='/api')

SOLVERS = {
    'backtracking': BacktrackingSolver,
    'ac3_mrv': AC3MRVSolver,
    'forward_checking': ForwardCheckingSolver,
    'simulated_annealing': SimulatedAnnealingSolver
}

@solver_bp.route('/solve', methods=['POST'])
def solve():
    """Solve a Sudoku puzzle with specified algorithm."""
    data = request.get_json()
    puzzle = data.get('puzzle')
    algorithm = data.get('algorithm', 'backtracking')
    include_steps = data.get('include_steps', False)

    if not puzzle or len(puzzle) != 9 or any(len(row) != 9 for row in puzzle):
        return jsonify({
            'success': False,
            'error': 'Invalid puzzle format'
        }), 400

    if algorithm not in SOLVERS:
        return jsonify({
            'success': False,
            'error': f'Unknown algorithm: {algorithm}'
        }), 400

    try:
        solver = SOLVERS[algorithm]()
        solution = solver.solve(puzzle, track_steps=include_steps)

        if solution:
            return jsonify({
                'success': True,
                'algorithm': algorithm,
                'solution': solution,
                'metrics': solver.get_metrics(),
                'steps': solver.get_steps() if include_steps else []
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Could not solve puzzle with {algorithm}'
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
