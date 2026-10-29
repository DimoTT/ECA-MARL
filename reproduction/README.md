#!/usr/bin/env python3
"""Run the approximate ECA-MARL experiment matrix and write CSV results.

This wrapper is intentionally simple and paper-driven: it uses the reported setup
values from the supporting materials collection and produces a reproducible output
file for exploration and comparison.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from reproduction.config import MANUSCRIPT_CONFIG
from reproduction.simulator import run_experiment


DEFAULT_OUTPUT = Path(__file__).resolve().parent / "results" / "experiment_summary.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Approximate ECA-MARL experiment runner")
    parser.add_argument("--method", choices=["ECA-MARL", "DRL-CCMCO", "DTOSC"], default=None,
                        help="If set, run only this method; otherwise run all three.")
    parser.add_argument("--task-count", type=int, default=None,
                        help="Override task count for a single-method run.")
    parser.add_argument("--compute-scale", type=float, default=None,
                        help="Override task compute scale for a single-method run.")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT),
                        help="Where to write the experiment CSV summary.")
    return parser.parse_args()


def build_rows(method_override=None, task_count_override=None, compute_scale_override=None):
    config = MANUSCRIPT_CONFIG
    methods = [method_override] if method_override else ["ECA-MARL", "DRL-CCMCO", "DTOSC"]
    task_counts = [task_count_override] if task_count_override is not None else list(config.task_counts)
    compute_scales = [compute_scale_override] if compute_scale_override is not None else list(config.task_compute_sweeps)

    rows = []
    for method in methods:
        for task_count in task_counts:
            for compute_scale in compute_scales:
                row = run_experiment(
                    method=method,
                    task_count=task_count,
                    compute_scale=compute_scale,
                    bandwidth_range=config.bandwidth_range,
                    seed=config.random_seed,
                )
                rows.append(row)
    return rows


def write_csv(rows, output_path: Path):
    fieldnames = [
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

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})

    return output_path


def main():
    args = parse_args()
    rows = build_rows(
        method_override=args.method,
        task_count_override=args.task_count,
        compute_scale_override=args.compute_scale,
    )
    output_path = write_csv(rows, Path(args.output))
    print(f"Generated {len(rows)} experiment rows in {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
