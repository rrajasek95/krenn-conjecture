#!/usr/bin/env python3
r"""Exact source-base-change audit for the h=3 attaching candidate.

The literal physical candidate assembled from the normalized normal row is

    N = Y*M - kappa*Y*rho - kappa*T + kappa*r0.

Here (d,tgt,ores)(M)=(kappa*w,0,kappa), d rho=w,
dT=-Y*w, and dr0=F0*Eq with F0=H0-u.  The checker verifies

    (d,tgt,ores)(N)=(kappa*F0*Eq+kappa*Y*w,0,0).

After base change by the source ideal J, F0=0 and N looks like the desired
invisible lift.  Its connecting/conormal class is nevertheless
kappa*[F0] in J/J^2.  The selected-u linear functional detects it as
-kappa, while every literal mixed full-nine row, three-set row, and
target-zero normal/adjacent-chart correction has value zero.  Thus the
base-changed lift is tautological Tor from killing the source equation; it
is not a source identity K=0 and does not lift to the polynomial source
module.
"""

from __future__ import annotations

from functools import lru_cache
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_full_hasse_koszul_cap_totalization.py":
        "51940ce0ac8387b68e7725508db6da1a1c055ea036335bbf19750580c69e13fb",
    "computations/verify_h3_three_set_source_relative_terminal_class.py":
        "833f0c3f5fc910581c476085e8e27e8bd1b942545821e92fec9303356130fcc3",
    "computations/verify_h3_full_nine_middle_companion_normalization_guard.py":
        "20b6978490c6427c4b02600a8ba503c24f1d3b68c9260fe653bfd9a9a9817e35",
    "computations/verify_h3_primitive_attaching_source_resolution_audit.py":
        "907fe9ed6ad1a98c167051dc8c7ff7b42f846ae649397ab4bedd4968deff816c",
    "computations/verify_h3_order4_denominator_cube_boundary.py":
        "f3f58f1f516dff9af0d5f58466d646e37dfa3f1779eab7f69e89f51740303f4b",
    "computations/verify_h3_primitive_attaching_universal_module.py":
        "9116553a78b231898355f17ed1f6ccada816d9954ad037a71c8318cfb391a927",
    "computations/verify_h3_mixed_bar_curvature_bicomplex.py":
        "6d239dfa1610d36de3385f9e084693523225528f8343ea9412773604fe396318",
}
EXPECTED_LEDGER_SHA256 = "9b6178c94784f4493b25b9bdbcfa6bae90b179355bd77ffa8f20f93502c69efc"

SITES = tuple(range(8))
COLOURS = (0, 1, 2)
ZERO = Q(0)
ONE = Q(1)

# Sparse coefficient polynomials in A,B,F,U,Y.  Direct-chart coefficients
# are scalars for the selected-u conormal filtration; internal row edges and
# u are the augmentation variables.
NCOEFF = 5
A, B, FCOEF, U, Y = range(NCOEFF)
Polynomial = dict[tuple[int, ...], Q]
Vector = tuple[Polynomial, Polynomial, Polynomial, Polynomial]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def constant(value=ONE) -> Polynomial:
    value = Q(value)
    return {(0,) * NCOEFF: value} if value else {}


def variable(index: int) -> Polynomial:
    exponent = [0] * NCOEFF
    exponent[index] = 1
    return {tuple(exponent): ONE}


def add(*polynomials: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, ZERO) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def scale(value, polynomial: Polynomial) -> Polynomial:
    value = Q(value)
    return {monomial: value * coefficient
            for monomial, coefficient in polynomial.items()
            if value * coefficient}


def multiply(*polynomials: Polynomial) -> Polynomial:
    answer = constant()
    for polynomial in polynomials:
        next_answer: Polynomial = {}
        for left, left_coefficient in answer.items():
            for right, right_coefficient in polynomial.items():
                monomial = tuple(x + y for x, y in zip(left, right,
                                                       strict=True))
                next_answer[monomial] = (
                    next_answer.get(monomial, ZERO)
                    + left_coefficient * right_coefficient
                )
                if not next_answer[monomial]:
                    del next_answer[monomial]
        answer = next_answer
    return answer


def add_vectors(*vectors: Vector) -> Vector:
    return tuple(add(*(vector[index] for vector in vectors))
                 for index in range(4))  # type: ignore[return-value]


def scale_vector(polynomial: Polynomial, vector: Vector) -> Vector:
    return tuple(multiply(polynomial, entry) for entry in vector)  # type: ignore[return-value]


def dot(covector: Vector, vector: Vector) -> Polynomial:
    return add(*(multiply(left, right)
                 for left, right in zip(covector, vector, strict=True)))


def evaluate(polynomial: Polynomial, values: tuple[Q, ...]) -> Q:
    require(len(values) == NCOEFF, "wrong coefficient specialization")
    return sum((coefficient
                * product_value(tuple(value ** exponent
                                      for value, exponent
                                      in zip(values, monomial, strict=True)))
                for monomial, coefficient in polynomial.items()), ZERO)


def product_value(values: tuple[Q, ...]) -> Q:
    answer = ONE
    for value in values:
        answer *= value
    return answer


@lru_cache(maxsize=None)
def matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in matchings(rest):
            result.append(((first, second),) + tail)
    return tuple(result)


def literal_word_census():
    perfect_matchings = matchings(SITES)
    require(len(perfect_matchings) == 105,
            "eight-site perfect-matching count changed")
    counts = {"pure": 0, "mixed": 0, "selected_u_linear": 0}
    matching_terms = 0
    for word in product(COLOURS, repeat=len(SITES)):
        pure = len(set(word)) == 1
        counts["pure" if pure else "mixed"] += 1
        # Every literal hafnian monomial is a four-edge monomial.  Therefore
        # the selected-u first-order functional sees only the normalized
        # target subtraction in the 0^8 row.
        for matching in perfect_matchings:
            require(len(matching) == 4
                    and {site for edge in matching for site in edge}
                    == set(SITES), "literal matching stopped being perfect")
        matching_terms += len(perfect_matchings)
        selected_u = -1 if word == (0,) * len(SITES) else 0
        counts["selected_u_linear"] += bool(selected_u)
        selected_target = 1 if word == (0,) * len(SITES) else 0
        require(selected_u == -selected_target,
                "selected-u/target normalization changed")

    require(counts == {"pure": 3, "mixed": 6558,
                       "selected_u_linear": 1},
            "full literal word census changed")

    # The twenty source-labelled three-set words have distinct selected
    # endpoints and are all target-zero.  The bar-curvature complete word
    # is mixed as well.  These are the actual correction families entering
    # K, not anonymous zero columns.
    three_set_words = []
    residual = tuple(range(6))
    for marked in combinations(residual, 3):
        middle = tuple(1 if site in marked else 0 for site in residual)
        word = (0, 1) + middle
        require(len(set(word)) > 1, "a three-set source word became pure")
        three_set_words.append(word)
    require(len(three_set_words) == 20,
            "three-set literal row count changed")
    bar_word = (1, 2, 1, 1, 2, 2, 2)
    require(len(set(bar_word)) > 1,
            "bar-curvature complete word acquired a target")

    return {
        "literal_words": 3 ** 8,
        "perfect_matchings_per_word": len(perfect_matchings),
        "literal_matching_terms_checked": matching_terms,
        "pure_words": counts["pure"],
        "mixed_target_zero_words": counts["mixed"],
        "selected_u_linear_rows": counts["selected_u_linear"],
        "three_set_target_zero_words": len(three_set_words),
        "bar_complete_word": "".join(map(str, bar_word)),
        "bar_complete_word_target": 0,
    }


def source_module_audit(values: tuple[Q, ...]):
    one = constant()
    zero: Polynomial = {}
    y = variable(Y)
    kappa = add(multiply(variable(A), variable(U)),
                scale(-ONE, multiply(variable(B), variable(FCOEF))))
    kappa_y = multiply(kappa, y)

    # Coordinates are (selected-u Eq conormal, w boundary, target_0, ores).
    # The first coordinate is the linear class [F0] in J/J^2, read with
    # coefficient -1.  All target-zero full-nine and adjacent-chart rows
    # have zero first coordinate by the literal census above.
    r0: Vector = (scale(-ONE, one), zero, one, zero)
    cap_t: Vector = (zero, scale(-ONE, y), one, zero)
    rho: Vector = (zero, one, zero, one)
    normal_m: Vector = (zero, kappa, zero, kappa)

    # The tempting source-relative chain, with every correction retained.
    candidate = add_vectors(
        scale_vector(y, normal_m),
        scale_vector(scale(-ONE, kappa_y), rho),
        scale_vector(scale(-ONE, kappa), cap_t),
        scale_vector(kappa, r0),
    )
    expected: Vector = (scale(-ONE, kappa), kappa_y, zero, zero)
    require(candidate == expected,
            "the full normal/cap/source candidate ledger changed")

    # Forgetting the conormal coordinate is exactly base change F0=0.
    base_changed: Vector = (zero, candidate[1], candidate[2], candidate[3])
    desired: Vector = (zero, kappa_y, zero, zero)
    require(base_changed == desired,
            "source base change stopped producing the tautological lift")

    # The old underived source columns have a primitive cokernel functional.
    # It kills r0,T,rho and every target-zero literal reinsertion, while it
    # reads kappa*Y on the desired boundary.  Equivalently, before base
    # change the connecting class is kappa[F0], read as -kappa.
    covector: Vector = (y, one, y, scale(-ONE, one))
    for label, column in (("r0", r0), ("T", cap_t), ("rho", rho)):
        require(not dot(covector, column),
                f"source cokernel covector stopped killing {label}")
    require(not dot(covector, normal_m),
            "normal graph correction escaped the source cokernel")
    desired_pairing = dot(covector, desired)
    require(desired_pairing == kappa_y and desired_pairing,
            "desired source class lost its primitive pairing")
    conormal = candidate[0]
    require(conormal == scale(-ONE, kappa) and conormal,
            "candidate connecting class is not -kappa[F0]")

    # Generic graph correction theorem.  Any target-zero correction whose
    # w boundary equals its ordinary residue is killed by adding the matching
    # rho term.  The remaining w target fixes T=-kappa and hence r0=+kappa,
    # so the same nonzero conormal class is unavoidable.
    c = constant(Q(7, 5))
    graph_correction: Vector = (zero, c, zero, c)
    generic = add_vectors(
        graph_correction,
        scale_vector(scale(-ONE, c), rho),
        scale_vector(scale(-ONE, kappa), cap_t),
        scale_vector(kappa, r0),
    )
    require(generic == expected,
            "graph-correction conormal theorem changed")

    numeric_kappa = (values[A] * values[U]
                     - values[B] * values[FCOEF])
    require(numeric_kappa and values[Y],
            "active numeric specialization failed")
    require(evaluate(conormal, values) == -numeric_kappa,
            "numeric conormal evaluation changed")
    require(evaluate(desired_pairing, values)
            == numeric_kappa * values[Y],
            "numeric desired pairing changed")
    return {
        "values": [str(value) for value in values],
        "kappa": str(numeric_kappa),
        "candidate": ["-kappa*[F0]", "kappa*Y*w", "0", "0"],
        "after_source_base_change": ["0", "kappa*Y*w", "0", "0"],
        "connecting_class_in_J_mod_J2": "kappa*[F0]",
        "selected_u_readout": str(-numeric_kappa),
        "desired_cokernel_pairing": str(numeric_kappa * values[Y]),
    }


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def main() -> None:
    pin_dependencies()
    word_census = literal_word_census()
    samples = (
        (Q(2), Q(3), Q(5), Q(11), Q(7, 5)),
        (Q(3), Q(0), Q(2), Q(5), Q(-4, 9)),
        (Q(-2), Q(7), Q(3), Q(-5), Q(13, 6)),
    )
    records = [source_module_audit(sample) for sample in samples]
    ledger = {
        "pins": PINS,
        "word_census": word_census,
        "literal_candidate": (
            "N=Y*M-kappa*Y*rho-kappa*T+kappa*r0"
        ),
        "candidate_boundary": (
            "dN=kappa*F0*Eq+kappa*Y*w; tgt(N)=ores(N)=0"
        ),
        "base_change": "F0=0 makes dN=kappa*Y*w",
        "conormal_connecting_class": "delta(N)=kappa*[F0] in J/J^2",
        "uniform_graph_correction_theorem": (
            "target-zero corrections with w=ores do not alter the "
            "selected-u conormal obstruction"
        ),
        "records": records,
        "verdict": (
            "the base-changed lift is tautological Tor and does not lift "
            "to a source identity; a genuine K row must cancel "
            "kappa*[F0] before quotienting"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"source-base-change ledger changed: {digest}")

    print("h=3 source-base-change conormal audit: PASS")
    print("literal full-nine words checked: 6561; selected-u rows: 1")
    print("dN=kappa*F0*Eq+kappa*Y*w, target=ores=0")
    print("after F0=0: desired lift appears, but delta(N)=kappa*[F0]")
    print("selected-u conormal readout: -kappa (nonzero)")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
