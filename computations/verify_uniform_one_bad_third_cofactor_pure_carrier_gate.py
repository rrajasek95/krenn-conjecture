#!/usr/bin/env python3
r"""The first genuine third-cofactor recurrence kills the formal tower guard.

The packet of commit 535c0cf retains a genuine common q, all four binary
response rows, and formal first/second cofactors F,G satisfying the top and
first-cofactor Euler recurrences. This checker imposes the next recurrence

    sum_g q_g H_{e,f,g} = (h-2) G_{e,f}

without assuming that H is genuine. On each of the four corrected pairs it
selects a word for which G is nonzero but q has no matching cell on the
remaining sites. The left side is therefore zero for arbitrary H, while
the right side is nonzero for every h >= 3.

The reusable statement is the word-carrier lemma: a nonzero word coefficient
of G in a genuine third recurrence requires at least one disjoint q cell
whose endpoint colours agree with that word. This closes the particular
formal tower guard, not the carrier-rich genuine common-q branch.
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
    "computations/verify_uniform_one_bad_second_cofactor_tower_gate.py":
        "e4a65916d1e41c7486d0f119f7a13043a0b60959fbac538967ff93f601db3f1d",
    "notes/uniform-one-bad-second-cofactor-tower-gate.md":
        "2342cd71485ad5812e3c724d721cb57e31de4030423f4f601c94c35a6874e149",
    "computations/verify_uniform_one_bad_minimal_response_counterguard.py":
        "57d0a980a26f50bc236f2dcf0b468584a801be049e3cc8cc9418ab0e08ed3b04",
}
EXPECTED_LEDGER_SHA256 = (
    "49ce7d73c3212e610ac1cdf83025f4ee0a8d9cad37c61dc8681aa6081f517759"
)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def load_module(relative: str, name: str):
    path = ROOT / relative
    specification = importlib.util.spec_from_file_location(name, path)
    require(specification is not None and specification.loader is not None,
            f"cannot load {relative}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def restrict_word(full_word: tuple[int, ...], removed: frozenset[int]):
    return tuple(colour for site, colour in enumerate(full_word)
                 if site not in removed)


def matching_colours_on_word(
    h: int,
    tower,
    removed: frozenset[int],
    word: tuple[int, ...],
):
    """Return q cells on the complement whose colours agree with word."""
    complement = tuple(site for site in range(2 * h) if site not in removed)
    position = {site: index for index, site in enumerate(complement)}
    carriers = []
    for edge, entries in tower.q_cells(h).items():
        if edge[0] not in position or edge[1] not in position:
            continue
        wanted = (word[position[edge[0]]], word[position[edge[1]]])
        for colours, coefficient in entries:
            if colours == wanted and coefficient:
                carriers.append((edge, colours, coefficient))
    return tuple(carriers)


def build_formal_g_corrections(h: int, tower, minimal):
    sites, desired_response_f, words = minimal.build_formal_cofactors(h)
    require(sites == tuple(range(2 * h)), "site convention changed")
    edges = tower.all_edges(h)
    actual_f = {
        edge: tower.matching_tensor(h, frozenset(edge)) for edge in edges
    }
    formal_f = dict(actual_f)
    for holes, tensor in desired_response_f.items():
        formal_f[tuple(sorted(holes))] = Counter(tensor)

    corrections = {}
    for response_edge, (bridge_edge, bridge_colours) in (
        tower.correction_data().items()
    ):
        delta_f = tower.subtract_tensors(
            formal_f[response_edge], actual_f[response_edge]
        )
        quotient = tower.divide_by_cell(
            h, frozenset(response_edge), bridge_edge,
            bridge_colours, delta_f
        )
        delta_g = tower.scale_tensor(quotient, Fraction(h - 1))
        corrections[(response_edge, bridge_edge)] = delta_g
    return words, corrections


def distinguished_words(h: int):
    x1 = (1,) * (2 * h)
    x2 = (2,) * (2 * h)
    y = list(x1)
    y[2] = 0
    z = list(x2)
    z[0] = 0
    return {
        ((0, 5), (1, 4)): (x1, Fraction(h - 1)),
        ((1, 5), (0, 4)): (tuple(y), Fraction(-(h - 1))),
        ((2, 4), (3, 5)): (x2, Fraction(h - 1)),
        ((3, 4), (2, 5)): (tuple(z), Fraction(-(h - 1))),
    }


def audit_order(h: int, tower, minimal):
    # This reruns the genuine q top, all four response rows, top Euler, and
    # the complete symmetric first-cofactor Euler recurrence.
    lower = tower.audit_order(h, minimal)
    require(lower["responses"] == {
        "11": "X1", "12": "0", "21": "0", "22": "X2"
    }, "the four binary rows changed")

    _words, corrections = build_formal_g_corrections(h, tower, minimal)
    failures = {}
    for pair, (full_word, expected_coefficient) in distinguished_words(h).items():
        response_edge, bridge_edge = pair
        removed = frozenset(response_edge) | frozenset(bridge_edge)
        word = restrict_word(full_word, removed)
        delta_g = corrections[pair]
        require(delta_g[word] == expected_coefficient,
                f"distinguished G coefficient changed at h={h}, pair={pair}")

        # The genuine background G is pure zero on this complement, whereas
        # every distinguished word contains colour 1 or 2.
        actual_g = tower.matching_tensor(h, removed)
        require(actual_g[word] == 0,
                f"genuine background entered the selected word at h={h}")
        formal_coefficient = delta_g[word]

        # Coefficient extraction from the third recurrence is exact:
        # only q cells agreeing with the two endpoint colours of word can
        # contribute. There are none, so the left side vanishes for every H.
        carriers = matching_colours_on_word(h, tower, removed, word)
        require(not carriers,
                f"the sharp no-carrier guard disappeared at h={h}, pair={pair}")
        left_for_arbitrary_h = Fraction(0)
        right = Fraction(h - 2) * formal_coefficient
        require(left_for_arbitrary_h != right and right,
                f"third recurrence no longer contradicts at h={h}, pair={pair}")
        label = (
            f"{response_edge[0]}{response_edge[1]}|"
            f"{bridge_edge[0]}{bridge_edge[1]}"
        )
        failures[label] = {
            "selected_word": "".join(map(str, word)),
            "G_coefficient": str(formal_coefficient),
            "q_word_carriers": 0,
            "third_recurrence_left_for_arbitrary_H": "0",
            "third_recurrence_right": str(right),
        }

    require(len(failures) == 4, "not all four formal corrections were killed")
    return {
        "h": h,
        "q_top": "X0",
        "responses": lower["responses"],
        "top_euler": lower["top_euler"],
        "first_cofactor_euler": lower["first_cofactor_euler"],
        "arbitrary_H_third_recurrence_failures": failures,
    }


def main() -> None:
    pin_dependencies()
    tower = load_module(
        "computations/verify_uniform_one_bad_second_cofactor_tower_gate.py",
        "second_tower",
    )
    minimal = load_module(
        "computations/verify_uniform_one_bad_minimal_response_counterguard.py",
        "minimal_response",
    )
    audits = [audit_order(h, tower, minimal) for h in range(3, 9)]
    ledger = {
        "pins": PINS,
        "uniform_coefficient_identity": (
            "[(sum_g q_g H_efg)]_w = "
            "sum_{g disjoint ef} q_g[w|g] H_efg[w|complement g]"
        ),
        "necessary_carrier": (
            "if (h-2)[G_ef]_w is nonzero, some disjoint q cell must agree "
            "with w on its two endpoints"
        ),
        "representative_exact_audits": audits,
        "verdict": (
            "the 535c0cf formal F,G tower cannot satisfy the first genuine "
            "third-cofactor recurrence even with an arbitrary formal H"
        ),
        "remaining_branch": (
            "a genuine common-q one-bad packet is carrier-rich automatically; "
            "one must combine the colour-0 top matching and the two diagonal "
            "near-perfect colour carriers with both crossed-zero rows to get "
            "square-zero concentration or N-to-N-2 descent"
        ),
        "scope": (
            "uniform carrier obstruction for the sharp formal tower guard; "
            "not a proof that every genuine carrier-rich one-bad packet "
            "concentrates, and not a Krenn counterexample"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"third-cofactor carrier ledger changed: {digest}")

    print("uniform one-bad third-cofactor pure-carrier gate: PASS")
    print("actual q top retained; formal F carries all four binary rows")
    print("top and first-cofactor Euler recurrences: exact")
    print("arbitrary formal H: impossible on all four corrected pairs")
    print("next genuine branch: carrier-rich matching exchange")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
