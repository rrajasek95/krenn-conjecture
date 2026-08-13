#!/usr/bin/env python3
"""Classify mixed versus pure target fibres of the switch packets.

For each literal C4, C2+, and P2 lower packet, all three terms carry one
common output word.  The word may be mixed or monochromatic; global site and
colour covariance preserves that distinction, so a fixed nonzero pure packet
cannot simply be relabelled to a mixed one.

With target value tau_w (zero for mixed, one for normalized pure), put

    H=F+C1+C2=tau_w,
    t1=C1-F, t2=C2-F.

The determinant-three coordinate change gives

    t1=t2=0  <=>  F=C1=C2=tau_w/3.

Thus switch-dark mixed packets vanish.  Switch-dark pure packets do not:
they are the unique affine flat vector (1/3,1/3,1/3).  Explicit decorated
physical monomials realize both a mixed bright packet and a pure dark packet
for every topology.  Therefore mixed-word brightness is unconditional only
after the lower packet is a literal same-grade GHZ coefficient; it cannot be
chosen by recolouring.

On all words/heads, darkness removes every centered switch carrier.  The
pure affine survivor is the invariant augmentation-one line.  For C4 it is
exactly the pinned U_C4/colon source gate.  The C2+/P2 centered occurrence
debt vanishes, but target/unary product-rule compatibility remains part of
the same restriction/reinsertion map.  No new centered carrier appears.

Crucially, the current lower packet is not yet such a literal coefficient.
It lies in Hasse order two with its varied direction pair retained.  The
mixed GHZ row is Hasse order zero.  Explicit physical response-polynomial
evaluations have mixed word 001122, response value zero, and second-Hasse
packet value one for QQ-target, QQ-response/C2+, DQ/PS-C4, and PQ/SQ-P2.
Thus mixed target zero does not close the packet before the missing physical
restriction/algebraization map.  The first failure is precisely the
direction-pair component of the repeated source grade, even after output
word, endpoint head, and fine labels agree.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_chart_switch_physical_minor_landing_gate.py":
        "0b75284d08d15f70005263d09816d98980252d5a6b4496d47d1e842e876308f3",
    "notes/uniform-chart-switch-physical-minor-landing-gate.md":
        "8b6dd471f2ce320309207cf690aa69c2941c1c7158886abc74f19436b192f682",
    "computations/verify_h3_generic_symmetric_c4_placement_terminal_gate.py":
        "ecb8725715747c3270fb069545309283d1890fbac6e66dfb6ed2f53b609e0030",
    "notes/h3-generic-symmetric-c4-placement-terminal-gate.md":
        "dcf0ef4adf500b4bee46ca301b12241e95ed1343a509a4fe4110d5dd3a906e92",
    "computations/verify_h3_generic_symmetric_c4_core_saturation_tor_gate.py":
        "7307cb245996376f9847ff4852a4fdcd0a774152b4011ed92822022f93af03e5",
    "notes/h3-generic-symmetric-c4-core-saturation-tor-gate.md":
        "d0ea7112c33c94de2063e754e70dde9a6671d5fcd5213d4f2f1b62c51aa102bd",
    "computations/verify_h3_pure_trapped_h2_c2_c4_p2_descent_reduction.py":
        "026eb42fac96e2c21e6466f51322a18d45d975bcf5f48e0dc33f9cfa740d8d41",
    "notes/h3-pure-trapped-h2-c2-c4-p2-descent-reduction.md":
        "699a9debf8de2646249f949e80312baa58251a1f36639bed249d40e2dc74b2ea",
    "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py":
        "b03c096eb5bc4e6307cafa966f3d66d8c087e78bb8793c8448eec33f51e7e76a",
    "notes/h3-active-coloop-redistribution-second-hasse-face-classification.md":
        "985737011ea321c70096a89ea2a719db207c304d947ff4899133b39e14c46276",
}
EXPECTED_LEDGER_SHA256 = "b3b9522faf0444ebb5f8d573c1db11cef4e069a3d4e2a85a47368e12fa870c2d"

Factor = tuple[str, tuple[tuple[int, int], ...]]
Term = tuple[Factor, ...]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def factor(name: str, *site_colours: tuple[int, int]) -> Factor:
    return name, tuple(sorted(site_colours))


def term(*factors: Factor) -> Term:
    return tuple(factors)


def word_of(term_value: Term, sites: tuple[int, ...]) -> tuple[int, ...]:
    colours: dict[int, int] = {}
    for _name, assignments in term_value:
        for site, colour in assignments:
            require(site not in colours, ("site covered twice", term_value, site))
            colours[site] = colour
    require(set(colours) == set(sites), (term_value, sites, colours))
    return tuple(colours[site] for site in sites)


def packet_terms() -> dict[str, dict[str, object]]:
    return {
        "C4": {
            "sites": (0, 1, 2, 3),
            "pure": (
                term(factor("q01", (0, 0), (1, 0)),
                     factor("q23", (2, 0), (3, 0))),
                term(factor("q02", (0, 0), (2, 0)),
                     factor("q13", (1, 0), (3, 0))),
                term(factor("q03", (0, 0), (3, 0)),
                     factor("q12", (1, 0), (2, 0))),
            ),
            "mixed": (
                term(factor("q01", (0, 0), (1, 0)),
                     factor("q23", (2, 1), (3, 1))),
                term(factor("q02", (0, 0), (2, 1)),
                     factor("q13", (1, 0), (3, 1))),
                term(factor("q03", (0, 0), (3, 1)),
                     factor("q12", (1, 0), (2, 1))),
            ),
        },
        "C2plus": {
            "sites": (2, 3),
            "pure": (
                term(factor("D"), factor("q23", (2, 0), (3, 0))),
                term(factor("p2", (2, 0)), factor("s3", (3, 0))),
                term(factor("p3", (3, 0)), factor("s2", (2, 0))),
            ),
            "mixed": (
                term(factor("D"), factor("q23", (2, 0), (3, 1))),
                term(factor("p2", (2, 0)), factor("s3", (3, 1))),
                term(factor("p3", (3, 1)), factor("s2", (2, 0))),
            ),
        },
        "P2": {
            "sites": (1, 2, 3),
            "pure": (
                term(factor("s1", (1, 0)), factor("q23", (2, 0), (3, 0))),
                term(factor("s2", (2, 0)), factor("q13", (1, 0), (3, 0))),
                term(factor("s3", (3, 0)), factor("q12", (1, 0), (2, 0))),
            ),
            "mixed": (
                term(factor("s1", (1, 0)), factor("q23", (2, 0), (3, 1))),
                term(factor("s2", (2, 0)), factor("q13", (1, 0), (3, 1))),
                term(factor("s3", (3, 1)), factor("q12", (1, 0), (2, 0))),
            ),
        },
    }


def target_value(word: tuple[int, ...]) -> Q:
    return Q(1 if len(set(word)) == 1 else 0)


def word_packet_audit() -> dict[str, object]:
    records = {}
    for name, packet in packet_terms().items():
        sites = packet["sites"]
        pure_terms = packet["pure"]
        mixed_terms = packet["mixed"]
        pure_words = tuple(word_of(item, sites) for item in pure_terms)
        mixed_words = tuple(word_of(item, sites) for item in mixed_terms)
        require(len(set(pure_words)) == len(set(mixed_words)) == 1,
                (name, pure_words, mixed_words))
        pure_word = pure_words[0]
        mixed_word = mixed_words[0]
        require(target_value(pure_word) == 1
                and target_value(mixed_word) == 0,
                (name, pure_word, mixed_word))

        # The target-normalized dark pure point and the mixed bright point
        # are realized by assigning one scalar factor in each distinct term.
        pure_values = (Q(1, 3), Q(1, 3), Q(1, 3))
        mixed_values = (Q(1), Q(-1), Q(0))
        require(sum(pure_values, Q(0)) == target_value(pure_word)
                and pure_values[1] - pure_values[0] == 0
                and pure_values[2] - pure_values[0] == 0,
                (name, pure_values))
        require(sum(mixed_values, Q(0)) == target_value(mixed_word)
                and (mixed_values[1] - mixed_values[0],
                     mixed_values[2] - mixed_values[0]) == (Q(-2), Q(-1)),
                (name, mixed_values))
        records[name] = {
            "pure_word": list(pure_word),
            "pure_target": "1",
            "pure_switch_dark_term_values": ["1/3", "1/3", "1/3"],
            "mixed_word": list(mixed_word),
            "mixed_target": "0",
            "mixed_switch_bright_term_values": ["1", "-1", "0"],
            "same_word_for_all_three_terms": True,
            "fixed_source_can_have_pure_only_packet": True,
        }
    return records


def covariance_and_affine_audit() -> dict[str, object]:
    colours = (0, 1, 2)
    words = tuple(itertools.product(colours, repeat=4))
    pure = tuple(word for word in words if target_value(word))
    mixed = tuple(word for word in words if not target_value(word))
    require(len(pure) == 3 and len(mixed) == 78,
            (len(pure), len(mixed)))
    for permutation in itertools.permutations(colours):
        require(all(bool(target_value(word))
                    == bool(target_value(tuple(permutation[colour]
                                               for colour in word)))
                    for word in words),
                permutation)

    kappa = tuple(map(Q, (2, 2, -1, -1, -1, -1)))
    require(sum(kappa, Q(0)) == 0,
            "the pure affine target stopped cancelling coarsely in kappa")
    return {
        "four_site_ternary_words": len(words),
        "pure_words": len(pure),
        "mixed_words": len(mixed),
        "global_colour_permutation_preserves_pure_mixed": True,
        "site_permutation_preserves_pure_mixed": True,
        "local_colour_change_can_make_pure_mixed": (
            "yes, but it changes the physical word and carries the target/"
            "product-rule defect; it is the Cplus comparison, not covariance"
        ),
        "affine_inverse": {
            "H=tau": "F=(tau-t1-t2)/3",
            "t1=t2=0": "F=C1=C2=tau/3",
            "mixed_tau_0": "zero packet",
            "pure_tau_1": "unique flat packet (1/3,1/3,1/3)",
        },
        "kappa_sum": str(sum(kappa, Q(0))),
        "coarse_pure_target_on_kappa_packet": 0,
        "fine_labelled_source_boundary_from_coarse_cancellation": False,
    }


def evaluate_matching_polynomial(monomials, values) -> Q:
    return sum((product(Q(values.get(variable, 0)) for variable in monomial)
                for monomial in monomials), Q(0))


def product(values) -> Q:
    answer = Q(1)
    for value in values:
        answer *= value
    return answer


def hasse_pair(monomials, first, second):
    require(first != second, (first, second))
    answer = []
    for monomial in monomials:
        if first not in monomial or second not in monomial:
            continue
        remainder = list(monomial)
        remainder.remove(first)
        remainder.remove(second)
        answer.append(tuple(remainder))
    return tuple(answer)


def mixed_hasse_grade_counterguards() -> dict[str, object]:
    face = load(
        "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py",
        "word_target_hasse_classifier",
    )
    target, response = face.source_monomials()
    q = face.q
    p = face.p
    s = face.s
    d = face.D
    all_variables = set(variable for monomial in target + response
                        for variable in monomial)

    prototypes = {
        "QQ_target_one_edge": {
            "family": target,
            "pair": (q(0, 1), q(2, 3)),
            "nonzero_remainder": {q(4, 5): Q(1)},
            "packet": "one-edge target face",
            "grade": "Hasse[2](Q01,Q23)",
        },
        "QQ_response_C2plus": {
            "family": response,
            "pair": (q(0, 1), q(2, 3)),
            "nonzero_remainder": {d: Q(1), q(4, 5): Q(1)},
            "packet": "D*q45+p4*s5+p5*s4",
            "grade": "Hasse[2](Q01,Q23)",
        },
        "DQ_response_C4": {
            "family": response,
            "pair": (d, q(0, 1)),
            "nonzero_remainder": {q(2, 3): Q(1), q(4, 5): Q(1)},
            "packet": "q23*q45+q24*q35+q25*q34",
            "grade": "Hasse[2](D,Q01)",
        },
        "PS_response_C4": {
            "family": response,
            "pair": (p(0), s(1)),
            "nonzero_remainder": {q(2, 3): Q(1), q(4, 5): Q(1)},
            "packet": "q23*q45+q24*q35+q25*q34",
            "grade": "Hasse[2](P0,S1)",
        },
        "PQ_response_P2": {
            "family": response,
            "pair": (p(0), q(1, 2)),
            "nonzero_remainder": {s(3): Q(1), q(4, 5): Q(1)},
            "packet": "s3*q45+s4*q35+s5*q34",
            "grade": "Hasse[2](P0,Q12)",
        },
        "SQ_response_P2": {
            "family": response,
            "pair": (s(0), q(1, 2)),
            "nonzero_remainder": {p(3): Q(1), q(4, 5): Q(1)},
            "packet": "p3*q45+p4*q35+p5*q34",
            "grade": "Hasse[2](S0,Q12)",
        },
    }
    records = {}
    for name, prototype in prototypes.items():
        values = {variable: Q(0) for variable in all_variables}
        values.update(prototype["nonzero_remainder"])
        first, second = prototype["pair"]
        require(values[first] == values[second] == 0,
                (name, first, second, values[first], values[second]))
        family_value = evaluate_matching_polynomial(prototype["family"], values)
        lower = hasse_pair(prototype["family"], first, second)
        lower_value = evaluate_matching_polynomial(lower, values)
        require(family_value == 0 and lower_value == 1,
                (name, family_value, lower_value, lower))
        records[name] = {
            "mixed_output_word": "001122",
            "degree_zero_family_value": str(family_value),
            "second_Hasse_value": str(lower_value),
            "second_Hasse_grade": prototype["grade"],
            "packet": prototype["packet"],
            "varied_pair_base_values": ["0", "0"],
            "nonzero_remainder_values": {
                repr(variable): str(value) for variable, value in
                prototype["nonzero_remainder"].items()
            },
        }

    # The direct-sum source grading detects the mismatch before any target,
    # anchor, q, ridge, or terminal row is assigned.
    grade_keys = (
        ("001122", "Hasse[0]", "no direction pair"),
        ("001122", "Hasse[2]", "QQ"),
        ("001122", "Hasse[2]", "DQ"),
        ("001122", "Hasse[2]", "PS"),
        ("001122", "Hasse[2]", "PQ"),
        ("001122", "Hasse[2]", "SQ"),
    )
    require(len(set(grade_keys)) == len(grade_keys), grade_keys)
    return {
        "literal_counterguards": records,
        "degree_zero_mixed_GHZ_grade": {
            "word": "001122",
            "Hasse_order": 0,
            "direction_pair": None,
        },
        "lower_packet_grade": {
            "Hasse_order": 2,
            "direction_pair_retained": True,
            "direct_sum_separated_from_degree_zero": True,
        },
        "first_precise_mismatch": (
            "Hasse order/direction-pair component of the repeated source "
            "grade, even after output word/head/fine labels agree and before "
            "augmented readouts"
        ),
        "mixed_target_zero_implies_lower_H_zero": False,
        "needed_bridge": (
            "a source-valid Hasse restriction/algebraization cell including "
            "the product-rule faces; evaluation of the point equation is insufficient"
        ),
    }


def pinned_frontier_audit() -> dict[str, object]:
    switch = load(
        "computations/verify_uniform_chart_switch_physical_minor_landing_gate.py",
        "word_target_switch_pin",
    )
    switch_ledger, switch_digest = switch.audit()
    require(switch_digest == switch.EXPECTED_LEDGER_SHA256,
            switch_digest)

    placement = load(
        "computations/verify_h3_generic_symmetric_c4_placement_terminal_gate.py",
        "word_target_c4_placement_pin",
    )
    placement_ledger, placement_digest = placement.audit()
    require(placement_digest == placement.EXPECTED_LEDGER_SHA256,
            placement_digest)
    missing = placement_ledger["missing_column_and_terminal_extension"]
    require(missing["one_explicit_missing_source_column"]["status"]
                == "NOT CONSTRUCTED BY ANY PINNED CELL"
            and missing["one_explicit_missing_source_column"]
                ["occurrence_augmentation"] == "1",
            missing)

    tor = load(
        "computations/verify_h3_generic_symmetric_c4_core_saturation_tor_gate.py",
        "word_target_c4_tor_pin",
    )
    tor_ledger, tor_digest = tor.audit()
    require(tor_digest == tor.EXPECTED_LEDGER_SHA256,
            tor_digest)
    colon = tor_ledger["nonunit_core_colon"]["invariant_quotient"]
    require(colon["dimension"] == 1,
            colon)

    lower = load(
        "computations/verify_h3_pure_trapped_h2_c2_c4_p2_descent_reduction.py",
        "word_target_lower_pin",
    )
    lower_ledger, lower_digest = lower.audit()
    require(lower_digest == lower.EXPECTED_LEDGER_SHA256,
            lower_digest)
    p2 = lower_ledger["C2plus_and_P2"]
    require(p2["P2_relative_graph"]["selected_line"] == "t_zprivate"
            and p2["P2_relative_graph"]["physical_landing_status"] == "OPEN",
            p2)
    return {
        "switch_physical_ledger": switch_digest,
        "generic_C4_placement_ledger": placement_digest,
        "generic_C4_Tor_ledger": tor_digest,
        "lower_C2plus_C4_P2_ledger": lower_digest,
        "all_switch_dark_effect": {
            "mixed_words": "packet zero, once it is an actual GHZ coefficient",
            "pure_words": (
                "centered switch carrier zero; invariant augmentation-one "
                "target-normal packet remains"
            ),
            "C2plus_P2": (
                "the selected centered t_zprivate debt vanishes, but the "
                "source-valid target/unary restriction map is not manufactured"
            ),
            "C4": (
                "exactly U_C4 / one invariant colon-Tor line; after same-grade "
                "placement the pinned filler-or-terminal fork is exhaustive"
            ),
        },
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "uniform chart switch word/target affine gate",
        "pins": PINS,
        "literal_word_packets": word_packet_audit(),
        "covariance_and_affine_split": covariance_and_affine_audit(),
        "decisive_mixed_Hasse_grade_audit": mixed_hasse_grade_counterguards(),
        "pinned_physical_frontier": pinned_frontier_audit(),
        "verdict": (
            "The current lower H is not literally a target-zero mixed GHZ "
            "coefficient: it is a Hasse-order-two packet with a retained "
            "QQ/DQ/PS/PQ/SQ direction pair.  Explicit mixed-word evaluations "
            "give the degree-zero target/response value zero and the lower "
            "Hasse value one in every packet topology.  If a future source-"
            "valid restriction map algebraizes that packet as a literal lower "
            "coefficient, then the following affine split applies.  Every "
            "C2plus, C4 and P2 packet has both mixed and pure physical "
            "word realizations.  A fixed pure packet cannot be converted to "
            "mixed by site/global-colour covariance.  On an actual mixed GHZ "
            "coefficient, switch darkness forces the packet to zero.  On a "
            "normalized pure coefficient, darkness forces the unique flat "
            "vector (1/3,1/3,1/3).  Across all words/heads, darkness therefore "
            "kills every centered switch carrier but leaves one invariant "
            "augmentation-one affine packet.  For C4 this is exactly the "
            "pinned U_C4/colon gate; C2plus/P2 have no remaining centered "
            "carrier, but target/unary source naturality is not automatic."
        ),
        "shortest_remaining_theorem": (
            "construct the source-valid Hasse-to-coefficient word/head "
            "restriction map.  Its mixed "
            "components use unconditional target zero and the switch bright/"
            "dark fork; its pure component supplies the target-normal U_C4 "
            "augmentation-one column (or the pinned augmented terminal) and "
            "the unary product-rule faces"
        ),
        "scope": (
            "exact decorated coefficient words and target affine fibres; no "
            "claim that local colour change is target-safe or that a Hasse "
            "coefficient is automatically a physical point equation"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("mixed degree-zero GHZ zero -> lower Hasse zero: NO")
    print("first mismatch: HASSE[2] DIRECTION-PAIR GRADE")
    print("after physical algebraization, mixed packet + t-dark: ZERO")
    print("pure packet + t-dark: (1/3,1/3,1/3) AFFINE SURVIVOR")
    print("every topology can be pure-only: YES")
    print("global covariance can pure->mixed: NO")
    print("all-word darkness leaves: ONE AUGMENTATION-ONE C4/TOR GATE")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
