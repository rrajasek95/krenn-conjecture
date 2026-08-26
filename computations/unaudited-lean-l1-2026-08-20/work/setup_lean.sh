#!/bin/bash
# Detached, checkpointed Lean setup for the formal-conjectures clone.
#
# NOTE (environment): the pinned toolchain leanprover/lean4:v4.27.0 ships an
# x86_64 Mach-O binary and this host is arm64, so every Lean/Lake invocation
# runs under Rosetta 2. The first run of a cold binary can stall for minutes
# while Rosetta AOT-translates it. Never treat a slow first invocation as a
# failure. Every stage drops a marker file so a machine sleep is recoverable.
set -u
WORK=/Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20/work
FC=$WORK/fc
LOG=$WORK/LEAN_SETUP.txt
export PATH="$HOME/.elan/bin:$PATH"
say() { echo "[$(date -u +%FT%TZ)] $*" >> "$LOG"; }

cd "$FC" || { say "FATAL no fc dir"; exit 1; }
say "=== relaunch; toolchain $(cat lean-toolchain) ==="

say "--- warm the lean binary (Rosetta AOT) ---"
~/.elan/toolchains/leanprover--lean4---v4.27.0/bin/lean --version >> "$LOG" 2>&1
say "lean --version rc=$?"
touch "$WORK/LEAN_WARM_DONE"

say "=== stage 2: lake exe cache get (mathlib olean cache) ==="
lake exe cache get >> "$LOG" 2>&1
say "stage2 rc=$?"
touch "$WORK/LEAN_CACHE_DONE"

say "=== stage 3: build FormalConjecturesUtil ==="
lake build FormalConjecturesUtil >> "$LOG" 2>&1
say "stage3 rc=$?"
touch "$WORK/LEAN_UTIL_DONE"

say "=== stage 4: build the untouched upstream target module (baseline) ==="
lake build FormalConjectures.Paper.MonochromaticQuantumGraph >> "$LOG" 2>&1
say "stage4 rc=$?"
touch "$WORK/LEAN_BASELINE_DONE"

say "ALL STAGES ATTEMPTED"
touch "$WORK/LEAN_SETUP_FINISHED"
