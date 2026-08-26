#!/usr/bin/env python3
"""Exact H-invariant K24 column/Gram provider with restartable closure.

The provider never enumerates the ambient K24 row language.  A column orbit
vector is collected by moving one literal `(word,U)` column through H and
canonicalizing its at most 105 K24 outputs.  Its neighbour oracle uses literal
inverse incidence on those outputs.  This is exact but can still have a huge
column-orbit closure.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction
from functools import lru_cache
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HPL_SOURCE = (ROOT / "computations/unaudited-codex-orbit0-k16-lower-kernel-hpl-2026-08-23"
              / "audit_k16_lower_kernel_component.py")
D24_SOURCE = (ROOT / "computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20"
              / "audit_orbit0_t2_pivot_setup.py")


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


HPL = load("k24_gram_hpl", HPL_SOURCE)
D24 = load("k24_gram_d24", D24_SOURCE)
F = HPL.F
THREE_ANCHORS, _PACKET = HPL.fractionless_packet()
H = HPL.factor_stabilizer(THREE_ANCHORS)
require(len(H) == 384, len(H))


def move_word(word, action):
    sites, colours = F.EXPORT.STABILIZER[action]
    moved = [None] * 8
    for old_site, old_colour in enumerate(word):
        moved[sites[old_site]] = colours[old_colour]
    return tuple(moved)


def move_column(column, action):
    word, multiplier = column
    transform = F.EXPORT.TRANSFORMS[action]
    return (move_word(word, action),
            bytes(sorted(transform[cell] for cell in multiplier)))


def column_key(column):
    word, multiplier = column
    return "".join(map(str, word)) + ":" + multiplier.hex()


def parse_column_key(key):
    word, multiplier = key.split(":", 1)
    return tuple(map(int, word)), bytes.fromhex(multiplier)


@lru_cache(None)
def column_orbit(column):
    return tuple(sorted({move_column(column, action) for action in H}, key=repr))


@lru_cache(None)
def canonical_column(column):
    return column_orbit(column)[0]


@lru_cache(None)
def row_orbit(row):
    return tuple(sorted({F.move_row(row, action) for action in H}))


@lru_cache(None)
def canonical_row(row):
    return row_orbit(row)[0]


@lru_cache(None)
def top_outputs(column):
    word, multiplier = column
    require(len(word) == 8 and len(set(word)) > 1 and len(multiplier) == 20,
            "invalid mixed degree-24 column")
    return tuple(row for row in D24.degree24_column_rows(column)
                 if D24.row_k_degree(row) == 24)


@lru_cache(None)
def orbit_column_vector(column):
    """Return `(row_rep,total_mass,row_orbit_size)` for the orbit-sum column."""
    representative = canonical_column(column)
    masses = Counter()
    for moved in column_orbit(representative):
        for row in top_outputs(moved):
            masses[canonical_row(row)] += 1
    answer = []
    for row, mass in sorted(masses.items()):
        size = len(row_orbit(row))
        require(mass % size == 0,
                (column_key(representative), row.hex(), mass, size))
        answer.append((row, mass, size))
    return tuple(answer)


def gram_entry(left, right):
    """Exact dot product of the two H-orbit-sum column vectors."""
    first = {row: (mass, size)
             for row, mass, size in orbit_column_vector(left)}
    second = {row: (mass, size)
              for row, mass, size in orbit_column_vector(right)}
    answer = Fraction(0)
    for row in first.keys() & second.keys():
        left_mass, size = first[row]
        right_mass, other_size = second[row]
        require(size == other_size, "row orbit-size mismatch")
        answer += Fraction(left_mass * right_mass, size)
    require(answer.denominator == 1, (column_key(left), column_key(right), answer))
    return answer.numerator


def target_pairing(column, target_orbit_masses):
    """Pair an orbit-sum column with an H-invariant target in orbit-mass form."""
    answer = Fraction(0)
    for row, column_mass, size in orbit_column_vector(column):
        target_mass = target_orbit_masses.get(row, 0)
        answer += Fraction(column_mass * target_mass, size)
    return answer


def target_norm(target_orbit_masses):
    answer = Fraction(0)
    for row, mass in target_orbit_masses.items():
        answer += Fraction(mass * mass, len(row_orbit(row)))
    return answer


@lru_cache(None)
def neighbour_orbits(column):
    """Every H-column orbit with nonzero Gram pairing with `column`."""
    representative = canonical_column(column)
    neighbours = set()
    # It suffices to use the representative outputs: the H transports yield
    # the same canonical neighbour orbits.
    for row in top_outputs(representative):
        for incident in D24.incident_degree24_columns(row):
            neighbours.add(canonical_column(incident))
    return tuple(sorted(neighbours, key=repr))


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def close_column_component(seed_columns, checkpoint, column_cap, resume=False):
    if resume and checkpoint.exists():
        state = json.loads(checkpoint.read_text())
        require(state["schema"] == "orbit0-k24-H-column-closure-v1",
                "checkpoint schema drift")
        known = {parse_column_key(key) for key in state["known"]}
        processed = {parse_column_key(key) for key in state["processed"]}
        queue = deque(parse_column_key(key) for key in state["queue"])
    else:
        known = {canonical_column(column) for column in seed_columns}
        processed = set()
        queue = deque(sorted(known, key=repr))

    status = "COMPLETE"
    while queue:
        column = queue.popleft()
        if column in processed:
            continue
        neighbours = neighbour_orbits(column)
        for neighbour in neighbours:
            if neighbour not in known:
                known.add(neighbour)
                queue.append(neighbour)
        processed.add(column)
        if len(known) > column_cap:
            status = "COLUMN_CAP"
            break

    state = {
        "schema": "orbit0-k24-H-column-closure-v1",
        "status": status,
        "column_cap": column_cap,
        "known": [column_key(column) for column in sorted(known, key=repr)],
        "processed": [column_key(column)
                      for column in sorted(processed, key=repr)],
        "queue": [column_key(column) for column in queue],
        "scope": (
            "Exact H-column Gram-component closure. COMPLETE is required before "
            "forming a terminal membership Gram; COLUMN_CAP is unresolved."
        ),
    }
    atomic_json(checkpoint, state)
    return state


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-row", help="balanced K24 row as 48 hex digits")
    parser.add_argument("--checkpoint", type=Path,
                        default=HERE / "checkpoint_k24_column_closure.json")
    parser.add_argument("--column-cap", type=int, default=1000)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.seed_row is None:
        print(json.dumps({
            "status": "READY exact K24 H-column Gram provider",
            "H_order": len(H),
            "membership_criterion": (
                "For a closed column component, append the target orbit-mass "
                "vector to the orbit-column Gram. Over Q, target membership is "
                "equivalent to no augmented Gram-rank increase."
            ),
        }, indent=2))
        return
    row = bytes.fromhex(args.seed_row)
    require(len(row) == 24 and D24.row_k_degree(row) == 24,
            "seed is not a K24 row")
    seeds = D24.incident_degree24_columns(row)
    require(seeds, "seed row has no literal mixed column")
    state = close_column_component(seeds, args.checkpoint,
                                   args.column_cap, args.resume)
    print(json.dumps({key: value for key, value in state.items()
                      if key not in ("known", "processed", "queue")},
                     indent=2, sort_keys=True))
    print("known", len(state["known"]), "processed", len(state["processed"]),
          "queued", len(state["queue"]))


if __name__ == "__main__":
    main()
