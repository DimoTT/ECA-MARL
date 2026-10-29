#!/usr/bin/env python3
"""Convenience entry point for running the approximate ECA-MARL reproduction framework.

Usage:
    python run_experiments.py
    python run_experiments.py --method ECA-MARL --task-count 100 --compute-scale 2.0
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from reproduction.run_experiments import main


if __name__ == "__main__":
    main()
