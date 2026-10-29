from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Dict, Any
import random
import math


@dataclass
class Task:
    task_id: int
    source_node: int
    data_mb: float
    compute_cycles: float
    deadline: float


@dataclass
class EdgeServer:
    server_id: int
    compute_capacity: float
    network_bandwidth: float
    energy_per_bit: float
    queue_delay: float = 0.0

    def score(self, task: Task, method: str) -> float:
        # A deliberately simple but explainable proxy for the strategic server choice.
        # The goal is to be transparent enough to reason about, while matching the paper's
        # multi-agent optimization style without requiring the unavailable original code.
        if method == "ECA-MARL":
            return self.compute_capacity / max(1.0, self.queue_delay + 1e-3) - task.compute_cycles * 0.25
        if method == "DRL-CCMCO":
            return self.compute_capacity - self.queue_delay - task.compute_cycles * 0.15
        if method == "DTOSC":
            return self.compute_capacity / (self.queue_delay + 1.0) + self.network_bandwidth / 100.0
        raise ValueError(f"Unknown method: {method}")


class EdgeEnvironment:
    def __init__(self, num_servers: int, num_nodes: int, bandwidth_range, seed: int = 42):
        self.num_servers = num_servers
        self.num_nodes = num_nodes
        self.rng = random.Random(seed)
        self.servers = [
            EdgeServer(
                server_id=i,
                compute_capacity=3.0 + (i % 5) * 0.8 + self.rng.random() * 1.5,
                network_bandwidth=self.rng.uniform(*bandwidth_range),
                energy_per_bit=(1e-8) + self.rng.random() * 3e-8,
            )
            for i in range(num_servers)
        ]

    def generate_task(self, task_id: int, data_mb: float, compute_cycles: float) -> Task:
        source_node = self.rng.randint(0, self.num_nodes - 1)
        deadline = data_mb / max(1.0, self.rng.uniform(100.0, 300.0)) + compute_cycles / 2.0 + self.rng.uniform(0.1, 1.0)
        return Task(task_id=task_id, source_node=source_node, data_mb=data_mb, compute_cycles=compute_cycles, deadline=deadline)

    def assign_task(self, task: Task, method: str) -> Dict[str, float]:
        server = max(self.servers, key=lambda s: s.score(task, method))
        transmission_time = task.data_mb / max(1e-6, server.network_bandwidth)
        execution_time = task.compute_cycles / max(1e-6, server.compute_capacity)
        handover_time = 0.05 * (1.0 + (task.source_node % 5) / 10.0)
        completion_time = transmission_time + execution_time + handover_time
        energy = transmission_time * server.energy_per_bit * task.data_mb
        server.queue_delay += execution_time

        return {
            "server_id": server.server_id,
            "transmission_time": transmission_time,
            "handover_time": handover_time,
            "execution_time": execution_time,
            "completion_time": completion_time,
            "energy": energy,
        }


def summarize_results(results: Iterable[Dict[str, float]]) -> Dict[str, float]:
    records = list(results)
    if not records:
        return {
            "average_task_completion_time": 0.0,
            "task_transmission_time": 0.0,
            "task_handover_time": 0.0,
            "task_execution_time": 0.0,
            "task_transmission_energy": 0.0,
            "task_throughput": 0.0,
        }

    total_tasks = len(records)
    avg_completion = sum(r["completion_time"] for r in records) / total_tasks
    avg_transmission = sum(r["transmission_time"] for r in records) / total_tasks
    avg_handover = sum(r["handover_time"] for r in records) / total_tasks
    avg_execution = sum(r["execution_time"] for r in records) / total_tasks
    total_energy = sum(r["energy"] for r in records)
    throughput = total_tasks / max(avg_completion, 1e-6)

    return {
        "average_task_completion_time": avg_completion,
        "task_transmission_time": avg_transmission,
        "task_handover_time": avg_handover,
        "task_execution_time": avg_execution,
        "task_transmission_energy": total_energy,
        "task_throughput": throughput,
    }


def run_experiment(method: str, task_count: int, compute_scale: float, bandwidth_range=(100.0, 300.0), seed: int = 42) -> Dict[str, Any]:
    env = EdgeEnvironment(num_servers=10, num_nodes=50, bandwidth_range=bandwidth_range, seed=seed)
    tasks = [
        env.generate_task(task_id=i, data_mb=50.0, compute_cycles=compute_scale)
        for i in range(task_count)
    ]

    records = []
    for task in tasks:
        record = env.assign_task(task, method)
        records.append(record)

    summary = summarize_results(records)
    summary["method"] = method
    summary["task_count"] = task_count
    summary["compute_scale"] = compute_scale
    return summary
