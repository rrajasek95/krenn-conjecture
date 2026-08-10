#!/usr/bin/env python3
r"""Uniform common-q Euler/Hessian gate for the one-bad response circuit.

The 9b26452 formal response counterguard cannot have F_e=q^[h-1]_{\bar e}
and q^[h]=X0: its pure-zero top Euler row is 0=h.  This checker then builds
the sharp next guard.  It adjoins the genuine cofactors of a unary perfect-
matching q, so q^[h]=X0 and the complete top Euler identity hold, while the
same six-port response circuit and its nonzero p-row squares survive.

The augmented family is still not a common-q family.  It first fails the
cofactor Euler / Hessian recurrence

    (h-1) F_e = sum_{f disjoint e} q_f G_{e,f},
    G_{e,f}=q^[h-2]_{\overline{e union f}},

at each of the four response holes.  Thus a uniform concentration argument
must use the common-q two-jet, not only response minimality and top Euler.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_one_bad_minimal_response_counterguard.py":
        "57d0a980a26f50bc236f2dcf0b468584a801be049e3cc8cc9418ab0e08ed3b04",
    "notes/uniform-one-bad-minimal-response-counterguard.md":
        "b053f949eef97957c1d53f0c4d4bf1287ca5773a60fd09cbd04fd04c70887dd2",
    "computations/verify_uniform_one_bad_square_zero_clean_cap.py":
        "a943fffdc3ce86aa5506e6774ec3a6a8ff10c70491225417152a1298e2754883",
    "notes/uniform-one-bad-square-zero-clean-cap.md":
        "2af5f90040152079c094e03b0b1bb794761a07d2418182586ab06848ee820c2e",
}
EXPECTED_LEDGER_SHA256 = (
    "3592844ff7566d5131713f5c5acb35a45969d7eed5adc07d1c4f5d3f30e68454"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def load_minimal_response_checker():
    path = ROOT / "computations/verify_uniform_one_bad_minimal_response_counterguard.py"
    specification = importlib.util.spec_from_file_location("minimal_response", path)
    require(specification is not None and specification.loader is not None,
            "cannot load the minimal-response checker")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def unary_matching(h: int) -> tuple[tuple[int, int], ...]:
    require(h >= 3, "the uniform cap starts at h=3")
    # The first three edges avoid every p_i--s_j response hole in 9b26452.
    pairs = [(0, 1), (2, 3), (4, 5)]
    pairs.extend((site, site + 1) for site in range(6, 2 * h, 2))
    require(len(pairs) == h, pairs)
    return tuple(pairs)


def q_power_tensor(h: int, removed: frozenset[int]) -> Counter:
    """Return the divided matching power of the unary matching q.

    The exponent is determined by the complement size.  Every q edge has
    coefficient one and endpoint colours 00, so at most one matching lives.
    """
    sites = tuple(site for site in range(2 * h) if site not in removed)
    exponent = len(sites) // 2
    # With q supported on one perfect matching, a complement power is
    # nonzero exactly when the removed set is a union of complete q edges.
    union_of_edges = all(
        (left in removed) == (right in removed)
        for left, right in unary_matching(h)
    )
    tensor = (Counter({(0,) * len(sites): Fraction(1)})
              if union_of_edges else Counter())
    require(exponent == h - len(removed) // 2, "power degree changed")
    return tensor


def add_tensors(left: Counter, right: Counter) -> Counter:
    answer = Counter(left)
    answer.update(right)
    return Counter({word: coefficient for word, coefficient in answer.items()
                    if coefficient})


def glue_edge(h: int, edge: tuple[int, int], edge_colours: tuple[int, int],
              cofactor: Counter) -> Counter:
    sites = tuple(range(2 * h))
    holes = frozenset(edge)
    complement = tuple(site for site in sites if site not in holes)
    output = Counter()
    for word, coefficient in cofactor.items():
        full = [-1] * len(sites)
        full[edge[0]], full[edge[1]] = edge_colours
        for site, colour in zip(complement, word, strict=True):
            full[site] = colour
        output[tuple(full)] += coefficient
    return Counter({word: coefficient for word, coefficient in output.items()
                    if coefficient})


def actual_first_cofactors(h: int) -> dict[frozenset[int], Counter]:
    return {
        frozenset(edge): q_power_tensor(h, frozenset(edge))
        for edge in all_edges(h)
    }


def all_edges(h: int) -> tuple[tuple[int, int], ...]:
    return tuple((left, right) for left in range(2 * h)
                 for right in range(left + 1, 2 * h))


def audit_order(h: int, minimal) -> dict[str, object]:
    sites, response_extras, words = minimal.build_formal_cofactors(h)
    matching = unary_matching(h)
    actual = actual_first_cofactors(h)

    # The original formal circuit is killed immediately by genuine top
    # provenance: every one of its pure-zero F entries is zero.
    original_pure_zero = {
        holes: tensor.get((0,) * (2 * h - 2), Fraction(0))
        for holes, tensor in response_extras.items()
    }
    require(not any(original_pure_zero.values()),
            "the original response guard no longer has Euler row 0=h")

    # Augment it by every genuine first cofactor of q.  The extra response
    # holes are disjoint from the h matching edges, so the two parts do not
    # collide and the formal response circuit is unchanged.
    augmented = {holes: Counter(tensor) for holes, tensor in actual.items()
                 if tensor}
    for holes, tensor in response_extras.items():
        augmented[holes] = add_tensors(augmented.get(holes, Counter()), tensor)
    response_holes = frozenset(response_extras)
    matching_holes = frozenset(frozenset(edge) for edge in matching)
    require(response_holes.isdisjoint(matching_holes),
            "a response hole collided with the unary matching")

    p1 = ((0, 1, 1), (1, 1, 1))
    s1 = ((5, 1, 1),)
    p2 = ((2, 2, 1), (3, 2, 1))
    s2 = ((4, 2, 1),)
    rows = {
        "11": minimal.response(sites, augmented, p1, s1),
        "12": minimal.response(sites, augmented, p1, s2),
        "21": minimal.response(sites, augmented, p2, s1),
        "22": minimal.response(sites, augmented, p2, s2),
    }
    require(rows == {
        "11": Counter({words["X1"]: Fraction(1)}),
        "12": Counter(),
        "21": Counter(),
        "22": Counter({words["X2"]: Fraction(1)}),
    }, f"the Euler-complete response rows changed at h={h}")

    # Genuine unary top and coefficientwise top Euler identity.
    top = q_power_tensor(h, frozenset())
    require(top == Counter({(0,) * (2 * h): Fraction(1)}),
            f"q^[h] stopped being X0 at h={h}")
    top_euler = Counter()
    q_edges = {frozenset(edge) for edge in matching}
    for edge in all_edges(h):
        holes = frozenset(edge)
        if holes not in q_edges:
            continue
        top_euler.update(glue_edge(h, edge, (0, 0),
                                   augmented.get(holes, Counter())))
    require(top_euler == Counter({(0,) * (2 * h): Fraction(h)}),
            f"the complete top Euler identity failed at h={h}")

    # First-cofactor Euler/Hessian recurrence.  For each response hole e,
    # use the *actual* second cofactors of the same q.  The left side is zero
    # while the displayed formal F_e is nonzero.  This is the first common-q
    # integrability obstruction after the top Euler row has been repaired.
    failures = {}
    for holes in sorted(response_extras, key=lambda item: tuple(sorted(item))):
        edge = tuple(sorted(holes))
        recurrence_left = Counter()
        for second_edge in all_edges(h):
            second_holes = frozenset(second_edge)
            if holes & second_holes or second_holes not in q_edges:
                continue
            second_cofactor = q_power_tensor(h, holes | second_holes)
            # q_second_edge=1.  The second cofactor already lives on the
            # complement of e and f; insert f back into the complement of e.
            complement_e = tuple(site for site in sites if site not in holes)
            positions = {site: index for index, site in enumerate(complement_e)}
            local_edge = (positions[second_edge[0]], positions[second_edge[1]])
            local_h = h - 1
            local_output = Counter()
            local_sites = tuple(range(2 * local_h))
            local_complement = tuple(site for site in local_sites
                                     if site not in local_edge)
            for word, coefficient in second_cofactor.items():
                full = [-1] * (2 * local_h)
                full[local_edge[0]] = 0
                full[local_edge[1]] = 0
                for site, colour in zip(local_complement, word, strict=True):
                    full[site] = colour
                local_output[tuple(full)] += coefficient
            recurrence_left.update(local_output)
        recurrence_right = Counter({
            word: Fraction(h - 1) * coefficient
            for word, coefficient in augmented[holes].items()
        })
        require(not recurrence_left and recurrence_right,
                f"the first-cofactor obstruction vanished at h={h}, e={edge}")
        failures["".join(map(str, edge))] = {
            "left_terms": len(recurrence_left),
            "right_terms": len(recurrence_right),
        }

    return {
        "h": h,
        "unary_matching": [list(edge) for edge in matching],
        "q_top": "X0",
        "top_euler": f"{h}*X0",
        "responses": {"11": "X1", "12": "0", "21": "0", "22": "X2"},
        "nonzero_self_squares": ["p1^[2]", "p2^[2]"],
        "first_cofactor_euler_failures": failures,
    }


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def main() -> None:
    pin_dependencies()
    minimal = load_minimal_response_checker()
    audits = [audit_order(h, minimal) for h in range(3, 9)]
    ledger = {
        "pins": PINS,
        "uniform_orders": "every h>=3; representative audits h=3..8",
        "original_guard_with_common_q": (
            "impossible already at top Euler: every pure-zero F_e is zero, "
            "so sum q_e F_e=0 cannot equal h*q^[h]=h*X0"
        ),
        "sharp_augmented_guard": (
            "q is the unary matching 01|23|45|67|...; adjoin its genuine "
            "first cofactors to the six-port formal response circuit"
        ),
        "properties": audits,
        "verdict": (
            "q^[h]=X0, all four responses, response minimality, non-square "
            "p rows, and the complete top Euler identity coexist formally"
        ),
        "first_failure": (
            "the common-q first-cofactor Euler/Hessian recurrence fails at "
            "holes 05,15,24,34"
        ),
        "next_identity": (
            "a concentration proof must use (h-1)F_e=sum_f q_f G_ef with "
            "one symmetric common second-cofactor family G_ef, then couple "
            "that identity to the four response rows"
        ),
        "scope": (
            "uniform formal top-compatible counterguard, not a common-q "
            "source, not a one-bad packet, and not a Krenn counterexample"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"common-q Euler/Hessian ledger changed: {digest}")

    print("uniform one-bad common-q Euler/Hessian gate: PASS")
    print("original 9b26452 guard + genuine common q: impossible (0=h Euler row)")
    print("sharp augmented guard: genuine q^[h]=X0 and full top Euler")
    print("four binary responses: exact; non-square rows: p1,p2")
    print("first failure: cofactor Euler/Hessian recurrence at 05,15,24,34")
    print("next necessary input: common symmetric second-cofactor family")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
