#!/bin/bash
LANE=/Users/rishi/workplace/krenn-conjecture/computations/unaudited-lean-l1-2026-08-20
LOG=$LANE/work/CHAIN.txt
: > $LOG
echo "start $(date -u +%FT%TZ)" >> $LOG
$LANE/work/lean_build.sh Rup Haf Product Normal Symm Wlog >> $LOG 2>&1
echo "rc=$? end $(date -u +%FT%TZ)" >> $LOG
touch $LANE/work/CHAIN_DONE
