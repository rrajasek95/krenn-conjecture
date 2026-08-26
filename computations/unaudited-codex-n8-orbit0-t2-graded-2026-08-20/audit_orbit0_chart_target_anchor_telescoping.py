#!/usr/bin/env python3
"""Benchmark the orbit-0 chart-local product a*T against the T^2 pivot."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPAN_PATH = HERE / "audit_r8prime_p0_binary_packet_span.py"
SPAN_SPEC = importlib.util.spec_from_file_location("p0_span_chart", SPAN_PATH)
SPAN = importlib.util.module_from_spec(SPAN_SPEC)
SPAN_SPEC.loader.exec_module(SPAN)
BASE = SPAN.BASE
EXPORT = SPAN.EXPORT
R8P = SPAN.R8P
OUT = HERE / "results_orbit0_chart_target_anchor_telescoping.json"

M0 = tuple(EXPORT.M0)
A = bytes(sorted(EXPORT.ANCHORS))
# The four entries give the constant colour on each physical M0 pair.
# The next two rows are cyclic colour shifts.  At each pair the three rows
# use all colours, while every row itself is mixed.
PAIR_COLOURS = ((0, 0, 1, 1), (1, 1, 2, 2), (2, 2, 0, 0))


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def row_k_degree(row: bytes) -> int:
    return sum(cell not in EXPORT.ANCHORS for cell in row)


def word_from_pair_colours(colours):
    return tuple(colour for colour in colours for _ in range(2))


def subtract(row: bytes, divisor: bytes) -> bytes:
    remaining = Counter(row)
    remaining.subtract(divisor)
    require(all(value >= 0 for value in remaining.values()),
            "monomial divisor is absent")
    return bytes(sorted(cell for cell, value in remaining.items()
                        for _ in range(value)))


def move_row(row: bytes, action: int) -> bytes:
    transform = EXPORT.TRANSFORMS[action]
    return bytes(sorted(transform[cell] for cell in row))


def orbit_under(row: bytes, actions) -> frozenset[bytes]:
    return frozenset(move_row(row, action) for action in actions)


def invariant_orbit_count(full_orbit: set[bytes], actions) -> int:
    unseen = set(full_orbit)
    count = 0
    while unseen:
        orbit = orbit_under(min(unseen), actions)
        require(orbit <= full_orbit, "subgroup orbit left full orbit")
        unseen.difference_update(orbit)
        count += 1
    return count


def polynomial_product(left: Counter, right: Counter) -> Counter:
    answer = Counter()
    for first, first_value in left.items():
        for second, second_value in right.items():
            answer[bytes(sorted(first + second))] += first_value * second_value
    return +answer


def invariant_quotient(polynomial: Counter, actions):
    unseen = set(polynomial)
    quotient = Counter()
    orbit_sizes = Counter()
    while unseen:
        seed = min(unseen)
        orbit = orbit_under(seed, actions)
        supported = orbit & set(polynomial)
        require(supported == orbit, "polynomial support is not subgroup-invariant")
        coefficients = {polynomial[row] for row in orbit}
        require(len(coefficients) == 1,
                "polynomial coefficient is not subgroup-invariant")
        representative = min(orbit)
        quotient[representative] = next(iter(coefficients)) * len(orbit)
        orbit_sizes[len(orbit)] += 1
        unseen.difference_update(orbit)
    return quotient, orbit_sizes


def formal_telescoping(signs=(1, -1, 1)):
    """Expand the three-atom identity in a six-symbol free polynomial ring."""
    # A monomial is a sorted tuple among t0,t1,t2,e0,e1,e2.
    def mul(*factors):
        polynomial = Counter({(): 1})
        for factor in factors:
            updated = Counter()
            for left, coefficient in polynomial.items():
                for right, value in factor.items():
                    updated[tuple(sorted(left + right))] += coefficient * value
            polynomial = +updated
        return polynomial

    t = [Counter({(f"t{i}",): 1}) for i in range(3)]
    e = [Counter({(f"e{i}",): 1}) for i in range(3)]
    h = [t[i] + e[i] for i in range(3)]
    lhs = mul(t[0], t[1], t[2]) + mul(e[0], e[1], e[2])
    rhs = Counter()
    for sign, factors in zip(signs,
                             ((h[0], t[1], t[2]),
                              (e[0], h[1], t[2]),
                              (e[0], e[1], h[2]))):
        term = mul(*factors)
        for monomial, coefficient in term.items():
            rhs[monomial] += sign * coefficient
    return +lhs, +rhs


def main() -> None:
    raw = json.loads(R8P.read_text())
    residual = Counter({bytes.fromhex(row): Fraction(numerator, denominator)
                        for row, numerator, denominator in raw["residual"]})
    require(len(residual) == 120
            and all(len(row) == 12 and row_k_degree(row) == 8
                    for row in residual),
            "R8' input changed")

    words = tuple(word_from_pair_colours(colours)
                  for colours in PAIR_COLOURS)
    require(all(len(set(word)) > 1 for word in words),
            "an anchor factor word became pure")
    terms = tuple(BASE.word_terms(word) for word in words)
    anchor_terms = tuple(BASE.term_ids(word, M0) for word in words)
    require(bytes(sorted(b"".join(anchor_terms))) == A,
            "three anchor terms no longer partition a")

    layer_profiles = []
    errors = []
    leading_errors = []
    for matching_terms, anchor_term in zip(terms, anchor_terms):
        profile = Counter(row_k_degree(term) for term in matching_terms)
        require(profile == {0: 1, 2: 12, 3: 32, 4: 60},
                "mixed anchor word K-profile changed")
        require(tuple(term for term in matching_terms if row_k_degree(term) == 0)
                == (anchor_term,), "K0 term is not unique")
        layer_profiles.append(dict(sorted(profile.items())))
        error = Counter({term: 1 for term in matching_terms if term != anchor_term})
        errors.append(error)
        leading_errors.append(Counter({term: 1 for term in matching_terms
                                       if row_k_degree(term) == 2}))

    # Every quotient row of a*R8' has three literal unary K8 pivots, one for
    # each anchor term.  No group/rank calculation is involved.
    unary_checks = 0
    for row in residual:
        target = bytes(sorted(A + row))
        for anchor_term, matching_terms in zip(anchor_terms, terms):
            multiplier = subtract(target, anchor_term)
            require(len(multiplier) == 20 and row_k_degree(multiplier) == 8,
                    "unary multiplier has wrong bidegree")
            leading = [bytes(sorted(multiplier + term))
                       for term in matching_terms
                       if row_k_degree(multiplier + term) == 8]
            require(leading == [target], "K8 source column is not unary")
            unary_checks += 1

    lhs, rhs = formal_telescoping()
    require(lhs == rhs, "anchor telescoping signs are wrong")
    _lhs, hostile = formal_telescoping((1, 1, 1))
    require(_lhs != hostile, "hostile telescoping sign mutation did not fire")

    # E0_2 E1_2 E2_2 is the universal K6 packet multiplying the K8 leading
    # residual.  It is invariant under the stabilizer of the unordered
    # three-factor anchor partition.
    leading_packet = polynomial_product(
        polynomial_product(leading_errors[0], leading_errors[1]),
        leading_errors[2],
    )
    require(sum(leading_packet.values()) == 12 ** 3
            and all(len(row) == 12 and row_k_degree(row) == 6
                    for row in leading_packet),
            "leading K6 packet changed")
    factor_set = frozenset(anchor_terms)
    factor_stabilizer = tuple(
        action for action in range(len(EXPORT.STABILIZER))
        if frozenset(move_row(term, action) for term in anchor_terms) == factor_set
    )
    require(len(factor_stabilizer) == 384,
            "anchor-factorization stabilizer is not order 384")
    packet_quotient, packet_orbit_sizes = invariant_quotient(
        leading_packet, factor_stabilizer
    )

    # Count how the 120 full-G quotient rows split under the order-384
    # factorization stabilizer.  Coefficients stay constant on every split.
    split_r8_orbits = 0
    split_histogram = Counter()
    labelled_r8_support = 0
    for row, mass in residual.items():
        full_orbit = set(EXPORT.row_orbit(row))
        labelled_r8_support += len(full_orbit)
        count = invariant_orbit_count(full_orbit, factor_stabilizer)
        split_r8_orbits += count
        split_histogram[count] += 1
        require(mass / len(full_orbit) != 0, "R8' labelled coefficient vanished")
    require(labelled_r8_support == 148_176,
            "R8' labelled support changed")

    result = {
        "status": "UNAUDITED exact orbit-0 chart-target benchmark",
        "input_r8prime_sha256": sha256(R8P.read_bytes()).hexdigest(),
        "anchor_product_degree": len(A),
        "anchor_factor_words": ["".join(map(str, word)) for word in words],
        "anchor_factor_terms": [term.hex() for term in anchor_terms],
        "anchor_terms_partition_a": True,
        "anchor_word_K_profiles": layer_profiles,
        "r8prime_quotient_orbits": len(residual),
        "r8prime_labelled_support": labelled_r8_support,
        "gr8_unary_columns_checked": unary_checks,
        "unary_columns_per_r8prime_orbit": 3,
        "gr8_unary_zero": True,
        "telescoping_identity": (
            "t0*t1*t2 + E0*E1*E2 = H0*t1*t2 - E0*H1*t2 "
            "+ E0*E1*H2, where Hi=ti+Ei are mixed word hafnians"
        ),
        "consequence": (
            "If T-S=R has K-degree at least 8 with S in I_mix, then "
            "a*T is congruent to -R*E0*E1*E2 modulo I_mix and therefore "
            "lies in I_mix+K^14. Its leading K14 residual is "
            "-R8'*E0_2*E1_2*E2_2."
        ),
        "leading_K6_packet": {
            "raw_term_occurrences": 12 ** 3,
            "distinct_labelled_monomials": len(leading_packet),
            "factorization_stabilizer_order": len(factor_stabilizer),
            "full_orbit_cosets": len(EXPORT.STABILIZER) // len(factor_stabilizer),
            "quotient_row_orbits": len(packet_quotient),
            "quotient_orbit_size_histogram": {
                str(size): count for size, count in sorted(packet_orbit_sizes.items())
            },
            "quotient_total_mass": sum(packet_quotient.values()),
        },
        "r8prime_under_factorization_stabilizer": {
            "quotient_row_orbits": split_r8_orbits,
            "full_orbit_split_histogram": {
                str(count): multiplicity
                for count, multiplicity in sorted(split_histogram.items())
            },
        },
        "leading_K14_factored_block_upper_count": (
            split_r8_orbits * len(packet_quotient)
        ),
        "leading_K14_raw_labelled_product_occurrences": (
            labelled_r8_support * 12 ** 3
        ),
        "next_source_family": (
            "For a positive residual-led K14 cleanup, close the target "
            "R8'*E0_2*E1_2*E2_2 under every incident degree-24 column "
            "Q*H_w, w mixed, retaining exactly outputs of K-degree 14. "
            "A negative claim additionally requires the whole cutoff<15 "
            "lower-kernel transfer."
        ),
        "comparison_to_T2": (
            "The chart target begins two K-degrees earlier (14 versus 16), "
            "but its leading packet is a product of the 120-orbit R8' with "
            "three 12-term layers and has a 384-element stabilizer. The T2 "
            "pure-anchor residual had 1,578,292 nonzero H768 row orbits, and "
            "its clean binary-J shortcut is exactly obstructed."
        ),
        "scope": (
            "This proves the orbit-0 finite lift a*T in I_mix+K^14, not "
            "localized membership. Degree-24 membership ends only after "
            "cutoff 25, and the 31-chart cover still requires transport or "
            "separate identities on every chart."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(encoded.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("orbit0 a*T anchor telescoping audit: PASS")
    print("R8' unary checks / K lift:", unary_checks, "8 -> 14")
    print("factor stabilizer / packet orbits:",
          len(factor_stabilizer), len(packet_quotient))
    print("R8' split orbits / block upper count:",
          split_r8_orbits, result["leading_K14_factored_block_upper_count"])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
