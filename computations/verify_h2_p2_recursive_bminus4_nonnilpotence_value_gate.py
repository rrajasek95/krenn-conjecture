#!/usr/bin/env python3
"""Test recursive B-4 repair and the value of the P2 private face.

Forget the labels of the one-root Hasse directions and define the strongest
coefficientwise recursive repair on all four-site ternary words:

  1. invert B-4 on the endpoint-even private B=0,-2 sectors;
  2. take every one-root endpoint/residual Hasse face;
  3. quotient each target word by its complete response line.

This operator is not nilpotent.  Its square has exact trace 109/3 on the
81-word, five-private-coordinate module.  Starting from the 0102 private
face, the first iterate already returns nontrivially to 0112, and the second
returns nontrivially to 0102.  Hence word distance is not a decreasing
filtration and recursive use of the same unlabelled cone does not close P2.

The labelled Boolean Hasse/cobar differential remains finite and squares to
zero; forgetting the direction labels and restarting their degree creates
the spurious recursion.  Thus the positive finite object is one labelled
Hasse square with the missing physical occurrence-local section.

Finally, H_0102=0 alone does not kill the private polynomial.  On the
two-occurrence slice m0=1,m1=-1, the complete row is zero while the private
value is -13/12.  This is an exact response-coordinate pivot, not a claim
that the slice satisfies every other augmented physical source equation.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py":
        "20646d25c248a39d27a8be29332d85b7995e9091e106fc1026fe343847df5eed",
    "notes/h2-p2-0102-private-parity-reinsertion-gate.md":
        "c8c19b6bcd63a5e5b2a0854eac685643d36791ede811924137df717f39b6f620",
    "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py":
        "8ec18f05034b6483512644c49d0009b4b166b0d6b978f6895195321ca9d8417a",
    "computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py":
        "47ea1f915429dc7937ef2e81037c0494136d9ae379d76e0584bb22cef8e0d390",
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py":
        "5b41444ef5f4844bc1bd87a6a4e81e60a631f3549eed21c160efdcb428582ea4",
}
EXPECTED_LEDGER_SHA256 = (
    "efdb245d2055178250441190d82b5fb7f5488ecb368d8c9877cda49a890e23db"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * value for value in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def matrix_add(*matrices):
    return tuple(tuple(sum(entries, Q(0))
                       for entries in zip(*rows, strict=True))
                 for rows in zip(*matrices, strict=True))


def matrix_scale(coefficient, matrix):
    return tuple(tuple(Q(coefficient) * entry for entry in row)
                 for row in matrix)


def diagonal(values):
    size = len(values)
    return tuple(tuple(Q(values[row]) if row == column else Q(0)
                       for column in range(size)) for row in range(size))


def trace(matrix):
    return sum((matrix[index][index] for index in range(len(matrix))), Q(0))


def word_text(word):
    return "".join(map(str, word))


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    parity = load(
        "computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py",
        "p2_recursive_parity",
    )
    occurrence, values, lookup, swap, b_matrix, s_matrix = parity.endpoint_data()
    size = len(values)
    identity = parity.identity(size)
    one = (Q(1),) * size

    # Projection to the five-dimensional endpoint-even augmentation-zero
    # quotient: (I+S)/2 minus the complete constant line.
    constant_projector = tuple(tuple(Q(1, size) for _column in range(size))
                               for _row in range(size))
    private_projector = matrix_add(
        matrix_scale(Q(1, 2), matrix_add(identity, s_matrix)),
        matrix_scale(-1, constant_projector),
    )
    require(parity.matmul(private_projector, private_projector)
            == private_projector
            and parity.rank(list(zip(*private_projector, strict=True))) == 5,
            "the endpoint-even private projector changed")

    b_plus_two = matrix_add(b_matrix, matrix_scale(2, identity))
    b_minus_four = matrix_add(b_matrix, matrix_scale(-4, identity))
    p_zero = matrix_scale(
        Q(-1, 8), parity.matmul(b_minus_four, b_plus_two)
    )
    p_minus_two = matrix_scale(
        Q(1, 12), parity.matmul(b_minus_four, b_matrix)
    )
    lift = parity.matmul(private_projector, matrix_add(
        matrix_scale(Q(-1, 4), p_zero),
        matrix_scale(Q(-1, 6), p_minus_two),
    ))
    require(parity.matmul(b_minus_four, lift) == private_projector,
            "the recursive B-4 inverse changed")

    def transition_diagonals(word):
        """Counts of one-root faces, retaining the occurrence label."""
        answer = defaultdict(lambda: [0] * size)
        for index, (p_site, s_site, matching) in enumerate(values):
            require(len(matching) == 1, "h2 residual stopped being one edge")
            residual = matching[0]
            for endpoint in (p_site, s_site):
                for selected in residual:
                    if word[endpoint] == word[selected]:
                        continue
                    for changed in (endpoint, selected):
                        target = list(word)
                        target[changed] = (
                            word[selected] if changed == endpoint
                            else word[endpoint]
                        )
                        answer[tuple(target)][index] += 1
        return {target: diagonal(counts)
                for target, counts in answer.items()}

    def blocks(word):
        return {
            target: parity.matmul(
                private_projector, parity.matmul(direction, lift)
            )
            for target, direction in transition_diagonals(word).items()
        }

    words = tuple((a, b, c, d) for a in range(3) for b in range(3)
                  for c in range(3) for d in range(3))
    word_blocks = {word: blocks(word) for word in words}
    require(len(words) == 81
            and all(word not in word_blocks[word] for word in words),
            "a one-root face stopped changing its word")

    # If the global recursive operator were nilpotent, every positive-power
    # trace would vanish.  Compute trace(R^2) without forming the 405-square
    # matrix, by summing all two-word round trips.
    trace_square = Q(0)
    oriented_round_trips = 0
    for source in words:
        for target, forward in word_blocks[source].items():
            backward = word_blocks[target].get(source)
            if backward is None:
                continue
            trace_square += trace(parity.matmul(backward, forward))
            oriented_round_trips += 1
    require(oriented_round_trips == 288 and trace_square == Q(109, 3),
            ("the recursive round-trip trace changed",
             oriented_round_trips, trace_square))

    private_gate = load(
        "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py",
        "p2_recursive_private",
    )
    private_ledger, private_digest = private_gate.audit()
    require(private_digest == private_gate.EXPECTED_LEDGER_SHA256,
            "the 0102 private ledger changed")
    start = tuple(map(Q, private_ledger["endpoint_adjacency_decomposition"]
                      ["private_part"]))
    start_word = tuple(map(int, "0102"))
    original_word = tuple(map(int, "0112"))
    detector = tuple(Q(index in (0, 3)) - Q(index in (1, 6))
                     for index in range(size))

    def recursive_step(states):
        output = defaultdict(lambda: [Q(0)] * size)
        for source, vector in states.items():
            for target, block in word_blocks[source].items():
                image = parity.matvec(block, vector)
                for index, value in enumerate(image):
                    output[target][index] += value
        return {word: tuple(vector) for word, vector in output.items()
                if any(vector)}

    states = {start_word: start}
    iteration_records = []
    for iteration in range(1, 7):
        states = recursive_step(states)
        distances = [sum(left != right for left, right in
                         zip(word, original_word, strict=True))
                     for word in states]
        iteration_records.append({
            "iteration": iteration,
            "nonzero_words": len(states),
            "minimum_distance_from_0112": min(distances),
            "maximum_distance_from_0112": max(distances),
            "detector_on_0112": str(dot(
                detector, states.get(original_word, (Q(0),) * size)
            )),
            "detector_on_0102": str(dot(
                detector, states.get(start_word, (Q(0),) * size)
            )),
        })
    require([record["nonzero_words"] for record in iteration_records[:4]]
            == [8, 32, 64, 81]
            and iteration_records[0]["detector_on_0112"] == "35/72"
            and iteration_records[1]["detector_on_0102"] == "-857/3888"
            and all(record["minimum_distance_from_0112"] == 0
                    for record in iteration_records),
            ("the selected recursive spread changed", iteration_records))

    # Value-level response quotient.  Let m_i be the twelve literal
    # occurrence monomials.  H=sum m_i.  The private coefficient is not
    # constant, so it survives the same-degree quotient by H.  The explicit
    # two-coordinate evaluation is the smallest pivot witness.
    require(sum(start, Q(0)) == 0 and start != (Q(0),) * size,
            "the private polynomial changed")
    occurrence_evaluation = tuple(Q(1 if index == 0 else
                                    -1 if index == 1 else 0)
                                  for index in range(size))
    complete_value = dot(one, occurrence_evaluation)
    private_value = dot(start, occurrence_evaluation)
    require(complete_value == 0 and private_value == Q(-13, 12),
            ("the occurrence-coordinate pivot changed",
             complete_value, private_value))

    # The source Hasse totalization itself is finite.  On two labelled root
    # directions, reduced coproduct sends {0,1} to 0|1+1|0 and the cobar
    # boundary of either singleton vanishes, so the next boundary is zero.
    hasse = load(
        "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py",
        "p2_recursive_hasse",
    )
    two_direction_top = 0b11
    first_boundary = hasse.cobar_boundary((two_direction_top,))
    second_boundary = hasse.apply_cobar(first_boundary)
    require(first_boundary == {
        (0b01, 0b10): 1,
        (0b10, 0b01): 1,
    } and not second_boundary,
            ("the labelled two-direction Hasse square changed",
             first_boundary, second_boundary))

    ledger = {
        "theorem": "h2 recursive B-4 nonnilpotence and value gate",
        "pins": PINS,
        "raw_recursive_operator": {
            "word_count": len(words),
            "private_dimension_per_word": 5,
            "total_dimension": 405,
            "definition": (
                "R=Ppriv*one-root-Hasse*(B-4)^-1 on every word block"
            ),
            "oriented_two_step_round_trips": oriented_round_trips,
            "trace_R": "0 (every one-root face changes word)",
            "trace_R_squared": str(trace_square),
            "nilpotent": False,
        },
        "selected_0102_iteration": iteration_records,
        "word_filtration": {
            "starting_distance_from_0112": 1,
            "first_iterate_0112_detector": "35/72",
            "second_iterate_0102_detector": "-857/3888",
            "strictly_decreasing": False,
            "all_81_words_reached_at_iteration": 4,
        },
        "finite_labelled_replacement": {
            "root_directions": 2,
            "first_cobar_boundary": ["01|10", "10|01"],
            "second_cobar_boundary": 0,
            "interpretation": (
                "retain the Hasse direction labels and totalize one square; "
                "do not reset Hasse degree after each B-4 lift"
            ),
            "physical_occurrence_section_constructed": False,
        },
        "value_level_pivot": {
            "response_polynomial": "H_0102=sum_i m_i",
            "evaluation": "m0=1,m1=-1, all other m_i=0",
            "H_0102_value": str(complete_value),
            "r_private_value": str(private_value),
            "H_zero_implies_private_zero": False,
            "same_degree_membership": (
                "r_private is not a scalar multiple of the complete row"
            ),
            "scope": (
                "literal occurrence-coordinate/associated-graded slice; "
                "not asserted to satisfy all other augmented physical rows"
            ),
        },
        "frontier": (
            "recursive copies of the unlabelled even Cartan/B-4 cone do not "
            "close P2 and do not define a decreasing filtration.  The "
            "finite source-side object is the one labelled Hasse square, "
            "whose missing physical datum remains the occurrence-local "
            "one-endpoint section together with its dq23 reinsertion face"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("h2 recursive B-4 ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("raw recursive B-4 trace(R^2)=109/3: NOT NILPOTENT")
    print("0102 -> 0112 -> 0102: NONZERO PRIVATE ROUND TRIP")
    print("word-distance filtration: NOT DECREASING")
    print("labelled two-direction Hasse cobar: d^2=0")
    print("H_0102=0 does not kill r_private: value -13/12")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
