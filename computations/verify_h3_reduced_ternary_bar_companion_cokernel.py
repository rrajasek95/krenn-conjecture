#!/usr/bin/env python3
"""Exact source-labelled no-go for the reduced ternary GL3 bar comparison.

The favourable reduced comparison has coefficient sum zero, so the coarse
normalized-bar/ordinary-residue augmentation vanishes.  Its contragredient
companion is nevertheless graded by the complete eight-site output word.
Cancelling that companion with the complete full-nine rows is coefficientwise.
The coefficient of the desired all-zero endpoint therefore uses the pure X0
anchor and leaves its target.  Cancelling that target with the split cap
recreates the familiar Eq defect.

This is a finite module statement for the standard local-covariance bar,
the complete 3^8 word rows, and the old split cap.  It does not exclude a new
source-resolution generator with a different augmentation.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


EXPECTED_DIGEST = "358aefc192c989c981e34be4b7cb42aa49823a17f4cda427742bb5adad02fa75"
COLORS = (0, 1, 2)
INPUT_WORD = (0, 1, 2, 1, 1, 2, 2, 2)
ZERO_WORD = (0,) * 8
ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_sitewise_gl3_covariance_face_tau_no_go.py":
        "bda92248adc08434896a99d5dfd241321e9be926ab7e8117daf55ee9df74c685",
    "notes/h3-sitewise-gl3-covariance-face-tau-no-go.md":
        "b7052c310034500d1e720484c958a11ce167056a68db12be9a9b6129f384cbfd",
    "computations/verify_oo_complete_order4_spencer_output_cascade.py":
        "8c74bc61cdeac3cbc93add6ae05e2c56bcface7de7f80002ebc34c02656cbf43",
    "notes/oo-complete-order4-spencer-output-cascade.md":
        "6aad7ab7ef2583fa5288cdf5076e0a281432b973438f55970f3021643df853ae",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def add_coefficient(vector, word, coefficient):
    value = vector.get(word, F(0)) + F(coefficient)
    if value:
        vector[word] = value
    elif word in vector:
        del vector[word]


def coefficient_sum(vector):
    return sum(vector.values(), F(0))


def diagonal_projection(vector):
    """Projection to the three independently labelled diagonal targets."""
    return tuple(vector.get((color,) * 8, F(0)) for color in COLORS)


def target_action_of_word_change(output_word):
    """Product E_(output_i <- INPUT_i) acting on ternary GHZ Delta.

    A pure GHZ summand survives only if every input label is the same.
    The selected h=3 word contains 0, 1, and 2, so every output endpoint is
    target-zero before one adds rows to cancel its source companion.
    """
    require(len(output_word) == len(INPUT_WORD), "output word length")
    if len(set(INPUT_WORD)) != 1:
        return ()
    return (tuple(output_word),)


def pair_reduced_comparison(alternative=1):
    """(0-alternative) at the two endpoint-2 sites, other outputs fixed 0."""
    require(alternative in (1, 2), "alternative output colour")
    answer = {}
    for left_choice, right_choice in product((0, alternative), repeat=2):
        word = [0] * 8
        word[6] = left_choice
        word[7] = right_choice
        coefficient = (-1) ** ((left_choice == alternative)
                               + (right_choice == alternative))
        add_coefficient(answer, tuple(word), coefficient)
    return answer


def rank(columns):
    if not columns:
        return 0
    work = [list(map(F, row)) for row in zip(*columns, strict=True)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), F(0))


def word_module_audit():
    words = tuple(product(COLORS, repeat=8))
    word_set = set(words)
    pure_words = tuple((color,) * 8 for color in COLORS)
    mixed_words = tuple(word for word in words if word not in pure_words)
    require(len(words) == 6561 and len(mixed_words) == 6558,
            "complete ternary word count")
    require(len({(word[0], word[1:]) for word in words}) == 6561,
            "x-sector/residual-word source labels collided")
    require(all(not target_action_of_word_change(word) for word in words),
            "a word-changing endpoint acquired direct GHZ target")

    # The full row used to cancel the D companion has the same word label.
    # Therefore the companion map is the 6561-dimensional identity: its
    # cancellation coefficient is unique.  Its target is the diagonal
    # projection, with one independent anchor in each x-sector.
    companion_rank = len(words)
    anchor_rank = len(pure_words)
    augmentation_rank = 1
    reduced_dimension = len(words) - augmentation_rank
    invisible_reduced_dimension = len(words) - augmentation_rank - anchor_rank
    require(reduced_dimension == 6560
            and invisible_reduced_dimension == 6557,
            "reduced/invisible word dimensions changed")

    pair_records = []
    for alternative in (1, 2):
        candidate = pair_reduced_comparison(alternative)
        require(set(candidate).issubset(word_set) and len(candidate) == 4,
                "endpoint comparison support")
        require(coefficient_sum(candidate) == 0,
                "endpoint comparison lost reduced augmentation")
        require(candidate.get(ZERO_WORD) == 1,
                "desired all-zero endpoint coefficient changed")
        projection = diagonal_projection(candidate)
        require(projection == (F(1), F(0), F(0)),
                "mixed companions unexpectedly cancelled X0")
        require(all(not target_action_of_word_change(word) for word in candidate),
                "candidate bar acquired direct target")
        pair_records.append({
            "alternative": alternative,
            "support": ["".join(map(str, word)) for word in sorted(candidate)],
            "coefficients": [int(candidate[word]) for word in sorted(candidate)],
            "coarse_augmentation": int(coefficient_sum(candidate)),
            "direct_target_terms": 0,
            "target_after_companion_cancellation": [int(x) for x in projection],
        })

    # A direct pure-colour contrast is also augmentation-zero, but the three
    # diagonal target grades do not scalar-cancel.  The cyclic telescoper is
    # literally zero and hence cannot retain the desired endpoint.
    pure_contrast = {pure_words[0]: F(1), pure_words[1]: F(-1)}
    require(coefficient_sum(pure_contrast) == 0
            and diagonal_projection(pure_contrast) == (F(1), F(-1), F(0)),
            "pure target contrast collapsed its labels")
    cyclic = {}
    for left, right in ((0, 1), (1, 2), (2, 0)):
        add_coefficient(cyclic, pure_words[left], 1)
        add_coefficient(cyclic, pure_words[right], -1)
    require(not cyclic, "ternary cyclic endpoint sum is not the zero chain")

    # The desired coefficient functional is exactly the X0 component of the
    # diagonal target projection.  Hence it vanishes on every reduced chain
    # whose uniquely cancelled companion leaves target zero.  Mixed rows and
    # the other two anchors cannot change this coefficientwise statement.
    probes = []
    reference_mixed = next(word for word in mixed_words if word != ZERO_WORD)
    for color in COLORS:
        vector = {pure_words[color]: F(1), reference_mixed: F(-1)}
        require(coefficient_sum(vector) == 0,
                "target-surjectivity probe lost augmentation zero")
        probes.append(diagonal_projection(vector))
    require(rank(probes) == 3,
            "diagonal target projection on the reduced space lost rank")

    return {
        "word_count": len(words),
        "x_sectors": 3,
        "residual_words_per_sector": 2187,
        "mixed_full_rows": len(mixed_words),
        "diagonal_anchor_rows": len(pure_words),
        "source_labelled_companion_rank": companion_rank,
        "normalized_augmentation_rank": augmentation_rank,
        "reduced_dimension": reduced_dimension,
        "invisible_reduced_dimension": invisible_reduced_dimension,
        "diagonal_projection_rank_on_reduced_space": rank(probes),
        "desired_functional": "coefficient(00000000)=X0-target-coordinate",
        "pair_comparisons": pair_records,
        "pure_contrast_target": [1, -1, 0],
        "cyclic_three_colour_sum": "zero chain",
    }


def physical_block_audit():
    records = []
    for y in (F(1), F(2), F(-3, 2)):
        # One direct-summand copy for the X0 source label.  X1 and X2 have
        # independent copies, so they cannot cancel these coordinates.
        full_row = (F(-1), F(0), F(1), F(0))
        cap_target = (F(0), -y, F(1), F(0))
        ordinary = (F(0), F(1), F(0), F(1))
        after_target_cancellation = tuple(
            left - right for left, right in
            zip(full_row, cap_target, strict=True)
        )
        desired = (F(0), y, F(0), F(0))
        require(after_target_cancellation == (F(-1), y, F(0), F(0)),
                "target cancellation stopped recreating the Eq defect")
        old = (full_row, cap_target, ordinary)
        require(rank(old) == 3 and rank(old + (desired,)) == 4,
                "reduced comparison physical rank changed")
        covector = (y, F(1), y, F(-1))
        require(all(dot(covector, column) == 0 for column in old),
                "physical cokernel stopped killing old columns")
        require(dot(covector, desired) == y,
                "physical cokernel stopped detecting desired boundary")
        records.append({
            "Y": str(y),
            "target_cancelled_column": [str(x) for x in after_target_cancellation],
            "old_rank": rank(old),
            "rank_with_desired": rank(old + (desired,)),
            "cokernel_on_desired": str(y),
        })
    return records


def main():
    pin_dependencies()
    word_module = word_module_audit()
    physical = physical_block_audit()
    ledger = {
        "pins": PINS,
        "input_word": "".join(map(str, INPUT_WORD)),
        "word_module": word_module,
        "physical_blocks": physical,
        "verdict": (
            "reduced augmentation kills coarse ores, but coefficientwise "
            "companion cancellation consumes X0 and recreates the Eq defect"
        ),
        "scope": (
            "standard ternary local-covariance bar + all 3^8 full rows + "
            "three labelled anchors + old split cap"
        ),
    }
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    require(EXPECTED_DIGEST != "TO_BE_FILLED", "pin EXPECTED_DIGEST")
    require(digest == EXPECTED_DIGEST, ("ledger digest changed", digest))
    print("h=3 reduced ternary bar companion cokernel: PASS")
    print("word companion rank 6561; mixed rows 6558; anchor rank 3")
    print("22->00 reduced pair has coarse ores 0 but leaves X0 after companion cancellation")
    print("target cancellation recreates -Eq+Yw; desired invisible Yw raises rank 3->4")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()
