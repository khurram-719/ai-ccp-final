from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.puzzle import puzzle_bp
from routes.solver import solver_bp
from routes.comparison import comparison_bp

def create_app(config_name='development'):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    # Register blueprints
    app.register_blueprint(puzzle_bp)
    app.register_blueprint(solver_bp)
    app.register_blueprint(comparison_bp)

    @app.route('/api/health', methods=['GET'])
    def health():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'message': 'Sudoku Solver API is running'
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Endpoint not found'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)
