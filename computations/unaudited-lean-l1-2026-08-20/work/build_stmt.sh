#!/bin/bash
set -u
W=/Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20/work
export PATH="$HOME/.elan/bin:$PATH"
cd "$W/fc" || exit 1
: > "$W/STMT_BUILD.txt"
echo "start $(date -u +%FT%TZ)" >> "$W/STMT_BUILD.txt"
lake --wfail build FormalConjectures.Paper.MonochromaticQuantumGraph >> "$W/STMT_BUILD.txt" 2>&1
echo "rc=$? end $(date -u +%FT%TZ)" >> "$W/STMT_BUILD.txt"
touch "$W/STMT_DONE"
