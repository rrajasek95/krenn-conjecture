#!/bin/bash
# Build the N8Diagonal algebra modules against the SIBLING formal-conjectures
# checkout, read-only, exactly as formal/FORMALIZATION.md already documents
# ("the sibling formal-conjectures checkout was used only for imports and
# compilation"). No .lake tree of our own, so no Mathlib copy in this lane.
set -u
LANE=/Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20
ROOT=$LANE/staged/formal/n8-diagonal
OUT=$LANE/work/build
FC=/Users/rishi/workplace/formal-conjectures
export PATH="$HOME/.elan/bin:$PATH"
mkdir -p "$OUT/N8Diagonal"
LP=$(cd "$FC" && lake env sh -c 'echo $LEAN_PATH')
[ -z "$LP" ] && { echo "FATAL: could not read LEAN_PATH from $FC"; exit 1; }
cd "$ROOT" || exit 1
rc=0
for m in "$@"; do
  echo "--- $m ---"
  LEAN_PATH="$LP:$OUT" nice -n 15 lean -o "$OUT/N8Diagonal/$m.olean" "N8Diagonal/$m.lean" || rc=1
done
exit $rc
