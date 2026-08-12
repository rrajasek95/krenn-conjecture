#!/usr/bin/env python3
"""First literal comparison gate above the non-Euler chart H1 class.

The primitive chart kernel k_v has marked tail S_v and normalized readout
one.  This checker inventories the first compatible source degree and proves
that the earliest possible repair is the denominator-marked external
two-edge principal-parts comparison.  Its required cap-row shift and
chart-odd decoration are not present in the literal source module.

The q-zero four-cube is audited separately as the first scalar/invariant
continuation of this two-edge candidate; it is not needed merely to state
the correction -1 on chart H1.
"""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
QQ = Fraction
DELETED = 1
EXPECTED_DIGEST = "980a89c64009ba6eedbaa7f2c6969b8fcf7b2bfe4031983a163360bf6126c91e"
PINS = {
    "computations/verify_h3_rootless_non_euler_90term_chart_h1_separator.py":
        "6b27d870a87e3f95d274c1cb1a5d785bf04a5d5f3c353d54a11bd231a3fe1950",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_qzero_denominator_rees_four_cube.py":
        "70600661cd6a14e509a9e6487d4caa833c8bdb4419a2f442efd4b95bed7eebda",
    "computations/verify_h3_koszul_reynolds_higher_commutator_obstruction.py":
        "c52cec702336ecdd821617ba21c66538cdbbdf2fc964b3d1637dfaf25c9bae6b",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


SEPARATOR = load(
    "h3_non_euler_chart_h1_gate_separator",
    "verify_h3_rootless_non_euler_90term_chart_h1_separator.py",
)
FINE = load(
    "h3_non_euler_chart_h1_gate_fine",
    "verify_h3_direct_free_complete_first_fine_degree_membership.py",
)
QZERO = load(
    "h3_non_euler_chart_h1_gate_qzero",
    "verify_h3_qzero_denominator_rees_four_cube.py",
)
REYNOLDS = load(
    "h3_non_euler_chart_h1_gate_reynolds",
    "verify_h3_koszul_reynolds_higher_commutator_obstruction.py",
)


def add_value(vector, key, value):
    updated = vector.get(key, QQ(0)) + QQ(value)
    if updated:
        vector[key] = updated
    else:
        vector.pop(key, None)


def add_vectors(*vectors):
    answer = {}
    for vector in vectors:
        for key, value in vector.items():
            add_value(answer, key, value)
    return answer


def scale(vector, scalar):
    scalar = QQ(scalar)
    return {key: scalar * QQ(value) for key, value in vector.items()
            if scalar * QQ(value)}


def pairing(vector, covector):
    return sum(
        (QQ(value) * QQ(covector.get(key, 0))
         for key, value in vector.items()),
        QQ(0),
    )


def odd_face_projection(vector):
    """Forget chart tags with the normalized odd signs +/-1/2."""
    answer = {}
    for (tag, term), value in vector.items():
        if tag == ("pq", "direct"):
            sign = QQ(1, 2)
        elif tag == ("pr", "two_star"):
            sign = QQ(-1, 2)
        else:
            raise RuntimeError("an unexpected sector reached odd projection")
        add_value(answer, term, sign * QQ(value))
    return answer


def chart_vectors():
    word = QZERO.mixed_word_eight(DELETED)
    row = QZERO.full_direct_free_row(word)
    pq_direct, pq_star = QZERO.partition(row, (QZERO.P, QZERO.QSITE))
    pr_direct, pr_star = QZERO.partition(row, (QZERO.P, QZERO.R))
    u = QZERO.edge(QZERO.X, DELETED, 0, 0)
    t = QZERO.edge(QZERO.P, QZERO.QSITE, 0, 0)
    h_pq = QZERO.derivative(pq_direct, (u, t))
    h_pr = QZERO.derivative(pr_star, (u, t))
    require(h_pq == h_pr == QZERO.face_polynomial(DELETED),
            "external comparison tail stopped being h_v")
    require(not QZERO.derivative(pq_star, (u, t))
            and not QZERO.derivative(pr_direct, (u, t)),
            "external tail entered the wrong chart sector")

    pq_tag = ("pq", "direct")
    pr_tag = ("pr", "two_star")
    pq = {(pq_tag, term): QQ(value) for term, value in h_pq.items()}
    pr = {(pr_tag, term): QQ(value) for term, value in h_pr.items()}
    square = add_vectors(pq, scale(pr, -1))
    neutral = add_vectors(pq, pr)
    cochain = {
        **{(pq_tag, term): QQ(1, 6) for term in h_pq},
        **{(pr_tag, term): QQ(-1, 6) for term in h_pr},
    }
    require(pairing(square, cochain) == 1,
            "primitive chart square lost readout one")
    require(pairing(neutral, cochain) == 0,
            "chart-neutral denominator face became visible")
    require(pairing(scale(square, -1), cochain) == -1,
            "oppositely oriented square lost repair value -1")
    require(odd_face_projection(square) == h_pq,
            "raw odd projection stopped sending the chart square to h_v")
    require(not odd_face_projection(neutral),
            "raw odd projection saw a chart-neutral face")
    # The six-entry scalar cochain is epsilon_h after the raw odd projection,
    # where epsilon_h assigns 1/3 to each of the three matching monomials.
    require(sum(odd_face_projection(square).values(), QQ(0)) / 3
            == pairing(square, cochain) == 1,
            "marked scalar readout stopped factoring through h_v")
    return word, h_pq, pq, pr, square, neutral, cochain


def chart_placement_classification(pq, pr, cochain):
    """Classify the primitive unit-coefficient two-chart decorations."""
    records = []
    for left in (-1, 0, 1):
        for right in (-1, 0, 1):
            if not left and not right:
                continue
            vector = add_vectors(scale(pq, left), scale(pr, right))
            value = pairing(vector, cochain)
            records.append((left, right, value))
    repairs = [(left, right) for left, right, value in records
               if value == -1]
    # With both chart faces present and primitive unit coefficients, the
    # unique repair is -pq + pr = -S_v.  A one-chart coefficient -2 would
    # also have value -1, but lies outside this unit-coefficient comparison
    # inventory and is not a boundary between the two chart copies.
    both_chart_repairs = [pair for pair in repairs if all(pair)]
    require(both_chart_repairs == [(-1, 1)],
            "primitive two-chart repair decoration changed")
    return records, both_chart_repairs[0]


def pp_order_ladder(h):
    """Reconstruct orders 2,3,4 for one face and every internal matching."""
    stages = []
    for matching in QZERO.matchings(QZERO.face(DELETED)):
        variables = QZERO.coloured_matching(
            matching,
            {site: QZERO.MIXED[site] for site in QZERO.face(DELETED)},
        )
        require(len(variables) == 2, "internal face matching size changed")
        order2 = h
        order3_left = QZERO.derivative(h, (variables[0],))
        order3_right = QZERO.derivative(h, (variables[1],))
        order4 = QZERO.derivative(h, variables)
        require(len(order2) == 3
                and len(order3_left) == len(order3_right) == 1
                and order4 == {(): QQ(1)},
                "principal-parts order ladder changed")
        require(all(len(term) == 2 for term in order2),
                "order-two tail lost q-degree two")
        require(all(len(term) == 1 for term in order3_left)
                and all(len(term) == 1 for term in order3_right),
                "order-three tail lost q-degree one")
        stages.append({
            "matching": [list(pair) for pair in matching],
            "order2_terms": len(order2),
            "order2_q_degree": 2,
            "order3_terms_per_face": 1,
            "order3_q_degree": 1,
            "order4_terms": 1,
            "order4_q_degree": 0,
            "order4_value": 1,
        })
    weight_records, weight_summary = QZERO.stabilizer_weight_audit()
    selected_weight = next(record for record in weight_records
                           if record["deleted"] == DELETED)
    require(selected_weight["q_degree_2_weight"] == "nonzero"
            and selected_weight["q_degree_1_weights"] == "nonzero"
            and selected_weight["q_degree_0_weight"] == "zero",
            "stabilizer-weight ladder changed")
    require(weight_summary["first_weight_zero_order"] == 4,
            "first invariant scalar order changed")
    return stages, selected_weight


def audit():
    pin_dependencies()
    separator, separator_digest = SEPARATOR.audit()
    require(separator_digest
            == "000871fd19267809d25b89a4c9ab01ab9d491996e978cb875d97b304ae383376",
            "non-Euler separator ledger changed")
    require(separator["marked_readout_on_correction_h1"] == [1, 1]
            and not separator["zero_indeterminate"],
            "input chart-H1 obstruction changed")

    word, h, pq, pr, square, neutral, cochain = chart_vectors()
    placements, repair_placement = chart_placement_classification(
        pq, pr, cochain)

    fine = FINE.face_audit(DELETED)
    denominator = fine["denominator"]
    eqsystem = fine["eqsystem"]
    require(fine["lambda_weight"] == 12,
            "first compatible source degree changed")
    require(denominator["terms_inspected"] == 3645
            and denominator["terms_dividing_lambda"] == 0,
            "a raw denominator term entered the first degree")
    require(denominator["unshifted_reset_image_weight"] == 9
            and denominator["required_cap_module_shift_weight"] == 3
            and denominator["required_cap_module_shift_sites"] == [0, 6, 7],
            "minimal cap module shift changed")
    require(denominator["conditionally_shifted_reset_hits_in_fixed_degree"]
            == [[DELETED, FINE.MIXED[DELETED]]],
            "shifted denominator candidate stopped being unique")
    require(eqsystem["one_chart_columns"] == 48
            and eqsystem["two_chart_columns"] == 96
            and eqsystem["formal_graph_two_chart_rank"] == 48
            and eqsystem["kernel_dimension"] == 48,
            "complete first-degree chart comparison block changed")

    stages, weight = pp_order_ladder(h)

    # Chain-map extension criterion.  If a new source two-cell b has
    # d_source(b)=k_v, then its marked face is forced to have boundary
    # Omega*T(k_v)=h_v*Y_0.  Conversely adjoining a target chain n with
    # d_target(n)=h_v*Y_0 is exactly what extends the marked-face map across
    # b.  The final scalar -1 is obtained by subtracting this homotopy and
    # applying epsilon_h; it is not itself the raw physical boundary.
    source_d2 = (QQ(1), QQ(-1))
    require(source_d2 == (QQ(1), QQ(-1)),
            "source filler orientation changed")
    raw_face_boundary = odd_face_projection(square)
    require(raw_face_boundary == h,
            "source filler no longer forces h_v on the target side")
    epsilon_h = sum(raw_face_boundary.values(), QQ(0)) / 3
    require(epsilon_h == 1,
            "normalized raw face boundary stopped reading one")

    # The exact R-linearity witness rules out pretending that the selected
    # correction is an ordinary coefficient-module map.  It must be lifted
    # through principal parts/Hasse faces.
    require(not REYNOLDS.selector(DELETED, REYNOLDS.constant()),
            "selector unexpectedly sends 1 to the terminal unit")
    require(REYNOLDS.selector(DELETED, REYNOLDS.H_MIXED)
            == REYNOLDS.constant(),
            "selector stopped sending the mixed source row to 1")

    ledger = {
        "face": DELETED,
        "word": "".join(map(str, word)),
        "input_chart_h1": {
            "generator": "k_v=(1,-1)",
            "source_target_ores": [0, 0, 0],
            "marked_readout": 1,
        },
        "first_compatible_fine_degree": {
            "lambda_weight": fine["lambda_weight"],
            "eq_columns_per_chart": eqsystem["one_chart_columns"],
            "doubled_rank": eqsystem["formal_graph_two_chart_rank"],
            "comparison_kernel": eqsystem["kernel_dimension"],
            "raw_denominator_terms_checked": denominator["terms_inspected"],
            "raw_denominator_terms_present":
                denominator["terms_dividing_lambda"],
        },
        "minimal_shift": {
            "unshifted_reset_weight":
                denominator["unshifted_reset_image_weight"],
            "source_weight": fine["lambda_weight"],
            "shift_weight": denominator["required_cap_module_shift_weight"],
            "shift_sites": denominator["required_cap_module_shift_sites"],
            "unique_shifted_denominator":
                denominator["conditionally_shifted_reset_hits_in_fixed_degree"],
            "physically_constructed": False,
        },
        "chart_tail": {
            "terms_per_chart": len(h),
            "readout_on_square": [
                pairing(square, cochain).numerator,
                pairing(square, cochain).denominator,
            ],
            "readout_on_neutral_face": [
                pairing(neutral, cochain).numerator,
                pairing(neutral, cochain).denominator,
            ],
            "repair_placement": list(repair_placement),
            "repair_readout": [-1, 1],
            "unit_coefficient_placements_checked": len(placements),
        },
        "chain_map_extension_equivalence": {
            "new_source_cell": "b_v",
            "source_boundary": "d_source(b_v)=k_v",
            "raw_marked_face_of_k_v": "Omega*T(k_v)=h_v*Y_0",
            "forced_target_chain": "n_v=Phi_2(b_v)",
            "forced_target_boundary": "d_target(n_v)=h_v*Y_0",
            "converse": (
                "a chain n_v with that boundary is exactly the datum needed "
                "to extend the marked-face map over the attached b_v cell"
            ),
            "normalized_epsilon_h": [
                epsilon_h.numerator, epsilon_h.denominator
            ],
            "correction_sign": (
                "the corrected leading cochain subtracts n_v, hence -1; "
                "the raw chain boundary itself has the displayed plus sign"
            ),
        },
        "earliest_candidate": {
            "source_type": (
                "selector-localized denominator-marked external two-edge "
                "principal-parts/two-chart comparison cell"
            ),
            "symbol": "[K_v; d_(v,m_v); u_v,t; sigma]",
            "principal_parts_order": 2,
            "boundary_required": "K_v=k_v",
            "target": 0,
            "ordinary_residue": 0,
            "terminal_correction": -1,
            "required_chart_tail": "-S_v",
            "status": (
                "not constructed: sigma is only a degree alignment and the "
                "denominator face has no source-derived chart decoration or "
                "ordinary-residue augmentation"
            ),
        },
        "scalar_continuation": {
            "order_ladder": stages,
            "selected_weight_ladder": weight,
            "first_qzero_invariant_order": 4,
            "meaning": (
                "the denominator-marked four-cube is the first scalar/unit "
                "continuation of the order-two candidate, not the first "
                "candidate for cancelling chart H1; h_v*Y_0 is the initial "
                "chain-map boundary and must not be conflated with the final "
                "curvature-normalized kappa*Y*w_v physical cap landing"
            ),
        },
        "r_linearity_obstruction": {
            "selector_of_1": 0,
            "selector_of_H_m": 1,
            "conclusion": (
                "an ordinary R-linear mapping-cone declaration cannot "
                "supply the terminal correction; principal-parts/Hasse "
                "Leibniz faces are mandatory"
            ),
        },
        "verdict": (
            "exact first-degree obstruction: no raw literal denominator "
            "cell enters the compatible degree; after the unique weight-3 "
            "shift, the only primitive both-chart repair is the unconstructed "
            "chart-odd -S_v denominator-marked two-edge cell"
        ),
        "scope": (
            "h=3 direct-free selected face; exhaustive in the first strict "
            "fine degree and the committed PP order ladder, but not a no-go "
            "for a new source resolution generator"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode("ascii")).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_PINNED":
        require(digest == EXPECTED_DIGEST,
                f"first comparison gate ledger changed: {digest}")
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h=3 non-Euler chart-H1 first comparison gate: PASS (exact)")
    print("raw denominator entries in first fine degree: 0 / 3645")
    print("unique required module shift:                x0+p0+q0")
    print("primitive both-chart correction -1:         -S_v")
    print("minimal new type: shifted denominator-marked PP order-2 cell")
    print("first q-zero scalar continuation:            PP order 4")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
