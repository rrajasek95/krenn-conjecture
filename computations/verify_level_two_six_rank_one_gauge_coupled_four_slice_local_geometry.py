#!/usr/bin/env python3
"""Exact local four-slice geometry at the rank-50 gauge-coupled packet.

The fixed endpoint stars give a quadratic map from the 60 residual cells
to four binary six-site slices (256 scalar coordinates).  This checker
reconstructs its 256-by-60 Jacobian, restricts the homogeneous quadratic
part to the 15-dimensional Jacobian kernel, and certifies the resulting
six-generator exact-line cone and its two linear components.

Singular is used only for exact radical/intersection and function-field
syzygy computations.  Everything else uses the Python standard library;
all checks stay live under -O and -I -S.
"""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations_with_replacement, product
from pathlib import Path
from runpy import run_path
from shutil import which
from subprocess import run


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
SIX = run_path(str(
    HERE / "verify_level_two_six_rank_one_gauge_coupled_repair.py"
))
CORE = SIX["CORE"]
BASE = SIX["BASE"]
CELLS = CORE["CELLS"]
WORDS = CORE["WORDS"]
COLOURS = SIX["COLOURS"]
SITES = SIX["SITES"]
N_CELLS = len(CELLS)
MONOMIALS = tuple(combinations_with_replacement(range(15), 2))


class Jet:
    """A rational value and its gradient in the 60 residual cells."""

    __slots__ = ("value", "gradient")

    def __init__(self, value, gradient=None):
        self.value = Q(value)
        self.gradient = (
            tuple(Q(0) for _ in CELLS)
            if gradient is None else tuple(Q(entry) for entry in gradient)
        )

    def __add__(self, other):
        other = other if isinstance(other, Jet) else Jet(other)
        return Jet(
            self.value + other.value,
            (left + right for left, right
             in zip(self.gradient, other.gradient, strict=True)),
        )

    __radd__ = __add__

    def __mul__(self, other):
        other = other if isinstance(other, Jet) else Jet(other)
        return Jet(
            self.value * other.value,
            (
                self.value * right + left * other.value
                for left, right
                in zip(self.gradient, other.gradient, strict=True)
            ),
        )

    __rmul__ = __mul__


class Quad:
    """A homogeneous quadratic in the 15 Jacobian-kernel coordinates."""

    __slots__ = ("coefficients",)

    def __init__(self, coefficients=None):
        self.coefficients = {
            tuple(monomial): Q(coefficient)
            for monomial, coefficient in (coefficients or {}).items()
            if coefficient
        }

    def __add__(self, other):
        if other == 0:
            return self
        require(isinstance(other, Quad), ("bad quadratic addend", other))
        coefficients = dict(self.coefficients)
        for monomial, coefficient in other.coefficients.items():
            coefficients[monomial] = (
                coefficients.get(monomial, Q(0)) + coefficient
            )
        return Quad(coefficients)

    __radd__ = __add__

    def __mul__(self, scalar):
        require(isinstance(scalar, (int, Q)),
                ("bad quadratic scalar", scalar))
        return Quad({
            monomial: scalar * coefficient
            for monomial, coefficient in self.coefficients.items()
        })

    __rmul__ = __mul__


class Linear:
    """A homogeneous linear form in the kernel coordinates."""

    __slots__ = ("coefficients",)

    def __init__(self, coefficients=None):
        self.coefficients = {
            int(variable): Q(coefficient)
            for variable, coefficient in (coefficients or {}).items()
            if coefficient
        }

    def __add__(self, other):
        if other == 0:
            return self
        require(isinstance(other, Linear), ("bad linear addend", other))
        coefficients = dict(self.coefficients)
        for variable, coefficient in other.coefficients.items():
            coefficients[variable] = (
                coefficients.get(variable, Q(0)) + coefficient
            )
        return Linear(coefficients)

    __radd__ = __add__

    def __mul__(self, other):
        if isinstance(other, Linear):
            coefficients = {}
            for left, left_value in self.coefficients.items():
                for right, right_value in other.coefficients.items():
                    monomial = tuple(sorted((left, right)))
                    coefficients[monomial] = (
                        coefficients.get(monomial, Q(0))
                        + left_value * right_value
                    )
            return Quad(coefficients)
        require(isinstance(other, (int, Q)),
                ("bad linear scalar", other))
        return Linear({
            variable: other * coefficient
            for variable, coefficient in self.coefficients.items()
        })

    __rmul__ = __mul__


class Poly:
    """A sparse rational polynomial, used for the two affine planes."""

    __slots__ = ("coefficients",)

    def __init__(self, coefficients=None):
        self.coefficients = {
            tuple(sorted(monomial)): Q(coefficient)
            for monomial, coefficient in (coefficients or {}).items()
            if coefficient
        }

    def __eq__(self, other):
        if not isinstance(other, Poly):
            other = Poly({(): other})
        return self.coefficients == other.coefficients

    def __add__(self, other):
        if not isinstance(other, Poly):
            other = Poly({(): other})
        coefficients = dict(self.coefficients)
        for monomial, coefficient in other.coefficients.items():
            coefficients[monomial] = (
                coefficients.get(monomial, Q(0)) + coefficient
            )
        return Poly(coefficients)

    __radd__ = __add__

    def __neg__(self):
        return Poly({
            monomial: -coefficient
            for monomial, coefficient in self.coefficients.items()
        })

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return Poly({(): other}) - self

    def __mul__(self, other):
        if not isinstance(other, Poly):
            other = Poly({(): other})
        coefficients = {}
        for left, left_value in self.coefficients.items():
            for right, right_value in other.coefficients.items():
                monomial = tuple(sorted(left + right))
                coefficients[monomial] = (
                    coefficients.get(monomial, Q(0))
                    + left_value * right_value
                )
        return Poly(coefficients)

    __rmul__ = __mul__


def rational_rref(rows):
    matrix = [list(map(Q, row)) for row in rows]
    require(matrix and matrix[0], "empty exact matrix")
    pivots = []
    pivot_row = 0
    for column in range(len(matrix[0])):
        selected = next(
            (row for row in range(pivot_row, len(matrix))
             if matrix[row][column]),
            None,
        )
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = (
            matrix[selected], matrix[pivot_row]
        )
        pivot = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / pivot for entry in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                entry - multiple * pivot_entry
                for entry, pivot_entry
                in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return matrix, tuple(pivots)


def rational_nullspace(rows):
    reduced, pivots = rational_rref(rows)
    free = tuple(
        column for column in range(len(rows[0])) if column not in pivots
    )
    basis = []
    for free_column in free:
        vector = [Q(0)] * len(rows[0])
        vector[free_column] = Q(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        basis.append(tuple(vector))
    return tuple(basis)


def four_tangents(u_star, v_star):
    return tuple(
        BASE["factored_tangent"](u_star, v_star, s, t)
        for s, t in product(COLOURS, repeat=2)
    )


def flatten_outputs(packet, tangents):
    return tuple(
        output
        for tangent in tangents
        for output in CORE["apply_differential"](packet, tangent)
    )


EXPECTED_KERNEL_SUPPORT = (
    (((0, 1, 0, 0), Q(-1, 2)), ((0, 3, 0, 0), Q(1))),
    (((0, 1, 1, 0), Q(-1, 2)), ((0, 3, 1, 0), Q(1))),
    (((0, 4, 0, 1), Q(-17, 19)), ((0, 5, 0, 1), Q(1))),
    (((0, 4, 1, 1), Q(-17, 19)), ((0, 5, 1, 1), Q(1))),
    (((0, 1, 0, 0), Q(-1)), ((1, 2, 0, 0), Q(1))),
    (((0, 1, 0, 1), Q(-1)), ((1, 2, 1, 0), Q(1))),
    (((0, 2, 1, 1), Q(-5, 7)), ((1, 3, 1, 1), Q(1))),
    (((0, 4, 0, 0), Q(11, 13)), ((1, 4, 0, 0), Q(1))),
    (((0, 4, 0, 1), Q(11, 13)), ((1, 4, 0, 1), Q(1))),
    (((0, 5, 0, 0), Q(11, 13)), ((1, 5, 0, 0), Q(1))),
    (((0, 4, 0, 1), Q(187, 247)), ((1, 5, 0, 1), Q(1))),
    (((1, 4, 1, 1), Q(-17, 19)), ((1, 5, 1, 1), Q(1))),
    (((2, 4, 0, 1), Q(-17, 19)), ((2, 5, 0, 1), Q(1))),
    (((2, 4, 1, 1), Q(-17, 19)), ((2, 5, 1, 1), Q(1))),
    (
        ((0, 1, 0, 0), Q(-1, 3)),
        ((2, 3, 0, 0), Q(-2, 3)),
        ((4, 5, 0, 0), Q(1)),
    ),
)


EXPECTED_QUADRICS = (
    {(14, 14): Q(-1, 9)},
    {
        (0, 4): Q(1, 35),
        (0, 14): Q(1, 105),
        (4, 14): Q(2, 105),
        (14, 14): Q(2, 315),
    },
    {(0, 5): Q(1, 35), (5, 14): Q(2, 105)},
    {(1, 4): Q(1, 35), (1, 14): Q(1, 105)},
    {(1, 5): Q(1, 35)},
    {(6, 6): Q(-1, 49)},
)
QUADRATIC_ROWS = (0, 195, 211, 227, 243, 255)


def audit_jacobian_and_cone():
    packet, u_star, v_star, _previous = SIX["rank50_member"]()
    tangents = four_tangents(u_star, v_star)
    target = (
        tuple(int(word == (0,) * 6) for word in WORDS)
        + (0,) * 64
        + (0,) * 64
        + tuple(int(word == (1,) * 6) for word in WORDS)
    )
    require(flatten_outputs(packet, tangents) == target,
            "the rank-50 precursor left the fixed four-slice fibre")

    jets = {}
    for column, cell in enumerate(CELLS):
        gradient = [Q(0)] * N_CELLS
        gradient[column] = Q(1)
        jets[cell] = Jet(packet[cell], gradient)
    jet_outputs = flatten_outputs(jets, tangents)
    require(tuple(output.value for output in jet_outputs) == target,
            "the jet reconstruction changed the precursor values")
    jacobian = [list(output.gradient) for output in jet_outputs]
    _reduced, pivots = rational_rref(jacobian)
    require((len(jacobian), len(jacobian[0]), len(pivots))
            == (256, 60, 45),
            ("four-slice Jacobian changed", len(pivots)))
    kernel = rational_nullspace(jacobian)
    require(len(kernel) == 15,
            ("four-slice Jacobian nullity changed", len(kernel)))
    support = tuple(tuple(
        (cell, vector[column])
        for column, cell in enumerate(CELLS) if vector[column]
    ) for vector in kernel)
    require(support == EXPECTED_KERNEL_SUPPORT,
            "the pinned 15-coordinate Jacobian kernel changed")

    direction = {
        cell: Linear({
            variable: kernel[variable][column]
            for variable in range(15)
        })
        for column, cell in enumerate(CELLS)
    }
    quadratic_outputs = flatten_outputs(direction, tangents)
    coefficient_matrix = [
        [output.coefficients.get(monomial, Q(0))
         for monomial in MONOMIALS]
        for output in quadratic_outputs
    ]
    _quadratic_rref, quadratic_pivots = rational_rref(coefficient_matrix)
    _transpose_rref, independent_rows = rational_rref(
        list(map(list, zip(*coefficient_matrix, strict=True)))
    )
    require(len(quadratic_pivots) == 6,
            ("quadratic restriction rank changed", len(quadratic_pivots)))
    require(independent_rows == QUADRATIC_ROWS,
            ("quadratic generator rows changed", independent_rows))
    quadrics = tuple(
        quadratic_outputs[row].coefficients for row in independent_rows
    )
    require(quadrics == EXPECTED_QUADRICS,
            ("the six exact cone quadrics changed", quadrics))
    return packet, u_star, v_star, tangents, target, kernel, quadrics


COMPONENTS = {
    # Radical prime (y0,y1,y6,y14); the precursor itself is sharp here.
    "flat": {
        "free": (2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13),
        "full_rank": 50,
        "mixed_rank": 48,
        "full_syzygies": (11, 10),
        "mixed_syzygies": (12, 12),
    },
    # Radical prime (y4,y5,y6,y14); this contains the rank-lifting line.
    "lifting": {
        "free": (0, 1, 2, 3, 7, 8, 9, 10, 11, 12, 13),
        "full_rank": 51,
        "mixed_rank": 49,
        "full_syzygies": (9, 9),
        "mixed_syzygies": (11, 11),
    },
}


def symbolic_component_packet(packet, kernel, free):
    result = {}
    for column, cell in enumerate(CELLS):
        coefficients = {(): packet[cell]}
        for local, variable in enumerate(free):
            coefficients[(local,)] = kernel[variable][column]
        result[cell] = Poly(coefficients)
    return result


def specialized_component_packet(packet, kernel, free, parameters):
    require(len(free) == len(parameters) == 11,
            "component specialization length changed")
    result = dict(packet)
    for local, variable in enumerate(free):
        for column, cell in enumerate(CELLS):
            result[cell] += parameters[local] * kernel[variable][column]
    result = {
        cell: (value.numerator
               if isinstance(value, Q) and value.denominator == 1 else value)
        for cell, value in result.items()
    }
    return result


def as_poly(value):
    return value if isinstance(value, Poly) else Poly({(): value})


def audit_exact_affine_components(packet, tangents, target, kernel):
    symbolic_packets = {}
    for name, data in COMPONENTS.items():
        symbolic = symbolic_component_packet(packet, kernel, data["free"])
        outputs = flatten_outputs(symbolic, tangents)
        expected = tuple(Poly({(): entry}) for entry in target)
        require(tuple(map(as_poly, outputs)) == expected,
                ("an affine cone component left the four-slice fibre", name))
        symbolic_packets[name] = symbolic
    return symbolic_packets


def rational_string(value):
    value = Q(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"({value.numerator}/{value.denominator})"


def polynomial_string(value, variable="t"):
    polynomial = as_poly(value)
    pieces = []
    for monomial, coefficient in sorted(
        polynomial.coefficients.items(),
        key=lambda item: (len(item[0]), item[0]),
    ):
        variables = "*".join(f"{variable}{index}" for index in monomial)
        piece = rational_string(coefficient)
        if variables:
            piece += f"*{variables}"
        pieces.append(piece)
    return "+".join(pieces).replace("+-", "-") or "0"


def quadratic_string(coefficients):
    pieces = []
    for (left, right), coefficient in sorted(coefficients.items()):
        pieces.append(
            f"{rational_string(coefficient)}*y{left}*y{right}"
        )
    return "+".join(pieces).replace("+-", "-") or "0"


def singular_matrix(name, matrix):
    entries = ",".join(
        polynomial_string(entry) for row in matrix for entry in row
    )
    return f"matrix {name}[{len(matrix)}][{len(matrix[0])}]={entries};"


def singular_script(quadrics, symbolic_packets):
    lines = [
        'ring tangent=0,(y0,y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11,y12,y13,y14),dp;',
        'LIB "primdec.lib";',
        'LIB "control.lib";',
        "ideal I=" + ",".join(map(quadratic_string, quadrics)) + ";",
        "ideal R=radical(I);",
        "ideal Pflat=y0,y1,y6,y14;",
        "ideal Plifting=y4,y5,y6,y14;",
        "ideal U=intersect(Pflat,Plifting);",
        'if (size(reduce(std(R),std(U)))!=0) { print("FAIL_R_U"); exit; }',
        'if (size(reduce(std(U),std(R)))!=0) { print("FAIL_U_R"); exit; }',
        'if (dim(std(Pflat))!=11) { print("FAIL_DIM_FLAT"); exit; }',
        'if (dim(std(Plifting))!=11) { print("FAIL_DIM_LIFT"); exit; }',
    ]
    for name, data in COMPONENTS.items():
        packet = symbolic_packets[name]
        derivative = CORE["differential_matrix"](packet)
        mixed = [
            row for row, word in zip(derivative, WORDS, strict=True)
            if word not in ((0,) * 6, (1,) * 6)
        ]
        prefix = "F" if name == "flat" else "L"
        lines.extend((
            f"ring {name}=0,(t0,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10),dp;",
            singular_matrix(prefix + "D", derivative),
            singular_matrix(prefix + "E", mixed),
            f"module {prefix}KD=syz({prefix}D);",
            f"module {prefix}KE=syz({prefix}E);",
            (
                f'if (ncols({prefix}KD)!={data["full_syzygies"][0]}) '
                f'{{ print("FAIL_{prefix}_DKGEN"); exit; }}'
            ),
            (
                f'if (colrank({prefix}KD)!={data["full_syzygies"][1]}) '
                f'{{ print("FAIL_{prefix}_DKRANK"); exit; }}'
            ),
            (
                f'if (ncols({prefix}KE)!={data["mixed_syzygies"][0]}) '
                f'{{ print("FAIL_{prefix}_EKGEN"); exit; }}'
            ),
            (
                f'if (colrank({prefix}KE)!={data["mixed_syzygies"][1]}) '
                f'{{ print("FAIL_{prefix}_EKRANK"); exit; }}'
            ),
        ))
    lines.append('print("CAS_OK");')
    return "\n".join(lines) + "\n"


EXPECTED_CAS_SHA256 = (
    "3a6be8d30de5e3cf3d235e1476c3700f"
    "947902706bf5ad1f9b714d58142684e5"
)


def audit_exact_cas(quadrics, symbolic_packets):
    executable = which("Singular")
    require(executable is not None,
            "Singular is required for the exact local-geometry audit")
    script = singular_script(quadrics, symbolic_packets)
    digest = sha256(script.encode()).hexdigest()
    require(digest == EXPECTED_CAS_SHA256,
            ("the pinned Singular input changed", digest))
    result = run(
        [executable, "-q"],
        input=script,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    require(result.returncode == 0,
            ("Singular failed", result.returncode, result.stderr))
    require(result.stdout.strip() == "CAS_OK",
            ("Singular certificate failed", result.stdout, result.stderr))
    return digest


def differential_ranks(packet):
    derivative = CORE["differential_matrix"](packet)
    mixed = [
        row for row, word in zip(derivative, WORDS, strict=True)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    return (
        BASE["ranks_over_fields"](derivative),
        BASE["ranks_over_fields"](mixed),
    )


def audit_full_r2_calibration(packet, u_star, v_star, expected_ranks):
    full_rank, mixed_rank = expected_ranks
    ranks = differential_ranks(packet)
    require(ranks == (
        (full_rank,) * 4,
        (mixed_rank,) * 4,
    ), ("component calibration ranks changed", ranks))
    selected = SIX["selected_family"](SITES)
    endpoint_ranks = tuple(
        CORE["rational_rank"](selected[site]) for site in SITES
    )
    require(endpoint_ranks == (1,) * 6,
            ("the full-R2 endpoint pattern changed", endpoint_ranks))
    require(SIX["audit_selected_equations"](packet, selected) == 60,
            "a full-R2 calibration left the generic kernel")
    require(SIX["audit_literal_slices"](
        packet, u_star, v_star, selected
    ) == 256, "a full-R2 calibration lost a literal slice")
    witnesses = {
        root: SIX["audit_capable_root"](packet, root) for root in SITES
    }
    require(all(set(table) == {0, 1} for table in witnesses.values()),
            ("a calibration lost a complete R2 witness pair", witnesses))
    return ranks, witnesses


def audit_calibrations(packet, u_star, v_star, kernel):
    flat = specialized_component_packet(
        packet, kernel, COMPONENTS["flat"]["free"], (0,) * 11
    )
    require(flat == packet, "the flat-component origin moved")
    flat_audit = audit_full_r2_calibration(
        flat, u_star, v_star, (50, 48)
    )

    lifting_parameters = (-26, -26, 0, 0, 0, 0, -26, 0, 0, 0, 0)
    lifting = specialized_component_packet(
        packet,
        kernel,
        COMPONENTS["lifting"]["free"],
        lifting_parameters,
    )
    repaired, repaired_u, repaired_v, _repair = SIX["repaired_member"]()
    require(lifting == repaired,
            "the known rank-lifting line left its cone component")
    require((u_star, v_star) == (repaired_u, repaired_v),
            "the endpoint stars changed on the rank-lifting line")
    lifting_audit = audit_full_r2_calibration(
        lifting, u_star, v_star, (51, 49)
    )
    return flat_audit, lifting_audit, lifting_parameters


def main():
    packet, u_star, v_star, tangents, target, kernel, quadrics = (
        audit_jacobian_and_cone()
    )
    symbolic_packets = audit_exact_affine_components(
        packet, tangents, target, kernel
    )
    digest = audit_exact_cas(quadrics, symbolic_packets)
    flat, lifting, lifting_parameters = audit_calibrations(
        packet, u_star, v_star, kernel
    )
    print("six-rank-one local four-slice geometry: all checks passed")
    print("  residual Jacobian           : 256x60, rank 45, nullity 15")
    print("  exact-line cone             : 6 quadrics, radical = two 11-planes")
    print("  flat component maximum      : D/Emixed = "
          f"{flat[0][0][0]}/{flat[0][1][0]}")
    print("  lifting component maximum   : D/Emixed = "
          f"{lifting[0][0][0]}/{lifting[0][1][0]}")
    print(f"  lifting coordinates         : {lifting_parameters}")
    print("  full R2 calibration         : complete at all six roots on both")
    print(f"  Singular input SHA-256      : {digest}")


if __name__ == "__main__":
    main()
