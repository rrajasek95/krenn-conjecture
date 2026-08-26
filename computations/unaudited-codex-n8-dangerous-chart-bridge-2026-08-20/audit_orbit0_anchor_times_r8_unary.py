#!/usr/bin/env python3
"""Exact three-packet reduction of the K8 part of a_0*T.

This checker deliberately proves only the associated-graded K8 statement.
The cutoff-nine certificate for T can have a K9 tail; that tail must be
expanded separately before claiming a representative of the full a_0*T.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
FACT_PATH = HERE / "audit_orbit0_sparse_r8_factorization.py"
SPEC = importlib.util.spec_from_file_location("r8_factor", FACT_PATH)
FACT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FACT)
T2 = FACT.T2
INPUT = HERE / "results_orbit0_cutoff9_sparse_r8.json"
OUT = HERE / "results_orbit0_anchor_times_r8_unary.json"

WORDS = (
    (1, 1, 1, 1, 2, 2, 2, 2),
    (2, 2, 2, 2, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, 1, 1, 1),
)


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def subtract_multiset(row: bytes, divisor: bytes) -> bytes:
    residual = list(row)
    for cell in divisor:
        residual.remove(cell)
    return bytes(sorted(residual))


def add_anchor(row: bytes, anchor: bytes) -> bytes:
    return bytes(sorted(row + anchor))


def labelled_r8() -> Counter:
    raw = json.loads(INPUT.read_text())
    actual = Counter()
    for row_hex, numerator, denominator in raw["residual"]:
        representative = bytes.fromhex(row_hex)
        orbit = T2.row_orbit(representative)
        coefficient = Fraction(numerator, denominator) / len(orbit)
        require(coefficient.denominator == 1,
                "R8' labelled coefficient is nonintegral")
        for row in orbit:
            require(row not in actual, "R8' quotient orbits overlap")
            actual[row] = coefficient
    require(len(actual) == 148_176, "R8' labelled support changed")
    return actual


def main() -> None:
    raw = json.loads(INPUT.read_text())
    r8 = labelled_r8()
    pure = {
        colour: bytes(sorted(T2.BASE.CELL_ID[(u, v, colour, colour)]
                             for u, v in T2.M0))
        for colour in T2.BASE.COLORS
    }
    anchor_product = bytes(sorted(b"".join(pure.values())))
    require(anchor_product == bytes(sorted(T2.ANCHORS)),
            "orbit-0 anchor product changed")

    factors = {colour: Counter() for colour in T2.BASE.COLORS}
    target = Counter()
    for row, coefficient in r8.items():
        anchors = bytes(cell for cell in row if cell in T2.ANCHORS)
        colours = {T2.BASE.CELLS[cell][2] for cell in anchors}
        require(len(colours) == 1, "R8' row has ambiguous pure factor")
        colour = next(iter(colours))
        require(anchors == pure[colour], "R8' pure factor changed")
        factor = subtract_multiset(row, anchors)
        factors[colour][factor] = coefficient
        target[add_anchor(row, anchor_product)] = coefficient

    leading_replay = Counter()
    packets = []
    raw_tail_histogram = Counter()
    for colour, word in enumerate(WORDS):
        terms = T2.BASE.word_terms(word)
        degree_histogram = Counter(T2.row_k_degree(term) for term in terms)
        require(degree_histogram == {0: 1, 2: 12, 3: 32, 4: 60},
                "pair-constant matching K histogram changed")
        leading_terms = tuple(term for term in terms
                              if T2.row_k_degree(term) == 0)
        require(len(leading_terms) == 1, "K0 source term is not unique")
        q = leading_terms[0]
        anchor_numerator = bytes(sorted(anchor_product + pure[colour]))
        anchor_cofactor = subtract_multiset(anchor_numerator, q)
        require(len(anchor_cofactor) == 12,
                "source anchor cofactor has wrong degree")

        for factor, coefficient in factors[colour].items():
            multiplier = bytes(sorted(anchor_cofactor + factor))
            desired = bytes(sorted(q + multiplier))
            leading_replay[desired] += coefficient
        for term in terms:
            if term == q:
                continue
            # Every P_c monomial has K degree eight.
            raw_tail_histogram[8 + T2.row_k_degree(term)] += len(factors[colour])

        packets.append({
            "colour": colour,
            "word": "".join(map(str, word)),
            "leading_M0_term": q.hex(),
            "anchor_cofactor": anchor_cofactor.hex(),
            "P_support": len(factors[colour]),
            "H_term_K_histogram": {str(k): v
                                    for k, v in sorted(degree_histogram.items())},
            "factored_source": (
                "H_" + "".join(map(str, word))
                + " * anchor_cofactor * P_" + str(colour)
            ),
        })

    require(leading_replay == target,
            "three source packets do not replay a*R8' at K8")
    require(raw_tail_histogram == {10: 1_778_112,
                                   11: 4_741_632,
                                   12: 8_890_560},
            "factored tail raw census changed")

    # A coefficient mutation must destroy the literal K8 replay.
    mutated = leading_replay.copy()
    first = min(mutated)
    mutated[first] += 1
    require(mutated != target, "mutation control failed")

    result = {
        "status": "UNAUDITED exact orbit0 a*R8' K8 unary reduction",
        "input_sha256": sha256(INPUT.read_bytes()).hexdigest(),
        "input_logical_sha256": raw["result_sha256"],
        "anchor_product": anchor_product.hex(),
        "anchor_K_degree": T2.row_k_degree(anchor_product),
        "target_total_degree": 24,
        "target_K_degree": 8,
        "target_labelled_support": len(target),
        "source_packets": packets,
        "exact_labelled_K8_replay": True,
        "coefficient_mutation_fires": True,
        "nonleading_H_K_histogram_per_packet": {"2": 12, "3": 32, "4": 60},
        "factored_tail_raw_contribution_histogram": {
            str(k): v for k, v in sorted(raw_tail_histogram.items())
        },
        "identity": (
            "a*R8' - sum_c H_{w_c}*(a*m_c/q_c)*P_c = "
            "-sum_c (H_{w_c}-q_c)*(a*m_c/q_c)*P_c, in K^10"
        ),
        "conclusion": (
            "The K8 initial form of a*R8' is in gr_K(I_mix), and the chosen "
            "three-packet correction has no K9 output."
        ),
        "scope_guard": (
            "This does not yet put the full a*T in I_mix+K^10. The exact "
            "cutoff-nine representative T=R8' mod (I_mix+K^9) can have a "
            "K9 tail; a separate full-column expansion must add a times that "
            "tail to obtain the true next residual."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("orbit0 a*R8' unary K8 reduction: PASS")
    print("target labelled support:", len(target))
    print("packets:", len(packets))
    print("raw tail histogram:", dict(sorted(raw_tail_histogram.items())))
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
