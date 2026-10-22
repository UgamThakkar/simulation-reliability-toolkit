import json
import re
from collections import Counter, defaultdict

CATEGORY = {
    10: "user/input problem",
    20: "code/numerical bug",
    30: "infrastructure problem",
    40: "timeout (performance or infra)",
    50: "resource limit (code or config)",
    60: "flaky failure",
}

def normalize(message):
    """Mask the parts that change every time so similar messages look identical."""
    message = re.sub(r"worker-[0-9a-f]+", "worker-<ID>", message)  # worker names first
    message = re.sub(r"\d+", "<N>", message)                        # then any numbers
    return message

def main():
    runs = []
    with open("runs.jsonl") as f:
        for line in f:
            runs.append(json.loads(line))

    failures = [r for r in runs if r["exit_code"] != 0]

    # Group failures by (exit code, normalized message)
    groups = Counter()
    time_wasted = defaultdict(float)
    for r in failures:
        signature = (r["exit_code"], normalize(r["message"]))
        groups[signature] += 1
        time_wasted[signature] += r["duration_ms"]

    total_time = sum(r["duration_ms"] for r in runs)
    failed_time = sum(r["duration_ms"] for r in failures)

    print(f"Total runs:     {len(runs)}")
    print(f"Failed runs:    {len(failures)}")
    print(f"Root causes:    {len(groups)}")
    print(f"Compute spent on failed runs: {failed_time / total_time:.1%}")
    print()
    print("Failure signatures (most common first):")
    print("-" * 70)
    for (code, sig), count in groups.most_common():
        category = CATEGORY.get(code, "unknown")
        print(f"{count:>5}x  code {code}  [{category}]")
        print(f"        {sig}")

if __name__ == "__main__":
    main()