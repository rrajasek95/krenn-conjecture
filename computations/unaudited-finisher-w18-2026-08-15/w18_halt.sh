#!/bin/zsh
# UNAUDITED PROBE (W18) -- halt all W18 compute and clear scratch.
# Kept in its OWN FILE so that a monitor invoking it does not carry the kill
# patterns on its own command line: `pkill -f` matches the watcher too, which
# is how two guards silently killed themselves (exit 144).
T=/var/folders/f9/tg39mf5n5qx1k1_9sf587wbw0000gn/T
for pat in run_reemit run_backfill_chain.sh "w18_sweep.py --m" \
           "cadical --binary" "drat-trim /var" "rup18 /var"; do
  pkill -f "$pat" >/dev/null 2>&1
done
sleep 2
rm -rf $T/w18proof* $T/w18reemit* $T/w18ledger* $T/w18fixrow* >/dev/null 2>&1
exit 0
