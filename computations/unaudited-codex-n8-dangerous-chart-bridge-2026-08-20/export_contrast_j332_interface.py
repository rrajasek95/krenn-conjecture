#!/usr/bin/env python3
"""Export the 112-variable signed-S8 contrast/J332 radical interface."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "audit_dangerous_charts.py"
SPEC = importlib.util.spec_from_file_location("contrast_export_base", BASE_PATH)
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
SEED = HERE / "contrast_j332_seed.txt"
PROVENANCE = HERE / "contrast_j332_raw256_provenance.jsonl"
RESULT = HERE / "results_contrast_j332_interface.json"

KINDS = ("a", "b", "c", "h")
VECTORS = ((1, -1, 0), (1, 0, -1), (0, 1, -1))  # p,q,r=q-p
ASSIGNMENTS = tuple(sorted(set(permutations((0, 0, 0, 1, 1, 1, 2, 2)))))


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def edge_list():
    return tuple((u, v) for u in range(BASE.N) for v in range(u + 1, BASE.N))


EDGES = edge_list()
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def variable(edge: tuple[int, int], kind: int) -> int:
    return 4 * EDGE_INDEX[edge] + kind


def bilinear(left: int, right: int):
    """Coordinates of type-left^T X type-right in (a,b,c,h)."""
    if left == right:
        return ((left, Fraction(1)),)
    # a=pXp, b=qXq, c=rXr, h=pXq-qXp.
    table = {
        (0, 1): (1, 1, -1, 1),
        (1, 0): (1, 1, -1, -1),
        (0, 2): (-1, 1, -1, 1),
        (2, 0): (-1, 1, -1, -1),
        (1, 2): (-1, 1, 1, 1),
        (2, 1): (-1, 1, 1, -1),
    }
    return tuple((kind, Fraction(coefficient, 2))
                 for kind, coefficient in enumerate(table[(left, right)]))


def generator_polynomial(assignment):
    answer = Counter()
    for matching in BASE.PM8:
        partial = Counter({b"": Fraction(1)})
        for u, v in matching:
            updated = Counter()
            for row, coefficient in partial.items():
                for kind, factor in bilinear(assignment[u], assignment[v]):
                    updated[bytes(sorted(row + bytes((variable((u, v), kind),))))] += (
                        coefficient * factor
                    )
            partial = updated
        answer.update(partial)
    scaled = Counter({row: 16 * coefficient
                      for row, coefficient in answer.items() if coefficient})
    require(all(value.denominator == 1 for value in scaled.values()),
            "scale16 did not clear a P332 generator")
    return Counter({row: value.numerator for row, value in scaled.items()})


def raw_provenance(assignment):
    entries = []
    supports = [tuple(colour for colour, value in enumerate(VECTORS[kind]) if value)
                for kind in assignment]
    for word in product(*supports):
        coefficient = 1
        for site, colour in enumerate(word):
            coefficient *= VECTORS[assignment[site]][colour]
        require(coefficient in (-1, 1) and len(set(word)) > 1,
                "raw P332 provenance is not a signed mixed word")
        entries.append(("".join(map(str, word)), coefficient))
    require(len(entries) == 256
            and Counter(coefficient for _word, coefficient in entries)
            == {-1: 128, 1: 128}, "raw256 provenance changed")
    return entries


def multiply_symbolic(left, right):
    answer = Counter()
    for lexp, lc in left.items():
        for rexp, rc in right.items():
            answer[tuple(lexp[i] + rexp[i] for i in range(3))] += lc * rc
    return Counter({key: value for key, value in answer.items() if value})


def heron_symbolic():
    factors = (
        Counter({(1, 0, 0): 1, (0, 1, 0): 1, (0, 0, 1): -1}),
        Counter({(1, 0, 0): 1, (0, 1, 0): -1, (0, 0, 1): 1}),
        Counter({(1, 0, 0): -1, (0, 1, 0): 1, (0, 0, 1): 1}),
    )
    return multiply_symbolic(multiply_symbolic(factors[0], factors[1]), factors[2])


def main() -> None:
    require(len(EDGES) == 28 and len(KINDS) * len(EDGES) == 112,
            "contrast variable census changed")
    require(len(ASSIGNMENTS) == 560, "P332 generator count changed")
    require(bilinear(0, 1) == ((0, Fraction(1, 2)),
                               (1, Fraction(1, 2)),
                               (2, Fraction(-1, 2)),
                               (3, Fraction(1, 2))),
            "h convention changed")

    seed_lines = [
        "KRENN_CONTRAST_J332_V1",
        "N 8",
        "COORDINATES a=pXp b=qXq c=rXr h=pXq-qXp",
        "BASIS p=1,-1,0 q=1,0,-1 r=0,1,-1=q-p",
        "GENERATOR_SCALE 16",
        "HERON_TO_T_SCALE 8",
        "TARGET_POWER 2",
    ]
    for edge_index, (u, v) in enumerate(EDGES):
        seed_lines.append(f"BLOCK {edge_index} {u} {v} "
                          + " ".join(f"{kind}={4*edge_index+i}"
                                     for i, kind in enumerate(KINDS)))
    for sites in permutations(range(BASE.N)):
        seed_lines.append("ACTION " + "".join(map(str, sites)))
    for index, assignment in enumerate(ASSIGNMENTS):
        seed_lines.append(f"GENERATOR {index} " + "".join(map(str, assignment)))
    heron = heron_symbolic()
    for exponent, coefficient in sorted(heron.items()):
        seed_lines.append("HERON_TERM %d %d %d %d" % (*exponent, coefficient))
    seed_payload = "\n".join(seed_lines) + "\n"
    SEED.write_text(seed_payload)

    provenance_lines = [json.dumps({
        "format": "krenn-contrast-j332-raw256-provenance-v1",
        "generator_scale": 16,
        "identity": "P_sigma=sum_w coefficient(w)*H_w; stored generator=16*P_sigma",
        "seed_sha256": sha256(seed_payload.encode("ascii")).hexdigest(),
    }, sort_keys=True, separators=(",", ":"))]
    for index, assignment in enumerate(ASSIGNMENTS):
        provenance_lines.append(json.dumps({
            "assignment": "".join(map(str, assignment)),
            "generator": index,
            "terms": raw_provenance(assignment),
        }, sort_keys=True, separators=(",", ":")))
    provenance_payload = "\n".join(provenance_lines) + "\n"
    PROVENANCE.write_text(provenance_payload)

    support_histogram = Counter()
    coefficient_histogram = Counter()
    for assignment in ASSIGNMENTS:
        polynomial = generator_polynomial(assignment)
        support_histogram[len(polynomial)] += 1
        coefficient_histogram.update(polynomial.values())

    result = {
        "status": "UNAUDITED exact 112-variable contrast/J332 interface",
        "base_sha256": sha256(BASE_PATH.read_bytes()).hexdigest(),
        "seed_sha256": sha256(seed_payload.encode("ascii")).hexdigest(),
        "provenance_sha256": sha256(provenance_payload.encode("ascii")).hexdigest(),
        "edges": len(EDGES),
        "variables": 4 * len(EDGES),
        "coordinates": {
            "a": "p^T X p", "b": "q^T X q", "c": "r^T X r",
            "h": "p^T X q - q^T X p",
        },
        "offdiagonal_inverse": {
            "pXq": "(a+b-c+h)/2",
            "qXp": "(a+b-c-h)/2",
        },
        "orientation_action": (
            "A site permutation sends an unordered edge block to its image; "
            "if image endpoint order reverses, a,b,c are unchanged and h "
            "acquires sign -1. Thus S8 acts by signed variable permutations."
        ),
        "site_actions": math_factorial_8(),
        "generators": len(ASSIGNMENTS),
        "generator_scale": 16,
        "generator_support_histogram": {
            str(k): v for k, v in sorted(support_histogram.items())
        },
        "generator_coefficient_histogram": {
            str(k): v for k, v in sorted(coefficient_histogram.items())
        },
        "raw_mixed_words_per_generator": 256,
        "raw_provenance_terms": 256 * len(ASSIGNMENTS),
        "A_B_C": "A=Haf(a_uv), B=Haf(b_uv), C=Haf(c_uv), each 105 terms",
        "Heron_symbolic_terms": [
            {"A_power": exponent[0], "B_power": exponent[1],
             "C_power": exponent[2], "coefficient": coefficient}
            for exponent, coefficient in sorted(heron.items())
        ],
        "target": "Heron^2, homogeneous degree24; source multipliers degree20",
        "normalization_contract": (
            "Unscaled P_sigma is the exact signed 256-word mixed-H "
            "contraction. The stored generator is G_sigma=16 P_sigma; 16 is "
            "a unit over Q. In R/I_mix, Heron=8T. Therefore an exact identity "
            "Heron^m in <G_sigma> implies 8^m T^m in I_mix and hence "
            "T^m in I_mix over characteristic zero."
        ),
        "negative_scope_guard": (
            "Failure of Heron^m membership in J332 is only failure of this "
            "560-generator subideal and does not imply T^m is outside I_mix."
        ),
        "positive_scope_guard": (
            "A positive identity must replay over Q with all generator "
            "outputs and the scale16/scale8 factors above; a modular result "
            "alone is not a proof."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("contrast J332 interface: PASS")
    print("actions/generators/provenance:", math_factorial_8(), len(ASSIGNMENTS),
          256 * len(ASSIGNMENTS))
    print("seed sha256:", result["seed_sha256"])
    print("provenance sha256:", result["provenance_sha256"])
    print("result sha256:", result["result_sha256"])


def math_factorial_8() -> int:
    return 40_320


if __name__ == "__main__":
    main()
