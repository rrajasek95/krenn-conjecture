#!/usr/bin/env python3
from hashlib import sha256
import importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DESIGN=ROOT/'computations/unaudited-codex-orbit0-filtered-k24-reducer-design-2026-08-23/filtered_k24_reducer.py'
OUT=HERE/'filtered_k18_k4.bin'
def load(path):
 s=importlib.util.spec_from_file_location('k18d',path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
D=load(DESIGN)
with OUT.open('wb') as f:
 f.write(b'K18K4A1')
 for p in range(78):
  tails=D.CTX.tails[p][4];assert len(tails)==60
  for t in tails:f.write(t)
print(sha256(OUT.read_bytes()).hexdigest())
