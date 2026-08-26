#!/bin/sh
# Single-entry replay of the N = 8 diagonal obstruction certificate.
#
#   ./replay.sh                 full replay (controls + 87 orbits + N=6)
#   ./replay.sh --smoke         controls + the first 5 orbits only
#   ./replay.sh --verify-only   re-check the SHIPPED CNF/DRAT pairs in place
#
# What the full replay does, in order:
#   0. reproduces the case ledger (4096 cases / 87 orbits at N = 8) by two
#      independent routes -- canonical enumeration and Burnside -- and refuses
#      to continue unless they agree;
#   1. runs the broken-proof controls (truncated / corrupted / cross-case must
#      all be REJECTED; a k = 3 instance must come back SAT);
#   2. rebuilds each of the 87 orbit CNFs from the encoder, solves each with
#      CaDiCaL emitting a solver-native DRAT proof, and verifies each proof
#      with drat-trim;
#   3. repeats (2) for all 64 cases at N = 6.
#
# EXACT SOLVER BUILDS USED FOR THE RECORDED RUNS (hygiene lane H1):
#   CaDiCaL   computations/unaudited-hygiene-h1-2026-08-15/tools/cadical/build/cadical
#             `cadical --version` -> 3.0.1
#   drat-trim computations/unaudited-hygiene-h1-2026-08-15/tools/drat-trim/drat-trim
#             (Marijn Heule's reference checker, built from the upstream git
#              checkout kept beside the binary; invoked as `drat-trim CNF DRAT -f`
#              and required to print the literal string "s VERIFIED")
# Override either with the CADICAL / DRATTRIM environment variables.
#
# The independently written PySAT sweep of audit A9 additionally cross-checked
# every orbit with five engines (cadical195, minisat22, glucose42, maplesat,
# lingeling) -- see `computations/unaudited-audit-a9-2026-08-20/results_a9_03_sat.json`,
# key `multi`.  That sweep is not re-run here; it needs the `python-sat`
# package, whereas this replay needs only CPython plus the two binaries above.
#
# Exit status 0 iff every requested check passes.

set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$HERE"

: "${CADICAL:=/Users/rishi/workplace/krenn-conjecture/computations/unaudited-hygiene-h1-2026-08-15/tools/cadical/build/cadical}"
: "${DRATTRIM:=/Users/rishi/workplace/krenn-conjecture/computations/unaudited-hygiene-h1-2026-08-15/tools/drat-trim/drat-trim}"
export CADICAL DRATTRIM

echo "=== tools ==="
echo "cadical    : $CADICAL"
"$CADICAL" --version 2>&1 | head -1
echo "drat-trim  : $DRATTRIM"
test -x "$DRATTRIM" || { echo "drat-trim missing or not executable"; exit 2; }
python3 --version

# Python bytecode caches are not shipped artifacts and are not hashed; drop any
# left by a previous run so the SHA-256 manifest describes the tree exactly.
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

if [ "${1:-}" = "--verify-only" ]; then
    echo
    echo "=== re-verifying the SHIPPED proofs in orbits/ ==="
    n=0; bad=0
    for cnf in orbits/n8k4_*.cnf; do
        drat="${cnf%.cnf}.drat"
        n=$((n + 1))
        if "$DRATTRIM" "$cnf" "$drat" -f 2>/dev/null | grep -q "s VERIFIED"; then
            :
        else
            echo "NOT VERIFIED: $cnf"; bad=$((bad + 1))
        fi
    done
    echo "verified $((n - bad)) / $n shipped orbit proofs"
    echo
    echo "=== SHA-256 manifest check ==="
    if command -v shasum >/dev/null 2>&1; then
        shasum -a 256 -c SHA256SUMS.txt
    else
        sha256sum -c SHA256SUMS.txt
    fi
    [ "$bad" -eq 0 ] || exit 1
    exit 0
fi

echo
echo "=== step 0: the case ledger, two independent routes ==="
python3 orbit_ledger.py orbit_ledger.json

echo
if [ "${1:-}" = "--smoke" ]; then
    echo "=== steps 1-2 (SMOKE: controls + 5 orbits) ==="
    python3 replay_orbits.py --mode controls --out replay_results_controls.json
    python3 replay_orbits.py --mode orbits --limit 5 \
        --out replay_results_smoke.json
else
    echo "=== steps 1-3: controls, 87 orbits at N=8, 64 cases at N=6 ==="
    python3 replay_orbits.py --mode all --out replay_results.json
fi
echo
echo "replay finished; results JSON written beside this script."
