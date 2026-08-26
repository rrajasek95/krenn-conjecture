#!/bin/bash
# Kernel-check all 87 orbit refutations through the bespoke RUP checker.
#
# UNAUDITED — lane L1. Runs in work/rup/, a ZERO-DEPENDENCY lake project: no
# Mathlib, no formal-conjectures. Nothing here needs the pruned Mathlib tree.
#
# SERIAL by design. The box carries seven lanes; at launch it had 48 GB RAM with
# well under 100 MB free, so Lake's default 18-way parallelism at ~1 GB per
# kernel reduction would have been reckless. Serial also yields an exact
# per-orbit wall time, which is what the PR description needs.
#
# Checkpointed on the LOG, not on build output: an orbit already recorded
# `rc=0` in ORBITS_ALL.txt is skipped. That lets us delete each orbit's build
# intermediates the moment its kernel check succeeds, which keeps the lane
# footprint flat while the Mathlib cache is resident on a shared box. The
# durable record is the log line plus the generating core files; re-verifying a
# single orbit is always one command away.
set -u
LANE=/Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20
P=$LANE/work/rup
LOG=$LANE/work/ORBITS_ALL.txt
export PATH="$HOME/.elan/bin:$PATH"

FREE_MB=$(df -m /Users/rishi | tail -1 | awk '{print $4}')
if [ "$FREE_MB" -lt 4096 ]; then
  echo "ABORT: only ${FREE_MB} MiB free; need 4 GiB headroom" | tee -a "$LOG"
  exit 1
fi

# single-instance lock: two concurrent loops interleave and duplicate work
LOCK=$LANE/work/.orbits.lock
if ! mkdir "$LOCK" 2>/dev/null; then
  echo "ABORT: another orbit loop holds $LOCK" | tee -a "$LOG"
  exit 1
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

echo "=== run start $(date -u +%FT%TZ)  free=${FREE_MB}MiB (serial) ===" >> "$LOG"

cd "$P" || exit 1
ok=0; skip=0; fail=0
for i in $(seq 0 86); do
  if grep -q "^orbit $i rc=0 " "$LOG" 2>/dev/null; then skip=$((skip+1)); continue; fi
  if [ ! -f "N8Diagonal/Orbit$i.lean" ]; then
    python3 "$LANE/encoder/gen_rup_core.py" "$i" "N8Diagonal/Orbit$i.lean" >/dev/null 2>&1
  fi
  T0=$(python3 -c 'import time;print(time.time())')
  lake build "N8Diagonal.Orbit$i" > /tmp/l1_orbit_$i.log 2>&1
  RC=$?
  T1=$(python3 -c 'import time;print(time.time())')
  D=$(python3 -c "print(f'{$T1-$T0:.1f}')")
  if [ "$RC" -eq 0 ]; then ok=$((ok+1)); else fail=$((fail+1)); fi
  echo "orbit $i rc=$RC secs=$D free=$(df -m /Users/rishi | tail -1 | awk '{print $4}')MiB" >> "$LOG"
  rm -f /tmp/l1_orbit_$i.log
  # clean as we go: the log line is the record, the .lean and core files are the source
  if [ "$RC" -eq 0 ]; then
    rm -f .lake/build/lib/lean/N8Diagonal/Orbit$i.olean* \
          .lake/build/lib/lean/N8Diagonal/Orbit$i.ilean* \
          .lake/build/lib/lean/N8Diagonal/Orbit$i.trace \
          .lake/build/lib/lean/N8Diagonal/Orbit$i.ir* \
          "N8Diagonal/Orbit$i.lean"
  fi
  # box-wide courtesy guard: stop cleanly rather than help hit the wall
  FREE_NOW=$(df -m /Users/rishi | tail -1 | awk '{print $4}')
  if [ "$FREE_NOW" -lt 4608 ]; then
    echo "PAUSING: free=${FREE_NOW}MiB below 4.5 GiB guard; rerun to resume" >> "$LOG"
    break
  fi
done
echo "=== run end $(date -u +%FT%TZ) ok=$ok skipped=$skip fail=$fail ===" >> "$LOG"
VERIFIED=$(grep -c "^orbit .* rc=0 " "$LOG" 2>/dev/null || echo 0)
echo "orbits verified (cumulative, from the log): $VERIFIED / 87" >> "$LOG"
echo ".lake = $(du -sm .lake | cut -f1) MiB; lane = $(du -sm $LANE | cut -f1) MiB" >> "$LOG"
touch "$LANE/work/ORBITS_ALL_DONE"
