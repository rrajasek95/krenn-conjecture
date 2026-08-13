#!/usr/bin/env python3
"""Show that sigma-evenized odd Cartan cells do not cancel root-even ores.

The nearest physical root-even K_Eq lift carries labelled ordinary residue

    -E,  E=2 D_root tensor v,
    D_root=(-1,1,-1,1), v=(B1+B4)/2.

The physical endpoint-odd Cartan cell K_alpha has zero lower/Eq and residue

    alpha=B0+B2-B3-B5.

The within-grade stabilizer acts as (B0 B5)(B2 B3), while the physical
two-cut sigma, expressed through the pinned K4 charts, has transition
(B0 B5 B3 B2)(B1 B4).  The first sends alpha to -alpha; the second sends it
to alpha'=B0-B2-B3+B5.  Both fix v.  Even granting independent K_alpha,
K_alpha', and scalar-diagonal residue lines in every root-word copy, their
span is root tensor <1,alpha,alpha'>.  The
primitive label covector chi=(0,1,-1,0,1,-1) kills this span and reads one
on v, so it detects all four nonzero root coefficients of E.  Cartan
evenization preserves lower/Eq, but cannot cancel the labelled residue.

The missing object is therefore a pure labelled d_even section (or the two
fixed B1/B4 sections).  Gate I's fixed+paired rank-two Tor quotient does not
imply this section; the relevant two-fixed quotient is different.
"""

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_cplus_root_even_koszul_physical_dressing_gate.py":
        "9bd2c9f482dc3277d07bd96a4e2189034e766f97e7800d3864179a75e03cef17",
    "computations/verify_h3_reduced_eq_cartan_cap_augmentation_dressing.py":
        "3397fc0b7d773d97fb26e737eb490136c3062549951b07eca701ee46739ff2bb",
    "computations/verify_h3_trace_cartan_even_repair_fixed_label_symmetry_guard.py":
        "09fe871e83bb9b9e8cdac7c4ac94600cc10dc330f28674514eec48d578c60a9d",
    "computations/verify_h3_denominator_tor_two_repair_projection_gate.py":
        "b2baa9f90310002a9eb0001d8e757f8f7518295a3a8dbe7869ea29a5db880c3d",
    "computations/verify_h3_cut_swap_shared_repair_source_scope_guard.py":
        "96280ef01c70b4f3381e6d85d2c9fb64b1620850305a4346601fccbd7d63dc44",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h2_lower_delta_plus_iota_target_rank_gate.py":
        "01e36f89b4df4bb020607d2f00871deb96775a7e58b42e85eaef76c20097e5cf",
}


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def add(*vectors):
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(scalar, vector):
    return tuple(Q(scalar) * Q(entry) for entry in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def tensor(left, right):
    return tuple(Q(a) * Q(b) for a in left for b in right)


def unit(index, width):
    return tuple(Q(int(position == index)) for position in range(width))


def rank(columns):
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def apply_label_action(action, vector):
    answer = [Q(0)] * len(vector)
    for source, target in enumerate(action):
        answer[target] += Q(vector[source])
    return tuple(answer)


def pin_inputs():
    for relative, expected in PINS.items():
        actual = digest(ROOT / relative)
        require(actual == expected, (relative, actual, expected))


def sigma_cartan_audit():
    diagonal = (Q(1),) * 6
    alpha = tuple(map(Q, (1, 0, 1, -1, 0, -1)))
    v = tuple(map(Q, (0, Q(1, 2), 0, 0, Q(1, 2), 0)))
    chi = tuple(map(Q, (0, 1, -1, 0, 1, -1)))

    # There are two different physical actions.  Inside the canonical h=3
    # grade, the stabilizer induces (B0 B5)(B2 B3).  The lower-cut sigma
    # moves between two chosen K4 charts.  Conjugating sigma=(2 5)(3 4)
    # through those charts gives the transition below.
    within_grade = (5, 1, 3, 2, 4, 0)
    holes = ((0, 2), (0, 1), (0, 3), (1, 3), (2, 3), (1, 2))
    hole_index = {hole: index for index, hole in enumerate(holes)}
    abstract_transition = (2, 3, 1, 0)
    cross_cut = tuple(hole_index[tuple(sorted((abstract_transition[left],
                                               abstract_transition[right])))]
                      for left, right in holes)
    require(cross_cut == (5, 4, 0, 2, 1, 3),
            "the cross-cut K4 transition changed")
    alpha_prime = apply_label_action(cross_cut, alpha)
    require(alpha_prime == tuple(map(Q, (1, 0, -1, -1, 0, 1)))
            and apply_label_action(within_grade, alpha) == scale(-1, alpha)
            and apply_label_action(within_grade, v) == v
            and apply_label_action(cross_cut, v) == v
            and apply_label_action(cross_cut, diagonal) == diagonal,
            "a physical Cartan/fixed-plane transition changed")
    require(dot(chi, diagonal) == dot(chi, alpha)
            == dot(chi, alpha_prime) == 0
            and dot(chi, v) == 1,
            "the fixed-plane residue dual changed")

    # Two object copies display exactly what sigma-evenization does.  Start
    # with K_alpha in the first object.  Its cross-cut sigma translate has
    # residue alpha_prime in the second object.  The even and odd combinations
    # remain in the objectwise Cartan lines.  This grant is stronger than the physical
    # inventory because it treats the two translates as independently usable.
    zero6 = (Q(0),) * 6
    k_left = alpha + zero6
    sigma_k_left = zero6 + alpha_prime
    k_even = add(k_left, sigma_k_left)
    k_odd = add(k_left, scale(-1, sigma_k_left))
    chi_left = chi + zero6
    chi_right = zero6 + chi
    require(k_even == alpha + alpha_prime
            and k_odd == alpha + scale(-1, alpha_prime),
            "sigma Cartan parity changed")
    require(all(dot(covector, column) == 0
                for covector in (chi_left, chi_right)
                for column in (k_left, sigma_k_left, k_even, k_odd)),
            "a sigma Cartan residue reached the fixed plane")

    d_root = tuple(map(Q, (-1, 1, -1, 1)))
    e = scale(2, tensor(d_root, v))
    residue_to_cancel = scale(-1, e)

    # Strongest natural old-residue grant: independent diagonal, K_alpha,
    # and cross-cut K_alpha_prime lines in every root word.  The physical sigma orbit is a subspace of
    # this grant, so failure here rules out sigma-evenization a fortiori.
    granted = []
    covectors = []
    pairings = []
    for root in range(4):
        root_unit = unit(root, 4)
        granted.extend((tensor(root_unit, diagonal),
                        tensor(root_unit, alpha),
                        tensor(root_unit, alpha_prime)))
        covector = tensor(root_unit, chi)
        covectors.append(covector)
        require(all(dot(covector, column) == 0 for column in granted),
                ("root-word residue dual sees granted line", root))
        pairing = dot(covector, residue_to_cancel)
        require(pairing == -2 * d_root[root] and pairing,
                ("root-word residual pairing changed", root, pairing))
        pairings.append(pairing)
    require(rank(granted) == 12
            and rank(granted + [residue_to_cancel]) == 13,
            "the root-word Cartan/scalar residue span guard changed")

    # K_alpha is an ores/terminal cell with zero lower and Eq.  Therefore
    # every sigma combination preserves those rows.  The obstruction above
    # survives even if its terminal packet is generously declared cancelled.
    zero24 = (Q(0),) * 24
    cartan_signature = zero24 + zero24 + tensor(unit(0, 4), alpha)
    require(cartan_signature[:48] == zero24 + zero24,
            "K_alpha acquired lower or Eq")

    pure_even = e
    require(add(residue_to_cancel, pure_even) == zero24,
            "a pure d_even section stopped cancelling the residual")
    return {
        "within_grade_action": "(B0 B5)(B2 B3), fixing B1,B4",
        "cross_cut_sigma_action": "(B0 B5 B3 B2)(B1 B4)",
        "within_grade_on_alpha": "-alpha",
        "cross_cut_on_alpha": "alpha_prime=B0-B2-B3+B5",
        "both_actions_fix_v": True,
        "sigma_even_Kalpha_residue": "(alpha,alpha_prime) objectwise",
        "sigma_odd_Kalpha_residue": "(alpha,-alpha_prime) objectwise",
        "lower_and_Eq_preserved_by_Kalpha": True,
        "terminal_cancellation_granted_for_no_go": True,
        "strong_granted_residue_space": "Q^4 tensor <1,alpha,alpha_prime>",
        "strong_granted_rank": rank(granted),
        "rank_after_required_minus_E": rank(granted + [residue_to_cancel]),
        "root_word_dual_pairings_on_minus_E": [str(value) for value in pairings],
        "verdict": (
            "sigma-evenized physical K_alpha preserves lower/Eq but cannot "
            "cancel -E; a labelled fixed-plane residue section is necessary"
        ),
    }


def tor_relation_audit():
    diagonal = (Q(1),) * 6
    alpha = tuple(map(Q, (1, 0, 1, -1, 0, -1)))
    alpha_prime = tuple(map(Q, (1, 0, -1, -1, 0, 1)))
    b1 = unit(1, 6)
    b4 = unit(4, 6)
    p05 = scale(Q(1, 2), add(unit(0, 6), unit(5, 6)))
    p23 = scale(Q(1, 2), add(unit(2, 6), unit(3, 6)))
    v = scale(Q(1, 2), add(b1, b4))

    # Gate I asks for one fixed and one paired section.  For every allowed
    # choice that quotient is still missing v, even after both physical
    # Cartan residue lines are granted.  Do not grant the diagonal here: the
    # committed scalar ordinary-residue row has no six-label section.
    records = {}
    for fixed_name, fixed in (("B1", b1), ("B4", b4)):
        for pair_name, pair in (("B0+B5", p05), ("B2+B3", p23)):
            base = (alpha, alpha_prime, fixed, pair)
            before = rank(base)
            after = rank(base + (v,))
            require((before, after) == (4, 5),
                    ("Gate-I quotient unexpectedly supplied v",
                     fixed_name, pair_name, before, after))
            records[fixed_name + " / " + pair_name] = [before, after]

    require(rank((alpha, alpha_prime, b1, b4))
            == rank((alpha, alpha_prime, b1, b4, v)) == 4,
            "the two fixed sections stopped supplying v")

    # A genuine labelwise diagonal section would compress the problem to a
    # paired section plus alpha_prime.  This is not presently physical.
    require(add(scale(Q(1, 2), diagonal),
                scale(Q(1, 2), alpha_prime), scale(-2, p05)) == v
            and add(scale(Q(1, 2), diagonal),
                    scale(Q(-1, 2), alpha_prime), scale(-2, p23)) == v,
            "the conditional diagonal/paired compression changed")

    two = load(
        "computations/verify_h3_denominator_tor_two_repair_projection_gate.py",
        "cplus_ores_two_repair",
    )
    ledger, ledger_digest = two.audit()
    require(ledger_digest == two.EXPECTED_LEDGER_SHA256,
            "the two-repair Tor ledger changed")
    direct = ledger["direct_free"]["projections"]["evaluated_tail_faces_3_5"]
    tilted = ledger["tilted"]["projections"]["evaluated_tail_faces_3_5"]
    require(direct["two_section_memberships"] == [True, True]
            and tilted["two_section_memberships"] == [True, False],
            "the face3/face5 Tor control changed")
    return {
        "current_root_even_weakest_gate": (
            "one physical membership for d_even with ores=(B1+B4)/2 and "
            "all lower/Eq/W/target/ainc/terminal rows zero"
        ),
        "stronger_sufficient_gate": (
            "rank-two fixed-plane memberships d_B1 and d_B4"
        ),
        "Gate_I_rank_two_gate": (
            "one fixed plus one paired section; logically different and "
            "does not imply d_even even after both Cartan lines"
        ),
        "Gate_I_plus_two_Cartan_lines_ranks_before_after_v": records,
        "two_fixed_sections_supply_v": True,
        "conditional_diagonal_compression": {
            "with_pair_B0_B5": "v=1/2*1+1/2*alpha_prime-2*p05",
            "with_pair_B2_B3": "v=1/2*1-1/2*alpha_prime-2*p23",
            "physical_now": False,
            "reason": "the scalar ores row has no six-label diagonal section",
        },
        "denominator_face_routes": ["face3->B4", "face5->B1"],
        "direct_free_conditional_memberships": [True, True],
        "tilted_conditional_memberships": [True, False],
        "membership_form": (
            "for r_even:X->Q d_even, K=ker(r_even), the section exists "
            "exactly when J s(d_even) belongs to J(K); failure is the "
            "rank-one dual alternative"
        ),
    }


def audit():
    pin_inputs()
    return {
        "theorem": "root-even labelled-ores sigma-Cartan no-go",
        "pins": PINS,
        "sigma_Cartan": sigma_cartan_audit(),
        "relation_to_denominator_Tor": tor_relation_audit(),
        "sharp_frontier": (
            "construct one same-grade sigma-covariant d_even section, or "
            "prove both fixed face3/B4 and face5/B1 memberships; K_alpha "
            "and its sigma orbit cannot replace either construction"
        ),
    }


def main():
    result = audit()
    payload = json.dumps(result, sort_keys=True, separators=(",", ":"))
    ledger = sha256(payload.encode()).hexdigest()
    print("h3 root-even labelled-ores sigma-Cartan gate: SHARP NO-GO")
    print("K_alpha/sigma orbit: lower=Eq=0; residue stays in Cartan plane")
    print("required fixed-plane residue: detected in all four root words")
    print("next: d_even membership, or both fixed B1/B4 memberships")
    print("ledger sha256:", ledger)


if __name__ == "__main__":
    main()
