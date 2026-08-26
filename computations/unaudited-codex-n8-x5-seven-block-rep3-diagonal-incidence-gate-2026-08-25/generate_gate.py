#!/usr/bin/env python3
"""Generate exact rep3 diagonal-incidence ideals after eliminating A36."""

from __future__ import annotations

import hashlib
import itertools
import json
import os
from collections import Counter
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / "computations/unaudited-codex-n8-x5-seven-block-guard-dual-gate-2026-08-25/results_full_family_obligation.json"
PARENT_SHA = "22b471512c6ac6a6ff86bb65fbd4f1fec094208a1c99d338865dfee89c0cb3a0"
FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
VARIABLE = frozenset(((0, 4), (1, 2), (3, 5), (6, 7)))
ADDED = frozenset(((0, 6), (1, 4), (1, 7), (2, 5), (2, 6), (3, 6), (3, 7)))
NONFIXED = tuple(sorted(VARIABLE | ADDED))
ELIMINATED = (3, 6)
RETAINED = tuple(item for item in NONFIXED if item != ELIMINATED)
SUPPORT = FIXED | set(NONFIXED)
COLORS = tuple(range(3))
CHARTS = ((0, 0), (0, 1), (1, 0), (1, 1), (1, 2))


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


PM8 = tuple(sorted(matchings(tuple(range(8)))))
SUPPORTED = tuple(matching for matching in PM8 if set(matching) <= SUPPORT)
assert len(PM8) == 105 and len(SUPPORTED) == 12
SOURCE = {(edge, i, j): f"a{edge[0]}{edge[1]}_{i}{j}" for edge in RETAINED for i, j in itertools.product(COLORS, repeat=2)}
X = tuple(f"x{i}" for i in COLORS)
Y = tuple(f"y{i}" for i in COLORS)
Z = tuple(f"z{i}" for i in COLORS)
SAT = "sat"


def atom_product(*factors):
    if any(factor == "0" for factor in factors):
        return "0"
    factors = [factor for factor in factors if factor != "1"]
    return "*".join(factors) if factors else "1"


def sum_string(terms):
    terms = [term for term in terms if term != "0"]
    return "+".join(terms).replace("+-", "-") if terms else "0"


def wrapped(value):
    return f"({value})" if "+" in value or ("-" in value[1:]) or value.startswith("-") else value


def product(*factors):
    if any(factor == "0" for factor in factors):
        return "0"
    factors = [wrapped(factor) for factor in factors if factor != "1"]
    return "*".join(factors) if factors else "1"


def source(edge, i, j):
    return SOURCE[edge, i, j]


def entry(edge, i, j):
    if edge in FIXED:
        return "1" if i == j else "0"
    if edge == ELIMINATED:
        # A36^T=-A26*A37^T, hence A36=-A37*A26^T.
        value = sum_string(atom_product(source((3, 7), i, k), source((2, 6), j, k)) for k in COLORS)
        return f"-({value})"
    return source(edge, i, j)


def amplitude(word):
    terms = []
    for matching in SUPPORTED:
        factors = []
        for block in matching:
            value = entry(block, word[block[0]], word[block[1]])
            if value == "0":
                break
            factors.append(value)
        else:
            terms.append(product(*factors))
    return sum_string(terms)


def parent_digest_and_census():
    records = []
    census = Counter()
    for word in itertools.product(COLORS, repeat=8):
        terms = []
        for matching in SUPPORTED:
            factors = []
            for block in matching:
                i, j = word[block[0]], word[block[1]]
                if block in FIXED:
                    if i != j:
                        break
                else:
                    factors.append(f"A{block[0]}{block[1]}[{i}{j}]")
            else:
                terms.append("*".join(factors) or "1")
        target = 1 if len(set(word)) == 1 else 0
        census[len(terms)] += 1
        records.append(("".join(map(str, word)), target, tuple(terms)))
    payload = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest(), dict(sorted(census.items()))


def guard_equations():
    equations = []
    # A06*A37^T=0.
    for i, j in itertools.product(COLORS, repeat=2):
        equations.append(sum_string(atom_product(source((0, 6), i, k), source((3, 7), j, k)) for k in COLORS))
    # (I-A17*A26)*A37^T=0.
    for i, j in itertools.product(COLORS, repeat=2):
        correction = sum_string(
            atom_product(source((1, 7), i, k), source((2, 6), k, ell), source((3, 7), j, ell))
            for k, ell in itertools.product(COLORS, repeat=2)
        )
        equations.append(f"{source((3, 7), j, i)}-({correction})")
    return equations


def incidence_equations(coordinate=0):
    equations = []
    # e_coordinate in P=Col(A06).
    for i in COLORS:
        value = sum_string(atom_product(source((0, 6), i, j), X[j]) for j in COLORS)
        equations.append(f"({value})-{int(i == coordinate)}")
    # e_coordinate in Q=ColSpan(A35,A37).
    for i in COLORS:
        value = sum_string(
            [atom_product(source((3, 5), i, j), Y[j]) for j in COLORS]
            + [atom_product(source((3, 7), i, j), Z[j]) for j in COLORS]
        )
        equations.append(f"({value})-{int(i == coordinate)}")
    return equations


def build_program(ring, chart, algorithm="slimgb"):
    full = []
    for word in itertools.product(COLORS, repeat=8):
        value = amplitude(word)
        full.append(f"({value})-1" if len(set(word)) == 1 else value)
    guard = guard_equations()
    incidence = incidence_equations(0)
    saturation = f"{source((3, 7), chart[0], chart[1])}*{SAT}-1"
    equations = full + guard + incidence + [saturation]
    variables = list(SOURCE.values()) + list(X) + list(Y) + list(Z) + [SAT]
    assert len(variables) == 100 and len(set(variables)) == 100
    assert len(equations) == 6586
    lines = [
        "option(noredefine);",
        f"ring r={ring},({','.join(variables)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_GENERATORS="+string(size(I)));',
        f"ideal G={algorithm}(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',
        "poly remainder=reduce(1,G);",
        'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',
        "quit;",
    ]
    return "\n".join(lines) + "\n"


def atomic_write(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value)
    os.replace(temporary, path)


def main():
    assert sha256(PARENT) == PARENT_SHA
    parent = json.loads(PARENT.read_text())["six_full_family_representatives"][3]
    digest, census = parent_digest_and_census()
    assert parent["representative_id"] == 3
    assert digest == parent["full_x5_6561_equation_sha256"] == "ee9c9d10bc3735ad4e8be0253275411fb021e51d5c46ffc3a02420ac63a1382e"
    assert {str(k): v for k, v in census.items()} == parent["full_x5_term_count_census"]
    assert parent["guard"]["fixed_identity_substitution"] == ["A06*A37^T=0", "A37^T+A17*A36^T=0", "A26*A37^T+A36^T=0"]
    inputs = {}
    for chart in CHARTS:
        chart_id = f"p{chart[0]}{chart[1]}"
        inputs[chart_id] = {}
        for label_ring, ring in (("p32003", "32003"), ("Q", "0")):
            program = build_program(ring, chart)
            path = HERE / f"rep3_e0_{chart_id}_{label_ring}.sing"
            atomic_write(path, program)
            inputs[chart_id][label_ring] = {"path": path.name, "sha256": hashlib.sha256(program.encode()).hexdigest()}
    metadata = {
        "schema": "KRENN_X5_REP3_DIAGONAL_INCIDENCE_GATE_V1",
        "status": "PASS_INPUT_GENERATION",
        "representative_id": 3,
        "source_orientation": {"elimination": "A36=-A37*A26^T", "guard": ["A06*A37^T=0", "(I-A17*A26)*A37^T=0"], "P_incidence": "A06*x=e0", "Q_incidence": "A35*y+A37*z=e0"},
        "s3_normalization": {"diagonal_coordinate": "i=0", "residual_stabilizer": "swap colors 1 and 2", "outside_entry_orbits": [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2]], "charts_complete": True},
        "counts": {"variables": 100, "equations": 6586, "full_x5": 6561, "guard_after_elimination": 18, "incidence": 6, "saturation": 1},
        "parent_full_x5_digest": digest,
        "parent_term_census": census,
        "inputs": inputs,
        "scope": {"only_chart_to_run_now": "p00", "other_charts_generated_not_run": True, "Q_requires_modular_unit": True},
    }
    atomic_write(HERE / "gate_metadata.json", json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": metadata["status"], "charts": len(CHARTS), "variables": 100, "equations": 6586}, sort_keys=True))


if __name__ == "__main__":
    main()
