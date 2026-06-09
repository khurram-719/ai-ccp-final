from flask import Blueprint, request, jsonify
from modules.puzzle_generator import PuzzleGenerator

puzzle_bp = Blueprint('puzzle', __name__, url_prefix='/api')
generator = PuzzleGenerator()

@puzzle_bp.route('/generate', methods=['POST'])
def generate():
    """Generate a new Sudoku puzzle."""
    data = request.get_json()
    difficulty = data.get('difficulty', 'Medium')

    try:
        puzzle = generator.generate(difficulty)

        # Count filled cells
        num_filled = sum(1 for row in puzzle for cell in row if cell != 0)

        return jsonify({
            'success': True,
            'puzzle': puzzle,
            'difficulty': difficulty,
            'num_cells_filled': num_filled
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
