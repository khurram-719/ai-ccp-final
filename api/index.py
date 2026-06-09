import os
import sys

# Make the backend package importable (its modules use absolute imports
# like `from routes.puzzle import puzzle_bp` and `from config import Config`).
BACKEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app import create_app

# Vercel's Python runtime detects a WSGI/ASGI callable named `app`.
app = create_app("production")
