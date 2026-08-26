#!/bin/bash
set -u
P=/Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20/skeleton/lrat-probe
W=/Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20/work
LOG=$W/PROBE_BUILD.txt
export PATH="$HOME/.elan/bin:$PATH"
cd "$P" || exit 1
: > "$LOG"
echo "=== A: native_decide (LratProbe.Orbit0) ===" >> "$LOG"
echo "start $(date -u +%FT%TZ)" >> "$LOG"
/usr/bin/time -l lake env lean LratProbe/Orbit0.lean >> "$LOG" 2>&1
echo "native rc=$? $(date -u +%FT%TZ)" >> "$LOG"
touch "$W/PROBE_NATIVE_DONE"
echo "=== B: kernel decide (LratProbe.Kernel), 20 min cap ===" >> "$LOG"
echo "start $(date -u +%FT%TZ)" >> "$LOG"
/usr/bin/time -l timeout 1200 lake env lean LratProbe/Kernel.lean >> "$LOG" 2>&1
echo "kernel rc=$? $(date -u +%FT%TZ)" >> "$LOG"
touch "$W/PROBE_DONE"
