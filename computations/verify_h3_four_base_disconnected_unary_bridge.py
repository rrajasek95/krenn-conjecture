#!/usr/bin/env python3
"""Close the minimal disconnected four-base packet by three source rows.

On six residual sites take

  A=01|23|45, B=01|24|35, K=02|15|34, L=05|12|34.

The selected diagonal endpoint holes are e=01 and f=34.  At the pure-unary
word, inclusion-exclusion gives

 top - x_e H_e - x_f H_f = sum_(M avoids e,f) x_M - x_(01|25|34).

The diagonal response targets have zero pure-0 coefficient.  Therefore the
minimal four-base support is an ordinary three-row unit.  On arbitrary
support, exactness forces one of eleven additional pure-0 perfect matchings;
nine physically bridge the two C4 components, while two are C6 separators.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_c4_base_exchange_connected_flat_propagation.py":
        "1e1b6ff1ae607b860330a6117f61045640b73f546275c36d4d62daff9ab6e383",
    "notes/c4-base-exchange-connected-flat-propagation.md":
        "9cf4b98c6ca5f9492c854aaf3c726b7eeb48a1294cfa7609a1b521b0df3e2eef",
    "computations/verify_even_cycle_flat_transport_vertex_gauge.py":
        "27b34edca2cd8b0acfc9b899c524c0e27d5edc4fc423a261712d22280ed838d4",
    "notes/even-cycle-flat-transport-vertex-gauge.md":
        "0b5dbaee9a1d4c93778778e833a0baa99741c5091f8f52058858990c65cdde3d",
    "computations/verify_uniform_axis_k3_unequal_tail_reduction.py":
        "ef4c7bc9554fbf6fc5a65aef754d35359c46e0bb67014bd20060114a34cd1843",
    "notes/uniform-axis-k3-unequal-tail-reduction.md":
        "352e02a73da833fb159b24d581e7a91653fe195a76fbe3cc5aa531fd3e141993",
}
EXPECTED_LEDGER_SHA256 = "a6f88257313af83c37a80bfa64cdb63a969c7ca9dbf021be7ba99d4145d0d47a"
SITES = tuple(range(6))
E = (0, 1)
F = (3, 4)
A = ((0, 1), (2, 3), (4, 5))
B = ((0, 1), (2, 4), (3, 5))
K = ((0, 2), (1, 5), (3, 4))
L = ((0, 5), (1, 2), (3, 4))
BASES = (A, B, K, L)
BASE_UNION = set().union(*(set(base) for base in BASES))
ENDPOINT_BLOCK = {
    "p1": (0, 1),
    "s1": (1, 1),
    "p2": (3, 2),
    "s2": (4, 2),
}
LITERAL_ROWS = {
    "top": {"word": (0, 0, 0, 0, 0, 0), "target": 1},
    "G11": {"holes": (0, 1), "word": (1, 1, 0, 0, 0, 0), "target": 0},
    "G12": {"holes": (0, 4), "word": (1, 0, 0, 0, 2, 0), "target": 0},
    "G21": {"holes": (3, 1), "word": (0, 1, 0, 2, 0, 0), "target": 0},
    "G22": {"holes": (3, 4), "word": (0, 0, 0, 2, 2, 0), "target": 0},
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(path):
    return sha256(path.read_bytes()).hexdigest()


def perfect_matchings(vertices):
    if not vertices:
        return [()]
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remaining):
            answer.append(tuple(sorted(((first, second),) + tail)))
    return answer


MATCHINGS = tuple(perfect_matchings(SITES))


class Poly:
    def __init__(self, terms=None):
        self.terms = {
            monomial: coefficient
            for monomial, coefficient in dict(terms or {}).items()
            if coefficient
        }

    @classmethod
    def constant(cls, value):
        return cls({(): value} if value else {})

    @classmethod
    def variable(cls, edge):
        return cls({(edge,): 1})

    def __add__(self, other):
        answer = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            answer[monomial] = answer.get(monomial, 0) + coefficient
            if not answer[monomial]:
                del answer[monomial]
        return Poly(answer)

    def __neg__(self):
        return Poly({monomial: -coefficient
                     for monomial, coefficient in self.terms.items()})

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        answer = Counter()
        for left, left_value in self.terms.items():
            for right, right_value in other.terms.items():
                answer[tuple(sorted(left + right))] += left_value * right_value
        return Poly(answer)

    def __bool__(self):
        return bool(self.terms)

    def restrict_edges(self, allowed):
        return Poly({monomial: coefficient
                     for monomial, coefficient in self.terms.items()
                     if set(monomial) <= allowed})


X = {edge: Poly.variable(edge)
     for edge in ((left, right) for left in SITES for right in SITES
                  if left < right)}


def matching_monomial(matching):
    answer = Poly.constant(1)
    for edge in matching:
        answer = answer * X[edge]
    return answer


def hafnian_after_holes(edge):
    remaining = tuple(site for site in SITES if site not in edge)
    answer = Poly.constant(0)
    for matching in perfect_matchings(remaining):
        answer = answer + matching_monomial(matching)
    return answer


def is_c4(left, right):
    return len(set(left) ^ set(right)) == 4


def audit_source_identity():
    require(LITERAL_ROWS["G11"]["holes"] == E
            and tuple(sorted(LITERAL_ROWS["G22"]["holes"])) == F,
            "the two selected diagonal response holes changed")
    require(tuple(sorted(LITERAL_ROWS["G12"]["holes"])) == (0, 4)
            and tuple(sorted(LITERAL_ROWS["G21"]["holes"])) == (1, 3),
            "the selected crossed response holes changed")
    require(LITERAL_ROWS["top"]["target"] == 1
            and all(LITERAL_ROWS[name]["target"] == 0
                    for name in ("G11", "G12", "G21", "G22")),
            "the literal source target coefficients changed")
    top = Poly.constant(0)
    for matching in MATCHINGS:
        top = top + matching_monomial(matching)
    h_e = hafnian_after_holes(E)
    h_f = hafnian_after_holes(F)
    overlap = ((0, 1), (2, 5), (3, 4))
    avoiding = tuple(matching for matching in MATCHINGS
                     if E not in matching and F not in matching)
    remainder = Poly.constant(0)
    for matching in avoiding:
        remainder = remainder + matching_monomial(matching)
    remainder = remainder - matching_monomial(overlap)
    require(not (top - X[E] * h_e - X[F] * h_f - remainder),
            "the pure-word matching inclusion-exclusion identity changed")

    # Literal normalized source generators at the pure-zero coefficient.
    # The two bright diagonal targets have zero coefficient here.
    g_top = top - Poly.constant(1)
    g_11 = h_e
    g_22 = h_f
    source_combination = g_top - X[E] * g_11 - X[F] * g_22
    require(not (source_combination - (remainder - Poly.constant(1))),
            "the three-row source certificate changed")

    # On the exact four-base physical support every extra monomial vanishes,
    # so q01*g11+q34*g22-g_top=1 is an ordinary integral source identity.
    restricted = source_combination.restrict_edges(BASE_UNION)
    require(restricted.terms == {(): -1},
            f"the minimal four-base packet stopped being a unit: {restricted.terms}")
    return {
        "full_identity": (
            "G_top(0^6)-q01^00*G_11(0^4)-q34^00*G_22(0^4)="
            "sum_avoid q_M^00-q_(01|25|34)^00-1"
        ),
        "minimal_support_certificate":
            "1=q01^00*G_11(0^4)+q34^00*G_22(0^4)-G_top(0^6)",
        "source_rows_used": 3,
        "crossed_rows_needed_for_unit": 0,
        "minimum_selected_endpoint_block": ENDPOINT_BLOCK,
        "literal_full_source_rows": LITERAL_ROWS,
        "avoiding_matchings": len(avoiding),
    }, avoiding, overlap


def audit_forced_topology(avoiding, overlap):
    candidates = (overlap,) + avoiding
    records = []
    counts = Counter()
    for matching in candidates:
        adjacency = tuple(index for index, base in enumerate(BASES)
                          if is_c4(matching, base))
        bridge = bool(set(adjacency) & {0, 1}) and bool(set(adjacency) & {2, 3})
        if bridge:
            kind = "physical_C4_bridge"
        else:
            require(not adjacency,
                    "a nonbridge candidate has a one-component C4 adjacency")
            require(all(len(set(matching) ^ set(base)) == 6 for base in BASES),
                    "the nonbridge candidate stopped being C6 from every base")
            kind = "C6_separator"
        counts[kind] += 1
        cross_holes = tuple(edge for edge in ((0, 4), (1, 3))
                            if edge in matching)
        records.append({
            "matching": matching,
            "kind": kind,
            "C4_adjacent_base_indices": adjacency,
            "selected_cross_hole_edges": cross_holes,
        })
    require(counts == Counter({"physical_C4_bridge": 9,
                               "C6_separator": 2}),
            f"the forced topology split changed: {counts}")
    separators = [record for record in records
                  if record["kind"] == "C6_separator"]
    require({record["matching"] for record in separators} == {
        ((0, 3), (1, 4), (2, 5)),
        ((0, 4), (1, 3), (2, 5)),
    }, "the two C6 separators changed")
    require(Counter(len(record["selected_cross_hole_edges"])
                    for record in separators) == Counter({0: 1, 2: 1}),
            "the crossed-row visibility of the C6 pair changed")
    return {
        "candidate_count": len(candidates),
        "type_counts": dict(sorted(counts.items())),
        "records": records,
        "sharp_residual": (
            "one C6 separator 03|14|25 is silent at both selected crossed "
            "hole edges; the other 04|13|25 enters both crossed companions"
        ),
    }


def audit_base_graph():
    induced = tuple(matching for matching in MATCHINGS
                    if set(matching) <= BASE_UNION)
    require(set(induced) == set(BASES) and len(induced) == 4,
            "the minimal physical support acquired another matching")
    graph_edges = tuple((left, right)
                        for left in range(4) for right in range(left + 1, 4)
                        if is_c4(BASES[left], BASES[right]))
    require(graph_edges == ((0, 1), (2, 3)),
            "the disconnected typed-C4 graph changed")
    return {
        "bases": BASES,
        "physical_edge_count": len(BASE_UNION),
        "supported_perfect_matchings": len(induced),
        "C4_graph_edges": graph_edges,
        "selected_diagonal_holes": (E, F),
        "selected_crossed_holes": ((0, 4), (1, 3)),
    }


def main():
    for relative, expected in PINS.items():
        actual = file_sha256(ROOT / relative)
        require(actual == expected,
                f"dependency changed: {relative}: {actual} != {expected}")
    source, avoiding, overlap = audit_source_identity()
    ledger = {
        "minimal_disconnected_graph": audit_base_graph(),
        "literal_source_identity": source,
        "forced_extension_topology": audit_forced_topology(avoiding, overlap),
        "theorem": (
            "the minimal four-base support is source-empty; every full "
            "source extension has a nonzero pure-zero matching monomial "
            "which is either a physical C4 bridge between both components "
            "or one of two explicit C6 separators"
        ),
        "scope": (
            "physical C4 adjacency is not yet a certified typed carrier; "
            "the complete companion word must synchronize decorations. "
            "The unit is full-source and uses unary plus the two diagonal "
            "rows; the topology promotion is the sharp next typing gate"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"four-base unary bridge ledger changed: {digest}")
    print("h3 four-base disconnected unary bridge: PASS")
    print("minimal support unit; extensions force 9 C4 bridges or 2 C6 separators")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
