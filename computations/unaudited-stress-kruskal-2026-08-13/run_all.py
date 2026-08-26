#!/usr/bin/env python3
"""Run the whole UNAUDITED stress test and emit one content digest."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = ["t1_fusion_stress.py", "t2_kruskal_boundary.py",
           "t3_program_hypotheses.py", "t4_mutation_controls.py"]


def main():
    ledger = {}
    ok = True
    for name in SCRIPTS:
        proc = subprocess.run([sys.executable, str(HERE / name)],
                              capture_output=True, text=True, cwd=str(HERE))
        status = "PASS" if proc.returncode == 0 else "FAIL"
        ok = ok and proc.returncode == 0
        ledger[name] = {
            "status": status,
            "stdout_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest(),
            "lines": len(proc.stdout.splitlines()),
        }
        print(f"{status}  {name}  "
              f"(stdout sha256 {ledger[name]['stdout_sha256'][:16]}...)")
        if proc.returncode != 0:
            print(proc.stdout[-2000:])
            print(proc.stderr[-2000:])
    for name in SCRIPTS + ["exactlin.py"]:
        ledger.setdefault(name, {})["source_sha256"] = \
            hashlib.sha256((HERE / name).read_bytes()).hexdigest()
    digest = hashlib.sha256(
        json.dumps(ledger, sort_keys=True).encode()).hexdigest()
    print(f"\noverall: {'PASS' if ok else 'FAIL'}")
    print(f"ledger sha256: {digest}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
