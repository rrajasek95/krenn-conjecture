#!/bin/bash
# Produce Lean-consumable LRAT for the 87 N=8 diagonal orbit refutations.
#
# FINDING (see feasibility.md): drat-trim's `-L` LRAT conversion of our stored
# DRAT files is REJECTED by Lean's LRAT checker
# (Std.Tactic.BVDecide.Reflect.verifyCert returns false) even though drat-trim
# itself and drat-trim's own `lrat-check` both report VERIFIED. CaDiCaL's
# native `--lrat=true` output is accepted. So the Lean route re-solves each
# CNF with CaDiCaL emitting LRAT directly, exactly as algal's
# krenn-gu-6x3-certificate does.
#
# This does not weaken anything: the CNF is the audited artifact, the LRAT is
# an independently produced refutation of that same CNF, and it is checked
# three ways -- by CaDiCaL's own internal LRAT checker (--checkproof=2), by
# drat-trim's lrat-check, and by Lean.
#
# Detached and checkpointed: one line per orbit in LRAT_PROGRESS.txt.
set -u
ROOT=/Users/rishi/workplace/krenn-conjecture
PKG=$ROOT/computations/unaudited-promotion-diag-2026-08-20/certified_package/orbits
OUT=$ROOT/computations/unaudited-lean-l1-2026-08-20/lrat
WORK=$ROOT/computations/unaudited-lean-l1-2026-08-20/work
CAD=$ROOT/computations/unaudited-hygiene-h1-2026-08-15/tools/cadical/build/cadical
LC=$ROOT/computations/unaudited-hygiene-h1-2026-08-15/tools/drat-trim/lrat-check
mkdir -p "$OUT"
PROG=$WORK/LRAT_PROGRESS.txt
: > "$PROG"
echo "start $(date -u +%FT%TZ)" >> "$PROG"
echo "cadical $($CAD --version)  route: --lrat=true --no-binary --checkproof=2" >> "$PROG"

rm -f "$OUT"/*.lrat
ok=0; fail=0
for i in $(seq 0 86); do
  cnf=$PKG/n8k4_${i}.cnf
  lrat=$OUT/n8k4_${i}.lrat
  log=$WORK/cad_${i}.log
  t0=$(python3 -c 'import time;print(time.time())')
  "$CAD" "$cnf" "$lrat" --lrat=true --no-binary --checkproof=2 > "$log" 2>&1
  rc=$?          # cadical exits 20 on UNSAT
  t1=$(python3 -c 'import time;print(time.time())')
  dur=$(python3 -c "print(f'{$t1-$t0:.2f}')")
  sz=$(stat -f%z "$lrat" 2>/dev/null || echo 0)
  # independent re-check of the emitted LRAT against the same CNF
  lcok=$("$LC" "$cnf" "$lrat" 2>&1 | tr '\r' '\n' | grep -c '^c VERIFIED')
  echo "orbit $i cadical_rc=$rc lrat_bytes=$sz secs=$dur lratcheck_verified=$lcok" >> "$PROG"
  if [ "$rc" -eq 20 ] && [ "$lcok" -ge 1 ] && [ "$sz" -gt 0 ]; then ok=$((ok+1)); else fail=$((fail+1)); fi
done
echo "done ok=$ok fail=$fail $(date -u +%FT%TZ)" >> "$PROG"

# manifest with sizes and checksums
( cd "$OUT" && shasum -a 256 *.lrat > SHA256SUMS.txt )
touch "$WORK/LRAT2_FINISHED"
