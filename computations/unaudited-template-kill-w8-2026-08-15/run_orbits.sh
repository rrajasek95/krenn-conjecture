#!/bin/sh
# UNAUDITED PROBE (W8): per-orbit parallel band decision (bounded concurrency).
M=$1; MODE=$2; SECS=$3; JOBS=${4:-12}
seq 0 30 | xargs -P $JOBS -I{} sh -c \
  "python3 w8_band.py --m $M --mode $MODE --seconds $SECS --only {} \
   --out orbits/results_m${M}_${MODE}_o{}.json > orbits/log_m${M}_${MODE}_o{}.txt 2>&1"
echo "done m=$M mode=$MODE"
