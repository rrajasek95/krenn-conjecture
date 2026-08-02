#!/usr/bin/env python3
"""Public entry point for the exact chart-25 degree-two lift audit."""

import importlib.util
from pathlib import Path


ANALYZER = Path(__file__).resolve().with_name(
    "analyze_n8_chart25_degree2_lift.py"
)
SPEC = importlib.util.spec_from_file_location("n8_chart25_degree2", ANALYZER)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


if __name__ == "__main__":
    MODULE.main()
