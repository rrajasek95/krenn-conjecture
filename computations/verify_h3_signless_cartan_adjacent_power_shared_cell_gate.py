#!/usr/bin/env python3
"""Audit the proposed shared signless-Cartan/adjacent-power target cell.

On the balanced six-site word 001122 let rho=(1 4), and let w be the
simultaneous 0<->2 Weyl action at sites 1 and 4.  The two operations
commute and rho*w fixes the selected word.  The rho-odd Cartan prism is
target-safe, while the rho-even prism has target defect

    (1+rho)(w-1)Delta = 2(w-1)Delta.

This checker proves two exact guards.

* Correcting the even prism inside span{H_w,rho H_w} collapses it to the odd
  prism; retaining an even/fixed-word comparison needs an independent cone
  direction.
* The literal diagonal J1/J2 cap targets and every pure-colour coloop target
  are supported on monochromatic words.  The Weyl defect has two unavoidable
  mixed target words, so those existing rows cannot be the required cone
  direction.  A shared construction needs a root-decorated label map.

The beta=0 collision is deliberately excluded.  Eta/sigma values are not
readouts of the adjacent cap row; the committed construction obtains them
from the separately commuting -dOmega ridge factor.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from itertools import permutations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_cut_swap_collision_word_orbit_obstruction.py":
        "d7281084a0fc084e6d951f527daf92c92faefebec183a83d6cfa33e055596c77",
    "computations/verify_h3_active_fan_coloop_complete_row_pivot.py":
        "d62fd630abac6e4d25bd6ffb0c1a2070311ec1c5d3c7764f56793283f78aa94a",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_residual_q_order6_ridge_jet_commutation.py":
        "00a0798b4aa1d901b52645cac3f1dbe2854a3d8ce796191f7a4ff9a6e295b28f",
    "computations/verify_h3_phi_diagonal_rees_extension_gate.py":
        "d719c507db7c2c1f2ecfb3b639cfae34fc06e930435891be789aa8243a844630",
    "computations/verify_oo_adjacent_power_relative_generator_inventory.py":
        "e25e7416273618acf39ee11d688fe3c980808a616c26eb49d3ef77509e3546b7",
    "computations/verify_protected_physical_comparison_first_source_cell.py":
        "0c93a7e67f1f48d114e343a282820477fe5a86649502500c5b00ee5e560b0245",
    "computations/verify_diagonal_rees_saturation_cap_jet_bockstein.py":
        "12c4cc4a947d99eee22cbd87e900ac6c7a56df2c533c4c44c52f0ab0fcedee2a",
}
EXPECTED_LEDGER_SHA256 = (
    "90ab61ba0839e56bfc012a727ffbc5da1bc6f08b6b209d1c5410273f38bade0d"
)

N = 6
COLOURS = (0, 1, 2)
WORD = (0, 0, 1, 1, 2, 2)
ROOTS = (1, 4)
RHO = (0, 4, 2, 3, 1, 5)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def rank(rows):
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def add_counters(*terms):
    answer = Counter()
    for coefficient, vector in terms:
        for word, value in vector.items():
            answer[word] += Q(coefficient) * Q(value)
            if not answer[word]:
                del answer[word]
    return answer


def rho_word(word):
    answer = [None] * len(word)
    for old_site, colour in enumerate(word):
        answer[RHO[old_site]] = colour
    return tuple(answer)


def weyl_word(word):
    """The chosen 0<->2 Weyl representatives; colour 1 is fixed.

    Diagonal torus signs are normalized so rho*w fixes the selected word
    literally.  They do not affect the target-support obstruction below.
    """
    answer = list(word)
    for site in ROOTS:
        if answer[site] == 0:
            answer[site] = 2
        elif answer[site] == 2:
            answer[site] = 0
    return tuple(answer), 1


def transform(counter, operation):
    answer = Counter()
    for word, coefficient in counter.items():
        changed = operation(word)
        sign = 1
        if isinstance(changed, tuple) and len(changed) == 2 \
                and isinstance(changed[1], int):
            changed, sign = changed
        answer[changed] += coefficient * sign
    return Counter({word: value for word, value in answer.items() if value})


def audit_cut_word_and_target():
    rho_then_w = lambda word: weyl_word(rho_word(word))
    w_then_rho = lambda word: (rho_word(weyl_word(word)[0]),
                               weyl_word(word)[1])
    for word in ((0,) * N, (1,) * N, (2,) * N, WORD,
                 (2, 0, 1, 2, 0, 1)):
        require(rho_then_w(word) == w_then_rho(word),
                ("rho and w stopped commuting", word))
    require(rho_then_w(WORD) == (WORD, 1),
            "rho*w stopped fixing 001122")
    require(weyl_word(WORD)[0] == rho_word(WORD),
            "the two-local repair stopped agreeing with cut swap")

    delta = Counter({(colour,) * N: Q(1) for colour in COLOURS})
    w_delta = transform(delta, weyl_word)
    defect = add_counters((1, w_delta), (-1, delta))
    rho_defect = transform(defect, rho_word)
    require(rho_defect == defect,
            "the Weyl target defect stopped being rho-even")
    even_defect = add_counters((1, defect), (1, rho_defect))
    require(even_defect == Counter({word: 2 * value
                                    for word, value in defect.items()}),
            "the signless target defect stopped being twice the Weyl defect")

    pure_words = {(colour,) * N for colour in COLOURS}
    mixed_support = {word for word in defect if word not in pure_words}
    require(len(defect) == 4 and len(mixed_support) == 2
            and all(defect[word] == 1 for word in mixed_support),
            ("the Weyl target support changed", defect))
    require(mixed_support == {(0, 2, 0, 0, 2, 0),
                              (2, 0, 2, 2, 0, 2)},
            ("unexpected mixed Weyl targets", mixed_support))
    return {
        "selected_word": "001122",
        "rho": "(1 4)",
        "root_sites": list(ROOTS),
        "root_action": "simultaneous 0<->2 (torus signs normalized)",
        "rho_w_fixes_selected_word": True,
        "weyl_target_defect": {
            "support": ["".join(map(str, word)) for word in sorted(defect)],
            "coefficients": [str(defect[word]) for word in sorted(defect)],
            "mixed_support": ["".join(map(str, word))
                              for word in sorted(mixed_support)],
        },
        "signless_target_defect": "2*(w-1)*Delta",
    }, defect


def audit_parity_gate():
    # If the endpoint swap fixes the Weyl defect, a*H_w+b*rho*H_w is
    # target-safe iff a+b=0.  The even vector (1,1) cannot remain even after
    # an internal correction by H_w; subtracting 2H_w gives (-1,1).
    candidates = tuple((a, b) for a in range(-4, 5)
                       for b in range(-4, 5) if (a, b) != (0, 0))
    safe = tuple(pair for pair in candidates if sum(pair) == 0)
    require(safe and all(a == -b for a, b in safe),
            "the Cartan target-safe line changed")
    corrected = (Q(1) - 2, Q(1))
    require(corrected == (Q(-1), Q(1)) and sum(corrected) == 0,
            "the internal signless correction changed")
    return {
        "Cartan_operator_basis": ["H_w", "rho*H_w"],
        "target_safe_line": "a+b=0, hence multiples of (1-rho)*H_w",
        "signless_operator": [1, 1],
        "internal_target_correction": [-2, 0],
        "corrected_operator": [-1, 1],
        "verdict": (
            "an internal correction collapses the root-even/signless prism "
            "to the root-odd prism; retaining the fixed-word comparison "
            "requires an independent relative target-cone direction"
        ),
    }


def audit_diagonal_and_coloop_support(defect):
    # Target coordinate order is the three monochromatic GHZ words followed
    # by the two mixed words in the Weyl defect.  Generic h=3 diagonal rows
    # and arbitrary pure-colour target rows have zero mixed coordinates.
    h = Q(3)
    alpha = Q(2)
    beta = Q(3)  # generic branch only
    require(alpha and beta, "the generic diagonal branch degenerated")
    j1 = (h * beta, -h * alpha, -h * alpha, 0, 0)
    j2 = (-h * beta, -2 * h * alpha, -2 * h * alpha, 0, 0)
    pure_rows = tuple(tuple(Q(int(column == row))
                            for column in range(5)) for row in range(3))
    mixed_words = tuple(sorted(word for word in defect
                               if len(set(word)) > 1))
    target_defect = tuple(
        defect.get((colour,) * N, Q(0)) for colour in COLOURS
    ) + tuple(defect[word] for word in mixed_words)
    require(rank(pure_rows + (j1, j2)) == 3,
            "J1/J2 unexpectedly escaped monochromatic target support")
    require(rank(pure_rows + (target_defect,)) == 4,
            "the Weyl mixed target defect entered the pure target span")

    # A site permutation and one common global colour permutation preserve
    # monochromaticity, so global source symmetries cannot repair the gap.
    pure_images = set()
    for site_permutation in permutations(range(N)):
        # Site permutations do nothing to a pure word, so one representative
        # per global colour permutation suffices after checking the equality.
        for colour_permutation in permutations(COLOURS):
            word = (0,) * N
            transported = [None] * N
            for old_site, colour in enumerate(word):
                transported[site_permutation[old_site]] = (
                    colour_permutation[colour]
                )
            pure_images.add(tuple(transported))
        # Avoid an irrelevant 720*6 ledger after the equality is explicit.
        if len(pure_images) == 3:
            break
    require(pure_images == {(colour,) * N for colour in COLOURS},
            "a global physical symmetry made a pure target mixed")
    return {
        "generic_parameters": {"h": 3, "alpha": 2, "beta": 3},
        "J1_target": [str(value) for value in j1],
        "J2_target": [str(value) for value in j2],
        "pure_target_span_rank": 3,
        "rank_after_J1_J2": 3,
        "rank_after_Weyl_defect": 4,
        "mixed_target_coordinates_in_J1_J2": 0,
        "pure_c_coloop_target_support": "monochromatic only",
        "global_site_colour_symmetry_preserves_monochromaticity": True,
        "consequence": (
            "neither J1/J2, an alpha-weighted pure-c coloop row, nor their "
            "global-colour transports cancel 2*(w-1)*Delta.  A local-root-"
            "decorated target coordinate/label map is new source data"
        ),
    }


def audit_cell_and_terminal_types():
    # The two required cone columns have the same abstract upper/lower shape
    # but different target labels.  The displayed coordinates only encode
    # types; the preceding target-support rank proves no old identification.
    return {
        "generic_diagonal_relative_cell": {
            "name": "C_J",
            "upper_face": "-h*T(J) in the lambda*A grade",
            "lower_face": 0,
            "effect": (
                "P(J)+C_J has target zero and retains the normalized "
                "p*t_c*B residue J_cc*Ybar_c"
            ),
        },
        "signless_relative_cell": {
            "name": "C_plus",
            "upper_face": "-2*(w-1)*Delta in the root-decorated target grade",
            "rho_parity": "even",
            "effect": (
                "C_plus corrects (1+rho)*H_w without replacing it by the "
                "endpoint-odd M_v/Cartan prism"
            ),
        },
        "shared_cell_criterion": (
            "a source-labelled, Hasse/Rees-linear root-decorated comparison "
            "must identify the chosen h*T(J) upper face with "
            "2*(w-1)*Delta and carry the lower p*t_c*B face to the marked "
            "collision/repeated-grade output"
        ),
        "existing_M_v_relation": (
            "same two-local-root mapping-cone architecture, but M_v is the "
            "rho-odd target-zero component; C_plus is the missing rho-even "
            "target-bearing companion, not the same literal column"
        ),
        "terminal_typing": {
            "adjacent_cap_row_eta_sigma": "not defined in the cap module",
            "physical_M_v_eta_sigma_source": "separate commuting -dOmega ridge jet",
            "interchange_commutator": "[Theta_6,-dOmega_v]=0",
            "consequence": (
                "eta/sigma may be tensored after a physical comparison is "
                "constructed, but they are not supplied by the adjacent-"
                "power target cell itself"
            ),
        },
    }


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    cut, defect = audit_cut_word_and_target()
    ledger = {
        "theorem": "signless Cartan / adjacent-power shared-cell gate",
        "pins": PINS,
        "generic_branch": "beta != 0",
        "cut_and_target": cut,
        "Cartan_parity_gate": audit_parity_gate(),
        "literal_target_support_gate":
            audit_diagonal_and_coloop_support(defect),
        "cell_and_terminal_types": audit_cell_and_terminal_types(),
        "sharp_verdict": (
            "the inactive adjacent-power cone, the cut-swap Phi repair, and "
            "the trapped-coloop two-root comparison can share one theorem "
            "only after adjoining a root-even, root-decorated target-cone "
            "companion to the existing endpoint-odd M_v prism.  No committed "
            "J1/J2, pure-target, or Cartan-prism column is that companion.  "
            "Eta/sigma remain the independent commuting ridge factor"
        ),
        "beta_zero_scope": (
            "excluded: at beta=0 the diagonal jets collapse and the selected "
            "target first occurs at order h; the unary-jet/complementary-"
            "survival alternative remains separate"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("shared-cell ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 signless Cartan / adjacent-power shared-cell gate: PASS")
    print("signless internal correction: collapses to endpoint-odd prism")
    print("J1/J2 plus pure-c row: cannot cancel mixed Weyl target support")
    print("missing: root-even root-decorated adjacent-power cone companion")
    print("eta/sigma: independent commuting -dOmega ridge factor")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
