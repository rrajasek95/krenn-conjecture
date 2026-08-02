#!/usr/bin/env python3
"""Exact h=3 multi-label target-Koszul selected-row no-go.

This checker audits the bounded scalar/word-tag model in
``notes/h3-multilabel-target-koszul-crossword-no-go.md``.  It combines the
three target/residue cap graphs, diagonal anchors, a crossed target-zero
row, the h=3 adjacent-power target representatives, and the exact missing
full-word rows of the direct-free and tilted selected-cap packets.

It is deliberately not a checker for the full tensor-valued EqSystem and
does not construct a physical relative Rees complex.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json


Q = Fraction
ZERO = Q(0)
ONE = Q(1)
COLORS = range(3)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def zeros(rows, columns):
    return [[ZERO for _ in range(columns)] for _ in range(rows)]


def rank(matrix):
    if not matrix:
        return 0
    work = [list(row) for row in matrix]
    rows = len(work)
    columns = len(work[0])
    result = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(result, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[result], work[pivot] = work[pivot], work[result]
        scale = work[result][column]
        work[result] = [entry / scale for entry in work[result]]
        for row in range(rows):
            if row == result:
                continue
            coefficient = work[row][column]
            if coefficient:
                work[row] = [
                    entry - coefficient * pivot_entry
                    for entry, pivot_entry in zip(work[row], work[result])
                ]
        result += 1
    return result


def nullspace(matrix):
    """Return a column-basis of the rational right kernel."""
    if not matrix:
        return []
    work = [list(row) for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivots = []
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(rows):
            if row != pivot_row and work[row][column]:
                coefficient = work[row][column]
                work[row] = [
                    entry - coefficient * pivot_entry
                    for entry, pivot_entry in zip(work[row], work[pivot_row])
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    free = [column for column in range(columns) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [ZERO] * columns
        vector[free_column] = ONE
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -work[row][free_column]
        basis.append(vector)
    return basis


def columns_to_matrix(columns, rows=None):
    if not columns:
        return zeros(rows or 0, 0)
    return [[column[row] for column in columns] for row in range(len(columns[0]))]


def apply(matrix, vector):
    return [
        sum((entry * coefficient for entry, coefficient in zip(row, vector)), ZERO)
        for row in matrix
    ]


def vector_add(*vectors):
    require(vectors, "no vectors to add")
    require(all(len(vector) == len(vectors[0]) for vector in vectors),
            "vector dimensions disagree")
    return [
        sum((vector[index] for vector in vectors), ZERO)
        for index in range(len(vectors[0]))
    ]


def scale(scalar, vector):
    return [scalar * entry for entry in vector]


def basis_vector(size, index):
    result = [ZERO] * size
    result[index] = ONE
    return result


def symmetric_monomials(degree, variables=3):
    if variables == 1:
        return ((degree,),)
    answer = []
    for first in range(degree + 1):
        for tail in symmetric_monomials(degree - first, variables - 1):
            answer.append((first,) + tail)
    return tuple(answer)


def koszul_basis(total_degree, exterior_degree):
    symmetric_degree = total_degree - exterior_degree
    if symmetric_degree < 0:
        return ()
    return tuple(
        (wedge, monomial)
        for wedge in combinations(COLORS, exterior_degree)
        for monomial in symmetric_monomials(symmetric_degree)
    )


def koszul_differential(total_degree, exterior_degree):
    """Matrix K_p -> K_{p-1} for the regular target sequence X0,X1,X2."""
    source = koszul_basis(total_degree, exterior_degree)
    target = koszul_basis(total_degree, exterior_degree - 1)
    target_index = {item: index for index, item in enumerate(target)}
    matrix = zeros(len(target), len(source))
    for column, (wedge, monomial) in enumerate(source):
        for position, variable in enumerate(wedge):
            next_wedge = wedge[:position] + wedge[position + 1 :]
            next_monomial = list(monomial)
            next_monomial[variable] += 1
            row = target_index[(next_wedge, tuple(next_monomial))]
            matrix[row][column] += ONE if position % 2 == 0 else -ONE
    return matrix


def check_target_koszul_exactness():
    ledger = {}
    for total_degree in (2, 3):
        dimensions = [
            len(koszul_basis(total_degree, exterior_degree))
            for exterior_degree in range(total_degree + 1)
        ]
        ranks = {}
        differentials = {}
        for exterior_degree in range(1, total_degree + 1):
            matrix = koszul_differential(total_degree, exterior_degree)
            differentials[exterior_degree] = matrix
            ranks[exterior_degree] = rank(matrix)
        for exterior_degree in range(1, total_degree):
            outgoing_rank = ranks[exterior_degree]
            incoming_rank = ranks[exterior_degree + 1]
            require(
                dimensions[exterior_degree] - outgoing_rank == incoming_rank,
                f"Koszul homology survived in degree {total_degree}/{exterior_degree}",
            )
            composition = columns_to_matrix(
                [apply(differentials[exterior_degree], column)
                 for column in zip(*differentials[exterior_degree + 1])],
                rows=len(differentials[exterior_degree]),
            )
            require(
                all(entry == ZERO for row in composition for entry in row),
                "successive Koszul differentials do not compose to zero",
            )
        top = total_degree
        require(
            dimensions[top] - ranks[top] == 0,
            f"top target wedge survived at total degree {total_degree}",
        )
        ledger[str(total_degree)] = {
            "dimensions": dimensions,
            "ranks": [ranks[index] for index in sorted(ranks)],
        }
    require(ledger["2"] == {"dimensions": [6, 9, 3], "ranks": [6, 3]},
            "degree-two Koszul ledger changed")
    require(ledger["3"] == {"dimensions": [10, 18, 9, 1], "ranks": [10, 8, 1]},
            "degree-three Koszul ledger changed")
    return ledger


def wedge(vectors):
    """Exterior product in coordinate form."""
    result = {(): ONE}
    for vector in vectors:
        next_result = {}
        for support, coefficient in result.items():
            for index, value in enumerate(vector):
                if not value or index in support:
                    continue
                inversions = sum(existing > index for existing in support)
                ordered = tuple(sorted(support + (index,)))
                signed = coefficient * value * (-ONE if inversions % 2 else ONE)
                next_result[ordered] = next_result.get(ordered, ZERO) + signed
                if not next_result[ordered]:
                    del next_result[ordered]
        result = next_result
    return result


def contract(exterior, target_index):
    """Contract by the target covector dual to X_target_index."""
    answer = {}
    for support, coefficient in exterior.items():
        if target_index not in support:
            continue
        position = support.index(target_index)
        reduced = support[:position] + support[position + 1 :]
        value = coefficient * (-ONE if position % 2 else ONE)
        answer[reduced] = answer.get(reduced, ZERO) + value
        if not answer[reduced]:
            del answer[reduced]
    return answer


def exterior_to_vector(exterior, dimension):
    require(all(len(support) == 1 for support in exterior),
            "exterior expression is not linear")
    result = [ZERO] * dimension
    for support, coefficient in exterior.items():
        result[support[0]] += coefficient
    return result


DIRECT_FREE_FAILURES = (
    ((0, 0, 0, 0, 0, 0), 0, 0, ZERO, ONE),
    ((0, 1, 2, 1, 1, 2), 2, 2, ONE, ZERO),
    ((0, 1, 2, 2, 1, 2), 2, 1, ONE, ZERO),
    ((0, 1, 2, 2, 1, 2), 2, 2, ONE, ZERO),
    ((1, 1, 1, 1, 1, 1), 1, 1, ZERO, ONE),
    ((2, 2, 2, 2, 2, 2), 2, 2, ZERO, ONE),
)


TILTED_FAILURES = (
    ((0, 0, 0, 0, 0, 0), 0, 0, ZERO, ONE),
    ((0, 0, 2, 0, 1, 2), 2, 2, Q(1, 2), ZERO),
    ((0, 2, 2, 0, 1, 2), 0, 2, Q(-3, 2), ZERO),
    ((0, 2, 2, 0, 1, 2), 2, 0, Q(1, 2), ZERO),
    ((0, 2, 2, 0, 1, 2), 2, 2, Q(-1, 4), ZERO),
    ((1, 1, 1, 1, 1, 1), 1, 1, ZERO, ONE),
    ((2, 2, 2, 2, 2, 2), 2, 2, ZERO, ONE),
)


PACKETS = {
    "direct_free": {
        "kappa": Q(-1, 4),
        "failures": DIRECT_FREE_FAILURES,
        "mixed_tags": ("12112", "12212"),
    },
    "tilted": {
        "kappa": Q(-5, 2),
        "failures": TILTED_FAILURES,
        "mixed_tags": ("02012", "22012"),
    },
}


def audit_failure_locus(name, data):
    failures = data["failures"]
    pure = [item for item in failures if item[3] == 0 and item[4] == 1]
    mixed = [item for item in failures if item[3] != 0 and item[4] == 0]
    require(
        [(word, i, j) for word, i, j, _value, _target in pure]
        == [((color,) * 6, color, color) for color in COLORS],
        f"{name} pure target failures changed",
    )
    require(len(mixed) == len(failures) - 3, f"{name} mixed failure count")
    require(all(word[0] == 0 for word, *_rest in mixed),
            f"{name} distinguished x-label changed")
    odd_tags = tuple(sorted({"".join(map(str, word[1:])) for word, *_ in mixed}))
    require(odd_tags == data["mixed_tags"], f"{name} odd mixed tags changed")
    require("00000" not in odd_tags, f"{name} mixed row became the pure residue")
    return pure, mixed, odd_tags


def audit_multilabel_packet(name, data):
    pure, mixed, odd_tags = audit_failure_locus(name, data)
    response_tags = ("00000", "11111", "22222") + odd_tags
    response_index = {tag: index for index, tag in enumerate(response_tags)}
    response_dimension = len(response_tags)
    total_dimension = 3 + response_dimension

    # Phi sends each target label to its same-label pure odd residue.
    phi = zeros(response_dimension, 3)
    for color in COLORS:
        phi[color][color] = ONE

    def graph(target):
        return target + apply(phi, target)

    def sheared(vector):
        target = vector[:3]
        response = vector[3:]
        return target + vector_add(response, scale(-ONE, apply(phi, target)))

    target_basis = [basis_vector(3, color) for color in COLORS]
    anchors = [graph(vector) for vector in target_basis]
    require(all(sheared(anchor)[3:] == [ZERO] * response_dimension
                for anchor in anchors),
            f"{name} graph shear did not flatten the anchors")
    require(rank(columns_to_matrix([anchor[:3] for anchor in anchors])) == 3,
            f"{name} target anchors lost independence")

    scalar_zero_cap = scale(-ONE, vector_add(*anchors))
    require(sheared(scalar_zero_cap)[3:] == [ZERO] * response_dimension,
            f"{name} scalar-zero cap left the graph")

    # Existing crossed target-zero selected row has zero low target/residue
    # readout.  The missing mixed full-word rows are tested as the smallest
    # possible added d0-boundaries, preserving their exact coefficients and
    # their odd word tags after exposing x.
    crossed = [ZERO] * total_dimension
    missing_columns = []
    for word, _i, _j, value, target in mixed:
        require(target == 0 and value != 0, "mixed failure ledger changed")
        tag = "".join(map(str, word[1:]))
        column = [ZERO] * response_dimension
        column[response_index[tag]] = value
        missing_columns.append(column)
    missing_boundary = columns_to_matrix(missing_columns, rows=response_dimension)
    require(rank(missing_boundary) == 2, f"{name} mixed word span is not two")

    desired_response = basis_vector(response_dimension, response_index["00000"])
    require(
        rank([list(row) for row in missing_boundary] + []) == 2,
        f"{name} missing boundary rank mutation",
    )
    require(
        rank(columns_to_matrix(missing_columns + [desired_response])) == 3,
        f"{name} missing rows unexpectedly span the pure odd residue",
    )

    # h=3 adjacent-power representatives from the scalar-gate normal form.
    # Their target parts are s^2*T0 and s^2*TN.  In the strict selected-row
    # model no cross-word row fixes their defects, so use the two exact mixed
    # word directions as a countermodel.  This preserves every target
    # representative while making the missing source datum executable.
    s = Q(2)
    target0 = [Q(1), Q(2), Q(3)]
    targetn = [Q(2), Q(-1), Q(4)]
    defect0 = missing_columns[0]
    defectn = next(
        column for column in missing_columns
        if rank(columns_to_matrix([defect0, column])) == 2
    )

    def adjacent(target, defect):
        scaled_target = scale(s * s, target)
        return scaled_target + vector_add(apply(phi, scaled_target), defect)

    adjacent0 = adjacent(target0, defect0)
    adjacentn = adjacent(targetn, defectn)
    require(sheared(adjacent0)[3:] == defect0,
            f"{name} first adjacent defect changed")
    require(sheared(adjacentn)[3:] == defectn,
            f"{name} second adjacent defect changed")

    # Target cancellation by all three anchors leaves exactly the two
    # adjacent defects.  Adding every missing mixed row adds no new odd tag.
    generators = anchors + [scalar_zero_cap, adjacent0, adjacentn, crossed]
    target_matrix = columns_to_matrix([vector[:3] for vector in generators])
    response_matrix = columns_to_matrix([vector[3:] for vector in generators])
    kernel = nullspace(target_matrix)
    target_zero_responses = [apply(response_matrix, vector) for vector in kernel]
    require(rank(columns_to_matrix(target_zero_responses)) == 2,
            f"{name} target-zero response span changed")
    require(
        rank(columns_to_matrix(target_zero_responses + [desired_response])) == 3,
        f"{name} target cancellation manufactured Y0",
    )

    # Exterior/determinant test after graph shear.  Contract every wedge of
    # two or three generators by all target coordinate covectors until a
    # linear vector remains, then retain its target-cancelled response.  The
    # result stays in the same two mixed-word directions.
    sheared_generators = [sheared(vector) for vector in generators[:-1]]
    exterior_responses = []
    for exterior_degree in (2, 3):
        for chosen in combinations(sheared_generators, exterior_degree):
            expression = wedge(chosen)
            for covectors in product(COLORS, repeat=exterior_degree - 1):
                contracted = expression
                for covector in covectors:
                    contracted = contract(contracted, covector)
                vector = exterior_to_vector(contracted, total_dimension)
                response = vector[3:]
                if any(response):
                    exterior_responses.append(response)
    require(exterior_responses, f"{name} exterior audit was vacuous")
    require(rank(columns_to_matrix(exterior_responses)) == 2,
            f"{name} exterior contractions left the mixed defect span")
    require(
        rank(columns_to_matrix(exterior_responses + [desired_response])) == 3,
        f"{name} wedge/determinant manufactured the pure odd residue",
    )

    # The two differently labelled anchors have a nonzero target wedge, and
    # the triple anchor determinant is one.  Neither is a target-zero class.
    anchor_pair = wedge((sheared_generators[0], sheared_generators[1]))
    anchor_triple = wedge(tuple(sheared_generators[:3]))
    require(anchor_pair.get((0, 1), ZERO) == 1,
            f"{name} two-label anchor wedge vanished")
    require(anchor_triple.get((0, 1, 2), ZERO) == 1,
            f"{name} anchor determinant changed")

    desired_scaled = scale(-data["kappa"], desired_response)
    require(any(desired_scaled), f"{name} desired curvature residue vanished")
    require(
        rank(columns_to_matrix(missing_columns + [desired_scaled])) == 3,
        f"{name} exact missing rows supplied -kappa*Y0",
    )

    return {
        "failures": len(data["failures"]),
        "pure_failures": len(pure),
        "mixed_failures": len(mixed),
        "odd_tags": odd_tags,
        "kappa": str(data["kappa"]),
        "missing_boundary_rank": rank(missing_boundary),
        "target_zero_response_rank": rank(columns_to_matrix(target_zero_responses)),
        "exterior_response_rank": rank(columns_to_matrix(exterior_responses)),
        "desired_augmented_rank": rank(columns_to_matrix(missing_columns + [desired_scaled])),
    }


def main():
    koszul = check_target_koszul_exactness()
    packets = {
        name: audit_multilabel_packet(name, data)
        for name, data in PACKETS.items()
    }
    record = {"koszul": koszul, "packets": packets}
    payload = json.dumps(record, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode("utf-8")).hexdigest()
    print("h=3 multi-label target-Koszul cross-word no-go: PASS")
    print("Koszul total degrees: 2 and 3 exact in positive exterior degree")
    for name in sorted(packets):
        packet = packets[name]
        print(
            f"{name}: failures={packet['failures']}, mixed odd tags="
            f"{','.join(packet['odd_tags'])}, desired rank jump="
            f"{packet['missing_boundary_rank']}->{packet['desired_augmented_rank']}"
        )
    print("sha256:", digest)


if __name__ == "__main__":
    main()
