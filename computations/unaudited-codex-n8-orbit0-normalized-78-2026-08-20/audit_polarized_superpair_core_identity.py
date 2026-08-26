#!/usr/bin/env python3
"""Exact polarized four-superpair identity after normalizing M0 anchors.

For one colour, six arbitrary oriented 2x2 blocks M_ij connect the four
supervertices.  This script derives the permanent/triangle/four-site
invariants from literal perfect matchings and proves a compact identity for
the pure eight-site Hafnian.  It also records the literal mixed-edge tails
of the source rows that supply all terms except the self-polarized breaker.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_polarized_superpair_core_identity.json"
M0 = ((0, 1), (2, 3), (4, 5), (6, 7))
SUPER_EDGES = tuple(combinations(range(4), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(SUPER_EDGES)}
COMPLEMENTARY_EDGE_PAIRS = (((0, 1), (2, 3)),
                            ((0, 2), (1, 3)),
                            ((0, 3), (1, 2)))
ORIENTATIONS = tuple(bits for bits in product((0, 1), repeat=4)
                     if bits[0] == 0)
WORDS = {
    "pair_e_01": tuple(map(int, "00001122")),
    "triple_t_012": tuple(map(int, "00000011")),
    "breaker_s_0000": tuple(map(int, "01010101")),
    "breaker_s_0110": tuple(map(int, "01101001")),
}


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        result.extend(((first, second),) + tail
                      for tail in perfect_matchings(rest))
    return tuple(result)


PM8 = perfect_matchings(tuple(range(8)))
Monomial = tuple[int, ...]
Poly = Counter[Monomial]
ONE: Poly = Counter({(): 1})


def clean(poly: Poly) -> Poly:
    return Counter({monomial: coefficient
                    for monomial, coefficient in poly.items() if coefficient})


def add(*polys: Poly) -> Poly:
    result: Poly = Counter()
    for poly in polys:
        result.update(poly)
    return clean(result)


def scale(poly: Poly, scalar: int) -> Poly:
    return clean(Counter({monomial: scalar * coefficient
                          for monomial, coefficient in poly.items()}))


def multiply(*polys: Poly) -> Poly:
    result = ONE
    for poly in polys:
        updated: Poly = Counter()
        for left, left_coefficient in result.items():
            for right, right_coefficient in poly.items():
                updated[tuple(sorted(left + right))] += (
                    left_coefficient * right_coefficient
                )
        result = clean(updated)
    return result


def variable(i: int, j: int, left_clone: int, right_clone: int) -> Poly:
    require(i < j, "block variables require increasing supervertices")
    index = 4 * EDGE_INDEX[(i, j)] + 2 * left_clone + right_clone
    return Counter({(index,): 1})


def entry(i: int, j: int, clone_i: int, clone_j: int) -> Poly:
    if i < j:
        return variable(i, j, clone_i, clone_j)
    return variable(j, i, clone_j, clone_i)


def permanent(i: int, j: int) -> Poly:
    return add(multiply(entry(i, j, 0, 0), entry(i, j, 1, 1)),
               multiply(entry(i, j, 0, 1), entry(i, j, 1, 0)))


def determinant(i: int, j: int) -> Poly:
    return add(multiply(entry(i, j, 0, 0), entry(i, j, 1, 1)),
               scale(multiply(entry(i, j, 0, 1), entry(i, j, 1, 0)), -1))


def e_pair(i: int, j: int) -> Poly:
    return add(ONE, permanent(i, j))


def triangle(i: int, j: int, k: int) -> Poly:
    result: Poly = Counter()
    for clone_i, clone_j, clone_k in product((0, 1), repeat=3):
        result = add(result, multiply(
            entry(i, j, clone_i, clone_j),
            entry(i, k, 1 - clone_i, clone_k),
            entry(j, k, 1 - clone_j, 1 - clone_k),
        ))
    return result


def t_triple(i: int, j: int, k: int) -> Poly:
    return add(ONE, permanent(i, j), permanent(i, k), permanent(j, k),
               triangle(i, j, k))


def q_orientation(bits: tuple[int, int, int, int]) -> Poly:
    return add(*(multiply(entry(i, j, bits[i], bits[j]),
                           entry(k, l, bits[k], bits[l]))
                 for (i, j), (k, l) in COMPLEMENTARY_EDGE_PAIRS))


def complement(bits):
    return tuple(1 - bit for bit in bits)


def b_self(bits) -> Poly:
    return multiply(q_orientation(bits), q_orientation(complement(bits)))


def pure_hafnian() -> Poly:
    result: Poly = Counter()
    for matching in PM8:
        term = ONE
        for u, v in matching:
            super_u, clone_u = divmod(u, 2)
            super_v, clone_v = divmod(v, 2)
            if super_u == super_v:
                # The four selected same-colour M0 anchors are normalized 1.
                continue
            term = multiply(term, entry(super_u, super_v, clone_u, clone_v))
        result = add(result, term)
    return result


def no_internal_sector() -> Poly:
    result: Poly = Counter()
    for matching in PM8:
        if any(u // 2 == v // 2 for u, v in matching):
            continue
        term = ONE
        for u, v in matching:
            term = multiply(term, entry(u // 2, v // 2, u % 2, v % 2))
        result = add(result, term)
    return result


def clone_specialize(poly: Poly) -> Counter[tuple[int, int, int, int]]:
    """Identify all six blocks with [[a,b],[c,d]]."""
    result = Counter()
    for monomial, coefficient in poly.items():
        exponent = [0, 0, 0, 0]
        for index in monomial:
            exponent[index % 4] += 1
        result[tuple(exponent)] += coefficient
    return clean(result)


def tail_record(word):
    records = []
    histogram = Counter()
    for index, matching in enumerate(PM8):
        mixed = tuple((u, v) for u, v in matching if word[u] != word[v])
        histogram[len(mixed)] += 1
        if mixed:
            records.append({
                "matching_index": index,
                "matching": [list(edge) for edge in matching],
                "mixed_edges": [list(edge) for edge in mixed],
            })
    return histogram, records


def serialize(poly: Poly):
    return [{"variables": list(monomial), "coefficient": coefficient}
            for monomial, coefficient in sorted(poly.items())]


def main() -> None:
    require(len(PM8) == 105 and len(SUPER_EDGES) == 6
            and len(ORIENTATIONS) == 8, "base census changed")
    z = pure_hafnian()
    d_sector = no_internal_sector()
    sum_t = add(*(t_triple(*triple)
                  for triple in combinations(range(4), 3)))
    sum_b = add(*(b_self(bits) for bits in ORIENTATIONS))
    paired_permanents = add(*(multiply(permanent(*left), permanent(*right))
                              for left, right in COMPLEMENTARY_EDGE_PAIRS))
    sum_e_products = add(*(multiply(e_pair(*left), e_pair(*right))
                           for left, right in COMPLEMENTARY_EDGE_PAIRS))

    # First identity counts each four-cycle once and each doubled-edge
    # supergraph twice.  The second is the resulting pure Hafnian formula.
    require(sum_b == add(d_sector, paired_permanents),
            "orientation-square census identity failed")
    rhs = add(sum_t, sum_b, scale(sum_e_products, -1))
    require(z == rhs, "polarized pure-Hafnian identity failed")

    # det/permanent split of the two complementary entry products.
    for i, j in SUPER_EDGES:
        diagonal = multiply(entry(i, j, 0, 0), entry(i, j, 1, 1))
        antidiagonal = multiply(entry(i, j, 0, 1), entry(i, j, 1, 0))
        require(scale(diagonal, 2) == add(permanent(i, j), determinant(i, j)),
                "diagonal permanent/determinant split failed")
        require(scale(antidiagonal, 2) == add(permanent(i, j),
                                               scale(determinant(i, j), -1)),
                "antidiagonal permanent/determinant split failed")

    # Exact recovery of the earlier cloned three-row polynomials.
    cloned_e = clone_specialize(e_pair(0, 1))
    cloned_b0 = clone_specialize(b_self((0, 0, 0, 0)))
    cloned_b1 = clone_specialize(b_self((0, 1, 1, 0)))
    require(cloned_e == Counter({(0, 0, 0, 0): 1, (1, 0, 0, 1): 1,
                                  (0, 1, 1, 0): 1}),
            "cloned E specialization changed")
    require(cloned_b0 == Counter({(2, 0, 0, 2): 9}),
            "cloned 9(ad)^2 specialization changed")
    require(cloned_b1 == Counter({(2, 0, 0, 2): 1,
                                  (1, 1, 1, 1): 4,
                                  (0, 2, 2, 0): 4}),
            "cloned (ad+2bc)^2 specialization changed")

    tails = {}
    for name, word in WORDS.items():
        histogram, records = tail_record(word)
        expected_core = 3 if name == "pair_e_01" else (15 if name.startswith("triple") else 9)
        require(histogram[0] == expected_core,
                f"literal core term count changed for {name}")
        tails[name] = {
            "word": "".join(map(str, word)),
            "mixed_edge_count_histogram": dict(sorted(histogram.items())),
            "tail_matching_provenance": records,
        }

    # Mutation controls must disturb both exact identities.
    first_variable = variable(0, 1, 0, 0)
    require(add(sum_b, first_variable) != add(d_sector, paired_permanents),
            "orientation mutation did not fire")
    require(add(rhs, first_variable) != z,
            "pure-identity mutation did not fire")

    provenance_digest = sha256(json.dumps(tails, sort_keys=True,
                                            separators=(",", ":")).encode("ascii")).hexdigest()
    result = {
        "status": "UNAUDITED exact normalized polarized-superpair identity",
        "normalization": "the four selected same-colour M0 anchors equal 1",
        "variables": "six arbitrary oriented 2x2 blocks M_ij (24 entries)",
        "block_invariants": {
            "P_ij": "perm(M_ij)",
            "Delta_ij": "det(M_ij)",
            "diagonal_product": "(P_ij+Delta_ij)/2",
            "antidiagonal_product": "(P_ij-Delta_ij)/2",
            "e_ij": "1+P_ij",
            "C_ijk": "eight-term complementary-endpoint triangle contraction",
            "t_ijk": "1+P_ij+P_ik+P_jk+C_ijk",
            "Q_s": "Hafnian of the four endpoints selected by s",
            "b_s": "Q_s(M) Q_complement(s)(M)",
        },
        "orientation_representatives": ["".join(map(str, bits))
                                         for bits in ORIENTATIONS],
        "identity_1": (
            "sum_[s modulo complement] b_s = D + "
            "P01*P23+P02*P13+P03*P12"
        ),
        "identity_2": (
            "Z = sum_{|S|=3} t_S + sum_[s modulo complement] b_s "
            "- (e01*e23+e02*e13+e03*e12)"
        ),
        "polynomial_census": {
            "Z_terms_after_collection": len(z),
            "D_terms_after_collection": len(d_sector),
            "sum_b_terms_after_collection": len(sum_b),
            "total_perfect_matchings": len(PM8),
        },
        "cloned_specializations": {
            "e_01": "1+ad+bc",
            "b_0000": "9(ad)^2",
            "b_0110": "(ad+2bc)^2",
        },
        "source_residual_formula": (
            "Writing each literal mixed row as H_e=e+tau_e and "
            "H_t=t+tau_t, on V(I_mix) identity_2 gives "
            "Z=-sum tau_t + sum b_self - sum tau_e*tau_e_complement. "
            "The tail provenance below is literal."
        ),
        "cross_colour_polarization": (
            "A literal 4+4 breaker with colour c on orientation s and d on "
            "its complement has core Q_s(M^c)Q_complement(s)(M^d), not "
            "b_s(M^c). Recovering the eight self terms from these cross "
            "terms and their tails is the missing source-global lemma."
        ),
        "tail_provenance_sha256": provenance_digest,
        "tails": tails,
        "scope": (
            "This is a polynomial identity in 24 independent block entries "
            "and an exact source-tail decomposition. It is not yet a unit "
            "certificate for the full normalized ideal."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("polarized superpair core identity: PASS")
    print("Z/D/sum_b terms:", len(z), len(d_sector), len(sum_b))
    print("tail histograms:", {name: row["mixed_edge_count_histogram"]
                                for name, row in tails.items()})
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
