# AI-Powered Multi-Level Sudoku Solver and Evaluator

A clean, modular repository with two primary folders:
- `frontend/` — React + TypeScript user interface
- `backend/` — Python Flask API and solver implementation

## Repository Layout

- `backend/`
  - `app.py` — Flask application entry point
  - `config.py` — environment and difficulty settings
  - `requirements.txt` — Python dependencies
  - `modules/` — puzzle generation, CSP helper tools, performance tracking
  - `solvers/` — four solver modules
  - `routes/` — API endpoints
- `frontend/`
  - Vite-based React application
  - `src/` contains UI components, hooks, and types
- `docs/` — project documentation deliverables
- `.gitignore` — ignore rules for artifacts and generated files

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt
python app.py
```

Backend API runs on `http://localhost:5000`.

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend UI runs on `http://localhost:5173`.

## Notes

- Keep backend dependencies in `backend/requirements.txt`.
- Keep frontend dependencies in `frontend/package.json`.
- Documentation is stored in `docs/`.

## Documentation

- `docs/IMPLEMENTATION_GUIDE.md`
- `docs/CCP_SOLUTION_SUMMARY.md`
- `docs/SETUP_AND_TESTING.md`
- `backend/API_REFERENCE.md`

---
