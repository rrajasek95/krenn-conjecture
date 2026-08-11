#!/usr/bin/env python3
"""Exact genus-2 K8 Arf expansion and full-nine Pfaffian-syzygy probe.

This is deliberately a bounded proof-facing test.  It constructs a cellular
genus-2 rotation system for K8, an exact Kasteleyn orientation, four spin
twists, and the resulting 16-Pfaffian Arf formula.  It then applies the
principal Grassmann--Pluecker and Buchsbaum--Eisenbud grade tests to three
literal rows (two pure diagonal anchors and one crossed row) in two physical
two-site expansions of the same eight-site hafnian.

The result is negative: the nontrivial BE/Pluecker candidates have repeated
physical-site grade, while the squarefree Pluecker candidates are only the
four-site Pfaffian definitions within one fixed output word.  Nontrivial
spin-character multipliers also produce twisted Arf aggregates rather than
the original hafnian row.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import itertools
import json


VERTICES = tuple(range(8))
EDGES = tuple(itertools.combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
EXPECTED_LEDGER_SHA256 = (
    "5e6a7a702c8f8e633424628d87252418ed477703160c64d1d1f3e837360e77c8"
)

# A cellular orientable rotation system.  The face walk below has sixteen
# triangles and two quadrilaterals, hence Euler genus two.
ROTATION = {
    0: (1, 3, 7, 5, 4, 6, 2),
    1: (6, 5, 3, 0, 7, 4, 2),
    2: (1, 4, 3, 5, 7, 0, 6),
    3: (7, 0, 1, 5, 2, 4, 6),
    4: (2, 1, 7, 0, 5, 6, 3),
    5: (3, 1, 6, 4, 0, 7, 2),
    6: (4, 5, 1, 2, 0, 7, 3),
    7: (2, 5, 0, 3, 6, 4, 1),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(u, v):
    return (u, v) if u < v else (v, u)


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, partner in enumerate(vertices[1:], start=1):
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(rest):
            answer.append(((first, partner),) + tail)
    return tuple(answer)


def face_walks():
    seen = set()
    faces = []
    for u in VERTICES:
        for v in VERTICES:
            if u == v or (u, v) in seen:
                continue
            face = []
            dart = (u, v)
            while dart not in seen:
                seen.add(dart)
                face.append(dart)
                left, right = dart
                rotation = ROTATION[right]
                position = rotation.index(left)
                dart = (right, rotation[(position - 1) % len(rotation)])
            faces.append(tuple(face))
    require(len(seen) == 56, "the rotation stopped partitioning the darts")
    return tuple(faces)


def gf2_rref(rows, column_count):
    rows = list(rows)
    pivots = []
    pivot_row = 0
    for column in range(column_count):
        pivot = next((index for index in range(pivot_row, len(rows))
                      if (rows[index] >> column) & 1), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        for index in range(len(rows)):
            if index != pivot_row and ((rows[index] >> column) & 1):
                rows[index] ^= rows[pivot_row]
        pivots.append(column)
        pivot_row += 1
    return rows, tuple(pivots)


def gf2_rank(rows, column_count):
    return len(gf2_rref(rows, column_count)[1])


def gf2_nullspace(rows, column_count):
    reduced, pivots = gf2_rref(rows, column_count)
    free = tuple(column for column in range(column_count)
                 if column not in pivots)
    answer = []
    for free_column in free:
        vector = 1 << free_column
        for row, pivot in reversed(tuple(zip(reduced, pivots))):
            if (row & vector).bit_count() & 1:
                vector |= 1 << pivot
        answer.append(vector)
    return tuple(answer)


def gf2_solve(rows, right_hand_side, column_count):
    augmented = [row | ((value & 1) << column_count)
                 for row, value in zip(rows, right_hand_side, strict=True)]
    reduced, _pivots = gf2_rref(augmented, column_count + 1)
    variable_mask = (1 << column_count) - 1
    require(not any(not (row & variable_mask)
                        and ((row >> column_count) & 1) for row in reduced),
            "the Kasteleyn face system became inconsistent")
    solution = 0
    for row in reduced:
        variables = row & variable_mask
        if not variables:
            continue
        pivot = (variables & -variables).bit_length() - 1
        if (row >> column_count) & 1:
            solution |= 1 << pivot
    return solution


def matching_mask(matching):
    return sum(1 << EDGE_INDEX[edge(*pair)] for pair in matching)


def crossing_parity(matching):
    crossings = 0
    for (a, b), (c, d) in itertools.combinations(matching, 2):
        crossings += int(a < c < b < d or c < a < d < b)
    return crossings & 1


def polynomial_add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def polynomial_scale(polynomial, scalar):
    return {monomial: scalar * coefficient
            for monomial, coefficient in polynomial.items()
            if scalar * coefficient}


def polynomial_multiply(left, right):
    answer = Counter()
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            answer[tuple(sorted(left_monomial + right_monomial))] += (
                left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in answer.items()
            if coefficient}


def pfaffian_polynomial(vertices, sector, orientation, edge_labels):
    answer = Counter()
    for matching in matchings(tuple(vertices)):
        coefficient = -1 if crossing_parity(matching) else 1
        monomial = []
        for pair in matching:
            physical_edge = edge(*pair)
            index = EDGE_INDEX[physical_edge]
            exponent = ((orientation >> index) & 1)
            exponent ^= ((sector & edge_labels[physical_edge]).bit_count() & 1)
            if exponent:
                coefficient = -coefficient
            monomial.append(f"x{physical_edge[0]}{physical_edge[1]}")
        answer[tuple(sorted(monomial))] += coefficient
    return dict(answer)


def pfaffian_numeric(vertices, values, sector, orientation, edge_labels):
    total = 0
    for matching in matchings(tuple(vertices)):
        coefficient = -1 if crossing_parity(matching) else 1
        term = 1
        for pair in matching:
            physical_edge = edge(*pair)
            index = EDGE_INDEX[physical_edge]
            exponent = ((orientation >> index) & 1)
            exponent ^= ((sector & edge_labels[physical_edge]).bit_count() & 1)
            if exponent:
                coefficient = -coefficient
            term *= values[physical_edge]
        total += coefficient * term
    return total


def hafnian_numeric(vertices, values):
    return sum(
        product(values[edge(*pair)] for pair in matching)
        for matching in matchings(tuple(vertices))
    )


def product(values):
    answer = 1
    for value in values:
        answer *= value
    return answer


def decorated_cell(pair, word):
    u, v = edge(*pair)
    return f"{u}{v}:{word[u]}{word[v]}"


def hafnian_word(word):
    answer = Counter()
    for matching in matchings(VERTICES):
        answer[tuple(sorted(decorated_cell(pair, word)
                            for pair in matching))] += 1
    return dict(answer)


def chart_parts(word, chart_edge):
    direct = Counter()
    response = Counter()
    chart_edge = edge(*chart_edge)
    for matching in matchings(VERTICES):
        monomial = tuple(sorted(decorated_cell(pair, word)
                                for pair in matching))
        if chart_edge in matching:
            direct[monomial] += 1
        else:
            response[monomial] += 1
    return dict(direct), dict(response)


def site_colour_degree(monomial):
    degree = Counter()
    for label in monomial:
        u, v = int(label[0]), int(label[1])
        a, b = int(label[3]), int(label[4])
        degree[(u, a)] += 1
        degree[(v, b)] += 1
    return tuple(sorted(degree.items()))


def main():
    faces = face_walks()
    face_lengths = Counter(map(len, faces))
    require(face_lengths == Counter({3: 16, 4: 2}),
            f"the genus-2 face census changed: {face_lengths}")
    genus = (2 - len(VERTICES) + len(EDGES) - len(faces)) // 2
    require(genus == 2, f"the rotation genus changed: {genus}")

    face_rows = []
    canonical_disagreement = []
    for face in faces:
        row = 0
        disagreement = 0
        for u, v in face:
            row ^= 1 << EDGE_INDEX[edge(u, v)]
            disagreement ^= int(u > v)
        face_rows.append(row)
        canonical_disagreement.append(disagreement)
    require(gf2_rank(face_rows, len(EDGES)) == 17,
            "the cellular face-boundary rank changed")

    # Reverse a canonical low-to-high edge when its orientation bit is one.
    # Each coherently oriented face must then have odd disagreement count.
    orientation = gf2_solve(
        face_rows,
        tuple(1 ^ value for value in canonical_disagreement),
        len(EDGES),
    )
    for face, expected in zip(faces, canonical_disagreement, strict=True):
        actual = expected
        for u, v in face:
            actual ^= (orientation >> EDGE_INDEX[edge(u, v)]) & 1
        require(actual == 1, "a face lost its Kasteleyn parity")

    # Four cocycles modulo the seven vertex coboundaries give H^1(Sigma_2,F2).
    cocycles = gf2_nullspace(face_rows, len(EDGES))
    require(len(cocycles) == 11, "the cocycle dimension changed")
    coboundaries = []
    for vertex in VERTICES[:-1]:
        coboundaries.append(sum(
            1 << EDGE_INDEX[edge(vertex, other)]
            for other in VERTICES if other != vertex
        ))
    require(gf2_rank(coboundaries, len(EDGES)) == 7,
            "the vertex-coboundary rank changed")
    quotient_basis = []
    span = list(coboundaries)
    for cocycle in cocycles:
        if gf2_rank(span + [cocycle], len(EDGES)) > len(span):
            span.append(cocycle)
            quotient_basis.append(cocycle)
    require(len(quotient_basis) == 4,
            "the genus-2 cohomology quotient changed")
    edge_labels = {
        physical_edge: sum(
            (((cocycle >> EDGE_INDEX[physical_edge]) & 1) << coordinate)
            for coordinate, cocycle in enumerate(quotient_basis)
        )
        for physical_edge in EDGES
    }

    # The Kasteleyn sign of a matching factors through its four-bit homology
    # class.  Its truth table is a nondegenerate quadratic refinement.
    quadratic_table = {}
    for matching in matchings(VERTICES):
        mask = matching_mask(matching)
        homology = 0
        for physical_edge in matching:
            homology ^= edge_labels[edge(*physical_edge)]
        sign_bit = crossing_parity(matching) ^ ((orientation & mask).bit_count() & 1)
        if homology in quadratic_table:
            require(quadratic_table[homology] == sign_bit,
                    "the Kasteleyn sign stopped factoring through homology")
        quadratic_table[homology] = sign_bit
    require(len(quadratic_table) == 16,
            "the matching homology classes stopped being exhaustive")

    values = [quadratic_table[mask] for mask in range(16)]
    anf = values[:]
    for coordinate in range(4):
        for mask in range(16):
            if (mask >> coordinate) & 1:
                anf[mask] ^= anf[mask ^ (1 << coordinate)]
    require(not any(anf[mask] for mask in range(16)
                    if mask.bit_count() > 2),
            "the spin refinement acquired degree above two")
    polar_rows = [0] * 4
    for mask, coefficient in enumerate(anf):
        if coefficient and mask.bit_count() == 2:
            left, right = tuple(index for index in range(4)
                                if (mask >> index) & 1)
            polar_rows[left] |= 1 << right
            polar_rows[right] |= 1 << left
    require(gf2_rank(polar_rows, 4) == 4,
            "the spin quadratic form became degenerate")
    gauss_sum = sum((-1) ** value for value in values)
    require(abs(gauss_sum) == 4,
            f"the genus-2 Gauss sum changed: {gauss_sum}")

    arf_coefficients = []
    for sector in range(16):
        fourier = sum(
            (-1) ** (values[homology]
                     + ((sector & homology).bit_count() & 1))
            for homology in range(16)
        )
        coefficient = Fraction(fourier, 16)
        require(abs(coefficient) == Fraction(1, 4),
                "an Arf coefficient stopped being plus/minus one quarter")
        arf_coefficients.append(coefficient)

    # Termwise verification of the 16-Pfaffian formula, followed by a dense
    # integer evaluation as an independent polynomial-level guard.
    for matching in matchings(VERTICES):
        homology = 0
        mask = matching_mask(matching)
        for physical_edge in matching:
            homology ^= edge_labels[edge(*physical_edge)]
        coefficient = sum(
            arf_coefficients[sector]
            * (-1) ** (
                crossing_parity(matching)
                + ((orientation & mask).bit_count() & 1)
                + ((sector & homology).bit_count() & 1)
            )
            for sector in range(16)
        )
        require(coefficient == 1,
                "the Arf sum stopped giving an unsigned matching")
    numeric_values = {
        physical_edge: (7 * physical_edge[0] + 11 * physical_edge[1] + 3) % 17 - 8
        for physical_edge in EDGES
    }
    numeric_hafnian = hafnian_numeric(VERTICES, numeric_values)
    numeric_arf = sum(
        arf_coefficients[sector]
        * pfaffian_numeric(VERTICES, numeric_values, sector,
                           orientation, edge_labels)
        for sector in range(16)
    )
    require(numeric_arf == numeric_hafnian,
            "the dense Arf/Pfaffian evaluation disagrees with the hafnian")

    # One literal h=3 packet: two pure diagonal anchor words and the crossed
    # (0,1) word with pure residual colour 2.  Expand each on the physical
    # 01 and 02 charts.  These are the direct-plus-response full-nine rows.
    row_words = {
        "diagonal_00": (0,) * 8,
        "diagonal_11": (1,) * 8,
        "crossed_01_over_2": (0, 1, 2, 2, 2, 2, 2, 2),
    }
    chart_ledger = {}
    word_degrees = {}
    for row_label, word in row_words.items():
        full = hafnian_word(word)
        require(len(full) == 105, "a literal K8 word lost a matching")
        degrees = {site_colour_degree(monomial) for monomial in full}
        require(len(degrees) == 1,
                f"a literal row lost its fine multidegree: {row_label}")
        word_degrees[row_label] = next(iter(degrees))
        for chart in ((0, 1), (0, 2)):
            direct, response = chart_parts(word, chart)
            require((len(direct), len(response)) == (15, 90),
                    f"the full-nine split changed: {row_label}, {chart}")
            require(polynomial_add(direct, response) == full,
                    f"the two-site Laplace row changed: {row_label}, {chart}")
            chart_ledger[f"{row_label}@{chart[0]}{chart[1]}"] = {
                "direct_terms": len(direct),
                "response_terms": len(response),
            }
    require(len(set(word_degrees.values())) == 3,
            "the two anchors and crossed row lost their separate source grades")

    # Principal Pfaffian Pluecker quadrics are indexed by an even base S and
    # four new vertices.  All four terms have degree 2*S + the four new
    # vertices.  Only S=empty is squarefree.  Those 70 relations are exactly
    # the four-site Pfaffian definitions; multiplying by one of the three
    # complement matchings gives 210 tautological squarefree lifts per word.
    pluecker_by_base_size = Counter()
    squarefree_pluecker = 0
    for base_size in (0, 2, 4):
        for base in itertools.combinations(VERTICES, base_size):
            complement = tuple(vertex for vertex in VERTICES
                               if vertex not in base)
            for four in itertools.combinations(complement, 4):
                degree = tuple(2 if vertex in base else 1 if vertex in four else 0
                               for vertex in VERTICES)
                pluecker_by_base_size[base_size] += 1
                squarefree_pluecker += int(max(degree) <= 1)
    require(pluecker_by_base_size == Counter({0: 70, 2: 420, 4: 70}),
            f"the principal Pluecker census changed: {pluecker_by_base_size}")
    require(squarefree_pluecker == 70,
            "a nonempty-base Pluecker relation became squarefree")

    # Verify all empty-base identities in every spin sector.  They are the
    # defining four-site Pfaffian expansions, hence add no new row relation.
    empty_base_checks = 0
    for sector in range(16):
        for four in itertools.combinations(VERTICES, 4):
            i, j, k, ell = four
            p4 = pfaffian_polynomial(four, sector, orientation, edge_labels)
            pij = pfaffian_polynomial((i, j), sector, orientation, edge_labels)
            pkl = pfaffian_polynomial((k, ell), sector, orientation, edge_labels)
            pik = pfaffian_polynomial((i, k), sector, orientation, edge_labels)
            pjl = pfaffian_polynomial((j, ell), sector, orientation, edge_labels)
            pil = pfaffian_polynomial((i, ell), sector, orientation, edge_labels)
            pjk = pfaffian_polynomial((j, k), sector, orientation, edge_labels)
            identity = polynomial_add(
                p4,
                polynomial_scale(polynomial_multiply(pij, pkl), -1),
                polynomial_multiply(pik, pjl),
                polynomial_scale(polynomial_multiply(pil, pjk), -1),
            )
            require(not identity, "an empty-base Pfaffian definition failed")
            empty_base_checks += 1
    require(empty_base_checks == 1120,
            "the sectorwise empty-base check count changed")

    # Every odd-principal BE kernel row has one doubled physical vertex.
    # Nonnegative source multipliers cannot return it to the squarefree K8
    # coefficient grade.  Audit all odd sizes relevant inside K8.
    be_by_odd_size = Counter()
    be_squarefree = 0
    for odd_size in (3, 5, 7):
        for subset in itertools.combinations(VERTICES, odd_size):
            for row_vertex in subset:
                degree = tuple(2 if vertex == row_vertex
                               else 1 if vertex in subset else 0
                               for vertex in VERTICES)
                be_by_odd_size[odd_size] += 1
                be_squarefree += int(max(degree) <= 1)
    require(be_by_odd_size == Counter({3: 168, 5: 280, 7: 56}),
            f"the BE grade census changed: {be_by_odd_size}")
    require(be_squarefree == 0,
            "a Buchsbaum--Eisenbud row became squarefree")

    # Arf descent is a second independent guard.  Multiplication in one spin
    # sector by an edge of nonzero cohomology label twists the coefficient
    # vector by a nontrivial character.  That vector is never proportional to
    # the original Arf aggregate, so it is not an original hafnian row.
    label_histogram = Counter(edge_labels.values())
    require(label_histogram[0] == 12
            and sum(label_histogram.values()) == 28,
            f"the edge homology census changed: {label_histogram}")
    nontrivial_descent_checks = 0
    for homology in sorted(set(edge_labels.values()) - {0}):
        twisted = tuple(
            arf_coefficients[sector]
            * (-1) ** ((sector & homology).bit_count() & 1)
            for sector in range(16)
        )
        require(twisted != tuple(arf_coefficients)
                and twisted != tuple(-value for value in arf_coefficients),
                "a nontrivial spin character descended to the hafnian row")
        nontrivial_descent_checks += 1
    require(nontrivial_descent_checks == 9,
            "the nontrivial Arf-character count changed")

    ledger = {
        "surface": {
            "vertices": 8,
            "edges": 28,
            "faces": len(faces),
            "face_lengths": dict(face_lengths),
            "genus": genus,
            "face_boundary_rank": 17,
        },
        "kasteleyn": {
            "reversed_edge_indices": [index for index in range(28)
                                      if (orientation >> index) & 1],
            "cocycle_dimension": len(cocycles),
            "coboundary_dimension": 7,
            "spin_dimension": len(quotient_basis),
            "matching_homology_classes": len(quadratic_table),
            "quadratic_polar_rank": gf2_rank(polar_rows, 4),
            "gauss_sum": gauss_sum,
            "arf_signs": [int(4 * value) for value in arf_coefficients],
            "numeric_hafnian": numeric_hafnian,
        },
        "literal_two_chart_packet": chart_ledger,
        "literal_row_grades_distinct": True,
        "pluecker": {
            "by_base_size": dict(pluecker_by_base_size),
            "squarefree_relations": squarefree_pluecker,
            "sectorwise_empty_base_checks": empty_base_checks,
            "squarefree_complement_lifts_per_word": 210,
            "verdict": (
                "the only squarefree candidates are four-site Pfaffian "
                "definitions inside one fixed decorated word"
            ),
        },
        "buchsbaum_eisenbud": {
            "by_odd_size": dict(be_by_odd_size),
            "squarefree_rows": be_squarefree,
            "verdict": "every row has one doubled physical site",
        },
        "arf_descent": {
            "zero_label_edges": label_histogram[0],
            "nonzero_label_edges": 28 - label_histogram[0],
            "distinct_nontrivial_characters": nontrivial_descent_checks,
            "verdict": (
                "nontrivial sector multipliers give twisted Arf aggregates, "
                "not original hafnian rows"
            ),
        },
        "consequence": (
            "the direct genus-2 GP/BE probe yields neither a literal "
            "Component-III residual annihilator nor the scalar-zero "
            "single-edge cap landing; it reproduces only existing wordwise "
            "Laplace identities"
        ),
        "scope": (
            "standard principal-Pfaffian Grassmann--Pluecker quadrics and "
            "odd-principal Buchsbaum--Eisenbud kernel rows on one literal "
            "three-word, two-chart h=3 packet; no claim about higher derived "
            "cross-sector constructions"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"genus-2 Pfaffian probe ledger changed: {digest}")

    print("N=8 genus-2 Arf/full-nine Pfaffian probe: PASS")
    print("K8 embedding: 16 triangles + 2 quadrilaterals; genus 2")
    print("16-Pfaffian expansion: all 105 matching signs verified")
    print("literal packet: 3 rows x 2 charts, each 15+90 terms")
    print("GP/BE verdict: no new squarefree cross-word source identity")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
