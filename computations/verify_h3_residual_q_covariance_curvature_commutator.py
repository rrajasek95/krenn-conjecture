#!/usr/bin/env python3
r"""Identify the residual-q class as a covariance/curvature commutator.

The four relevant decorated matchings are the two endpoint orientations
E_+, E_- paired with the pure tail T_0=24:11|35:11 and the mixed tail
T_1=24:21|35:12.  With coefficients

    alpha=(-1,+1,+1,-1),

the complete fourth symbol has zero scalar top and zero codimension-one
shadow.  Its first nonzero shadow is the codimension-two product

    (E_- - E_+) (T_0 - T_1),

which is exactly the required -delta residual-q class.

The tail change is not a formal relabelling: two literal sitewise covariance
derivations carry the complete direct-free K8 row for the pure word to the
complete row for the mixed word, term by term and within both endpoint-hole
sectors.  Covariance supplies horizontal transport, however, not its
Spencer nullhomotopy.  The pinned standard transport module still obeys
R=D, so the commutator does not construct the missing mapping-cone cell.
It reduces that construction to one mixed covariance-curvature homotopy.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "2ff6aa922fd927096e33cef78bdfb684f26d6372a511eee5d7e1b20c04b14c1e"
PINS = {
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_residual_q_ks_standard_transport_graph_lock.py":
        "eede8aabd5c4740520ed13f1aacc897326a3a02573f860f5b2613c9df91fd53c",
    "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py":
        "b890195a8fc0c4e90c9c9c0c03c41a95690228c81026f4c2ea1fa95908564e38",
    "computations/verify_h3_full_hasse_cone_d4_descent_obstruction.py":
        "ed2f2b3451074500b39a100da91ffefed27f748636de172d81aabd5cfe394240",
}

SITES = tuple(range(8))
P, S = 6, 7
PURE_WORD = (1,) * 8
MIXED_WORD = (1, 1, 2, 1, 1, 2, 1, 1)
ALPHA = (Q(-1), Q(1), Q(1), Q(-1))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def edge(left: int, right: int, left_colour: int, right_colour: int):
    if left < right:
        return left, right, left_colour, right_colour
    return right, left, right_colour, left_colour


E_PLUS = (
    edge(P, 0, 1, 1),
    edge(S, 1, 1, 1),
)
E_MINUS = (
    edge(P, 1, 1, 1),
    edge(S, 0, 1, 1),
)
T_ZERO = (
    edge(2, 4, 1, 1),
    edge(3, 5, 1, 1),
)
T_ONE = (
    edge(2, 4, 2, 1),
    edge(3, 5, 1, 2),
)
CORNERS = tuple(
    tuple(sorted(endpoint + tail))
    for endpoint, tail in (
        (E_PLUS, T_ZERO),
        (E_MINUS, T_ZERO),
        (E_PLUS, T_ONE),
        (E_MINUS, T_ONE),
    )
)


def row_as_counter(base, word):
    return Counter({monomial: Q(1) for monomial in base.full_row(word)})


def recolour_site(polynomial, site: int, old: int, new: int):
    """Literal covariance derivation on a matching row.

    Every matching monomial has one cell incident with ``site``.  Recolouring
    that unique endpoint gives the termwise source-covariance image.
    """
    output = Counter()
    for monomial, coefficient in polynomial.items():
        incident = [position for position, cell in enumerate(monomial)
                    if site in cell[:2]]
        require(len(incident) == 1, ("matching incidence changed", site))
        position = incident[0]
        left, right, left_colour, right_colour = monomial[position]
        if left == site:
            require(left_colour == old, ("unexpected old colour", site))
            changed = (left, right, new, right_colour)
        else:
            require(right == site and right_colour == old,
                    ("unexpected old colour", site))
            changed = (left, right, left_colour, new)
        cells = list(monomial)
        cells[position] = changed
        output[tuple(sorted(cells))] += coefficient
    return +output


def physical_edges(monomial):
    return frozenset((left, right) for left, right, _a, _b in monomial)


def endpoint_sector(polynomial, endpoint_edges):
    endpoint_edges = frozenset(tuple(sorted(pair)) for pair in endpoint_edges)
    return Counter({
        monomial: coefficient
        for monomial, coefficient in polynomial.items()
        if endpoint_edges <= physical_edges(monomial)
    })


def shadow(remaining_size: int):
    answer = Counter()
    for coefficient, corner in zip(ALPHA, CORNERS, strict=True):
        for subset in combinations(corner, remaining_size):
            answer[tuple(sorted(subset))] += coefficient
    return Counter({key: value for key, value in answer.items() if value})


def expected_second_shadow():
    answer = Counter()
    for coefficient, endpoint, tail in (
        (Q(-1), E_PLUS, T_ZERO),
        (Q(1), E_MINUS, T_ZERO),
        (Q(1), E_PLUS, T_ONE),
        (Q(-1), E_MINUS, T_ONE),
    ):
        for endpoint_cell in endpoint:
            for tail_cell in tail:
                answer[tuple(sorted((endpoint_cell, tail_cell)))] += coefficient
    return Counter({key: value for key, value in answer.items() if value})


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "residual_q_commutator_base",
    )
    pure = row_as_counter(base, PURE_WORD)
    mixed = row_as_counter(base, MIXED_WORD)
    require(len(pure) == len(mixed) == 90,
            "direct-free full-nine row size changed")

    transported = recolour_site(pure, 2, 1, 2)
    transported = recolour_site(transported, 5, 1, 2)
    require(transported == mixed,
            "two-site covariance failed on the complete source row")

    plus_edges = ((P, 0), (S, 1))
    minus_edges = ((P, 1), (S, 0))
    pure_plus = endpoint_sector(pure, plus_edges)
    pure_minus = endpoint_sector(pure, minus_edges)
    mixed_plus = endpoint_sector(mixed, plus_edges)
    mixed_minus = endpoint_sector(mixed, minus_edges)
    require(tuple(map(len, (pure_plus, pure_minus, mixed_plus, mixed_minus)))
            == (3, 3, 3, 3),
            "endpoint-hole sector census changed")
    require(recolour_site(recolour_site(pure_plus, 2, 1, 2), 5, 1, 2)
            == mixed_plus,
            "covariance stopped preserving the plus endpoint sector")
    require(recolour_site(recolour_site(pure_minus, 2, 1, 2), 5, 1, 2)
            == mixed_minus,
            "covariance stopped preserving the minus endpoint sector")
    require(CORNERS[0] in pure_plus and CORNERS[1] in pure_minus
            and CORNERS[2] in mixed_plus and CORNERS[3] in mixed_minus,
            "selected covariance-curvature corners left their source rows")

    # The fourth derivative of a decorated matching row is one exactly on
    # its matching monomial.  Check the signed symbol on every one of the
    # 3^8 literal source rows, not only on the two active words.
    active_words = {}
    for word in product(range(3), repeat=8):
        row = set(base.full_row(word))
        hits = tuple(int(corner in row) for corner in CORNERS)
        value = sum(coefficient * hit
                    for coefficient, hit in zip(ALPHA, hits, strict=True))
        require(value == 0, ("signed fourth symbol is not source-tangent",
                             word, hits, value))
        if any(hits):
            active_words["".join(map(str, word))] = list(hits)
    require(active_words == {
        "11111111": [1, 1, 0, 0],
        "11211211": [0, 0, 1, 1],
    }, ("active source words changed", active_words))

    scalar_shadow = sum(ALPHA, Q(0))
    first_shadow = shadow(1)
    second_shadow = shadow(2)
    require(scalar_shadow == 0 and not first_shadow,
            "top or codimension-one cancellation changed")
    require(second_shadow == expected_second_shadow()
            and len(second_shadow) == 16
            and set(second_shadow.values()) == {Q(-1), Q(1)},
            "codimension-two commutator factorization changed")

    graph = load(
        "computations/verify_h3_residual_q_ks_standard_transport_graph_lock.py",
        "residual_q_commutator_graph",
    )
    graph_ledger, graph_digest = graph.audit()
    require(graph_digest == graph.EXPECTED_LEDGER_SHA256,
            "standard graph-lock replay changed")
    require(not graph_ledger["standard_transport_graph_lock"]
            ["required_correction_in_standard_span"],
            "standard graph unexpectedly acquired the commutator filler")

    ledger = {
        "theorem": "residual-q covariance-curvature commutator reduction",
        "source_words": {
            "pure": "11111111",
            "mixed": "11211211",
            "complete_direct_free_terms_each": 90,
            "two_site_covariance": "delta_2(1->2) delta_5(1->2)",
            "termwise_identity": True,
            "endpoint_plus_minus_sector_terms_each": 3,
            "active_fourth_symbol_words": active_words,
        },
        "corner_order": ["E+T0", "E-T0", "E+T1", "E-T1"],
        "alpha": [int(value) for value in ALPHA],
        "fourth_symbol_scalar_top": int(scalar_shadow),
        "codimension_one_shadow_terms": len(first_shadow),
        "first_nonzero_shadow": {
            "codimension": 2,
            "literal_terms": len(second_shadow),
            "factorization": "(E_minus-E_plus)*(T_zero-T_one)",
            "coarse_corner_coefficients": [int(value) for value in ALPHA],
            "identification": "required -delta residual-q class",
        },
        "standard_transport_replay": {
            "law": "R=D",
            "required_commutator_in_span": False,
            "primitive_pairings": [1, -1],
        },
        "construction_target": (
            "one relative Spencer homotopy for the mixed endpoint-curvature/"
            "two-site-covariance commutator, with the already pinned literal "
            "B_j/Eq image and eta/sigma terminal packet"
        ),
        "scope": (
            "the principal source symbol and its first surviving face are "
            "literal; no physical repeated-grade Spencer filler or terminal "
            "comparison is constructed"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("h=3 residual-q covariance/curvature commutator: SHARP REDUCTION")
    print("two-site covariance on complete rows: 90/90 termwise")
    print("signed fourth symbol: top 0; codimension-one 0")
    print("first nonzero face: codimension two = -delta (16 terms)")
    print("standard R=D transport fills it: NO")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
