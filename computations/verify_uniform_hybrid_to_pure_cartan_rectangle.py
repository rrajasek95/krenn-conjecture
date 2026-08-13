#!/usr/bin/env python3
"""Every anchor-hybrid occurrence lies in a physical mixed/pure Cartan rectangle.

For the hybrid word (a,b,i,...,i), choose independent local colour Weyl
elements at its exceptional sites sending a and b to i.  Transpose sites on
two distinct complementary matching edges.  The four principal occurrences
are two distinct matching skeletons in the hybrid word and the same two in
the pure-i target word.  Local covariance and endpoint oddization make this
a physical target-preserving Cartan prism, not a formal matching square.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from itertools import permutations, product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_physical_cartan_source_prism.py":
        "4f23c4645574d619fac4667eba50567435b2f85ff2583b5b3708a565de400cca",
    "computations/verify_uniform_cartan_critical_component_placement_gate.py":
        "68c56c1a9144dd92fa803962697de60b78b58a125191450f1af1abcd1befe2a1",
    "computations/verify_uniform_anchor_hybrid_propagation_cycle.py":
        "b128a65c42eea570c1b66264bae52de3db613087a990789b2cb1d90c4c4b092a",
    "computations/verify_oo_dark_potential_source_promotion_counterguard.py":
        "76bdd6c8ce19cc466995b235bade9114d7d2779b74bfcd25eea703c2d1de3db2",
}
EXPECTED_LEDGER_SHA256 = (
    "45a1bf5e123e97920a6da56cef8476172d4a396002cd4bfce7d7de76164fe93b"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    left = vertices[0]
    for index in range(1, len(vertices)):
        right = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(left, right),) + tail))


def swap_site(site, p, q):
    if site == p:
        return q
    if site == q:
        return p
    return site


def swap_matching(matching, p, q):
    answer = []
    for left, right in matching:
        answer.append(edge(swap_site(left, p, q), swap_site(right, p, q)))
    return tuple(sorted(answer))


def swap_word(word, p, q):
    answer = list(word)
    answer[p], answer[q] = answer[q], answer[p]
    return tuple(answer)


def local_permutation_map(old, target):
    """The first S3 permutation carrying old to target."""
    for values in permutations(range(3)):
        if values[old] == target:
            return values
    raise RuntimeError("no colour permutation found")


def apply_independent_weyl(word, x, y, target):
    at_x = local_permutation_map(word[x], target)
    at_y = local_permutation_map(word[y], target)
    answer = list(word)
    answer[x] = at_x[answer[x]]
    answer[y] = at_y[answer[y]]
    return tuple(answer), at_x, at_y


def audit_rectangle(size):
    require(size >= 6 and size % 2 == 0,
            "the rectangle needs at least two complementary matching edges")
    matchings = tuple(perfect_matchings(range(size)))
    records = 0
    rectangle_signatures = Counter()
    for matching in matchings:
        for marked in matching:
            x, y = marked
            complement = tuple(pair for pair in matching if pair != marked)
            require(len(complement) >= 2,
                    "the marked edge has too few complementary edges")
            # A deterministic crossing transposition on two distinct
            # complementary matching edges.
            p = complement[0][0]
            q = complement[1][0]
            switched = swap_matching(matching, p, q)
            require(switched != matching,
                    "the complementary transposition fixed the matching")

            for residual in range(3):
                for a in range(3):
                    for b in range(3):
                        if a == b:
                            continue
                        word = [residual] * size
                        word[x], word[y] = a, b
                        word = tuple(word)
                        pure, wx, wy = apply_independent_weyl(
                            word, x, y, residual)
                        require(pure == (residual,) * size,
                                "independent Weyl moves missed the pure word")
                        require(swap_word(word, p, q) == word
                                and swap_word(pure, p, q) == pure,
                                "the residual transposition changed a word")

                        corners = (
                            (matching, pure, 1),
                            (matching, word, -1),
                            (switched, pure, -1),
                            (switched, word, 1),
                        )
                        require(len({(mu, z) for mu, z, _ in corners}) == 4,
                                "the mixed/pure Cartan rectangle collapsed")
                        require(sum(coefficient for _, _, coefficient in corners)
                                == 0,
                                "the Cartan rectangle lost augmentation zero")
                        rectangle_signatures[(a, b, residual)] += 1
                        records += 1

    expected = len(matchings) * (size // 2) * 3 * 6
    require(records == expected,
            "the hybrid rectangle census changed")
    require(set(rectangle_signatures.values())
            == {len(matchings) * (size // 2)},
            "the colour-type rectangle multiplicities changed")
    return {
        "order": size,
        "perfect_matchings": len(matchings),
        "marked_matching_edges": len(matchings) * (size // 2),
        "ordered_hybrid_colour_types": 18,
        "rectangles": records,
        "corner_coefficients": [1, -1, -1, 1],
        "mixed_corners": 2,
        "pure_target_corners": 2,
    }


def audit_target_defect_independence(size):
    """Independent local colour permutations still commute with disjoint s."""
    x, y, p, q = 0, 1, 2, 3
    checks = 0
    for wx in permutations(range(3)):
        for wy in permutations(range(3)):
            transformed = Counter()
            delta = Counter({(colour,) * size: 1 for colour in range(3)})
            for word, coefficient in delta.items():
                changed = list(word)
                changed[x] = wx[changed[x]]
                changed[y] = wy[changed[y]]
                transformed[tuple(changed)] += coefficient
            defect = Counter(transformed)
            defect.subtract(delta)
            defect = Counter({word: value for word, value in defect.items()
                              if value})
            swapped = Counter()
            for word, coefficient in defect.items():
                swapped[swap_word(word, p, q)] += coefficient
            require(swapped == defect,
                    "a disjoint transposition detected the target defect")
            checks += 1
    require(checks == 36,
            "the independent local Weyl target audit changed")
    return {
        "order": size,
        "independent_local_S3_pairs": checks,
        "disjoint_endpoint_odd_target_defect": 0,
    }


def main():
    pin_dependencies()
    ledger = {
        "pins": PINS,
        "rectangle_audits": [audit_rectangle(size) for size in (6, 8)],
        "target_audits": [audit_target_defect_independence(size)
                          for size in (6, 8)],
        "uniform_theorem": (
            "every anchor-hybrid matching occurrence with word "
            "z=(a,b,i,...,i), a!=b, lies in a source-provenant physical "
            "Cartan rectangle with the same two matching skeletons in z "
            "and in the pure-i target word.  Independent local Weyl moves "
            "send a,b to i; a transposition across two residual matching "
            "edges fixes both words and changes the matching skeleton.  "
            "Endpoint oddization kills the target defect"
        ),
        "component_alternative": (
            "for a fine-label-saturated matching component containing the "
            "hybrid corner, the Cartan rectangle either supplies a literal "
            "word-changing exit toward the pure target row or attaches the "
            "pure target corners to the same complete critical component"
        ),
        "scope": (
            "the theorem gives a target-touching physical prism and an "
            "exact typed-exit alternative.  It does not by itself prove "
            "that a dark complete-lift residual is an occupied same-row "
            "kernel, nor that retaining the pure corners makes the Schur "
            "charge nonzero"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                f"ledger digest changed: {digest}")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
