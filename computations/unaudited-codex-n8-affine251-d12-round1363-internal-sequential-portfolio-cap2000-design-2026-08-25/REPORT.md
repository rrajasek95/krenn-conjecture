# Round 1363 portfolio and cap2.0 gate: prepared, held

This package freezes a one-round built-in sequential six-way tree portfolio at round 1363 (`auto/best`, `portfolio-period 1`, `portfolio-parallel no`, 16 workers), followed by a fixed replay of the exact winner. Only if the winner is cold/rare may the runner launch a second fixed replay with the cap changed from 1.75M to 2.0M. It never continues beyond round 1363.

The portfolio has native 520-second/watchdog 540-second/36-GiB family geometry. Fixed replays use native 120/watchdog 135 seconds based on the sealed round1262 74.15-second control and the metadata-only 93-second linear projection; this must be reconsidered fail-closed if the final round1362 support/frontier materially exceeds the projection.

The accepted round1343 manifest (`c07168d6...`) and production v4.1 source (`3139689f...`) are provisionally pinned. Because the production entry point deliberately rejects tree portfolio mode, `audit_source/main.rs` is an audit-only sibling with exactly that top-level fixed-mode guard deleted; the parser's hierarchical cold/rare guard and every computation line remain identical. Its source/binary (`2cf62905...`/`ade47c27...`) are byte-identical to the independently exercised round1061/round1262 audit engine. The production source is untouched.

The round1362 checkpoint, cache, counts, audit result, and audit manifest are intentionally unresolved. `freeze_future_input.py` rejects before opening any path, and `run_gate.py` rejects before cloning unless the resulting sealed `FUTURE_INPUT_PINS.json` exists.

Metadata from rounds1262--1343 projects round1362 at roughly 1.556M--1.576M columns, a 3.14--3.18-GiB cache, a 324--328-second sequential portfolio, and 23.2--23.5 GiB peak RSS under simple column-linear scaling. These are planning estimates, not acceptance evidence. No large cache read, clone, or solve is authorized before independent `FINAL_REPLAY_CLEAR`.
