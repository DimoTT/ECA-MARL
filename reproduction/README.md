# ECA-MARL approximate reproduction scaffold

This directory contains a minimal, paper-driven reproduction framework for the ECA-MARL experiment described in the repository's supporting metadata.

Important note:
- The repository currently contains only the supporting materials collection, not the original experiment code or raw simulation outputs.
- This reproduction is therefore an approximate implementation derived from the reported setup in `data_release_2026-10-28/documentation/reported_setup.tex` and `simulation_environment.json`.
- It is intended to provide a runnable starting point for further tuning, not a claim of exact reproduction of the original paper.

## Reported configuration used

- Number of edge servers: 10
- Number of WSN nodes: 50
- Transmission bandwidth: 100–300 Mbps
- Average task data size: 50 MB
- CPU cycles required: 0.5–4 Gcycle/s
- Batch size: 32 MB
- Gradient clipping threshold: 40
- Policy learning rate: 0.95
- Value learning rate: 0.85
- Attenuation level: 0.95
- Hidden layer size: 256
- Replay pool size: 200 GB
- Baselines: DRL-CCMCO, DTOSC

## Usage

```bash
cd reproduction
python run_experiments.py
```

This writes a CSV summary under:

```text
reproduction/results/experiment_summary.csv
```

## What the code does

- Generates synthetic edge tasks and placement requests.
- Simulates three policies:
  - ECA-MARL style scheduler
  - DRL-CCMCO style heuristic
  - DTOSC style heuristic
- Evaluates the reported metrics:
  - average task completion time
  - transmission time
  - handover time
  - execution time
  - transmission energy
  - throughput
- Sweeps task count and task computation size.

## Expected status

This project is a framework for reproduction, not a faithful reconstruction of the original closed-source implementation.
