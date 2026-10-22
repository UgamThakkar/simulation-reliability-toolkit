import random
import sys

# Exit codes
SUCCESS = 0
BAD_INPUT = 10
DIVERGED = 20
INFRA_ERROR = 30
TIMEOUT = 40
OUT_OF_MEMORY = 50
FLAKY = 60

def chaos_failure():
    """Randomly returns an infrastructure-style failure, or None for a normal run."""
    roll = random.random()
    if roll < 0.05:
        worker = random.choice(["a3f9c1", "7be204", "d51e88"])
        return {"exit_code": INFRA_ERROR,
                "message": f"worker-{worker} lost connection",
                "final_value": None}
    if roll < 0.08:
        return {"exit_code": TIMEOUT,
                "message": f"job timed out after {random.randint(300, 900)} seconds",
                "final_value": None}
    if roll < 0.10:
        return {"exit_code": OUT_OF_MEMORY,
                "message": f"out of memory: tried to allocate {random.randint(2000, 9000)} MB",
                "final_value": None}
    if roll < 0.14:
        return {"exit_code": FLAKY,
                "message": f"checksum mismatch on block {random.randint(1, 64)}",
                "final_value": None}
    return None

def simulate(steps, chaos=False):
    """Runs one simulation and returns a dictionary describing what happened."""
    if steps <= 0:
        return {"exit_code": BAD_INPUT, "message": "steps must be positive", "final_value": None}

    if chaos:
        failure = chaos_failure()
        if failure:
            return failure

    value = 1.0
    for i in range(steps):
        value *= random.uniform(0.9, 1.125)
        if value > 1000:
            return {"exit_code": DIVERGED, "message": f"value diverged at step {i}", "final_value": None}

    return {"exit_code": SUCCESS, "message": "finished ok", "final_value": round(value, 3)}

def run_simulation(steps):
    """Prints the outcome and returns the exit code (used by the tests)."""
    result = simulate(steps)
    print(result["message"])
    return result["exit_code"]

if __name__ == "__main__":
    sys.exit(run_simulation(steps=500))