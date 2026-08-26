#!/usr/bin/env python3
"""Expose and verify the compact structure of the 120-orbit sparse R8'."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
T2_PATH = HERE / "audit_orbit0_t2_pivot_setup.py"
SPEC = importlib.util.spec_from_file_location("orbit0_t2_factor", T2_PATH)
T2 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(T2)
INPUT = HERE / "results_orbit0_cutoff9_sparse_r8.json"
OUT = HERE / "results_orbit0_cutoff9_sparse_r8_factorization.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def subtract_multiset(row, divisor):
    residual = list(row)
    for cell in divisor:
        residual.remove(cell)
    return bytes(residual)


def site_cycle_type(row):
    adjacency = [[] for _ in range(8)]
    for cell_id in row:
        u, v, _a, _b = T2.BASE.CELLS[cell_id]
        adjacency[u].append(v)
        adjacency[v].append(u)
    require(all(len(neighbours) == 2 for neighbours in adjacency),
            "non-anchor factor is not site-2-regular")
    unseen = set(range(8))
    lengths = []
    while unseen:
        stack = [min(unseen)]
        unseen.remove(stack[0])
        length = 0
        while stack:
            site = stack.pop()
            length += 1
            for neighbour in adjacency[site]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    stack.append(neighbour)
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def main():
    raw = json.loads(INPUT.read_text())
    actual = Counter()
    for row_hex, numerator, denominator in raw["residual"]:
        representative = bytes.fromhex(row_hex)
        orbit = T2.row_orbit(representative)
        coefficient = Fraction(numerator, denominator) / len(orbit)
        require(coefficient.denominator == 1,
                "sparse R8' labelled coefficient is nonintegral")
        for row in orbit:
            require(row not in actual, "sparse residual orbits overlap")
            actual[row] = coefficient
    require(len(actual) == 148176, "labelled sparse residual support changed")

    anchor_products = {
        colour: bytes(sorted(T2.BASE.CELL_ID[(u, v, colour, colour)]
                             for u, v in T2.M0))
        for colour in T2.BASE.COLORS
    }
    factors = {colour: Counter() for colour in T2.BASE.COLORS}
    cycle_histogram = {colour: Counter() for colour in T2.BASE.COLORS}
    coefficient_histogram = {colour: Counter() for colour in T2.BASE.COLORS}
    for row, coefficient in actual.items():
        anchors = bytes(cell for cell in row if cell in T2.ANCHORS)
        colours = {T2.BASE.CELLS[cell][2] for cell in anchors}
        require(len(anchors) == 4 and len(colours) == 1,
                "R8' row does not contain one pure anchor product")
        colour = next(iter(colours))
        require(anchors == anchor_products[colour],
                "R8' pure anchors do not cover the physical matching")
        nonanchors = subtract_multiset(row, anchors)
        require(len(nonanchors) == 8
                and all(cell not in T2.ANCHORS for cell in nonanchors),
                "factor has wrong non-anchor degree")
        port_colours = [[] for _ in range(8)]
        for cell_id in nonanchors:
            u, v, a, b = T2.BASE.CELLS[cell_id]
            require((u, v) not in T2.M0,
                    "factor uses a physical-pair edge")
            port_colours[u].append(a)
            port_colours[v].append(b)
        complement = tuple(c for c in T2.BASE.COLORS if c != colour)
        require(all(tuple(sorted(values)) == complement for values in port_colours),
                "factor does not use each complementary colour port once")
        factors[colour][nonanchors] = coefficient
        cycle_histogram[colour][site_cycle_type(nonanchors)] += 1
        coefficient_histogram[colour][coefficient] += 1

    require(all(len(factors[colour]) == 49392 for colour in T2.BASE.COLORS),
            "factor support is not 49392 per colour")
    require(factors[0] and sum(len(value) for value in factors.values()) == len(actual),
            "factorization does not partition R8'")

    # Every cross-colour product is killed at K-degree sixteen by one fixed
    # mixed word per colour pair.  Choose colours c,c,d,d on the four physical
    # pairs; its M0 term divides every m_c*m_d product and is its unique K0
    # hafnian term.
    unary_controls = []
    for left in T2.BASE.COLORS:
        for right in range(left + 1, 3):
            assignment = (left, left, right, right)
            word = tuple(colour for colour in assignment for _ in range(2))
            leading = bytes(sorted(T2.BASE.CELL_ID[(u, v, assignment[pair],
                                                   assignment[pair])]
                                   for pair, (u, v) in enumerate(T2.M0)))
            sample_left = next(iter(factors[left]))
            sample_right = next(iter(factors[right]))
            row = bytes(sorted(anchor_products[left] + sample_left
                               + anchor_products[right] + sample_right))
            multiplier = subtract_multiset(row, leading)
            outputs = T2.degree24_column_rows((word, multiplier))
            degree_histogram = Counter(T2.row_k_degree(output) for output in outputs)
            require(outputs.count(row) == 1 and degree_histogram[16] == 1
                    and min(degree_histogram) == 16
                    and all(degree == 16 or degree >= 18 for degree in degree_histogram),
                    "mixed cross-term source is not unary in grade sixteen")
            unary_controls.append({
                "colours": [left, right],
                "word": "".join(map(str, word)),
                "leading_anchor_term": leading.hex(),
                "sample_multiplier": multiplier.hex(),
                "K_degree_histogram": dict(sorted(degree_histogram.items())),
            })

    # Signed factors force collision collection.  Freeze one exact zero-sum
    # collision in P_0^2; pair coefficients include the off-diagonal factor 2.
    items = tuple(sorted(factors[0].items()))
    seen = {}
    collision = None
    for left, (left_row, left_coefficient) in enumerate(items[:500]):
        for right in range(left, 500):
            right_row, right_coefficient = items[right]
            product_row = bytes(sorted(left_row + right_row))
            contribution = left_coefficient * right_coefficient
            if left != right:
                contribution *= 2
            if (product_row in seen
                    and seen[product_row][0] != contribution):
                first = seen[product_row]
                collision = {
                    "P0_product_row": product_row.hex(),
                    "first_indices": [first[1], first[2]],
                    "first_contribution": [first[0].numerator,
                                           first[0].denominator],
                    "second_indices": [left, right],
                    "second_contribution": [contribution.numerator,
                                            contribution.denominator],
                    "partial_sum": [(first[0] + contribution).numerator,
                                    (first[0] + contribution).denominator],
                }
                break
            seen[product_row] = (contribution, left, right)
        if collision is not None:
            break
    require(collision is not None and collision["partial_sum"] == [0, 1],
            "signed product collision control changed")

    odd_cycle_terms = sum(count for cycle, count in cycle_histogram[0].items()
                          if any(length % 2 for length in cycle))
    require(odd_cycle_terms == 5376 + 576 == 5952,
            "odd-cycle obstruction census changed")
    same_colour_cell_terms = sum(
        1 for row in factors[0]
        if any((lambda cell: cell[2] == cell[3])(T2.BASE.CELLS[cell_id])
               for cell_id in row)
    )
    require(same_colour_cell_terms,
            "standard bipartite determinant obstruction disappeared")

    quotient_masses = [abs(Fraction(item[1], item[2]))
                       for item in raw["residual"]]
    mass_gcd = 0
    for value in quotient_masses:
        require(value.denominator == 1, "mass gcd expects integers")
        mass_gcd = math.gcd(mass_gcd, value.numerator)
    require(mass_gcd == 72, "sparse residual orbit-mass scale changed")
    total_mass = sum(Fraction(item[1], item[2]) for item in raw["residual"])
    result = {
        "status": "UNAUDITED exact sparse-R8 factorization/unary referee",
        "input_sha256": sha256(INPUT.read_bytes()).hexdigest(),
        "input_logical_sha256": raw["result_sha256"],
        "labelled_support": len(actual),
        "labelled_coefficients_integral": True,
        "orbit_mass_gcd": mass_gcd,
        "square_scale": "72^2/2304 = 9/4",
        "square_total_orbit_mass": [(total_mass * total_mass).numerator,
                                    (total_mass * total_mass).denominator],
        "square_normalized_total_mass": [
            (total_mass * total_mass * Fraction(2304, 72**2)).numerator,
            (total_mass * total_mass * Fraction(2304, 72**2)).denominator,
        ],
        "factorization": (
            "R8' = m_0 P_0 + m_1 P_1 + m_2 P_2, where m_c is the four-cell "
            "pure anchor monomial on M0. Each P_c is an integral degree-eight "
            "polynomial in non-anchor cells, supported on site-2-regular "
            "multigraphs using at every site one port of each colour other "
            "than c."
        ),
        "factor_support_per_colour": {str(c): len(factors[c])
                                      for c in T2.BASE.COLORS},
        "factor_coefficient_histogram": {
            str(c): {str(value): count for value, count in
                     sorted(coefficient_histogram[c].items())}
            for c in T2.BASE.COLORS
        },
        "factor_site_cycle_histogram": {
            str(c): {"+".join(map(str, cycle)): count for cycle, count in
                     sorted(cycle_histogram[c].items())}
            for c in T2.BASE.COLORS
        },
        "ordinary_hafnian_product_obstruction": {
            "odd_cycle_terms_in_P0": odd_cycle_terms,
            "cycle_types": {"5+3": cycle_histogram[0][(5, 3)],
                            "3+3+2": cycle_histogram[0][(3, 3, 2)]},
            "conclusion": (
                "P0 is not in the span of G_w*G_complement(w), even when G_w "
                "retains all 60 M0-avoiding perfect matchings. Every monomial "
                "in such a product is the union of two site perfect matchings "
                "and therefore has only even site cycles, whereas P0 has 5952 "
                "nonzero odd-cycle monomials."
            ),
        },
        "single_port_hafnian_pfaffian_guard": (
            "P0 is not a single ordinary 16-port hafnian or Pfaffian with one "
            "scalar multiple of the corresponding cell variable per entry. "
            "All 96 nonphysical complementary-port cells occur somewhere in "
            "P0, so such a matrix would have all 96 edges live and hence all "
            "368064 perfect-matching monomials; P0 has only 49392. Distinct "
            "port matchings give distinct cell monomials, so Pfaffian signs "
            "cannot cancel the missing terms."
        ),
        "standard_bipartite_determinant_guard": {
            "P0_terms_using_a_same_colour_port_edge": same_colour_cell_terms,
            "conclusion": (
                "The natural determinant/permanent from colour-1 ports to "
                "colour-2 ports uses only cross-colour cells. P0 has nonzero "
                "terms containing 11 or 22 cells, so it is not that binary "
                "cycle-cover determinant or permanent."
            ),
        },
        "unary_cross_term_controls": unary_controls,
        "grade16_reduction": (
            "For c!=d, every monomial of m_c*m_d*P_c*P_d is the unique K16 "
            "term of a literal mixed H_w times a K16 degree-20 multiplier. "
            "Therefore [R8'^2] = sum_c [m_c^2 P_c^2] in gr_K^16(R/I_mix)."
        ),
        "signed_collision_control": collision,
        "collision_guard": (
            "The three surviving P_c^2 are signed. Product contributions "
            "must be collected by their degree-24 monomial (and then by row "
            "orbit); the frozen collision already cancels -2 against +2."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("sparse R8 factorization referee: PASS")
    print("factor supports:", [len(factors[c]) for c in T2.BASE.COLORS])
    print("mass scale / square:", mass_gcd, total_mass * total_mass)
    print("collision:", collision)
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
