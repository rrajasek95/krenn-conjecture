#!/bin/bash
set -u
P=/Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20/skeleton/lrat-probe
W=/Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20/work
LOG=$W/BUILD_ALL.txt
export PATH="$HOME/.elan/bin:$PATH"
cd "$P" || exit 1
: > "$LOG"
echo "start $(date -u +%FT%TZ)  ncpu=$(sysctl -n hw.ncpu)" >> "$LOG"
/usr/bin/time -l lake build LratProbe >> "$LOG" 2>&1
echo "rc=$? end $(date -u +%FT%TZ)" >> "$LOG"
touch "$W/BUILD_ALL_DONE"
