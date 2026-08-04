#!/usr/bin/env python3
"""Adversarial exact tests for the direct Laurent cuts.

These tests deliberately avoid the support SAT formula.  They manufacture
small exponent fibers inside the same 6-vertex/15-matching index set and
check the lattice calculation and the exact-fiber Tseitin encoding directly.

Every check below raises instead of asserting.  A bare ``assert`` is deleted
by ``python3 -O``, under which this whole file used to pass vacuously while
printing PASS for each test.  Solver outcomes are compared against ``True``
and ``False`` by identity, because ``Solver.solve`` returns ``None`` for an
interrupted or budget-limited call and ``not None`` would read as UNSAT.
"""

from __future__ import annotations

import itertools
import random

from pysat.formula import CNF
from pysat.formula import IDPool
from pysat.solvers import Solver

import search_f5_support_sat as base
import verify_f3_toric_obstruction as toric


def require(condition: object, message: str) -> None:
    """Check a load-bearing condition in a way ``python3 -O`` cannot remove."""

    if not condition:
        raise RuntimeError(message)


def solve_exactly(solver, expected: bool, message: str, assumptions=None):
    """Run one solve and require a definite ``True``/``False`` outcome."""

    answer = (
        solver.solve()
        if assumptions is None
        else solver.solve(assumptions=list(assumptions))
    )
    require(
        answer is expected,
        f"{message}: expected {expected}, solver returned {answer!r}",
    )


MIXED = tuple(c for c in base.COLORINGS if len(set(c)) > 1)


def synthetic_instance(fibers, dimension):
    """Build ``pool, signatures, model`` from exact synthetic fibers."""
    pool = IDPool()
    zero = (0,) * dimension
    signatures = {
        (coloring, matching): zero
        for coloring in base.COLORINGS
        for matching in range(len(base.MATCHINGS))
    }
    model = set()
    for coloring, exponents in fibers:
        require(
            len(exponents) <= len(base.MATCHINGS),
            f"fiber {coloring} lists more monomials than there are matchings",
        )
        for matching, exponent in enumerate(exponents):
            signatures[coloring, matching] = tuple(exponent)
            model.add(pool.id(("monomial", coloring, matching)))
    return pool, signatures, model


def test_primitive_single_class_conflict():
    fibers = (
        (MIXED[0], ((1, 0), (0, 0))),
        (MIXED[1], ((0, 1), (0, 0))),
        (MIXED[2], ((0, 0), (1, 0), (0, 1))),
    )
    pool, signatures, model = synthetic_instance(fibers, 2)
    answer = toric.single_fiber_laurent_conflict(
        pool, signatures, model
    )
    require(answer is not None, "the primitive single-class fiber was not cut")
    used, coloring, class_sums, kind = answer
    require(coloring == MIXED[2], f"the cut fiber is {coloring}, not MIXED[2]")
    require(kind == "single-laurent-class", f"unexpected cut kind {kind!r}")
    require(
        len([value for value in class_sums if value]) == 1,
        f"class sums {class_sums} do not have exactly one nonzero entry",
    )
    require(
        set(used) == {MIXED[0], MIXED[1], MIXED[2]},
        f"unexpected provenance {sorted(set(used))}",
    )


def test_exact_internal_cancellation_is_not_cut():
    fibers = (
        (MIXED[0], ((1, 0), (0, 0))),
        (MIXED[1], ((0, 1), (0, 0))),
        (MIXED[2], ((0, 0), (1, 0), (0, 1), (1, 1))),
    )
    pool, signatures, model = synthetic_instance(fibers, 2)
    require(
        toric.single_fiber_laurent_conflict(pool, signatures, model) is None,
        "an exactly cancelling fiber was cut",
    )


def test_two_surviving_classes_are_not_cut():
    fibers = (
        (MIXED[0], ((1, 0, 0), (0, 0, 0))),
        (MIXED[1], ((0, 0, 0), (0, 1, 0), (0, 0, 1))),
    )
    pool, signatures, model = synthetic_instance(fibers, 3)
    require(
        toric.single_fiber_laurent_conflict(pool, signatures, model) is None,
        "a fiber with two surviving Laurent classes was cut",
    )


def test_nonprimitive_basis_is_conservatively_declined():
    # Although the first two terms cancel using x^2=-1, the selected row has
    # coordinate minor 2.  The present routine intentionally makes no claim
    # on such a chart rather than confusing a lattice with its saturation.
    fibers = (
        (MIXED[0], ((2, 0), (0, 0))),
        (MIXED[1], ((0, 0), (2, 0), (1, 0))),
    )
    pool, signatures, model = synthetic_instance(fibers, 2)
    require(
        toric.single_fiber_laurent_conflict(pool, signatures, model) is None,
        "a nonprimitive coordinate minor was not conservatively declined",
    )


def test_redundant_even_parity_relation_is_cut():
    # x=-1, y=-1, and xy=-1 are inconsistent: the first two give xy=+1.
    fibers = (
        (MIXED[0], ((1, 0), (0, 0))),
        (MIXED[1], ((0, 1), (0, 0))),
        (MIXED[2], ((1, 1), (0, 0))),
    )
    pool, signatures, model = synthetic_instance(fibers, 2)
    answer = toric.single_fiber_laurent_conflict(
        pool, signatures, model
    )
    require(answer is not None, "the redundant odd-parity relation was not cut")
    used, coloring, _class_sums, kind = answer
    require(kind == "odd-binomial", f"unexpected cut kind {kind!r}")
    require(coloring == MIXED[2], f"the cut fiber is {coloring}, not MIXED[2]")
    require(
        set(used) == {MIXED[0], MIXED[1], MIXED[2]},
        f"unexpected provenance {sorted(set(used))}",
    )


def test_negative_laurent_coordinates():
    fibers = (
        (MIXED[0], ((1, 0), (0, 0))),
        (MIXED[1], ((0, 1), (0, 0))),
        (MIXED[2], ((0, 0), (-1, 0), (0, -1))),
    )
    pool, signatures, model = synthetic_instance(fibers, 2)
    answer = toric.single_fiber_laurent_conflict(
        pool, signatures, model
    )
    require(answer is not None, "the negative-coordinate fiber was not cut")
    require(
        answer[3] == "single-laurent-class",
        f"unexpected cut kind {answer[3]!r}",
    )
    require(
        all(isinstance(value, int) for value in answer[2]),
        f"class sums {answer[2]} are not all Python integers",
    )


def test_translated_trinomials_with_one_sign_change_conflict():
    # x=-1, together with
    #   1+y+y^2=0 and 1+xy+y^2=0,
    # forces 2y=0 on the Laurent torus.
    fibers = (
        (MIXED[0], ((1, 0), (0, 0))),
        (MIXED[1], ((0, 0), (0, 1), (0, 2))),
        (MIXED[2], ((0, 0), (1, 1), (0, 2))),
    )
    pool, signatures, model = synthetic_instance(fibers, 2)
    answer = toric.trinomial_sign_conflict(pool, signatures, model)
    require(answer is not None, "the one-sign-change trinomial pair was not cut")
    used, first, second, parities, *_sizes = answer
    require(
        {first, second} == {MIXED[1], MIXED[2]},
        f"unexpected trinomial pair {(first, second)}",
    )
    require(any(parities), f"parities {parities} record no sign change")
    require(
        set(used) == {MIXED[0], MIXED[1], MIXED[2]},
        f"unexpected provenance {sorted(set(used))}",
    )


def test_translated_trinomials_with_two_sign_changes_conflict():
    # The normalized equations become 1+y+z=0 and 1-y-z=0,
    # whose sum is 2=0.
    fibers = (
        (MIXED[0], ((1, 0, 0), (0, 0, 0))),
        (MIXED[1], ((0, 0, 0), (0, 1, 0), (0, 0, 1))),
        (MIXED[2], ((0, 0, 0), (1, 1, 0), (1, 0, 1))),
    )
    pool, signatures, model = synthetic_instance(fibers, 3)
    answer = toric.trinomial_sign_conflict(pool, signatures, model)
    require(answer is not None, "the two-sign-change trinomial pair was not cut")
    require(answer[3] == (1, 1), f"unexpected parities {answer[3]}")


def test_even_translated_trinomials_are_not_cut():
    # Translating one term by x^2 does not change its sign when x=-1, so
    # these are the same Laurent equation rather than a contradiction.
    fibers = (
        (MIXED[0], ((1, 0), (0, 0))),
        (MIXED[1], ((0, 0), (0, 1), (0, 2))),
        (MIXED[2], ((0, 0), (2, 1), (0, 2))),
    )
    pool, signatures, model = synthetic_instance(fibers, 2)
    require(
        toric.trinomial_sign_conflict(pool, signatures, model) is None,
        "an even translated trinomial pair was cut",
    )


def test_translated_trinomial_nonprimitive_basis_is_declined():
    fibers = (
        (MIXED[0], ((2, 0), (0, 0))),
        (MIXED[1], ((0, 0), (0, 1), (0, 2))),
        (MIXED[2], ((0, 0), (2, 1), (0, 2))),
    )
    pool, signatures, model = synthetic_instance(fibers, 2)
    require(
        toric.trinomial_sign_conflict(pool, signatures, model) is None,
        "a nonprimitive trinomial basis was not conservatively declined",
    )


def test_random_unimodular_changes_of_coordinates():
    rng = random.Random(20260724)
    for trial in range(40):
        # det=1 shears with negative entries exercise orientation and powers.
        shear = rng.randint(-7, 7)
        first = (1, shear)
        second = (0, 1)
        target = (
            (0, 0),
            tuple(-value for value in first),
            tuple(-value for value in second),
        )
        fibers = (
            (MIXED[3 * trial], (first, (0, 0))),
            (MIXED[3 * trial + 1], (second, (0, 0))),
            (MIXED[3 * trial + 2], target),
        )
        pool, signatures, model = synthetic_instance(fibers, 2)
        answer = toric.single_fiber_laurent_conflict(
            pool, signatures, model
        )
        require(answer is not None, f"shear {shear} was not cut")
        require(
            answer[3] == "single-laurent-class",
            f"shear {shear}: unexpected cut kind {answer[3]!r}",
        )


def test_random_class_sum_oracle_agreement():
    """Compare returned conflicts with an independent parity calculation."""
    rng = random.Random(8675309)
    for trial in range(80):
        shear = rng.randint(-5, 5)
        first = (1, shear)
        second = (0, 1)
        target = tuple(
            (rng.randint(-4, 4), rng.randint(-4, 4))
            for _ in range(rng.randint(3, 8))
        )
        representative = target[0]
        signed_sum = 0
        for x, y in (
            (a - representative[0], b - representative[1])
            for a, b in target
        ):
            # (x,y)=x*(1,shear)+(y-shear*x)*(0,1).
            coordinate_sum = x + y - shear * x
            signed_sum += -1 if coordinate_sum % 2 else 1

        fibers = (
            (MIXED[3 * trial], (first, (0, 0))),
            (MIXED[3 * trial + 1], (second, (0, 0))),
            (MIXED[3 * trial + 2], target),
        )
        pool, signatures, model = synthetic_instance(fibers, 2)
        answer = toric.single_fiber_laurent_conflict(
            pool, signatures, model
        )
        require(
            (answer is not None) == (signed_sum != 0),
            f"oracle disagreement: shear={shear}, target={target}, "
            f"signed_sum={signed_sum}, answer={answer}",
        )


def force_pattern(solver, pool, coloring, supported):
    supported = set(supported)
    for index in range(len(base.MATCHINGS)):
        literal = pool.id(("monomial", coloring, index))
        solver.add_clause([literal if index in supported else -literal])


def test_exact_fiber_indicator_and_cut():
    first, second = MIXED[:2]
    first_support = (0, 3, 8)
    second_support = (2, 5)

    # The indicator is true iff every one of the 15 support bits agrees.
    for coloring, supported in (
        (first, first_support),
        (second, second_support),
    ):
        pool = IDPool()
        with Solver(name="g4") as solver:
            indicator = toric.fiber_indicator(
                solver, pool, {}, coloring, supported
            )
            force_pattern(solver, pool, coloring, supported)
            solve_exactly(
                solver,
                True,
                f"fiber {coloring}: the exact support does not satisfy "
                "its indicator",
                [indicator],
            )
            solve_exactly(
                solver,
                False,
                f"fiber {coloring}: the exact support also satisfies the "
                "negated indicator",
                [-indicator],
            )
        for flipped in range(len(base.MATCHINGS)):
            pool = IDPool()
            with Solver(name="g4") as solver:
                indicator = toric.fiber_indicator(
                    solver, pool, {}, coloring, supported
                )
                changed = set(supported) ^ {flipped}
                force_pattern(solver, pool, coloring, changed)
                solve_exactly(
                    solver,
                    True,
                    f"fiber {coloring}, flipped bit {flipped}: the perturbed "
                    "support does not satisfy the negated indicator",
                    [-indicator],
                )
                solve_exactly(
                    solver,
                    False,
                    f"fiber {coloring}, flipped bit {flipped}: the perturbed "
                    "support still satisfies the indicator",
                    [indicator],
                )

    # The learned clause forbids exactly the conjunction of its source
    # patterns.  Perturbing either pattern leaves a satisfying assignment.
    for perturb in (None, first, second):
        pool = IDPool()
        cache = {}
        with Solver(name="g4") as solver:
            first_indicator = toric.fiber_indicator(
                solver, pool, cache, first, first_support
            )
            second_indicator = toric.fiber_indicator(
                solver, pool, cache, second, second_support
            )
            solver.add_clause([-first_indicator, -second_indicator])
            force_pattern(
                solver,
                pool,
                first,
                set(first_support) ^ ({0} if perturb == first else set()),
            )
            force_pattern(
                solver,
                pool,
                second,
                set(second_support) ^ ({2} if perturb == second else set()),
            )
            solve_exactly(
                solver,
                perturb is not None,
                f"learned clause with perturbation {perturb}",
            )


def ordered_support_coordinates(pool, exceptional):
    variables = []
    metadata = []
    for edge in sorted(base.ALL_EDGES):
        if edge in exceptional:
            for a, b in base.CELLS:
                variables.append(pool.id(("entry", edge, a, b)))
                metadata.append(("entry", edge, a, b))
        else:
            u, v = edge
            for color in base.COLORS:
                variables.append(pool.id(("factor", v, u, color)))
                metadata.append(("factor", v, u, color))
            for color in base.COLORS:
                variables.append(pool.id(("factor", u, v, color)))
                metadata.append(("factor", u, v, color))
    return tuple(variables), tuple(metadata)


def independently_mapped_key(item, vertex_permutation, color_permutation):
    if item[0] == "factor":
        _, tail, head, color = item
        return (
            "factor",
            vertex_permutation[tail],
            vertex_permutation[head],
            color_permutation[color],
        )
    _, (u, v), a, b = item
    uu, vv = vertex_permutation[u], vertex_permutation[v]
    aa, bb = color_permutation[a], color_permutation[b]
    if uu > vv:
        uu, vv = vv, uu
        aa, bb = bb, aa
    return "entry", (uu, vv), aa, bb


def test_support_lex_leaders_preserve_an_orbit_minimum():
    exceptional = {(0, 1)}
    identity = tuple(base.VERTICES)
    swap_endpoints = (1, 0, 2, 3, 4, 5)
    automorphisms = (identity, swap_endpoints)
    group_elements = tuple(
        itertools.product(automorphisms, itertools.permutations(base.COLORS))
    )
    rng = random.Random(24072026)

    for _trial in range(12):
        pool = IDPool()
        formula = CNF()
        comparisons = toric.add_support_lex_leaders(
            formula, pool, exceptional, automorphisms
        )
        require(
            comparisons == len(group_elements) - 1,
            f"{comparisons} lex-leader comparisons, expected "
            f"{len(group_elements) - 1}",
        )
        variables, metadata = ordered_support_coordinates(pool, exceptional)
        keys = tuple(pool.obj(variable) for variable in variables)
        key_index = {key: index for index, key in enumerate(keys)}
        seed = tuple(rng.randrange(2) for _ in variables)

        inverse_orbit = []
        for vertex_permutation, color_permutation in group_elements:
            inverse_orbit.append(
                tuple(
                    seed[
                        key_index[
                            independently_mapped_key(
                                item, vertex_permutation, color_permutation
                            )
                        ]
                    ]
                    for item in metadata
                )
            )
        representative = min(inverse_orbit)
        with Solver(name="g4", bootstrap_with=formula) as solver:
            assumptions = [
                variable if value else -variable
                for variable, value in zip(
                    variables, representative, strict=True
                )
            ]
            solve_exactly(
                solver,
                True,
                "the orbit minimum is not accepted by the lex leaders",
                assumptions,
            )

        # Every strictly larger image fails at the first differing bit when
        # it is compared with the symmetry carrying it back toward the min.
        for candidate in set(inverse_orbit) - {representative}:
            with Solver(name="g4", bootstrap_with=formula) as solver:
                assumptions = [
                    variable if value else -variable
                    for variable, value in zip(
                        variables, candidate, strict=True
                    )
                ]
                solve_exactly(
                    solver,
                    False,
                    f"the strictly larger image {candidate} is accepted by "
                    "the lex leaders",
                    assumptions,
                )


def main():
    tests = tuple(
        value
        for name, value in sorted(globals().items())
        if name.startswith("test_") and callable(value)
    )
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"direct Laurent adversarial audit passed ({len(tests)} tests)")


if __name__ == "__main__":
    main()
