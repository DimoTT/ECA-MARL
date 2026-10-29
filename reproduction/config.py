from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class SimulationConfig:
    num_edge_servers: int = 10
    num_wsn_nodes: int = 50
    bandwidth_range: Tuple[float, float] = (100.0, 300.0)
    avg_task_data_size_mb: float = 50.0
    cpu_cycles_range: Tuple[float, float] = (0.5, 4.0)
    batch_size_mb: float = 32.0
    gradient_clipping_threshold: int = 40
    policy_learning_rate: float = 0.95
    value_learning_rate: float = 0.85
    attenuation_level: float = 0.95
    hidden_layer_size: int = 256
    experience_replay_pool_size_gb: float = 200.0
    task_counts: Tuple[int, ...] = (50, 100, 150, 200)
    task_compute_sweeps: Tuple[float, ...] = (1.0, 2.0, 4.0, 8.0)
    random_seed: int = 42


MANUSCRIPT_CONFIG = SimulationConfig()
