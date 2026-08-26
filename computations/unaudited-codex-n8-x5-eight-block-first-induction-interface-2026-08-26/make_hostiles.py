#!/usr/bin/env python3
import json
import os
from pathlib import Path
from validate import hostiles

HERE = Path(__file__).resolve().parent
result = json.loads((HERE / "results_eight_block_interface.json").read_text())
data = {"schema": "KRENN_X5_EIGHT_BLOCK_INTERFACE_HOSTILES_V1", "status": "PASS", "cases": hostiles(result)}
tmp = HERE / "results_hostiles.json.tmp"
tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
os.replace(tmp, HERE / "results_hostiles.json")
