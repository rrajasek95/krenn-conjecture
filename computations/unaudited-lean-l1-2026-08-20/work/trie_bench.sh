#!/bin/bash
cd /Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20/work/rup
export PATH="$HOME/.elan/bin:$PATH"
LOG=../TRIE_BENCH.txt
: > $LOG
for O in 4 26 1; do
  echo "=== orbit $O ===" >> $LOG
  /usr/bin/time -p lake build N8Diagonal.Orbit$O >> $LOG 2>&1
  echo "rc=$?" >> $LOG
done
touch ../TRIE_BENCH_DONE
