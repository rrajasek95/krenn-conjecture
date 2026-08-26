#!/bin/zsh
# UNAUDITED PROBE (W18) -- finish the certificate backfill unattended.
#   1. wait for any in-flight run_reemit to exit
#   2. record corrected class rows for whatever was already replaced
#   3. re-emit every proof that still fails replay (cadical-native), fix rows
#   4. re-emit the whole pysat-emitted set, fix rows, drop BACKFILL_DONE
# drat-trim is the checker above 100 MB; rup18 double-checks everything below.
HERE=${0:a:h}
cd "$HERE" || exit 1
while pgrep -f "run_reemit.py 18 19" > /dev/null; do sleep 30; done
echo "[$(date +%H:%M:%S)] step 2: fixrows for already-replaced proofs"
python3 -u run_reemit_fixrows.py 18 19
echo "[$(date +%H:%M:%S)] step 3: re-emit remaining FAILED proofs"
python3 -u run_reemit.py 18 19 --which failed --rup-max-mb 100 \
    --out results_reemit_failed2.json
python3 -u run_reemit_fixrows.py 18 19
echo "[$(date +%H:%M:%S)] step 4: full pysat backfill"
python3 -u run_reemit.py 18 19 --which pysat --rup-max-mb 100 \
    --out results_reemit_all.json
python3 -u run_reemit_fixrows.py 18 19
touch "$HERE/BACKFILL_DONE"
echo "[$(date +%H:%M:%S)] backfill chain complete"
