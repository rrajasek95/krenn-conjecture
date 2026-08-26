#!/bin/bash
cd /Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20/work/fc
export PATH="$HOME/.elan/bin:$PATH"
LOG=../CACHE_GET.txt
: > $LOG
echo "start $(date -u +%FT%TZ) free=$(df -m /Users/rishi|tail -1|awk '{print $4}')MiB" >> $LOG
lake exe cache get >> $LOG 2>&1
echo "rc=$? end $(date -u +%FT%TZ) free=$(df -m /Users/rishi|tail -1|awk '{print $4}')MiB" >> $LOG
touch ../CACHE_DONE
