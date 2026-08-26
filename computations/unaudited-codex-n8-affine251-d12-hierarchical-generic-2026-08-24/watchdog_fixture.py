#!/usr/bin/env python3
"""Tiny child used only by watchdog race/resource hostiles."""

import os
from pathlib import Path
import sys
import time


def value(name: str) -> str:
    index = sys.argv.index(name)
    return sys.argv[index + 1]


mode = value("--fixture")
output = Path(value("--output"))
if mode == "fast":
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text("fast exit\n")
    os.replace(temporary, output)
elif mode == "race":
    time.sleep(0.01)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text("poll/exit race\n")
    os.replace(temporary, output)
elif mode == "overrun":
    blocks = []
    for _ in range(16):
        blocks.append(bytearray(8 << 20))
        time.sleep(0.02)
    time.sleep(5)
else:
    raise SystemExit("bad fixture mode")
