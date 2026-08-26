#!/bin/bash
set -u
D=/Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20/skeleton/defs-layer
W=/Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20/work
export PATH="$HOME/.elan/bin:$PATH"
cd "$D" || exit 1
: > "$W/DEFS_BUILD.txt"
echo "start $(date -u +%FT%TZ)" >> "$W/DEFS_BUILD.txt"
lake build KrennGuDiagonal >> "$W/DEFS_BUILD.txt" 2>&1
echo "rc=$? end $(date -u +%FT%TZ)" >> "$W/DEFS_BUILD.txt"
touch "$W/DEFS_DONE"
