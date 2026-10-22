import json
import time
from collections import Counter
from datetime import datetime, timezone

from sim import simulate

NUM_RUNS = 1000
STEPS = 500

def main():
    exit_codes = Counter()

    with open("runs.jsonl", "w") as f:
        for run_id in range(NUM_RUNS):
            start = time.perf_counter()
            # result = simulate(STEPS, infra_failure_rate=0.05)
            result = simulate(STEPS, chaos=True)
            duration_ms = (time.perf_counter() - start) * 1000

            record = {
                "run_id": run_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "steps": STEPS,
                "exit_code": result["exit_code"],
                "message": result["message"],
                "final_value": result["final_value"],
                "duration_ms": round(duration_ms, 3),
            }
            f.write(json.dumps(record) + "\n")
            exit_codes[result["exit_code"]] += 1

    print(f"Ran {NUM_RUNS} simulations. Results saved to runs.jsonl")
    print("Exit code counts:", dict(exit_codes))

if __name__ == "__main__":
    main()