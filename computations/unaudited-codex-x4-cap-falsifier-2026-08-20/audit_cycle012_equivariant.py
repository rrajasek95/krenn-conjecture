#!/usr/bin/env python3
"""Exact unit certificate for the joint shift/three-colour-cycle X4 ansatz.

Ansatz generator:

    A_{u+1,v+1}[sigma(a),sigma(b)] = A_{uv}[a,b],
    sigma = (0 1 2), sites modulo 8,

with endpoint reordering accompanied by matrix transposition.  The generator
has order lcm(8,3)=24 on endpoint cells and exactly 11 cell orbits.  Hence
assigning one coordinate to every orbit is exhaustive for this fixed locus.
All 4,881 raw X4 equations reduce to 121 distinct nonzero polynomials.  A
Singular source lift certifies that their ideal over Q contains one.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from itertools import product
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import classify_equivariant as CE  # noqa: E402


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def transformed_index(index):
    return CE.INDEX[CE.transform(CE.CELLS[index], 1, (1, 2, 0))]


def orbit(start):
    answer = []
    current = start
    while current not in answer:
        answer.append(current)
        current = transformed_index(current)
    require(current == start, "cell action did not close at orbit start")
    return tuple(answer)


def recursive_polynomial(word, qmap, vertices):
    vertices = tuple(vertices)
    if not vertices:
        return Counter({(0,) * (max(qmap) + 1): 1})
    u = vertices[0]
    answer = Counter()
    for position in range(1, len(vertices)):
        v = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        tail = recursive_polynomial(word, qmap, rest)
        raw_index = CE.cell_index(u, v, word[u], word[v])
        variable = qmap[raw_index]
        for exponent, coefficient in tail.items():
            new = list(exponent)
            new[variable] += 1
            answer[tuple(new)] += coefficient
    return answer


def singular_lift(generators, variable_count):
    variables = ",".join(f"x{i + 1}" for i in range(variable_count))
    code = f"ring R=0,({variables}),dp; option(redSB);\n"
    code += "ideal I=" + ",\n".join(CE.emit_poly(g) for g in generators) + ";\n"
    code += "matrix L; ideal G=liftstd(I,L);\n"
    code += (
        "if(size(G)!=1 || G[1]!=1 || nrows(L)!=size(I) || ncols(L)!=1)"
        "{ print(\"UNIT_LIFT_SHAPE_FAILED\"); exit(1); }\n"
    )
    code += (
        "if(matrix(I)*L-matrix(G)!=0)"
        "{ print(\"SOURCE_IDENTITY_FAILED\"); exit(1); }\n"
    )
    code += "int i; int nz=0; for(i=1;i<=nrows(L);i++){if(L[i,1]!=0){nz=nz+1;}}\n"
    code += "int firstactive=0; for(i=1;i<=nrows(L);i++){if(firstactive==0 && L[i,1]!=0){firstactive=i;}}\n"
    code += "matrix MUT=matrix(I); MUT[1,firstactive]=0;\n"
    code += (
        "if(MUT*L-matrix(G)==0)"
        "{ print(\"CERTIFICATE_MUTATION_SURVIVED\"); exit(1); }\n"
    )
    code += 'print("NONZERO"); print(nz); print("FIRSTACTIVE"); print(firstactive);\n'
    code += 'print("BEGIN_LIFT"); L; print("END_LIFT");\n'
    completed = subprocess.run(
        ["Singular", "-q", "--no-warn"], input=code, text=True,
        capture_output=True, timeout=120, check=False,
    )
    require(completed.returncode == 0, completed.stderr or completed.stdout[-2000:])
    require("UNIT_LIFT_SHAPE_FAILED" not in completed.stdout, "unit lift shape failed")
    require("SOURCE_IDENTITY_FAILED" not in completed.stdout, "source identity failed")
    require("CERTIFICATE_MUTATION_SURVIVED" not in completed.stdout,
            "deleting the first active source row did not break the lift identity")
    require(not any(line.lstrip().startswith("?") for line in completed.stdout.splitlines()),
            completed.stdout[-2000:])
    lines = completed.stdout.splitlines()
    marker = lines.index("NONZERO")
    nonzero = int(lines[marker + 1])
    first_marker = lines.index("FIRSTACTIVE")
    first_active = int(lines[first_marker + 1])
    lift_text = completed.stdout.split("BEGIN_LIFT\n", 1)[1].split("\nEND_LIFT", 1)[0]
    multipliers = []
    for index, line in enumerate(lift_text.splitlines(), start=1):
        prefix = f"L[{index},1]="
        require(line.startswith(prefix), f"unexpected lift row: {line[:100]}")
        multipliers.append(line[len(prefix):])
    require(len(multipliers) == len(generators), len(multipliers))
    require(sum(value != "0" for value in multipliers) == nonzero, nonzero)
    require(multipliers[first_active - 1] != "0", "first-active marker is zero")
    return multipliers, lift_text, first_active


def main():
    qmap, representatives = CE.quotient("cycle012")
    require(len(representatives) == 11, len(representatives))
    raw_orbits = {orbit(index) for index in representatives}
    require(sum(len(item) for item in raw_orbits) == 252, "orbits do not partition cells")
    require({len(item) for item in raw_orbits} == {12, 24},
            sorted(Counter(map(len, raw_orbits)).items()))
    require(all(transformed_index(index) != index for index in range(252)),
            "generator unexpectedly fixes a raw cell")
    # The 24th power is identity on every endpoint cell; the 8th power still
    # acts by sigma^2, so the joint action really is not an eight-cycle.
    for index in range(252):
        current = index
        for _ in range(24):
            current = transformed_index(current)
        require(current == index, "24th power is not identity")

    polynomial_words = {}
    multiplicities = Counter()
    raw_counts = Counter()
    recursive_checks = 0
    for word in product(CE.COLORS, repeat=8):
        word = tuple(word)
        off = CE.off_count(word)
        if off > 4:
            continue
        raw_counts[off] += 1
        poly = CE.polynomial(word, qmap, len(representatives))
        # Second raw engine on a deterministic 111-word spread plus all three
        # pures.  It recursively expands rather than using the PM table.
        number = sum(digit * 3 ** position for position, digit in enumerate(word))
        if len(set(word)) == 1 or number % 44 == 0:
            recursive = recursive_polynomial(word, qmap, CE.SITES)
            if len(set(word)) == 1:
                recursive[(0,) * len(representatives)] -= 1
            recursive_poly = tuple(sorted((e, c) for e, c in recursive.items() if c))
            require(recursive_poly == poly, f"raw engines disagree at {word}")
            recursive_checks += 1
        if poly:
            polynomial_words.setdefault(poly, word)
            multiplicities[poly] += 1
    generators = list(polynomial_words)
    require(len(generators) == 121, len(generators))
    require(sum(multiplicities.values()) <= 4881, "multiplicity overflow")

    multipliers, lift_text, first_active = singular_lift(
        generators, len(representatives)
    )
    active = []
    for index, multiplier in enumerate(multipliers):
        if multiplier == "0":
            continue
        word = polynomial_words[generators[index]]
        active.append({
            "generator_index": index + 1,
            "representative_word": "".join(map(str, word)),
            "raw_orbit_multiplicity": multiplicities[generators[index]],
            "generator": CE.emit_poly(generators[index]),
            "multiplier": multiplier,
        })
    require(active, "empty source certificate")

    result = {
        "status": "UNAUDITED_EXACT_UNIT_CERTIFICATE",
        "ansatz_equation": "A_(u+1,v+1)[sigma(a),sigma(b)] = A_(u,v)[a,b], sigma=(012), sites mod 8, endpoint reversal transposes",
        "exhaustiveness": "The fixed linear subspace is exactly one free coordinate per orbit of the order-24 generator on the 252 endpoint cells.",
        "raw_endpoint_cells": 252,
        "generator_order": 24,
        "cell_orbit_size_histogram": dict(sorted(Counter(map(len, raw_orbits)).items())),
        "quotient_variables": len(representatives),
        "representative_cells": [list(CE.CELLS[index]) for index in representatives],
        "raw_X4_word_counts": dict(sorted(raw_counts.items())),
        "recursive_engine_checks": recursive_checks,
        "distinct_nonzero_X4_generators": len(generators),
        "active_certificate_rows": active,
        "active_certificate_row_count": len(active),
        "certificate_row_deletion_mutation": {
            "deleted_generator_index": first_active,
            "identity_broken": True,
        },
        "lift_sha256": hashlib.sha256(lift_text.encode()).hexdigest(),
        "generator_list_sha256": hashlib.sha256(
            "\n".join(CE.emit_poly(g) for g in generators).encode()
        ).hexdigest(),
        "verdict": "The joint site-shift/color-cycle fixed locus contains no X4 point over characteristic zero.",
        "carrier_audit": "Vacuous: there is no X4 point in the ansatz to screen against the 728 carriers or 28 cap ideals.",
        "scope_warning": "This decides only the explicitly stated 11-dimensional fixed linear ansatz, not arbitrary X4.",
    }
    (HERE / "certificate_cycle012.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print("CYCLE012 UNIT: vars", len(representatives), "generators", len(generators),
          "active lift rows", len(active), "engine checks", recursive_checks)


if __name__ == "__main__":
    main()
