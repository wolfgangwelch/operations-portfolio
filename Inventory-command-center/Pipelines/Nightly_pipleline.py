import subprocess
import sys

STEPS = [
    [sys.executable, "src/load_purchases.py"],
    [sys.executable, "src/load_transfers.py"],
    [sys.executable, "src/load_pos_sales.py"],
    [sys.executable, "src/load_recipes.py"],
]


def run_step(step):
    print(f"Running: {' '.join(step)}")
    result = subprocess.run(step, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Step failed: {' '.join(step)}")


def main():
    for step in STEPS:
        run_step(step)
    print("Nightly pipeline completed successfully.")


if __name__ == "__main__":
    main()
