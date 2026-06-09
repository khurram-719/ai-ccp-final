import requests
import time
import json

API = 'http://127.0.0.1:5000/api'
DIFFICULTIES = ['Easy', 'Medium', 'Hard', 'Expert']
TRIALS_PER_DIFFICULTY = 5

def run_trial(difficulty):
    # Generate puzzle for difficulty
    resp = requests.post(f'{API}/generate', json={'difficulty': difficulty}, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    puzzle = data['puzzle']

    # Solve with simulated annealing
    start = time.time()
    solve = requests.post(f'{API}/solve', json={'puzzle': puzzle, 'algorithm': 'simulated_annealing', 'include_steps': False}, timeout=120)
    elapsed = (time.time() - start) * 1000
    result = None
    try:
        solve.raise_for_status()
        result = solve.json()
    except Exception as e:
        # capture error response if present
        try:
            result = solve.json()
        except Exception:
            result = {'success': False, 'error': str(e)}

    metrics = {
        'difficulty': difficulty,
        'elapsed_ms': elapsed,
        'puzzle_filled': data.get('num_cells_filled'),
        'result': result
    }
    return metrics

def main():
    report = {d: [] for d in DIFFICULTIES}

    for d in DIFFICULTIES:
        print(f'Running {TRIALS_PER_DIFFICULTY} trials for {d}...')
        for i in range(TRIALS_PER_DIFFICULTY):
            try:
                m = run_trial(d)
                report[d].append(m)
                print(f'  Trial {i+1}/{TRIALS_PER_DIFFICULTY}: success={m["result"].get("success", False)} time={m["elapsed_ms"]:.1f}ms')
            except Exception as e:
                print(f'  Trial {i+1}/{TRIALS_PER_DIFFICULTY} failed: {e}')
                report[d].append({'error': str(e)})

    out_file = 'sa_results.json'
    with open(out_file, 'w') as f:
        json.dump(report, f, indent=2)

    print('\nDone. Results written to', out_file)

if __name__ == '__main__':
    main()
