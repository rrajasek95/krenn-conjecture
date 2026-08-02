#!/usr/bin/env python3
"""Exact linear audit of the common-coloop anchor/polar response quotient.

On a fixed attainable scalar fibre, the full-nine anchor difference makes
all three diagonal increments factor through the same tangent response.
The checker compares the original tangent-parameter clean system with the
smaller response-quotient system, verifies invariance under the choice of
scalar lift, and exercises the polar-cokernel and each of the three
forced-diagonal strata.  Standard library only; live under -O and -I -S.
Research evidence only.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def q(value):
    return value if isinstance(value, Fraction) else Fraction(value)


def matrix(rows):
    result = tuple(tuple(q(value) for value in row) for row in rows)
    if result:
        width = len(result[0])
        require(all(len(row) == width for row in result),
                "a ragged matrix was supplied")
    return result


def matmul(left, right):
    require(not left or not right or len(left[0]) == len(right),
            ("matrix dimensions do not compose",
             len(left), len(left[0]) if left else 0,
             len(right), len(right[0]) if right else 0))
    if not left:
        return ()
    width = len(right[0]) if right else 0
    return tuple(
        tuple(
            sum(left[row][inner] * right[inner][column]
                for inner in range(len(right)))
            for column in range(width)
        )
        for row in range(len(left))
    )


def matvec(source, vector):
    require(not source or len(source[0]) == len(vector),
            "matrix and vector dimensions do not compose")
    return tuple(
        sum(entry * value for entry, value in zip(row, vector))
        for row in source
    )


def add_vectors(*vectors):
    require(vectors, "no vectors were supplied")
    require(len({len(vector) for vector in vectors}) == 1,
            "vector dimensions disagree")
    return tuple(sum(entries) for entries in zip(*vectors))


def scale_vector(scalar, vector):
    return tuple(q(scalar) * value for value in vector)


def dot(left, right):
    require(len(left) == len(right), "dot-product dimensions disagree")
    return sum(a * b for a, b in zip(left, right))


def columns_to_matrix(columns, height):
    require(all(len(column) == height for column in columns),
            "column height changed")
    return tuple(
        tuple(column[row] for column in columns)
        for row in range(height)
    )


def column(source, index):
    return tuple(row[index] for row in source)


def rref(source):
    work = [list(row) for row in source]
    if not work:
        return (), ()
    row_count = len(work)
    column_count = len(work[0])
    pivots = []
    pivot_row = 0
    for pivot_column in range(column_count):
        selected = next(
            (row for row in range(pivot_row, row_count)
             if work[row][pivot_column]),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        pivot = work[pivot_row][pivot_column]
        work[pivot_row] = [entry / pivot for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row:
                continue
            factor = work[row][pivot_column]
            if factor:
                work[row] = [
                    entry - factor * pivot_entry
                    for entry, pivot_entry
                    in zip(work[row], work[pivot_row])
                ]
        pivots.append(pivot_column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def rank(source):
    return len(rref(source)[1])


def solve(source, target):
    require(len(source) == len(target),
            "linear-system row count changed")
    if not source:
        return (), ()
    width = len(source[0])
    augmented = tuple(
        tuple(row) + (value,)
        for row, value in zip(source, target)
    )
    reduced, pivots_augmented = rref(augmented)
    if width in pivots_augmented:
        return None
    pivots = tuple(pivot for pivot in pivots_augmented if pivot < width)
    free = tuple(column_index for column_index in range(width)
                 if column_index not in pivots)
    particular = [Fraction(0) for _ in range(width)]
    pivot_to_row = {pivot: row for row, pivot in enumerate(pivots)}
    for pivot in pivots:
        particular[pivot] = reduced[pivot_to_row[pivot]][-1]
    kernel = []
    for free_column in free:
        vector = [Fraction(0) for _ in range(width)]
        vector[free_column] = 1
        for pivot in pivots:
            vector[pivot] = -reduced[pivot_to_row[pivot]][free_column]
        kernel.append(tuple(vector))
    return tuple(particular), tuple(kernel)


def nullspace(source):
    require(source, "nullspace needs an explicit ambient width")
    solution = solve(source, tuple(Fraction(0) for _ in source))
    require(solution is not None, "a homogeneous system became inconsistent")
    return solution[1]


def column_basis(source):
    if not source or not source[0]:
        return columns_to_matrix((), len(source)), ()
    pivots = rref(source)[1]
    basis = columns_to_matrix(
        tuple(column(source, pivot) for pivot in pivots),
        len(source),
    )
    return basis, pivots


def coordinates_in_basis(basis, vectors):
    coordinate_columns = []
    for vector in vectors:
        solution = solve(basis, vector)
        require(solution is not None,
                ("a response missed its declared basis", vector))
        particular, kernel = solution
        require(not kernel, "a declared response basis was dependent")
        coordinate_columns.append(particular)
    return columns_to_matrix(
        tuple(coordinate_columns),
        len(basis[0]) if basis else 0,
    )


ELL = matrix(((1, 1, 0, 0, 0),))[0]
RESPONSE = matrix((
    (1, 0, 0, 1, 0),
    (0, 1, 0, 1, 1),
    (0, 0, 1, 0, 1),
))
ANCHOR_ON_RESPONSE = matrix((
    (1, 0, 1),
    (0, 1, 1),
    (1, -1, 0),
))
ELL_CORRECTION = matrix((
    (2,),
    (-1,),
    (1,),
))
def outer(column_vector, row_vector):
    return tuple(
        tuple(left * right for right in row_vector)
        for left in column_vector
    )


def add_matrices(left, right):
    require(len(left) == len(right)
            and (not left or len(left[0]) == len(right[0])),
            "matrix dimensions disagree")
    return tuple(
        tuple(a + b for a, b in zip(left_row, right_row))
        for left_row, right_row in zip(left, right)
    )


DIAGONAL_MAP = add_matrices(
    matmul(ANCHOR_ON_RESPONSE, RESPONSE),
    outer(tuple(row[0] for row in ELL_CORRECTION), ELL),
)
EXPECTED_LEDGER_DIGEST = (
    "ddff27993f43fe3af46e0bcaac5bbbea82f8a7e34d60c29873af3a015c84f562"
)


def prepare_quotient(ell, response, diagonal):
    tangent_zero_columns = nullspace((ell,))
    tangent_zero = columns_to_matrix(
        tangent_zero_columns, len(ell)
    )
    response_zero = matmul(response, tangent_zero)
    diagonal_zero = matmul(diagonal, tangent_zero)
    response_basis, pivot_columns = column_basis(response_zero)
    response_columns = tuple(
        column(response_zero, index)
        for index in range(len(response_zero[0]))
    )
    coordinates = coordinates_in_basis(response_basis, response_columns)
    diagonal_hat = columns_to_matrix(
        tuple(column(diagonal_zero, pivot) for pivot in pivot_columns),
        len(diagonal),
    )
    require(matmul(diagonal_hat, coordinates) == diagonal_zero,
            "the diagonal map did not factor through response")
    require(rank(tuple(response_zero) + tuple(diagonal_zero))
            == rank(response_zero),
            "ker(response) was not contained in ker(diagonal)")
    return {
        "tangent_zero": tangent_zero,
        "response_zero": response_zero,
        "diagonal_zero": diagonal_zero,
        "response_basis": response_basis,
        "coordinates": coordinates,
        "diagonal_hat": diagonal_hat,
        "response_rank": len(pivot_columns),
    }


QUOTIENT = prepare_quotient(ELL, RESPONSE, DIAGONAL_MAP)
require(QUOTIENT["response_rank"] == 3,
        "the audit response rank changed")
require(matmul(ANCHOR_ON_RESPONSE, QUOTIENT["response_zero"])
        == QUOTIENT["diagonal_zero"],
        "the fixed-scalar full-nine anchor difference changed")
require(QUOTIENT["diagonal_hat"]
        == matmul(ANCHOR_ON_RESPONSE, QUOTIENT["response_basis"]),
        ("the induced anchor coordinates changed",
         QUOTIENT["diagonal_hat"]))


def scalar_lift(ell, sigma0, z):
    right = q(z) - q(sigma0)
    if all(not entry for entry in ell):
        return tuple(Fraction(0) for _ in ell) if not right else None
    solution = solve((ell,), (right,))
    return None if solution is None else solution[0]


def classify_case(case, lift=None):
    ell = case["ell"]
    response = case["response"]
    diagonal = case["diagonal"]
    sigma0 = case["sigma0"]
    z = case["z"]
    polar = case["polar"]
    constant = case["constant"]
    kappa0 = case["kappa0"]
    quotient = prepare_quotient(ell, response, diagonal)
    if lift is None:
        lift = scalar_lift(ell, sigma0, z)
    if lift is None:
        return {
            "attainable": False,
            "consistent": False,
            "active": False,
            "forced": (),
            "quotient": quotient,
        }
    require(dot(ell, lift) == z - sigma0,
            ("the chosen lift has the wrong scalar", case["name"], lift))
    response_at_lift = matvec(response, lift)
    diagonal_at_lift = add_vectors(kappa0, matvec(diagonal, lift))
    right = scale_vector(
        -1,
        add_vectors(constant, matvec(polar, response_at_lift)),
    )

    reduced_polar = matmul(polar, quotient["response_basis"])
    reduced_solution = solve(reduced_polar, right)
    full_polar = matmul(polar, quotient["response_zero"])
    full_solution = solve(full_polar, right)
    require((reduced_solution is None) == (full_solution is None),
            ("full/quotient consistency disagrees", case["name"]))
    if reduced_solution is None:
        return {
            "attainable": True,
            "consistent": False,
            "active": False,
            "forced": (),
            "quotient": quotient,
        }

    reduced_point, reduced_kernel = reduced_solution
    full_point, full_kernel = full_solution
    forced_reduced = []
    for label, anchor_row in enumerate(quotient["diagonal_hat"]):
        value = diagonal_at_lift[label] + dot(anchor_row, reduced_point)
        if not value and all(not dot(anchor_row, vector)
                             for vector in reduced_kernel):
            forced_reduced.append(label)
    forced_full = []
    for label, diagonal_row in enumerate(quotient["diagonal_zero"]):
        value = diagonal_at_lift[label] + dot(diagonal_row, full_point)
        if not value and all(not dot(diagonal_row, vector)
                             for vector in full_kernel):
            forced_full.append(label)
    require(tuple(forced_reduced) == tuple(forced_full),
            ("full/quotient activity disagrees", case["name"],
             forced_reduced, forced_full))
    active = bool(z) and not forced_reduced
    result = {
        "attainable": True,
        "consistent": True,
        "active": active,
        "forced": tuple(forced_reduced),
        "quotient": quotient,
        "lift": lift,
        "right": right,
        "response_point": reduced_point,
        "response_kernel": reduced_kernel,
        "diagonal_at_lift": diagonal_at_lift,
    }
    if active:
        result["witness"] = construct_active_witness(case, result)
    return result


def construct_active_witness(case, result):
    point = result["response_point"]
    kernel = result["response_kernel"]
    diagonal_hat = result["quotient"]["diagonal_hat"]
    diagonal_base = result["diagonal_at_lift"]
    response_coordinate = None
    coefficient_range = range(-3, 4)
    for coefficients in product(coefficient_range, repeat=len(kernel)):
        candidate = add_vectors(
            point,
            *(
                scale_vector(coefficient, vector)
                for coefficient, vector in zip(coefficients, kernel)
            ),
        ) if kernel else point
        diagonal_values = add_vectors(
            diagonal_base,
            matvec(diagonal_hat, candidate),
        )
        if all(diagonal_values):
            response_coordinate = candidate
            break
    require(response_coordinate is not None,
            ("the active response witness search failed", case["name"]))

    coordinate_solution = solve(
        result["quotient"]["coordinates"], response_coordinate
    )
    require(coordinate_solution is not None,
            ("an active response did not lift", case["name"]))
    tangent_coordinate = coordinate_solution[0]
    tangent_shift = matvec(
        result["quotient"]["tangent_zero"], tangent_coordinate
    )
    parameter = add_vectors(result["lift"], tangent_shift)
    total_response = matvec(case["response"], parameter)
    require(add_vectors(
        case["constant"], matvec(case["polar"], total_response)
    ) == tuple(Fraction(0) for _ in case["constant"]),
            ("the active witness is not clean", case["name"]))
    require(case["sigma0"] + dot(case["ell"], parameter) == case["z"],
            ("the active witness changed scalar", case["name"]))
    diagonals = add_vectors(
        case["kappa0"], matvec(case["diagonal"], parameter)
    )
    require(case["z"] and all(diagonals),
            ("the active witness hit an activity divisor",
             case["name"], diagonals))
    return parameter, total_response, diagonals


def make_case(name, polar, desired_diagonals, response_coordinate,
              *, z=1, inconsistent_right=None, ell=ELL, sigma0=0):
    polar = matrix(polar)
    ell = tuple(q(value) for value in ell)
    lift = scalar_lift(ell, sigma0, z)
    require(lift is not None, ("case scalar is unattainable", name))
    quotient = prepare_quotient(ell, RESPONSE, DIAGONAL_MAP)
    response_coordinate = tuple(q(value) for value in response_coordinate)
    response_variation = matvec(
        quotient["response_basis"], response_coordinate
    )
    response_at_lift = matvec(RESPONSE, lift)
    if inconsistent_right is None:
        constant = scale_vector(
            -1,
            matvec(
                polar,
                add_vectors(response_at_lift, response_variation),
            ),
        )
    else:
        wanted = tuple(q(value) for value in inconsistent_right)
        constant = scale_vector(
            -1, add_vectors(wanted, matvec(polar, response_at_lift))
        )
    desired_diagonals = tuple(q(value) for value in desired_diagonals)
    kappa0 = add_vectors(
        desired_diagonals,
        scale_vector(-1, matvec(DIAGONAL_MAP, lift)),
        scale_vector(
            -1,
            matvec(quotient["diagonal_hat"], response_coordinate),
        ),
    )
    return {
        "name": name,
        "ell": ell,
        "response": RESPONSE,
        "diagonal": DIAGONAL_MAP,
        "sigma0": q(sigma0),
        "z": q(z),
        "polar": polar,
        "constant": constant,
        "kappa0": kappa0,
    }


def audit_cases():
    cases = (
        make_case(
            "active-kernel",
            ((1, 0, 0),),
            (1, 1, 1),
            (0, 0, 0),
        ),
        make_case(
            "active-unique",
            ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            (1, 2, 3),
            (0, 0, 0),
        ),
        make_case(
            "polar-cokernel",
            ((1, 0, 0), (0, 0, 0)),
            (1, 1, 1),
            (0, 0, 0),
            inconsistent_right=(0, 1),
        ),
        make_case(
            "forced-diagonal-0",
            ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            (0, 2, 3),
            (0, 0, 0),
        ),
        make_case(
            "forced-diagonal-1",
            ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            (1, 0, 3),
            (0, 0, 0),
        ),
        make_case(
            "forced-diagonal-2",
            ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            (1, 2, 0),
            (0, 0, 0),
        ),
        make_case(
            "inactive-scalar",
            ((1, 0, 0),),
            (1, 1, 1),
            (0, 0, 0),
            z=0,
        ),
    )
    expected = {
        "active-kernel": (True, True, ()),
        "active-unique": (True, True, ()),
        "polar-cokernel": (False, False, ()),
        "forced-diagonal-0": (True, False, (0,)),
        "forced-diagonal-1": (True, False, (1,)),
        "forced-diagonal-2": (True, False, (2,)),
        "inactive-scalar": (True, False, ()),
    }
    ledger = []
    for case in cases:
        result = classify_case(case)
        observed = (
            result["consistent"], result["active"], result["forced"]
        )
        require(observed == expected[case["name"]],
                ("response-quotient case changed",
                 case["name"], observed))

        if result["attainable"]:
            tangent_zero = result["quotient"]["tangent_zero"]
            shift = column(tangent_zero, 0)
            shifted_lift = add_vectors(result.get(
                "lift", scalar_lift(case["ell"], case["sigma0"], case["z"])
            ), shift)
            shifted = classify_case(case, shifted_lift)
            require((
                shifted["consistent"], shifted["active"], shifted["forced"]
            ) == observed,
                ("the response quotient depends on scalar lift",
                 case["name"], shifted))
        ledger.append(
            f"{case['name']}:{int(result['attainable'])}:"
            f"{int(result['consistent'])}:{int(result['active'])}:"
            + ",".join(str(label) for label in result["forced"])
        )

    fixed_scalar = dict(cases[0])
    fixed_scalar.update({
        "name": "fixed-scalar-unattainable",
        "ell": (Fraction(0),) * 5,
        "diagonal": matmul(ANCHOR_ON_RESPONSE, RESPONSE),
        "sigma0": Fraction(1),
        "z": Fraction(2),
    })
    result = classify_case(fixed_scalar)
    require(not result["attainable"] and not result["active"],
            ("an unattainable fixed scalar became active", result))
    ledger.append("fixed-scalar-unattainable:0:0:0:")
    return tuple(ledger)


def main():
    ledger = audit_cases()
    digest = sha256("\n".join(ledger).encode("utf-8")).hexdigest()
    require(digest == EXPECTED_LEDGER_DIGEST,
            ("the response-quotient case ledger changed", digest))
    print("common-coloop anchor/polar response quotient: PASS")
    print(f"  tangent/response dimensions : 5/{QUOTIENT['response_rank']}")
    print(f"  induced anchor coordinates  : {QUOTIENT['diagonal_hat']}")
    print(f"  exact strata                : {ledger}")
    print(f"  case-ledger digest          : {digest}")
    print("  conclusion                  : one polar cokernel + three diagonal tests")


if __name__ == "__main__":
    main()
