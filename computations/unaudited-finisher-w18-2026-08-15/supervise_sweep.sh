#!/bin/zsh
# UNAUDITED PROBE (W18) -- keep the 18/19 sweep populated after the session ends.
#
# Keeps NM18 workers on m=18 and NM19 on m=19, each with --skip-done, and
# relaunches any that exit.  Stops when both supports are fully closed, when
# STOPFILE appears, or after MAXHOURS.
#
#   ./supervise_sweep.sh            # run in the foreground
#   nohup ./supervise_sweep.sh &    # or detached
#   touch STOP_SWEEP                # to stop it (workers finish their class)

HERE=${0:a:h}
cd "$HERE" || exit 1
NM18=${NM18:-3}
NM19=${NM19:-9}
SECONDS_PER=${SECONDS_PER:-5400}
DEEPT=${DEEPT:-120}
MAXHOURS=${MAXHOURS:-12}
STOPFILE="$HERE/STOP_SWEEP"
mkdir -p logs
start=$(date +%s)

closed() {  # $1 = support ; prints "closed total"
  python3 - "$1" <<'PY'
import glob, json, sys, os
m = sys.argv[1]
HERE = os.path.dirname(os.path.abspath("."))
tot = {"18": 437, "19": 310}[m]
done = set()
for f in glob.glob("results_sweep_m%s_*.jsonl" % m):
    for line in open(f):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r["status"] in ("UNSAT", "TRIVIAL-UNSAT"):
            done.add(r["mask"])
print(len(done), tot)
PY
}

while true; do
  [[ -e "$STOPFILE" ]] && { echo "STOP_SWEEP present, exiting"; break; }
  (( $(date +%s) - start > MAXHOURS * 3600 )) && { echo "max hours reached"; break; }

  read c18 t18 <<< "$(closed 18)"
  read c19 t19 <<< "$(closed 19)"
  echo "[$(date +%H:%M:%S)] m18 $c18/$t18  m19 $c19/$t19  workers $(ps ax | grep -c '[w]18_sweep.py')"
  [[ "$c18" == "$t18" && "$c19" == "$t19" ]] && { echo "both supports closed"; break; }

  # never oversubscribe: only top up to TARGET total sweep processes, so the
  # workers already running from an earlier pass are counted, not duplicated
  TARGET=${TARGET:-$((NM18 + NM19))}
  live=$(ps ax | grep -c '[w]18_sweep.py')
  slots=$((TARGET - live))
  (( slots <= 0 )) && { sleep 300; continue; }

  for i in $(seq 0 $((NM18 - 1))); do
    (( slots <= 0 )) && break
    if [[ "$c18" != "$t18" ]] && ! pgrep -f "w18_sweep.py --m 18 --stride $NM18 --offset $i " > /dev/null; then
      slots=$((slots - 1))
      nohup python3 -u w18_sweep.py --m 18 --stride $NM18 --offset $i \
        --seconds $SECONDS_PER --skip-done --sing-batch 24 --exact-after 1 \
        --deep-timeout $DEEPT --tag _sup18w$i >> logs/sup_m18_w$i.log 2>&1 &
      echo "  relaunched m18 offset $i"
    fi
  done
  for i in $(seq 0 $((NM19 - 1))); do
    (( slots <= 0 )) && break
    if [[ "$c19" != "$t19" ]] && ! pgrep -f "w18_sweep.py --m 19 --stride $NM19 --offset $i " > /dev/null; then
      slots=$((slots - 1))
      nohup python3 -u w18_sweep.py --m 19 --stride $NM19 --offset $i \
        --seconds $SECONDS_PER --skip-done --sing-batch 24 --exact-after 1 \
        --deep-timeout $DEEPT --tag _sup19w$i >> logs/sup_m19_w$i.log 2>&1 &
      echo "  relaunched m19 offset $i"
    fi
  done
  sleep 300
done
