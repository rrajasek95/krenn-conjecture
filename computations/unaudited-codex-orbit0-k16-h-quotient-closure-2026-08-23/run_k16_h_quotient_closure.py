#!/usr/bin/env python3
"""Restartable H-orbit/mass closure of the lex orbit-zero K14 target.

Rows and source columns retain full literal labels, but are canonicalized under
the order-384 factor stabilizer H.  Matrix entries are total masses from a
complete source-column orbit into a complete row orbit.  The run is bounded;
no membership or dual conclusion is drawn unless the bipartite component is
closed and the resulting statement is replayed literally.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import resource
import struct
import sys
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HPL_PATH = (ROOT / "computations/unaudited-codex-orbit0-k16-lower-kernel-hpl-2026-08-23"
            / "audit_k16_lower_kernel_component.py")
DAFSA_DIR = ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23"
DAFSA_SOURCE = DAFSA_DIR / "build_k16_weighted_dafsa.py"
DAFSA_BINARY = DAFSA_DIR / "weighted_k16_literal_orbits.dafsa"
CHECKPOINT = HERE / "checkpoint_k16_h_quotient.json"
RESULT = HERE / "results_k16_h_quotient_closure.json"
FRONTIER = HERE / "frontier_k16_h_quotient.json"

Q = bytes.fromhex("000004080d1955627575797d97c4c6cfd3d7e0e6eaeef2f3")


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


def file_sha256(path):
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


HPL = load("k16_h_quotient_hpl", HPL_PATH)
WD = load("k16_h_quotient_dafsa", DAFSA_SOURCE)
F = HPL.F
D24 = HPL.D24
THREE_ANCHORS, _PACKET = HPL.fractionless_packet()
H = HPL.factor_stabilizer(THREE_ANCHORS)
require(len(H) == 384, len(H))


def move_word(word, action):
    sites, colours = F.EXPORT.STABILIZER[action]
    moved = [None] * 8
    for old_site, old_colour in enumerate(word):
        moved[sites[old_site]] = colours[old_colour]
    require(None not in moved, (word, action))
    return tuple(moved)


def move_column(column, action):
    word, multiplier = column
    transform = F.EXPORT.TRANSFORMS[action]
    return move_word(word, action), bytes(sorted(transform[cell]
                                                 for cell in multiplier))


ROW_CANON = {}
COLUMN_CANON = {}
COLUMN_ORBIT_SIZE = {}


def canonical_row(row):
    answer = ROW_CANON.get(row)
    if answer is None:
        answer = min(F.move_row(row, action) for action in H)
        ROW_CANON[row] = answer
    return answer


def canonical_column(column):
    answer = COLUMN_CANON.get(column)
    if answer is None:
        images = {move_column(column, action) for action in H}
        answer = min(images)
        COLUMN_ORBIT_SIZE[answer] = len(images)
        for image in images:
            COLUMN_CANON[image] = answer
    return answer


def column_key(column):
    word, multiplier = column
    return "".join(map(str, word)) + ":" + multiplier.hex()


def parse_column_key(key):
    word, multiplier = key.split(":", 1)
    return tuple(map(int, word)), bytes.fromhex(multiplier)


class DafsaOracle:
    def __init__(self):
        self.offsets, header = WD.binary_index(DAFSA_BINARY)
        self.root = header[5]
        self.handle = DAFSA_BINARY.open("rb")

    def query(self, key):
        identifier = self.root
        for expected_depth, label in enumerate(key, 1):
            self.handle.seek(self.offsets[identifier])
            depth, flags, degree, numerator, denominator = WD.NODE.unpack(
                self.handle.read(WD.NODE.size))
            require(depth == expected_depth - 1 and not flags,
                    "DAFSA premature terminal")
            target = None
            for _ in range(degree):
                edge_label, child = WD.EDGE.unpack(self.handle.read(WD.EDGE.size))
                if edge_label == label:
                    target = child
            if target is None:
                return None
            identifier = target
        self.handle.seek(self.offsets[identifier])
        depth, flags, degree, numerator, denominator = WD.NODE.unpack(
            self.handle.read(WD.NODE.size))
        require(depth == 24 and degree == 0, "DAFSA terminal shape")
        return (numerator, denominator) if flags else None

    def close(self):
        self.handle.close()


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def column_vector(column):
    """Exact orbit-mass vector and base-representative provenance."""
    representative = canonical_column(column)
    orbit_size = COLUMN_ORBIT_SIZE[representative]
    entries = Counter()
    provenance = {}
    low_terms = 0
    for matching_index, row in enumerate(D24.degree24_column_rows(representative)):
        if D24.row_k_degree(row) > 16:
            continue
        low_terms += 1
        row_rep = canonical_row(row)
        entries[row_rep] += orbit_size
        provenance.setdefault(row_rep, []).append(matching_index)
    require(sum(entries.values()) == orbit_size * low_terms,
            (column_key(representative), orbit_size, low_terms, sum(entries.values())))
    return representative, orbit_size, entries, provenance


def literal_mass_replay(column, expected):
    """Hostile-scale literal replay for one complete source-column orbit."""
    representative = canonical_column(column)
    actual = Counter()
    source_orbit = {move_column(representative, action) for action in H}
    for literal_column in source_orbit:
        for row in D24.degree24_column_rows(literal_column):
            if D24.row_k_degree(row) <= 16:
                actual[canonical_row(row)] += 1
    require(actual == expected,
            (column_key(representative), "orbit-mass replay failed",
             len(actual), len(expected)))
    return len(source_orbit), sum(actual.values())


def equivariance_replay(column):
    representative = canonical_column(column)
    outputs = sorted(D24.degree24_column_rows(representative))
    for action in H:
        moved_column = move_column(representative, action)
        moved_outputs = sorted(F.move_row(row, action) for row in outputs)
        require(moved_outputs == sorted(D24.degree24_column_rows(moved_column)),
                (column_key(representative), action, "source action mismatch"))
    return len(H)


def empty_state(oracle):
    qrep = canonical_row(Q)
    qorbit = {F.move_row(Q, action) for action in H}
    require(qrep == Q and len(qorbit) == 384, (qrep.hex(), len(qorbit)))
    return {
        "schema": "orbit0-k16-H-quotient-closure-v1",
        "target": {qrep.hex(): [len(qorbit), 1]},
        "rows": {qrep.hex(): {
            "K_degree": D24.row_k_degree(qrep),
            "orbit_size": len(qorbit),
            "dafsa_mass": None,
        }},
        "queue": [qrep.hex()],
        "processed": [],
        "columns": {},
        "events": [],
    }


def load_state(oracle, resume):
    if resume and CHECKPOINT.exists():
        state = json.loads(CHECKPOINT.read_text())
        require(state["schema"] == "orbit0-k16-H-quotient-closure-v1",
                "checkpoint schema drift")
        return state
    return empty_state(oracle)


def max_rss_bytes():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # macOS reports bytes; Linux reports KiB.
    return int(value if sys.platform == "darwin" else value * 1024)


def compact_checkpoint(state, elapsed, status):
    state["runtime"] = {
        "elapsed_seconds": elapsed,
        "max_rss_bytes": max_rss_bytes(),
        "status": status,
    }
    atomic_json(CHECKPOINT, state)


def run(seconds, resume):
    started = time.monotonic()
    oracle = DafsaOracle()
    state = load_state(oracle, resume)
    queue = deque(state["queue"])
    queued = set(queue)
    rows = state["rows"]
    columns = state["columns"]
    processed = set(state["processed"])
    literal_replays = []
    equivariance_checks = 0
    last_checkpoint = time.monotonic()

    while queue:
        elapsed = time.monotonic() - started
        if elapsed >= seconds or max_rss_bytes() >= 11_500_000_000:
            status = "CAP_FRONTIER"
            break
        row_hex = queue.popleft()
        queued.remove(row_hex)
        row = bytes.fromhex(row_hex)
        require(row_hex not in processed, (row_hex, "processed twice"))
        incident = D24.incident_degree24_columns(row)
        canonical_incident = sorted({canonical_column(column) for column in incident},
                                    key=column_key)
        new_columns = 0
        new_rows = set()
        for source_column in canonical_incident:
            key = column_key(source_column)
            if key in columns:
                continue
            representative, orbit_size, entries, provenance = column_vector(source_column)
            require(representative == source_column, key)
            if len(literal_replays) < 8:
                equivariance_checks += equivariance_replay(source_column)
                replay_orbit, replay_terms = literal_mass_replay(source_column, entries)
                literal_replays.append({
                    "column": key,
                    "source_orbit_size": replay_orbit,
                    "low_literal_occurrences": replay_terms,
                    "quotient_entries": len(entries),
                })
            columns[key] = {
                "orbit_size": orbit_size,
                "entries": {target.hex(): value
                            for target, value in sorted(entries.items())},
                "provenance_matching_indices": {
                    target.hex(): indices
                    for target, indices in sorted(provenance.items())
                },
            }
            new_columns += 1
            for target in entries:
                target_hex = target.hex()
                if target_hex in rows:
                    continue
                orbit = {F.move_row(target, action) for action in H}
                require(min(orbit) == target, (target_hex, "noncanonical row"))
                mass = oracle.query(target) if D24.row_k_degree(target) == 16 else None
                rows[target_hex] = {
                    "K_degree": D24.row_k_degree(target),
                    "orbit_size": len(orbit),
                    "dafsa_mass": list(mass) if mass is not None else None,
                }
                new_rows.add(target_hex)
        processed.add(row_hex)
        for new_row in sorted(new_rows):
            queue.append(new_row)
            queued.add(new_row)
        state["events"].append({
            "processed_index": len(processed),
            "row": row_hex,
            "literal_incident_columns": len(incident),
            "H_column_orbits_incident": len(canonical_incident),
            "new_column_orbits": new_columns,
            "new_row_orbits": len(new_rows),
            "total_column_orbits": len(columns),
            "total_row_orbits": len(rows),
            "queued_row_orbits": len(queue),
        })
        state["queue"] = list(queue)
        state["processed"] = sorted(processed)
        if time.monotonic() - last_checkpoint >= 10:
            compact_checkpoint(state, time.monotonic() - started, "RUNNING")
            last_checkpoint = time.monotonic()
            print(json.dumps(state["events"][-1], sort_keys=True), flush=True)
    else:
        status = "CLOSED_COMPONENT"

    elapsed = time.monotonic() - started
    state["queue"] = list(queue)
    state["processed"] = sorted(processed)
    compact_checkpoint(state, elapsed, status)
    oracle.close()

    row_degree_histogram = Counter(record["K_degree"] for record in rows.values())
    row_orbit_size_histogram = Counter(record["orbit_size"] for record in rows.values())
    column_orbit_size_histogram = Counter(record["orbit_size"]
                                          for record in columns.values())
    dafsa_hits = sum(record["dafsa_mass"] is not None for record in rows.values())
    row_digest = sha256("\n".join(sorted(rows)).encode()).hexdigest()
    column_digest = sha256("\n".join(sorted(columns)).encode()).hexdigest()

    frontier = {
        "status": status,
        "processed_row_orbits": len(processed),
        "queued_row_orbits": len(queue),
        "row_orbits": len(rows),
        "source_column_orbits": len(columns),
        "row_K_degree_histogram": {str(k): v for k, v in sorted(row_degree_histogram.items())},
        "row_orbit_size_histogram": {str(k): v for k, v in
                                     sorted(row_orbit_size_histogram.items())},
        "column_orbit_size_histogram": {str(k): v for k, v in
                                        sorted(column_orbit_size_histogram.items())},
        "weighted_DAFSA_hits": dafsa_hits,
        "row_representative_digest": row_digest,
        "column_representative_digest": column_digest,
        "elapsed_seconds": elapsed,
        "max_rss_bytes": max_rss_bytes(),
        "last_complete_event": state["events"][-1] if state["events"] else None,
    }
    atomic_json(FRONTIER, frontier)

    # Peeling or linear algebra is sound only after complete closure.
    if status == "CLOSED_COMPONENT":
        verdict = "CLOSED_UNSOLVED"
        inference = (
            "The full H-orbit component closed. This bounded driver records the "
            "matrix but makes no member/dual claim until a target-aware exact-Q "
            "peel and a literal orbit-mass replay are separately frozen."
        )
    else:
        verdict = "UNRESOLVED_CAP"
        inference = (
            "The H-orbit component did not close within the gate. No singleton, "
            "rank, member, or dual inference is valid from this frontier."
        )

    result = {
        "format": "orbit0-k16-H-quotient-closure-result-v1",
        "status": verdict,
        "theorem_scope": {
            "target": "complete H-orbit sum of the lex K14 monomial q",
            "target_representative": Q.hex(),
            "target_orbit_mass": [384, 1],
            "rows": "H-orbits of literal degree24 rows with K-degree<=16",
            "columns": "H-orbits of literal mixed word times degree20 multiplier",
            "matrix_basis": "total orbit mass",
            "inference": inference,
        },
        "frontier": frontier,
        "provider_validation": {
            "H_order": len(H),
            "source_action_equivariance_checks": equivariance_checks,
            "complete_literal_mass_replays": literal_replays,
            "mass_formula": (
                "entry(R,C)=|Orb_H(C)| times the number of base-column matching "
                "terms whose literal output canonicalizes to R"
            ),
            "DAFSA_role": (
                "exact orbit-mass annotation for encountered nonzero K16 residual "
                "rows; K12--K15 and zero K16 rows remain source-generated"
            ),
        },
        "restart": {
            "checkpoint": str(CHECKPOINT.relative_to(ROOT)),
            "checkpoint_schema": state["schema"],
            "atomic_interval_seconds": 10,
            "resume_command": (
                "python3 " + str(Path(__file__).relative_to(ROOT)) +
                " --resume --seconds 285"
            ),
        },
        "pinned": {
            str(HPL_PATH.relative_to(ROOT)): file_sha256(HPL_PATH),
            str(DAFSA_SOURCE.relative_to(ROOT)): file_sha256(DAFSA_SOURCE),
            str(DAFSA_BINARY.relative_to(ROOT)): file_sha256(DAFSA_BINARY),
        },
    }
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    atomic_json(RESULT, result)
    print(json.dumps({
        "status": verdict,
        "logical_sha256": logical,
        **frontier,
    }, indent=2, sort_keys=True), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=285.0)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    run(args.seconds, args.resume)


if __name__ == "__main__":
    main()
