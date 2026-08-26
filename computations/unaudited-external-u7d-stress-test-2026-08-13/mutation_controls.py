"""Mutation controls for our own U7D verification and classification code.

UNAUDITED EXTERNAL STRESS TEST.  Task E: every checker in this directory is
attacked with a deliberate perturbation; a checker that still passes on a
mutated input is worthless.  Each control asserts that the corresponding
check FAILS (or changes its verdict) exactly as it should.
"""

from __future__ import annotations

import copy
import itertools
import random
from fractions import Fraction

import classify_u7d_our_machinery as C
import u7d_witness_data as D
import verify_u7d_witness as V

PASSED: list[str] = []


def expect_failure(name: str, action) -> None:
    """Assert that `action` raises: the checker must notice the mutation."""
    try:
        action()
    except AssertionError as error:
        PASSED.append(name)
        print(f"  KILLED  {name}: {str(error)[:90]}")
        return
    raise SystemExit(f"MUTATION SURVIVED (checker is blind): {name}")


def expect_success(name: str, action) -> None:
    """Assert that `action` completes: a control that must still pass."""
    action()
    PASSED.append(name)
    print(f"  OK      {name}")


class patched:
    """Temporarily replace attributes on the verification modules."""

    def __init__(self, **assignments):
        self.assignments = assignments
        self.saved = {}

    def __enter__(self):
        for target, value in self.assignments.items():
            module_name, attribute = target.split(".", 1)
            module = {"V": V, "C": C, "D": D}[module_name]
            self.saved[target] = getattr(module, attribute)
            setattr(module, attribute, value)
        return self

    def __exit__(self, *_):
        for target, value in self.saved.items():
            module_name, attribute = target.split(".", 1)
            module = {"V": V, "C": C, "D": D}[module_name]
            setattr(module, attribute, value)
        return False


def mutate_table(changes):
    """Return a copy of the witness table with the given pairs replaced."""
    table = dict(V.TABLE)
    table.update(changes)
    return table


# --------------------------------------------------------------------------
def control_enumeration():
    """The matching enumerator must be right at other orders too."""
    counts = {2: 1, 4: 3, 6: 15, 8: 105}
    for order, expected in counts.items():
        found = V.matchings_lowest_first(tuple(range(order)))
        assert len(found) == expected and len(set(found)) == expected, order
        assert set(found) == V.matchings_from_permutations(order), order


def control_sign_flip():
    """Flipping lambda_35 must break a cycle fibre and the holonomy."""
    table = mutate_table({(3, 5): (0, 1, -1)})
    with patched(**{"V.TABLE": table}):
        fibres = V.build_fibres()
        V.check_pure_and_cycle(fibres)


def control_sign_flip_holonomy():
    """The same flip must move H from -1 to +1."""
    table = mutate_table({(3, 5): (0, 1, -1)})
    with patched(**{"V.TABLE": table}):
        amplitudes = {edge: Fraction(data[2]) for edge, data in table.items()}
        value = V.laurent(V.circulation(), amplitudes)
        assert value == D.CLAIMED_HOLONOMY, f"H = {value} (mutation not seen)"


def control_label_change():
    """Relabelling 37 must destroy the pure colour-1 fibre."""
    table = mutate_table({(3, 7): (1, 0, 1)})
    with patched(**{"V.TABLE": table}):
        fibres = V.build_fibres()
        V.check_pure_and_cycle(fibres)


def control_balance_perturbation():
    """A single wrong auxiliary weight must break the endpoint balance."""
    balance = dict(D.AUX_BALANCE)
    balance[(3, 4)] = 6
    with patched(**{"V.AUX_BALANCE": balance}):
        V.check_balance()


def control_balance_sign():
    """A non-positive auxiliary weight must be rejected."""
    balance = dict(D.AUX_BALANCE)
    balance[(0, 5)] = 6 - 13   # keeps no balance and is negative
    with patched(**{"V.AUX_BALANCE": balance}):
        V.check_balance()


def control_coercivity_certificate():
    """A p that is positive but unbalanced must fail the Kempf-Ness check."""
    balance = {edge: 1 for edge in D.AUX_BALANCE}
    with patched(**{"V.AUX_BALANCE": balance}):
        V.exact_coercivity_proof()


def control_census_row():
    """A corrupted census certificate row must be caught."""
    census = copy.deepcopy(D.CLAIMED_CENSUS_TABLE)
    census["00011011"] = ("01|24|36|57",)
    with patched(**{"V.CLAIMED_CENSUS_TABLE": census}):
        V.check_census(V.build_fibres())


def control_census_counts():
    """A wrong 57/10/3 distribution must be caught."""
    with patched(**{"V.CLAIMED_CENSUS_COUNTS":
                    {"empty": 56, "singleton": 11, "binomial": 3}}):
        V.check_census(V.build_fibres())


def control_exposed_word():
    """Claiming a different exposed fibre must be caught."""
    with patched(**{"V.CLAIMED_EXPOSED_FIBRE": ((0, 4), (1, 7), (2, 5), (3, 6))}):
        V.check_exposed(V.build_fibres())


def control_circulation():
    """A wrong bridge set must break the zero-endpoint-character test."""
    bridge = (((2, 3), (4, 5)), ((1, 5), (2, 6)), ((4, 6), (1, 7)))
    with patched(**{"V.BRIDGE": bridge}):
        V.check_holonomy(V.build_fibres())


def control_gauge_invariance_detector():
    """A vector NOT in ker(incidence) must be seen to be gauge dependent."""
    exponent = {(0, 1): 1, (2, 3): -1}
    character = V.endpoint_character(exponent)
    assert character, "a non-invariant vector was reported as invariant"
    amplitudes = {edge: Fraction(data[2]) for edge, data in V.TABLE.items()}
    gauge_amplitudes = dict(amplitudes)
    gauge_amplitudes[(0, 1)] = amplitudes[(0, 1)] * 3
    assert (V.laurent(exponent, amplitudes)
            != V.laurent(exponent, gauge_amplitudes)), "no gauge sensitivity"


# --------------------------------------------------------------------------
# controls on the O1 engine
# --------------------------------------------------------------------------
def control_hnf_algebra():
    """H = U * M with U unimodular, on random integer matrices."""
    generator = random.Random(20260813)
    for _ in range(40):
        rows = generator.randint(2, 7)
        columns = generator.randint(2, 7)
        matrix = [[generator.randint(-6, 6) for _ in range(columns)]
                  for _ in range(rows)]
        hermite, transform = C.hnf_with_transform(matrix)
        for r in range(rows):
            for c in range(columns):
                assert hermite[r][c] == sum(transform[r][k] * matrix[k][c]
                                            for k in range(rows)), "H != U M"
        determinant = _determinant(transform)
        assert determinant in (1, -1), f"transform not unimodular: {determinant}"


def _determinant(matrix):
    """Exact integer determinant by fraction arithmetic."""
    size = len(matrix)
    work = [[Fraction(entry) for entry in row] for row in matrix]
    answer = Fraction(1)
    for column in range(size):
        pivot = next((r for r in range(column, size) if work[r][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        answer *= work[column][column]
        head = work[column][column]
        work[column] = [entry / head for entry in work[column]]
        for r in range(column + 1, size):
            if work[r][column]:
                factor = work[r][column]
                work[r] = [a - factor * b for a, b in zip(work[r], work[column])]
    assert answer.denominator == 1
    return int(answer)


def control_o1_positive():
    """A planted odd relation MUST be found (O1 engine is not vacuous)."""
    generator = random.Random(7)
    for _ in range(20):
        width = 9
        first = [generator.randint(-3, 3) for _ in range(width)]
        second = [generator.randint(-3, 3) for _ in range(width)]
        third = [-a - b for a, b in zip(first, second)]   # sum of three = 0
        relation = C.odd_relation([first, second, third])
        assert relation is not None, "planted odd 3-cycle relation missed"
        assert sum(relation) % 2 == 1, relation


def control_o1_even_negative():
    """A planted EVEN-only dependency must NOT be reported as O1."""
    generator = random.Random(11)
    for _ in range(20):
        width = 9
        first = [generator.randint(-3, 3) for _ in range(width)]
        second = [-entry for entry in first]              # sum of two = 0
        assert C.odd_relation([first, second]) is None, "false O1 on a 2-cycle"
        fourth = [generator.randint(-3, 3) for _ in range(width)]
        fifth = [generator.randint(-3, 3) for _ in range(width)]
        sixth = [-a - b for a, b in zip(fourth, fifth)]
        # doubling every row makes every dependency even in the SAME rows only
        # if we also drop the odd one; instead pair each row with its negative
        rows = [fourth, [-e for e in fourth], fifth, [-e for e in fifth]]
        assert C.odd_relation(rows) is None, "false O1 on paired negatives"
        del sixth


def control_o1_on_witness_cycle_is_a_true_negative():
    """The witness's own 3 rows have NO dependency at all -- verify directly."""
    fibres = V.build_fibres()
    cells = C.support_cells()
    cell_index = {cell: position for position, cell in enumerate(cells)}
    rows, _ = C.fibre_relations(fibres, list(D.CYCLE_WORDS), cells, cell_index)
    assert len(rows) == 3
    rank = C.rational_rank([[Fraction(v) for v in row] for row in rows])
    assert rank == 3, f"rank {rank}: the rows are dependent after all"
    assert C.odd_relation(rows) is None
    # and the true reason: their sum is z, which is nonzero
    total = [sum(row[k] for row in rows) for k in range(len(cells))]
    assert any(total), "the three rows sum to zero -- that WOULD be an O1 kill"
    nonzero = sum(1 for value in total if value)
    assert nonzero == 12, nonzero


def control_o1_would_fire_if_z_vanished():
    """Boundary probe: force a genuine 1 = -1 and confirm O1 fires.

    Keep the witness's first two cycle rows and replace the third by the one
    that would make the three-fibre cycle CLOSE, i.e. r_0 + r_1 + r_2 = 0.
    That is the hypothetical support where the odd cycle has trivial exponent
    dependency -- exactly the configuration our O1 mechanism is designed to
    kill -- and the engine must fire there.  It must also stay silent when a
    FOURTH fibre closes the cycle instead (an even cycle, epsilon = +1).
    """
    fibres = V.build_fibres()
    cells = C.support_cells()
    cell_index = {cell: position for position, cell in enumerate(cells)}
    rows, _ = C.fibre_relations(fibres, list(D.CYCLE_WORDS), cells, cell_index)

    closing_third = [-(rows[0][k] + rows[1][k]) for k in range(len(cells))]
    relation = C.odd_relation([rows[0], rows[1], closing_third])
    assert relation is not None, "O1 failed on a genuinely closing odd cycle"
    assert sum(relation) % 2 == 1, relation

    closing_fourth = [-sum(row[k] for row in rows) for k in range(len(cells))]
    assert C.odd_relation(rows + [closing_fourth]) is None, (
        "O1 fired on a four-fibre (even) closing cycle")


def control_o2_detector():
    """O2 must fire on the full target and not on the cycle subsystem."""
    fibres = V.build_fibres()
    cells = C.support_cells()
    cell_index = {cell: position for position, cell in enumerate(cells)}
    pure = [(colour,) * V.ORDER for colour in range(V.COLOURS)]
    mixed = [w for w in itertools.product(range(V.COLOURS), repeat=V.ORDER)
             if w not in pure]
    full = C.classify("control: full", fibres, mixed, pure, cells, cell_index)
    assert full["O2"] and full["singletons"] == 94, full
    partial = C.classify("control: cycle only", fibres, list(D.CYCLE_WORDS),
                         pure, cells, cell_index)
    assert not partial["O2"] and not partial["O1"], partial


def control_o2_blind_to_two_term_fibres():
    """O2 must not fire on a system whose fibres are all binomial."""
    fibres = V.build_fibres()
    cells = C.support_cells()
    cell_index = {cell: position for position, cell in enumerate(cells)}
    binomial_words = [word for word, terms in fibres.items() if len(terms) == 2]
    pure = [(colour,) * V.ORDER for colour in range(V.COLOURS)]
    result = C.classify("control: all binomial fibres", fibres, binomial_words,
                        pure, cells, cell_index)
    assert not result["O2"], result


def control_lattice_membership():
    """A perturbed z must be detected as leaving ker(unsigned incidence)."""
    exponent = dict(V.circulation())
    exponent[(0, 3)] = exponent.get((0, 3), 0) + 1
    assert V.endpoint_character(exponent), "perturbed z still reported in L"


def main():
    """Run every control."""
    print("UNAUDITED EXTERNAL STRESS TEST -- mutation controls (task E)\n")
    print(" positive controls (must pass):")
    expect_success("enumeration at orders 2,4,6,8", control_enumeration)
    expect_success("HNF identity H = U M, U unimodular", control_hnf_algebra)
    expect_success("O1 finds a planted odd relation", control_o1_positive)
    expect_success("O1 rejects even-only dependencies", control_o1_even_negative)
    expect_success("witness cycle rows are independent",
                   control_o1_on_witness_cycle_is_a_true_negative)
    expect_success("O1 fires when the odd cycle really closes",
                   control_o1_would_fire_if_z_vanished)
    expect_success("O2 fires on the full target only", control_o2_detector)
    expect_success("O2 silent on all-binomial systems",
                   control_o2_blind_to_two_term_fibres)
    expect_success("gauge-dependence detector", control_gauge_invariance_detector)
    expect_success("lattice membership detector", control_lattice_membership)

    print("\n mutations (must be killed):")
    expect_failure("flip lambda_35 -> cycle fibre check", control_sign_flip)
    expect_failure("flip lambda_35 -> holonomy value", control_sign_flip_holonomy)
    expect_failure("relabel edge 37 -> pure fibre check", control_label_change)
    expect_failure("perturb p_34 -> endpoint balance", control_balance_perturbation)
    expect_failure("negative p_05 -> endpoint balance", control_balance_sign)
    expect_failure("all-ones p -> coercivity certificate",
                   control_coercivity_certificate)
    expect_failure("corrupt census row -> 13-row certificate", control_census_row)
    expect_failure("wrong 57/10/3 counts -> census", control_census_counts)
    expect_failure("wrong exposed fibre -> eta check", control_exposed_word)
    expect_failure("wrong bridge B_2 -> circulation/holonomy", control_circulation)

    print(f"\nALL {len(PASSED)} CONTROLS BEHAVED AS REQUIRED")


if __name__ == "__main__":
    main()
