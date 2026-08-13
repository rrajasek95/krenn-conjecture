#!/usr/bin/env python3
"""Audit the first lower orientation face of the promoted occurrence cell.

For either marked order-two cut there are twelve ordered endpoint
occurrences.  Endpoint-role transposition tau pairs them freely.  The
centered marked vector has the integral parity decomposition

    c_f = [6(e_f+e_tf)-1] + 6(e_f-e_tf).

The complete response row and every residual-q selector are tau even.
Moreover site/root Cartan operations commute with tau, so applying them to
the complete response row cannot create the odd primitive e_f-e_tf.  The
constant theta arrow transports this primitive to a conjugate grade but has
zero first PP diagonal; it is not its boundary.  Thus a direct Cartan/KS
construction from the complete lower row stops at one primitive orientation
class.  The two physical cuts are related by a top-word stabilizer, so only
one representative cell type is needed.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py":
        "cb328adc1f23b38f6f9f9305635ddbaef888178633f8db91c205fdfbdca1ff34",
    "computations/verify_h3_centered_projector_e14_word_arrow_gate.py":
        "e1b8b17c75292f55439652ac9e5dcb1a24a3e4079c2d378e9fa63544e5491b46",
    "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py":
        "5b41444ef5f4844bc1bd87a6a4e81e60a631f3549eed21c160efdcb428582ea4",
    "computations/verify_h3_trapped_carrier_occurrence_euler_source_gate.py":
        "f4139b38728165240d1b033852aba2189e8f1a721d90d2f997755be0a077e6d0",
    "computations/verify_h3_endpoint_odd_cartan_prism_augmentation.py":
        "24ec9e3c1d1f9b689fa5a47faf9900c16724dc215fee0a41a0b653f410427fb3",
    "computations/verify_h3_trapped_hessian_theta_eq_grade_groupoid.py":
        "b30000bfe8383e1f254fb8fee4724cbd99d8f70a5e8447cffb1c9086a179aec0",
    "computations/verify_scalar_unit_c0_four_cut_common_carrier_gate.py":
        "56421c894acd613300841b7ae41d1bafecc6d65fcc9618982dc61ac198c2fa66",
    # Strong complementary endpoint-parity theorem: conditional active-clean
    # odd fork and the rank-five even centered residual/projector.
    "computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py":
        "47ea1f915429dc7937ef2e81037c0494136d9ae379d76e0584bb22cef8e0d390",
    "notes/h2-lower-centered-endpoint-parity-terminal-fork.md":
        "27d25d400daf8c26ff0da928a21cbfd3116058308799f3080cdcae8ae979ddbd",
}
EXPECTED_LEDGER_SHA256 = (
    "272db48227cb8875cd60b9d95377836d38ae63f408663aa555250153ec4ac2ac"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            ("cannot load", relative))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rank(columns: list[tuple[Q, ...]]) -> int:
    if not columns:
        return 0
    rows = [list(row) for row in zip(*columns, strict=True)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        value = rows[pivot_row][column]
        rows[pivot_row] = [entry / value for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right
                         in zip(rows[row], rows[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def add(left: tuple[Q, ...], right: tuple[Q, ...], scale=Q(1)):
    return tuple(a + scale * b for a, b in zip(left, right, strict=True))


def scale(value: Q, vector: tuple[Q, ...]):
    return tuple(value * entry for entry in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]):
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def endpoint_transpose(occurrence):
    p_site, s_site, matching = occurrence
    return s_site, p_site, matching


def permute_occurrence(occurrence, permutation):
    p_site, s_site, matching = occurrence

    def edge(item):
        left, right = (permutation.get(site, site) for site in item)
        return (left, right) if left < right else (right, left)

    return (permutation.get(p_site, p_site),
            permutation.get(s_site, s_site),
            tuple(sorted(edge(item) for item in matching)))


def parity_decomposition_audit() -> dict[str, object]:
    occurrence = load(
        "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py",
        "order2_orientation_occurrences",
    )
    values = occurrence.occurrences(tuple(range(4)))
    require(len(values) == occurrence.occurrence_count(2) == 12,
            "the order-two occurrence count changed")
    index = {item: position for position, item in enumerate(values)}
    tau_index = tuple(index[endpoint_transpose(item)] for item in values)
    require(all(tau_index[tau_index[position]] == position
                and tau_index[position] != position
                for position in range(len(values))),
            "endpoint transpose stopped being a free involution")

    marked = (0, 1, ((2, 3),))
    require(marked in index, "the canonical marked occurrence moved")
    f = index[marked]
    tf = tau_index[f]
    one = tuple(Q(1) for _ in values)
    e_f = tuple(Q(position == f) for position in range(len(values)))
    e_tf = tuple(Q(position == tf) for position in range(len(values)))
    centered = add(scale(Q(12), e_f), one, Q(-1))
    tau_centered = add(scale(Q(12), e_tf), one, Q(-1))
    even = scale(Q(1, 2), add(centered, tau_centered))
    odd = scale(Q(1, 2), add(centered, tau_centered, Q(-1)))
    pair = add(e_f, e_tf)
    primitive_odd = add(e_f, e_tf, Q(-1))
    require(even == add(scale(Q(6), pair), one, Q(-1)),
            "the endpoint-even centered component changed")
    require(odd == scale(Q(6), primitive_odd),
            "the endpoint-odd centered component changed")
    require(add(even, odd) == centered,
            "the parity components stopped reconstructing c_f")
    require(dot(one, even) == dot(one, odd) == 0,
            "a centered parity component acquired augmentation")

    # A residual-q logarithmic selector fixes the residual edge and hence
    # retains precisely its two ordered endpoint orientations.  It produces
    # the even pair, not the required oriented difference.
    residual_edge = marked[2][0]
    q_selected = tuple(Q(item[2] == (residual_edge,)) for item in values)
    require(q_selected == pair and dot(primitive_odd, q_selected) == 0,
            "the q-only selector acquired endpoint-odd support")

    # The primitive odd coordinate dual detects the odd class, kills the
    # complete row and the q-pair, and is independent from the even debt.
    odd_dual = primitive_odd
    require(dot(odd_dual, one) == dot(odd_dual, pair) == 0
            and dot(odd_dual, odd) == 12
            and dot(odd_dual, even) == 0,
            "the primitive endpoint-orientation dual changed")
    require(rank([one, pair]) == 2
            and rank([one, pair, primitive_odd]) == 3,
            "the first orientation class entered the even response span")

    return {
        "occurrences": len(values),
        "endpoint_role_orbits": len(values) // 2,
        "marked": repr(marked),
        "marked_mate": repr(values[tf]),
        "centered_class": "c_f=12*e_f-1",
        "even_component": "c_f^+=6*(e_f+e_tau_f)-1",
        "odd_component": "c_f^-=6*(e_f-e_tau_f)",
        "complete_response_vector": "1 (endpoint-even)",
        "residual_q_selector": "e_f+e_tau_f (endpoint-even)",
        "primitive_orientation": "o_f=e_f-e_tau_f",
        "primitive_orientation_dual_on_c_f_minus": "12",
        "rank_even_inventory": 2,
        "rank_after_orientation": 3,
    }


def commuting_operator_audit() -> dict[str, object]:
    occurrence = load(
        "computations/verify_uniform_centered_occurrence_restriction_insertion_gate.py",
        "order2_orientation_operators",
    )
    values = occurrence.occurrences(tuple(range(4)))
    index = {item: position for position, item in enumerate(values)}
    tau = tuple(index[endpoint_transpose(item)] for item in values)

    # Site covariance commutes literally with endpoint role transposition.
    tested = 0
    for left in range(4):
        for right in range(left + 1, 4):
            permutation = {left: right, right: left}
            for item in values:
                require(
                    endpoint_transpose(permute_occurrence(item, permutation))
                    == permute_occurrence(endpoint_transpose(item), permutation),
                    "site covariance stopped commuting with endpoint role",
                )
                tested += 1

    def transport(vector, permutation):
        answer = [Q(0)] * len(values)
        for position, item in enumerate(values):
            answer[index[permute_occurrence(item, permutation)]] += vector[position]
        return tuple(answer)

    def tau_transport(vector):
        answer = [Q(0)] * len(values)
        for position, target in enumerate(tau):
            answer[target] += vector[position]
        return tuple(answer)

    one = tuple(Q(1) for _ in values)
    # Every bar boundary from the complete response row under the site
    # covariance group is zero.  More generally all transported complete
    # rows remain tau even, so their odd projection vanishes.
    odd_projections = []
    bar_boundaries = []
    for left in range(4):
        for right in range(left + 1, 4):
            transported = transport(one, {left: right, right: left})
            boundary = add(transported, one, Q(-1))
            odd_projection = scale(Q(1, 2),
                                   add(transported, tau_transport(transported),
                                       Q(-1)))
            bar_boundaries.append(boundary)
            odd_projections.append(odd_projection)
    require(all(not any(vector) for vector in bar_boundaries)
            and all(not any(vector) for vector in odd_projections),
            "a complete-row site bar acquired an odd occurrence face")

    # The same representation-theoretic conclusion applies to colour-root
    # Cartan/KS operations: they act on variable colours at fixed sites and
    # do not exchange P with S, hence commute with tau.  Starting from the
    # tau-even complete response row, (1-tau)H(R)=0.  A nonzero odd prism
    # requires an occurrence-oriented seed, which is exactly the missing W.
    return {
        "site_transposition_commutation_checks": tested,
        "complete_row_bar_rank": rank(bar_boundaries),
        "complete_row_odd_projection_rank": rank(odd_projections),
        "Cartan_KS_parity_law": "[H_root,tau]=0",
        "consequence": "(1-tau)H_root(R_complete)=0",
        "nonzero_odd_prism_requires": (
            "an occurrence-oriented seed before applying (1-tau); this is "
            "the missing promoted-occurrence totalization, not an old row"
        ),
    }


def two_cut_covariance_audit() -> dict[str, object]:
    prior = load(
        "computations/verify_h3_centered_projector_e14_word_arrow_gate.py",
        "order2_orientation_prior",
    )
    prior_ledger, prior_digest = prior.audit()
    require(prior_digest == prior.EXPECTED_LEDGER_SHA256,
            "the centered/E14 prior ledger changed")
    lower = prior_ledger["lower_centered_convergence"]
    require(lower["literal_lower_cuts"] == [
        {"deleted_edge": "23", "lower_word": "0112",
         "reinsertion_tail": "q23:21"},
        {"deleted_edge": "45", "lower_word": "0121",
         "reinsertion_tail": "q45:12"},
    ] and lower["required_orientation"] == "p/s-odd",
            "the two literal lower cuts changed")

    top_word = tuple(map(int, "01211222"))
    permutation = {2: 5, 5: 2, 3: 4, 4: 3}
    transported_word = tuple(top_word[permutation.get(site, site)]
                             for site in range(len(top_word)))
    require(transported_word == top_word,
            "the cut-exchange permutation stopped fixing the top word")

    def decorated_edge(left, right, a, b):
        new_left = permutation.get(left, left)
        new_right = permutation.get(right, right)
        return ((new_left, new_right, a, b) if new_left < new_right else
                (new_right, new_left, b, a))

    require(decorated_edge(2, 3, 2, 1) == (4, 5, 1, 2),
            "q23:21 stopped transporting to q45:12")
    return {
        "cut_1": "0112 with q23:21 reinsertion",
        "cut_2": "0121 with q45:12 reinsertion",
        "top_word_stabilizer": "sigma=(2 5)(3 4)",
        "sigma_fixes_01211222": True,
        "sigma_maps_q23_21_to_q45_12": True,
        "sigma_commutes_with_endpoint_role": True,
        "cell_types_needed": 1,
        "coherence_needed": (
            "one representative p/s-odd lower cell and its sigma transport, "
            "with the two faces appearing with the same -5/8 coefficient"
        ),
    }


def source_and_terminal_scope_audit() -> dict[str, object]:
    # Pin load-bearing wording from the physical gates.  This makes explicit
    # that the coefficient orientation covector is not already an accepted
    # terminal and that the active-clean alternative is conditional on a
    # source-valid augmented projection.
    same_grade = (ROOT / "notes/h3-centered-occurrence-same-grade-physical-gate.md").read_text()
    cartan = (ROOT / "notes/h3-endpoint-odd-cartan-prism-augmentation.md").read_text()
    theta = (ROOT / "notes/h3-trapped-hessian-theta-eq-grade-groupoid.md").read_text()
    active = (ROOT / "notes/scalar-unit-c0-four-cut-common-carrier-gate.md").read_text()
    parity = (ROOT / "notes/h2-lower-centered-endpoint-parity-terminal-fork.md").read_text()
    require("occurrence dual becomes terminal only after proving" in same_grade
            and "does not place" in cartan
            and "d\\theta=0" in theta
            and "The identification in the second sentence is essential" in active
            and "augmentation-zero quotient has dimension five" in parity
            and "Pi_{\\rm even}" in parity,
            "a pinned physical typing guard changed")
    return {
        "theta_transport": (
            "constant two-object P<->S/head-transpose isomorphism; dtheta=0"
        ),
        "theta_boundary_of_orientation": False,
        "formal_odd_Cartan_augmentation": (
            "target/protected even rows vanish after oddization"
        ),
        "physical_odd_Cartan_descent": "not supplied by the complete row",
        "coefficient_orientation_dual_is_physical_terminal": False,
        "conditional_active_clean_exit": (
            "after a complete augmented W identifies o_f with the oriented "
            "clean-line quotient, nonzero projection is active-clean; if the "
            "projection is dark, the remaining full augmented cokernel dual "
            "is the Fredholm/relative-generator branch"
        ),
        "odd_dark_residual": (
            "the five-dimensional endpoint-even centered quotient; "
            "coefficientwise generated by the quadratic endpoint projector "
            "-(B+6I)(B-4I)/24"
        ),
        "physical_even_projector_lift_constructed": False,
        "first_missing_full_row": (
            "one source-valid p/s-odd occurrence cell with boundary "
            "e_f-e_tau_f, scalar/target correction, exact word/fine/repeated "
            "grade, and physical q/anchor/residue/eta/sigma/W typing"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "h3 order-two promoted-occurrence orientation gate",
        "pins": PINS,
        "parity_decomposition": parity_decomposition_audit(),
        "complete_response_and_Cartan": commuting_operator_audit(),
        "two_cut_covariance": two_cut_covariance_audit(),
        "physical_terminal_scope": source_and_terminal_scope_audit(),
        "verdict": (
            "The direct complete-response/Cartan/KS route does not construct "
            "the promoted-occurrence totalization W.  It stops first at the "
            "primitive endpoint-role orientation o_f=e_f-e_tau_f.  The even "
            "part is a residual-q pair minus the complete row; the odd part "
            "is invisible to both.  A top-word stabilizer identifies the "
            "0112 and 0121 orientation problems, so one representative "
            "source-valid odd cell plus its transported copy is the minimal "
            "new datum.  The occurrence dual is not an accepted terminal "
            "until the full augmented W/active-clean comparison is supplied."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("order-two orientation ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("order-2 occurrence module: 12 = 6 endpoint-role pairs")
    print("c_f^+=6(e_f+e_tau_f)-1; c_f^-=6(e_f-e_tau_f)")
    print("complete response/q selector: EVEN; direct Cartan odd image: ZERO")
    print("0112 and 0121 orientation cells: one type by (2 5)(3 4)")
    print("first missing datum: one physically typed endpoint-odd occurrence cell")
    print("coefficient odd dual: NOT YET A PHYSICAL TERMINAL")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
