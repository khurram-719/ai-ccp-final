# Flask Backend API Reference

## Server Configuration

**Base URL:** `http://localhost:5000`
**Timeout:** 30 seconds per request
**CORS:** Enabled for all origins

---

## Endpoints

### 1. Health Check

```
GET /api/health
```

**Purpose:** Verify backend is running

**Response (200):**
```json
{
  "status": "healthy",
  "message": "Sudoku Solver API is running"
}
```

---

### 2. Generate Puzzle

```
POST /api/generate
```

**Purpose:** Generate a new Sudoku puzzle

**Request Body:**
```json
{
  "difficulty": "Easy"
}
```

**Difficulty Options:**
- `Easy`: 35-40 cells filled
- `Medium`: 30-34 cells filled (default)
- `Hard`: 25-29 cells filled
- `Expert`: 20-24 cells filled

**Response (200):**
```json
{
  "success": true,
  "puzzle": [
    [0, 5, 0, 0, 0, 0, 0, 0, 3],
    [0, 0, 8, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 6, 0, 0, 0, 0],
    [0, 0, 4, 0, 0, 0, 0, 0, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 3, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0, 0],
    [0, 9, 0, 0, 0, 0, 2, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 4, 0]
  ],
  "difficulty": "Easy",
  "num_cells_filled": 38
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "Invalid difficulty level"
}
```

---

### 3. Solve Puzzle

```
POST /api/solve
```

**Purpose:** Solve a puzzle using specified algorithm

**Request Body:**
```json
{
  "puzzle": [
    [0, 5, 0, 0, 0, 0, 0, 0, 3],
    ...
  ],
  "algorithm": "ac3_mrv",
  "include_steps": false
}
```

**Algorithm Options:**
- `backtracking`: Uninformed DFS search (baseline)
- `ac3_mrv`: Arc Consistency 3 with MRV heuristic (recommended)
- `forward_checking`: Constraint propagation with domain reduction
- `simulated_annealing`: Local search with probabilistic moves

**Parameters:**
- `puzzle` (required): 9×9 grid with 0 for empty cells, 1-9 for filled
- `algorithm` (required): One of the four algorithms above
- `include_steps` (optional, default=false): Record solving steps for visualization

**Response (200):**
```json
{
  "success": true,
  "algorithm": "ac3_mrv",
  "solution": [
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [7, 8, 1, 2, 3, 4, 5, 6, 9],
    ...
  ],
  "metrics": {
    "time_ms": 45.23,
    "states_explored": 250,
    "backtracks": 8,
    "optimality": true
  },
  "steps": [
    {
      "cell": [0, 0],
      "value": 1,
      "state": [[1, 5, 0, ...], ...]
    },
    ...
  ]
}
```

**Metrics Explanation:**
- `time_ms`: Wall-clock execution time in milliseconds
- `states_explored`: Number of nodes visited in search tree
- `backtracks`: Number of times algorithm backed up after failure
- `optimality`: Whether a valid solution was found
- `steps`: Array of solving steps (only if `include_steps=true`)

**Error Response (400):**
```json
{
  "success": false,
  "error": "Invalid puzzle format"
}
```

**Error Response (500):**
```json
{
  "success": false,
  "error": "Could not solve puzzle with ac3_mrv"
}
```

---

### 4. Compare Algorithms

```
POST /api/compare
```

**Purpose:** Run all algorithms on same puzzle and compare performance

**Request Body:**
```json
{
  "puzzle": [
    [0, 5, 0, 0, 0, 0, 0, 0, 3],
    ...
  ],
  "algorithms": ["backtracking", "ac3_mrv", "forward_checking", "simulated_annealing"]
}
```

**Parameters:**
- `puzzle` (required): 9×9 grid
- `algorithms` (optional): Array of algorithms to compare. If omitted, all four are run.

**Response (200):**
```json
{
  "success": true,
  "results": [
    {
      "algorithm": "backtracking",
      "success": true,
      "solution": [[4, 5, ...], ...],
      "metrics": {
        "time_ms": 1250.45,
        "states_explored": 15000,
        "backtracks": 450,
        "optimality": true
      }
    },
    {
      "algorithm": "ac3_mrv",
      "success": true,
      "solution": [[4, 5, ...], ...],
      "metrics": {
        "time_ms": 45.23,
        "states_explored": 250,
        "backtracks": 8,
        "optimality": true
      }
    },
    {
      "algorithm": "forward_checking",
      "success": true,
      "solution": [[4, 5, ...], ...],
      "metrics": {
        "time_ms": 125.67,
        "states_explored": 1800,
        "backtracks": 45,
        "optimality": true
      }
    },
    {
      "algorithm": "simulated_annealing",
      "success": true,
      "solution": [[4, 5, ...], ...],
      "metrics": {
        "time_ms": 234.89,
        "states_explored": 25000,
        "backtracks": 0,
        "optimality": true
      }
    }
  ],
  "winner": "ac3_mrv",
  "analysis": "AC-3 + MRV was the fastest solver. backtracking was 27.7x slower, exploring 15000 states vs 250. forward_checking was 2.8x slower, exploring 1800 states vs 250."
}
```

**Analysis Field:**
The `analysis` field contains a human-readable summary of comparative performance, including:
- Winner identification (fastest algorithm)
- Slowdown ratios for each algorithm
- State exploration comparison

---

## Error Handling

All error responses follow this format:

```json
{
  "success": false,
  "error": "Descriptive error message"
}
```

**Common HTTP Status Codes:**
- `200 OK`: Successful request
- `400 Bad Request`: Invalid puzzle format or parameters
- `404 Not Found`: Endpoint does not exist
- `500 Internal Server Error`: Server error during processing

---

## Performance Expectations

### Execution Times by Difficulty

**Easy Puzzles (35-40 cells):**
- Backtracking: 10-100 ms
- AC-3+MRV: 5-20 ms ⚡ Fastest
- Forward Checking: 10-50 ms
- Simulated Annealing: 50-200 ms

**Medium Puzzles (30-34 cells):**
- Backtracking: 100-500 ms
- AC-3+MRV: 20-100 ms ⚡ Fastest
- Forward Checking: 50-300 ms
- Simulated Annealing: 100-500 ms

**Hard Puzzles (25-29 cells):**
- Backtracking: 500-5000 ms
- AC-3+MRV: 100-500 ms ⚡ Fastest
- Forward Checking: 300-2000 ms
- Simulated Annealing: 200-1000 ms

**Expert Puzzles (20-24 cells):**
- Backtracking: 5000-30000+ ms (may timeout)
- AC-3+MRV: 200-800 ms ⚡ Fastest
- Forward Checking: 500-3000 ms
- Simulated Annealing: 300-1500 ms

---

## Request Examples

### Generate an Easy Puzzle

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "difficulty": "Easy"
  }'
```

### Solve with AC-3+MRV

```bash
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{
    "puzzle": [
      [0, 5, 0, 0, 0, 0, 0, 0, 3],
      [0, 0, 8, 0, 0, 0, 0, 1, 0],
      [0, 0, 0, 0, 6, 0, 0, 0, 0],
      [0, 0, 4, 0, 0, 0, 0, 0, 8],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [2, 0, 0, 0, 0, 0, 3, 0, 0],
      [0, 0, 0, 0, 5, 0, 0, 0, 0],
      [0, 9, 0, 0, 0, 0, 2, 0, 0],
      [7, 0, 0, 0, 0, 0, 0, 4, 0]
    ],
    "algorithm": "ac3_mrv",
    "include_steps": false
  }'
```

### Compare All Algorithms

```bash
curl -X POST http://localhost:5000/api/compare \
  -H "Content-Type: application/json" \
  -d '{
    "puzzle": [
      [0, 5, 0, 0, 0, 0, 0, 0, 3],
      ...
    ],
    "algorithms": ["backtracking", "ac3_mrv", "forward_checking", "simulated_annealing"]
  }'
```

---

## Python Client Example

```python
import requests
import json

BASE_URL = "http://localhost:5000/api"

# Generate puzzle
response = requests.post(
    f"{BASE_URL}/generate",
    json={"difficulty": "Medium"}
)
puzzle_data = response.json()
puzzle = puzzle_data['puzzle']

# Solve with AC-3+MRV
response = requests.post(
    f"{BASE_URL}/solve",
    json={
        "puzzle": puzzle,
        "algorithm": "ac3_mrv",
        "include_steps": True
    }
)
solution_data = response.json()

print(f"Algorithm: {solution_data['algorithm']}")
print(f"Time: {solution_data['metrics']['time_ms']:.2f} ms")
print(f"States: {solution_data['metrics']['states_explored']}")

# Compare all algorithms
response = requests.post(
    f"{BASE_URL}/compare",
    json={"puzzle": puzzle}
)
comparison = response.json()

print(f"Winner: {comparison['winner']}")
print(comparison['analysis'])
```

---

## Notes

1. **Grid Format**: Always use 0 for empty cells, 1-9 for filled cells
2. **Timeout**: Very complex Expert puzzles with Backtracking may take > 30 seconds
3. **Uniqueness**: Generated puzzles always have exactly one unique solution
4. **Determinism**: Backtracking and AC-3+MRV are deterministic; Simulated Annealing is probabilistic
5. **CORS**: All endpoints support CORS; safe to call from browser
