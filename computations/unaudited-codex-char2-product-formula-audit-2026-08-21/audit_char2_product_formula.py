#!/usr/bin/env python3
"""Exact bounded audit of the char-2/product-formula globalization route."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import argparse
import gzip
import json
import pickle
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARITY = ROOT / "computations/degree9_source_ideal_char2_h27.pkl"
RESIDUAL = ROOT / "computations/degree9_char2_first_integral_residual.pkl.gz"
LIFT_CHECKER = ROOT / "computations/verify_degree9_integral_lift_obstruction.py"
FILTERED_CHECKER = ROOT / "computations/verify_valuation_filtered_laurent_circuit.py"
BINARY_CHECKER = ROOT / "computations/verify_binary_polystable_bad_reduction.py"
CYCLE_CHECKER = ROOT / "computations/verify_one_hot_source_cycle_invariant_separator.py"
OUT = HERE / "results_char2_product_formula.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode("ascii")).hexdigest()


def edge(u, v):
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append((edge(first, second),) + tail)
    return tuple(answer)


MATCHINGS6 = perfect_matchings(range(6))


class Quad:
    """a+b*sqrt(D), with exact rational coefficients."""

    __slots__ = ("a", "b", "D")

    def __init__(self, a=0, b=0, D=0):
        self.a = Fraction(a)
        self.b = Fraction(b)
        self.D = int(D)

    def _coerce(self, other):
        if isinstance(other, Quad):
            require(other.D == self.D, "quadratic fields changed")
            return other
        return Quad(other, 0, self.D)

    def __add__(self, other):
        other = self._coerce(other)
        return Quad(self.a + other.a, self.b + other.b, self.D)

    __radd__ = __add__

    def __mul__(self, other):
        other = self._coerce(other)
        return Quad(self.a * other.a + self.b * other.b * self.D,
                    self.a * other.b + self.b * other.a, self.D)

    __rmul__ = __mul__

    def __eq__(self, other):
        other = self._coerce(other)
        return self.a == other.a and self.b == other.b


def binary_source_family(N):
    D = 4 ** N - 1
    denominator = 2 ** N
    one = Quad(1, 0, D)
    a = Quad(Fraction(1, denominator), 0, D)
    b = Quad(0, Fraction(1, denominator), D)
    zero = Quad(0, 0, D)
    cells = {
        (edge(0, 1), 0): a,
        (edge(2, 3), 0): a,
        (edge(0, 2), 0): b,
        (edge(1, 3), 0): b,
        (edge(4, 5), 0): one,
        (edge(1, 2), 1): one,
        (edge(3, 4), 1): one,
        (edge(0, 5), 1): one,
    }
    amplitudes = {}
    for word in product(range(3), repeat=6):
        value = zero
        for matching in MATCHINGS6:
            term = one
            for u, v in matching:
                if word[u] != word[v]:
                    term = zero
                    break
                term = term * cells.get(((u, v), word[u]), zero)
            value = value + term
        amplitudes["".join(map(str, word))] = value
    require(amplitudes["000000"] == 1 and amplitudes["111111"] == 1,
            "binary pure normalization failed")
    require(all(value == 0 for word, value in amplitudes.items()
                if word not in ("000000", "111111")),
            "binary source acquired an unwanted coefficient")
    moment = {}
    for vertex in range(6):
        for colour in range(3):
            value = zero
            for (physical, cell_colour), coefficient in cells.items():
                if cell_colour == colour and vertex in physical:
                    value = value + coefficient * coefficient
            moment[vertex, colour] = value
    require([moment[vertex, 0] for vertex in range(6)] == [one] * 6 and
            [moment[vertex, 1] for vertex in range(6)] == [one] * 6 and
            [moment[vertex, 2] for vertex in range(6)] == [zero] * 6,
            "binary colourwise moment balance failed")
    q = Fraction(D, 2 ** (4 * N))
    return {
        "N": N,
        "field": f"Q(sqrt({D}))",
        "a": f"1/{denominator}",
        "b": f"sqrt({D})/{denominator}",
        "a_squared_plus_b_squared": 1,
        "amplitudes_checked": len(amplitudes),
        "nonzero_amplitudes": {"000000": 1, "111111": 1},
        "colourwise_squared_incidence": {"colour_0": 1, "colour_1": 1,
                                          "colour_2": 0},
        "target_torus_polystable": True,
        "balanced_monomial": f"(a*b)^2={q.numerator}/{q.denominator}",
        "balanced_port_degree": {
            "colour_0_each_site": 2,
            "colour_1_each_site": 0,
            "colour_2_each_site": 0,
        },
        "v2_balanced_monomial": -4 * N,
        "principal_norm": f"({D})^2/2^{8*N}",
    }


def v2_fraction(value):
    value = Fraction(value)
    numerator = abs(value.numerator)
    denominator = value.denominator
    answer = 0
    while numerator and numerator % 2 == 0:
        numerator //= 2
        answer += 1
    while denominator % 2 == 0:
        denominator //= 2
        answer -= 1
    return answer


def fixed_sum_slack():
    rows = []
    for N in range(2, 9):
        left = Fraction(1, 2 ** N)
        right = Fraction(1, 2) - left
        require(left + right == Fraction(1, 2), "fixed residual sum changed")
        require(v2_fraction(left) == v2_fraction(right) == -N,
                (N, left, right, v2_fraction(left), v2_fraction(right)))
        rows.append({
            "N": N,
            "x": str(left),
            "y": str(right),
            "x_plus_y": "1/2",
            "v2_x": -N,
            "v2_y": -N,
        })
    return {
        "examples": rows,
        "conclusion": (
            "Even the fixed equation R=1/2 permits contributing terms with "
            "arbitrarily negative 2-adic valuation, cancelled inside R. It "
            "does not bound a witness monomial or its global height."
        ),
    }


def decode_row(code):
    valid_edges = tuple(
        (left, right)
        for left in range(18)
        for right in range(left + 1, 18)
        if left // 3 != right // 3
    )
    answer = []
    while code:
        low = code & -code
        code ^= low
        left, right = valid_edges[low.bit_length() - 1]
        answer.append((left // 3, right // 3, left % 3, right % 3))
    return tuple(sorted(answer))


def star_value(occurrence):
    return -1 if occurrence[:2] in ((0, 1), (0, 2)) else 0


def tropical_star_audit():
    fibre_histogram = Counter()
    for word in product(range(3), repeat=6):
        values = [
            sum(-1 if pair in ((0, 1), (0, 2)) else 0
                for pair in matching)
            for matching in MATCHINGS6
        ]
        minimum = min(values)
        count = sum(value == minimum for value in values)
        require((minimum, count) == (-1, 6), (word, minimum, count))
        fibre_histogram[(minimum, count)] += 1
    require(fibre_histogram == {(-1, 6): 729}, fibre_histogram)

    with PARITY.open("rb") as stream:
        parity = pickle.load(stream)
    with gzip.open(RESIDUAL, "rb") as stream:
        residual = pickle.load(stream)["coefficients"]
    row = 1589
    gamma = decode_row(parity["row_codes"][row])
    expected = tuple(sorted({
        (0, 2, 0, 2),
        (0, 2, 1, 1),
        (0, 1, 2, 2),
        (1, 2, 0, 0),
        (1, 5, 1, 1),
        (3, 5, 0, 2),
        (3, 4, 1, 2),
        (3, 4, 2, 1),
        (4, 5, 0, 0),
    }))
    require(gamma == expected and residual[row] == -1, (gamma, residual[row]))
    stubs = sorted((stub for u, v, a, b in gamma
                    for stub in ((u, a), (v, b))))
    require(stubs == [(vertex, colour) for vertex in range(6)
                      for colour in range(3)], stubs)
    gamma_value = sum(star_value(item) for item in gamma)
    require(gamma_value == -3, gamma_value)
    nonzero = [coefficient for coefficient in residual if coefficient]
    require(len(nonzero) == 395542 and min(nonzero) == -12 and max(nonzero) == -1,
            (len(nonzero), min(nonzero), max(nonzero)))
    return {
        "valuation": "all 27 cells on physical edges 01 and 02 have weight -1; others 0",
        "generator_initial_fibres": 729,
        "minimum_terms_per_fibre": 6,
        "all_ones_F2_residue_value": "6=0",
        "common_torus_zero_of_all_generator_initial_forms": True,
        "residual_nonzero_orbits": len(nonzero),
        "selected_negative_row": row,
        "selected_coefficient": residual[row],
        "selected_gamma": [list(item) for item in gamma],
        "selected_gamma_balanced": True,
        "selected_gamma_valuation": gamma_value,
        "conclusion": (
            "The cone selected by this varying-Gamma witness cannot be "
            "discarded by the 729 generator initial forms. A generator-only "
            "finite tropical cover is not an emptiness certificate."
        ),
    }


def algebraic_globalization_ceiling():
    return {
        "normalized_fibre_ring": (
            "B=Z[z]/(F_mixed, F_000000-1, F_111111-1, F_222222-1)"
        ),
        "exact_integral_consequence": "1=2R in B",
        "scheme_theoretic_meaning": (
            "2 is a unit in B with inverse R; equivalently every component "
            "of Spec(B) lies over Spec(Z[1/2]) and the characteristic-two "
            "special fibre is empty."
        ),
        "number_field_value": "Every closed characteristic-zero point sends R to 1/2.",
        "norm_value": "N_K/Q(R)=2^(-[K:Q])",
        "product_formula_verdict": (
            "This fixed denominator is compatible with the product formula: "
            "negative orders above 2 are compensated by other finite and "
            "archimedean places. Spec(Z[1/2]) itself is the minimal model of "
            "the same phenomenon."
        ),
        "individual_monomials": (
            "The identity fixes only the balanced polynomial sum R. It does "
            "not make any z^Gamma an algebraic-integer unit or give a fixed "
            "odd norm to a finite product of them."
        ),
    }


def finite_product_guard():
    examples = []
    for count in (2, 3, 5):
        factors = [Fraction(1, 2)] + [Fraction(2) for _ in range(count - 1)]
        valuation = sum(v2_fraction(value) for value in factors)
        examples.append({
            "factor_count": count,
            "one_forced_negative_factor_v2": -1,
            "other_factor_v2": 1,
            "product_v2": valuation,
        })
    require([row["product_v2"] for row in examples] == [0, 1, 3], examples)
    return {
        "examples": examples,
        "conclusion": (
            "Knowing that at least one factor in a finite witness list is "
            "negative at a place gives no sign for their product. When the "
            "selected Gamma varies with the place, cross-factors may have "
            "arbitrary positive valuation there."
        ),
    }


def main(write_results=False):
    binary = [binary_source_family(N) for N in range(1, 7)]
    require([row["v2_balanced_monomial"] for row in binary] ==
            [-4, -8, -12, -16, -20, -24], binary)
    tropical = tropical_star_audit()
    result = {
        "status": "PASS exact char-2/product-formula globalization counteraudit",
        "integral_lift_globalization": algebraic_globalization_ceiling(),
        "fixed_sum_local_slack": fixed_sum_slack(),
        "finite_product_over_varying_witnesses": finite_product_guard(),
        "source_faithful_number_field_countermodel": {
            "scope": (
                "Exact binary GHZ embedded in the same six-site 3-colour "
                "source coordinates with the third target summand absent. "
                "This is not a ternary Krenn counterexample."
            ),
            "family": binary,
            "theorem_guard": (
                "Normalized exact matching equations, torus polystability, a "
                "balanced monomial of arbitrarily negative 2-adic valuation, "
                "and the global product formula are mutually compatible. "
                "Therefore no contradiction follows from those arithmetic "
                "properties alone."
            ),
        },
        "source_cycle_invariants": {
            "degree_at_n6": 9,
            "same_balanced_multidegree": True,
            "exact_ternary_fibre_value": 0,
            "reason": "I_M=H_m Q_M contains a mixed coefficient factor H_m.",
            "verdict": (
                "Cycle invariants separate the known boundary orbit, where "
                "they equal one, but on the exact GHZ fibre they vanish. They "
                "cannot turn a residual Gamma monomial into a nonzero unit."
            ),
        },
        "tropical_initial_cover": {
            "formal_finiteness": (
                "Yes in principle: the residual and coefficient generators "
                "have finite Newton support, so witness-minimum cones admit a "
                "finite polyhedral refinement. Varying Gamma is a size issue, "
                "not an infinitude obstruction."
            ),
            "order_zero_generator_cover_closes": False,
            "exact_countercone": tropical,
            "needed_enrichment": (
                "At least the next 2-adic digit/multi-term initial equations "
                "such as the known rank-45/46 four-row first-jet obstruction; "
                "a selected minimum Gamma and the 729 initial generators are "
                "insufficient."
            ),
        },
        "terminal_verdict": {
            "product_formula_or_height_route": False,
            "generator_level_tropical_cover": False,
            "higher_2_adic_initial_ideal_route": "open but genuinely new machinery",
            "precise_theorem": (
                "The degree-nine lift globalizes exactly to inversion of 2 in "
                "the normalized fibre ring. It proves arithmetic instability, "
                "not global nonexistence. Product formula supplies compensation, "
                "and source-cycle invariants vanish on the target fibre."
            ),
        },
        "pinned_sources": {
            str(PARITY.relative_to(ROOT)): file_sha(PARITY),
            str(RESIDUAL.relative_to(ROOT)): file_sha(RESIDUAL),
            str(LIFT_CHECKER.relative_to(ROOT)): file_sha(LIFT_CHECKER),
            str(FILTERED_CHECKER.relative_to(ROOT)): file_sha(FILTERED_CHECKER),
            str(BINARY_CHECKER.relative_to(ROOT)): file_sha(BINARY_CHECKER),
            str(CYCLE_CHECKER.relative_to(ROOT)): file_sha(CYCLE_CHECKER),
        },
    }
    result["logical_sha256"] = logical_sha(result)
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "binary_exact_models": len(binary),
        "binary_balanced_v2_range": [binary[0]["v2_balanced_monomial"],
                                     binary[-1]["v2_balanced_monomial"]],
        "star_initial_fibres": tropical["generator_initial_fibres"],
        "star_minima_per_fibre": tropical["minimum_terms_per_fibre"],
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
