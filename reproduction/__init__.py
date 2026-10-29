import csv
import os
from pathlib import Path

from reproduction.config import MANUSCRIPT_CONFIG
from reproduction.simulator import run_experiment


METRICS = [
    "method",
    "task_count",
    "compute_scale",
    "average_task_completion_time",
    "task_transmission_time",
    "task_handover_time",
    "task_execution_time",
    "task_transmission_energy",
    "task_throughput",
]


def run_experiment_matrix(config=MANUSCRIPT_CONFIG):
    rows = []
    for method in ["ECA-MARL", "DRL-CCMCO", "DTOSC"]:
        for task_count in config.task_counts:
            for compute_scale in config.task_compute_sweeps:
                result = run_experiment(
                    method=method,
                    task_count=task_count,
                    compute_scale=compute_scale,
                    bandwidth_range=config.bandwidth_range,
                    seed=config.random_seed,
                )
                rows.append(result)

    output_dir = Path(__file__).resolve().parent / "results"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "experiment_summary.csv"

    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=METRICS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in METRICS})

    return rows, output_path


if __name__ == "__main__":
    rows, output_path = run_experiment_matrix()
    print(f"Saved {len(rows)} rows to {output_path}")
