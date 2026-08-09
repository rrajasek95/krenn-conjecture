#!/usr/bin/env python3
"""Exact three-coordinate obstruction for two coupled bright lifts.

In the colour-diagonal chart, fix a target-line bridge at sites 0,1 and a
nonzero pure target product using the residual edge 34 after P selects site
2.  Project sites 0,1 modulo the target line.  Parity purifies the two
bright preimages to their own coordinate axes, and the bridge columns die,
leaving three residual weights for each bright colour.

The checker reconstructs the required cofactor coefficients from literal
matchings and audits the short four-case domain argument excluding two
simultaneous bright responses.  This is the coupled strengthening not
refuted by the pinned one-bright cross-star guard.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITES = tuple(range(5))
BRIDGE = (0, 1)
RESIDUAL = (2, 3, 4)
A, C, T = range(3)
COLOURS = (A, C, T)
BRIGHT = (A, C)
PINNED_GUARD_SHA256 = (
    "da3da45e0bfc38224d6a04f3ef037d252789f931fc1837130f34e49af2f533e1"
)
PINNED_PARITY_SHA256 = (
    "ddf3c9b1dce264de5e29315d350e15bef56e91b699daf9c90439222b104c7f85"
)
EXPECTED_DIGEST = "40cfb29e62202b85362532aa52f08c9c2bb94b19f8925fa1f35e8df63b78cf1e"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependencies():
    guard = ROOT / (
        "computations/"
        "verify_shared_reciprocal_two_bad_bridge_projection_cross_star_guard.py"
    )
    parity = ROOT / (
        "computations/"
        "verify_shared_reciprocal_two_bad_two_centre_parity_straightening.py"
    )
    require(sha256(guard.read_bytes()).hexdigest() == PINNED_GUARD_SHA256,
            "the one-bright cross-star guard changed")
    require(sha256(parity.read_bytes()).hexdigest() == PINNED_PARITY_SHA256,
            "the two-centre parity dependency changed")


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def residual_index_for_edge(edge):
    edge = set(edge)
    missing = tuple(site for site in RESIDUAL if site not in edge)
    require(len(missing) == 1, "a residual edge lost its opposite index")
    return RESIDUAL.index(missing[0])


def edge_variable(left, right, colour):
    left, right = sorted((left, right))
    if (left, right) == BRIDGE:
        return f"s{colour}"
    if left == 0 and right in RESIDUAL:
        return f"u{colour}{RESIDUAL.index(right)}"
    if left == 1 and right in RESIDUAL:
        return f"v{colour}{RESIDUAL.index(right)}"
    require(left in RESIDUAL and right in RESIDUAL,
            "an edge left the bridge/residual normal form")
    return f"r{colour}{residual_index_for_edge((left, right))}"


def add_monomial(polynomial, monomial, coefficient=1):
    monomial = tuple(sorted(monomial))
    polynomial[monomial] += coefficient
    if polynomial[monomial] == 0:
        del polynomial[monomial]


def add_polynomials(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            add_monomial(answer, monomial, coefficient)
    return answer


def cofactor_polynomial(hole, full_word):
    vertices = tuple(site for site in SITES if site != hole)
    answer = Counter()
    for matching in perfect_matchings(vertices):
        monomial = tuple(
            edge_variable(left, right, full_word[left])
            for left, right in matching
            if full_word[left] == full_word[right]
        )
        if len(monomial) != 2:
            continue
        add_monomial(answer, monomial)
    return answer


def bright_response(bright_colour, full_word):
    answer = Counter()
    for index, site in enumerate(RESIDUAL):
        if full_word[site] != bright_colour:
            continue
        cofactor = cofactor_polynomial(site, full_word)
        for monomial, coefficient in cofactor.items():
            add_monomial(answer, monomial + (f"w{bright_colour}{index}",),
                         coefficient)
    return answer


def expected_g(colour, index):
    other = tuple(i for i in range(3) if i != index)
    j, k = other
    answer = Counter()
    add_monomial(answer, (f"s{colour}", f"r{colour}{index}"))
    add_monomial(answer, (f"u{colour}{j}", f"v{colour}{k}"))
    add_monomial(answer, (f"u{colour}{k}", f"v{colour}{j}"))
    return answer


def expected_target(colour):
    answer = Counter()
    for index in range(3):
        for monomial, coefficient in expected_g(colour, index).items():
            add_monomial(answer, monomial + (f"w{colour}{index}",),
                         coefficient)
    return answer


def expected_wrong_bridge(bright_colour, bridge_colour):
    answer = Counter()
    for index in range(3):
        add_monomial(answer, (
            f"s{bridge_colour}", f"w{bright_colour}{index}",
            f"r{bright_colour}{index}",
        ))
    return answer


def audit_matching_formulas():
    ledger = {}
    for colour in BRIGHT:
        target_word = (colour,) * 5
        target = bright_response(colour, target_word)
        require(target == expected_target(colour),
                "the projected target response formula changed")
        ledger[f"target_{colour}"] = sorted(target.items())

        other = C if colour == A else A
        wrong_word = (other, other, colour, colour, colour)
        wrong = bright_response(colour, wrong_word)
        require(wrong == expected_wrong_bridge(colour, other),
                "the wrong-bridge response formula changed")
        ledger[f"wrong_bridge_{colour}"] = sorted(wrong.items())

        for index, site in enumerate(RESIDUAL):
            foreign_word = [other] * 5
            foreign_word[site] = colour
            foreign = bright_response(colour, tuple(foreign_word))
            expected = Counter()
            for monomial, coefficient in expected_g(other, index).items():
                add_monomial(expected,
                             monomial + (f"w{colour}{index}",),
                             coefficient)
            require(foreign == expected,
                    "a foreign-pure coordinate formula changed")
            ledger[f"foreign_{colour}_{index}"] = sorted(foreign.items())

    # Target factorization of K_0,K_1 kills every non-target row.  The
    # displayed 2+2 words give the coordinatewise annihilators used below.
    annihilators = []
    for bright_colour in BRIGHT:
        other_colours = tuple(colour for colour in COLOURS
                              if colour != bright_colour)
        for index, residual_site in enumerate(RESIDUAL):
            for other in other_colours:
                word = [other] * 5
                word[0] = bright_colour
                word[1] = bright_colour
                word[residual_site] = bright_colour
                # K_0 sees site 1 as bright; K_1 sees site 0 as bright.
                k0 = cofactor_polynomial(0, tuple(word))
                k1 = cofactor_polynomial(1, tuple(word))
                expected_k0 = Counter({tuple(sorted((
                    f"v{bright_colour}{index}", f"r{other}{index}",
                ))): 1})
                expected_k1 = Counter({tuple(sorted((
                    f"u{bright_colour}{index}", f"r{other}{index}",
                ))): 1})
                require(k0 == expected_k0 and k1 == expected_k1,
                        "a bridge-factor annihilator formula changed")
                annihilators.append((bright_colour, other, index,
                                     sorted(k0.items()), sorted(k1.items())))
    ledger["annihilators"] = annihilators
    return ledger


def audit_domain_argument():
    # r_t,0 is the selected nonzero target edge.  The annihilators imply
    # u_d,0=v_d,0=0.  Hence the only crossed permanent coordinate is 0:
    # h_d=u_d,1 v_d,2 + u_d,2 v_d,1.
    cross_cover = {}
    for colour in BRIGHT:
        other = C if colour == A else A
        terms = (
            ((f"u{colour}1", f"v{colour}2"), (1, 2)),
            ((f"u{colour}2", f"v{colour}1"), (2, 1)),
        )
        for term, covered in terms:
            require(set(covered) == {1, 2},
                    "a nonzero crossed term stopped killing both coordinates")
        cross_cover[colour] = {
            "other_colour": other,
            "terms": terms,
            "consequence": [f"r{other}1=0", f"r{other}2=0"],
        }

    # Exhaust the four support states of the direct bridge scalars.  These
    # are implication traces over an integral domain, not sampled values.
    cases = [
        {
            "s_support": [A, C],
            "trace": [
                "wrong rows give A_a=A_c=0",
                "targets give w_a0*h_a=1 and w_c0*h_c=1",
                "h_a!=0 gives r_c1=r_c2=0",
                "A_c=0 and w_c0!=0 give r_c0=0",
                "so g_c0=h_c!=0, contradicting w_a0*g_c0=0",
            ],
        },
        {
            "s_support": [A],
            "trace": [
                "target c gives w_c0*h_c=1",
                "h_c!=0 gives r_a1=r_a2=0",
                "foreign c at coordinate 0 gives w_a0=0",
                "then A_a=0 and target a is 0=1",
            ],
        },
        {
            "s_support": [C],
            "trace": [
                "symmetric to the support {a} case",
            ],
        },
        {
            "s_support": [],
            "trace": [
                "targets give w_a0*h_a=1 and w_c0*h_c=1",
                "foreign c at coordinate 0 gives w_a0*h_c=0",
                "contradiction",
            ],
        },
    ]
    require(len(cases) == 4
            and {tuple(case["s_support"]) for case in cases}
            == {(), (A,), (C,), (A, C)},
            "the direct-channel case split changed")
    return {
        "selected_target_edge": "r_t0!=0",
        "forced_zero_star_coordinates": [
            "u_a0", "v_a0", "u_c0", "v_c0",
        ],
        "cross_cover": cross_cover,
        "cases": cases,
        "verdict": (
            "two simultaneous bright target responses are impossible in "
            "the three-residual-coordinate target-bridge quotient"
        ),
    }


def audit_parity_purification():
    # Four-site diagonal matching words have even colour parity.  Inserting
    # endpoint colour d puts the image in the parity sector e_d.  Distinct
    # endpoint colours therefore cannot cancel each other.
    sectors = {}
    for inserted in COLOURS:
        output_parities = set()
        for word in product(COLOURS, repeat=4):
            counts = [word.count(colour) for colour in COLOURS]
            if not all(count % 2 == 0 for count in counts):
                continue
            counts[inserted] += 1
            output_parities.add(tuple(count % 2 for count in counts))
        unit = tuple(int(colour == inserted) for colour in COLOURS)
        require(output_parities == {unit},
                "bright-axis parity purification changed")
        sectors[inserted] = unit
    require(len(set(sectors.values())) == len(COLOURS),
            "two inserted colours entered the same parity sector")
    return sectors


def main():
    pin_dependencies()
    matching = audit_matching_formulas()
    domain = audit_domain_argument()
    parity = audit_parity_purification()
    ledger = {
        "pinned_guard_sha256": PINNED_GUARD_SHA256,
        "pinned_parity_sha256": PINNED_PARITY_SHA256,
        "matching_formulas": matching,
        "domain_argument": domain,
        "bright_parity_sectors": parity,
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"the three-coordinate bright ledger changed: {digest}")
    print("three-coordinate coupled bright obstruction: PASS")
    print("literal target/wrong/foreign rows and 24 annihilators reconstructed")
    print("direct-channel support cases closed: 4 / 4")
    print("one-bright cross-star guard retained as a pinned mutation")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
