#!/usr/bin/env python3
"""Goal-directed triangular lifting for the high off-diagonal P^2 layers.

This resumes the exact support checkpoint after degree three.  Instead of
closing an entire associated-graded component, it recursively assigns to
each needed non-cone row a leading column whose other non-cone outputs have
already been assigned.  A successful assignment is an explicit triangular
minor on precisely the dependency closure of the remainder.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import pickle
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.setrecursionlimit(200_000)
sys.path.insert(0, str(__file__).rsplit("/", 1)[0])

import complete_power2_filtration as C
import lift_power2_offdiag2 as L


CHECKPOINT_GLOB = "/tmp/krenn_p2_filter_after*.pkl"


def write_certificate(degree, assigned, cone_columns):
    """Audit and persist the explicit triangular pivot order."""
    seen = set()
    noncone_pivots = []
    for row, col in assigned.items():
        output = Counter(L.leading_outputs(col))
        assert output[row] > 0
        deps = {
            rr
            for rr in output
            if rr != row and not L.monomial_killed(rr)
        }
        assert deps <= seen
        noncone_pivots.append((row, col, output[row]))
        seen.add(row)

    cone_pivots = []
    for row, col in sorted(cone_columns.items()):
        output = Counter(L.leading_outputs(col))
        assert set(output) == {row}
        cone_pivots.append((row, col, output[row]))

    certificate = {
        "degree": degree,
        "cone_pivots": tuple(cone_pivots),
        "noncone_pivots": tuple(noncone_pivots),
    }
    payload = pickle.dumps(certificate, protocol=pickle.HIGHEST_PROTOCOL)
    digest = hashlib.sha256(payload).hexdigest()
    out_dir = Path(__file__).with_name("certificates")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"p2_degree{degree}_triangular.pkl.gz"
    with gzip.open(out_path, "wb", compresslevel=9) as fh:
        fh.write(payload)
    print(
        f"layer {degree}: pivot certificate={out_path}, sha256={digest}, "
        f"compressed_bytes={out_path.stat().st_size}",
        flush=True,
    )
    return digest


def triangular_dependency(starts, degree, persist=True):
    assigned = {}
    used_columns = set()
    visiting = set()
    calls = 0

    def prove(row):
        nonlocal calls
        calls += 1
        if L.monomial_killed(row) or row in assigned:
            return True
        if row in visiting:
            return False
        visiting.add(row)

        options = []
        for col in L.incident_leading_columns(row):
            if col in used_columns:
                continue
            deps = {
                rr
                for rr in L.leading_outputs(col)
                if rr != row and not L.monomial_killed(rr)
            }
            options.append((len(deps), col, tuple(sorted(deps))))
        options.sort(key=lambda z: (z[0], z[1]))

        for _, col, deps in options:
            if col in used_columns:
                continue
            if all(prove(rr) for rr in deps):
                # Recursive calls cannot have used this column without
                # depending back on the currently visiting row.
                if col in used_columns:
                    continue
                assigned[row] = col
                used_columns.add(col)
                visiting.remove(row)
                return True
        visiting.remove(row)
        return False

    survivor_starts = [r for r in starts if not L.monomial_killed(r)]
    for k, row in enumerate(survivor_starts):
        if not prove(row):
            print(
                f"layer {degree}: DFS FAILED at start {k+1}/{len(survivor_starts)}, "
                f"assigned={len(assigned)}, calls={calls}",
                flush=True,
            )
            return None
        if (k + 1) % 500 == 0:
            print(
                f"layer {degree}: starts proved={k+1}/{len(survivor_starts)}, "
                f"dependency rows={len(assigned)}, calls={calls}",
                flush=True,
            )

    # The recursion order gives an acyclic dependency proof.  Add independent
    # one-term columns for every cone row appearing initially or in a selected
    # column.
    killed_needed = {r for r in starts if L.monomial_killed(r)}
    for col in assigned.values():
        killed_needed.update(r for r in L.leading_outputs(col) if L.monomial_killed(r))
    correction = set(assigned.values())
    cone_columns = {}
    for row in sorted(killed_needed):
        mono = L.monomial_column(row)
        assert mono is not None
        assert set(L.leading_outputs(mono)) == {row}
        cone_columns[row] = mono
        correction.add(mono)
    print(
        f"layer {degree}: DFS triangular rows={len(assigned)}, "
        f"one-term rows={len(killed_needed)}, corrections={len(correction)}, calls={calls}",
        flush=True,
    )
    digest = write_certificate(degree, assigned, cone_columns) if persist else None
    return correction, digest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--replay-degree",
        type=int,
        help="replay one completed layer and write only its pivot certificate",
    )
    args = parser.parse_args()

    if args.replay_degree is not None:
        degree = args.replay_degree
        checkpoint = Path(f"/tmp/krenn_p2_filter_after{degree - 1}.pkl")
        with checkpoint.open("rb") as fh:
            saved = pickle.load(fh)
        starts = saved["supports"][degree]
        print(f"replay={checkpoint}, degree={degree}, starts={len(starts)}", flush=True)
        correction, _ = triangular_dependency(starts, degree)
        print(f"replay corrections={len(correction)}", flush=True)
        return

    candidates = sorted(
        Path("/tmp").glob("krenn_p2_filter_after*.pkl"),
        key=lambda p: int(p.stem.rsplit("after", 1)[1]),
    )
    checkpoint = candidates[-1]
    completed_degree = int(checkpoint.stem.rsplit("after", 1)[1])
    with checkpoint.open("rb") as fh:
        saved = pickle.load(fh)
    supports = defaultdict(set, saved["supports"])
    certificates = list(saved["certificates"])
    print(
        f"resume={checkpoint}, supports={ {k: len(v) for k,v in supports.items()} }",
        flush=True,
    )

    for degree in range(completed_degree + 1, 19):
        starts = supports.pop(degree, set())
        if not starts:
            print(f"layer {degree}: empty", flush=True)
            continue
        print(
            f"layer {degree}: starts={len(starts)}, "
            f"cones={sum(L.monomial_killed(r) for r in starts)}",
            flush=True,
        )
        result = triangular_dependency(starts, degree)
        if result is None:
            raise SystemExit(2)
        correction, certificate_digest = result
        created = C.add_higher_support(correction, degree, supports)
        certificates.append((degree, len(starts), len(correction), certificate_digest))
        print(f"layer {degree}: propagated={created}", flush=True)

        with Path(f"/tmp/krenn_p2_filter_after{degree}.pkl").open("wb") as fh:
            pickle.dump(
                {"supports": dict(supports), "certificates": certificates},
                fh,
                protocol=pickle.HIGHEST_PROTOCOL,
            )

        L.incident_leading_columns.cache_clear()
        L.leading_outputs.cache_clear()
        L.monomial_killed.cache_clear()
        L.monomial_column.cache_clear()

    tail = {k: len(v) for k, v in supports.items() if v}
    print(f"certificate blocks={certificates}", flush=True)
    print(f"tail={tail}", flush=True)
    assert not tail


if __name__ == "__main__":
    main()
