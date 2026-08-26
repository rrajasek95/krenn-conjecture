#!/bin/bash
set -u
M=/Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20/work/fc/.lake/packages
LOG=/Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20/work/FIXDEPS.txt
export PATH="$HOME/.elan/bin:$PATH"
: > $LOG
echo "start $(date -u +%FT%TZ)" >> $LOG
for p in batteries aesop proofwidgets Qq plausible importGraph LeanSearchClient Cli; do
  rm -rf $M/$p/.lake/build
done
echo "cleared dependency build dirs" >> $LOG
cd /Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20/work/fc
lake build FormalConjecturesUtil >> $LOG 2>&1
echo "rc=$? end $(date -u +%FT%TZ) free=$(df -m /Users/rishi|tail -1|awk '{print $4}')MiB" >> $LOG
touch /Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20/work/FIXDEPS_DONE
