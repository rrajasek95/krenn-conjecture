#!/usr/bin/env python3
"""Reduce every P2 labelled-p residue to ``d_even`` by a response gauge.

Assume the same-labelled primitive cap has been used to cancel the dq23
face of each pointed occurrence square.  Its tied labelled ordinary-residue
face is minus the coefficient used for that cancellation.  Collapse the
twelve ordered occurrences to the six endpoint-hole labels B0,...,B5 and
average the two physical cuts by

    tau_B=(B0 B5 B3 B2)(B1 B4).

For all eight first-root words, the result is a scalar multiple of

    delta_plus=(B1+B4)/2-(B0+B2+B3+B5)/4.

This is not literally d_even.  However the dq cancellation is required only
modulo the complete response row.  Adding a uniform occurrence coefficient
``k/8`` shifts ``k*delta_plus`` by ``k/4`` times the six-label diagonal and
gives exactly ``(3k/2)*d_even``.  Thus, conditional on the pointed response
section, the same-labelled p family, the pure d_even section, and the
already physical scalar-residue/complete-row gauges, no further labelled
ores direction is required.  Without the complete-row gauge, d_even alone
does not cancel the residual.
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
    "computations/verify_h3_pointed_occurrence_primitive_cap_p2_propagation_gate.py":
        "a8dfe952ce4fbbaf71ffd4ef748e456d5284dbf6b71655cce6f2f10576db0d06",
    "computations/verify_h2_p2_one_root_private_orbit_bright_dark_gate.py":
        "406c4be1a72a71c6c80fdf1c1929e64dce128847d5b20a02bb95e4a8582772d0",
    "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py":
        "8ec18f05034b6483512644c49d0009b4b166b0d6b978f6895195321ca9d8417a",
    "computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py":
        "47ea1f915429dc7937ef2e81037c0494136d9ae379d76e0584bb22cef8e0d390",
    "computations/verify_h2_b4_cplus_shared_interface_gate.py":
        "ee48f2d1446d938fc97cda4e0977472081ee9823d31dc91f3f4c46829f3d8400",
    "computations/verify_h3_centered_base_denominator_deven_composition_gate.py":
        "ee8952a30b9d1a583f3d0e78b8289e5ed839d399d0865b0457315c969c117291",
    "computations/verify_h3_cplus_root_even_labelled_ores_sigma_cartan_gate.py":
        "144d1fd64d8a733f3ec737edd301c540e66d545c9d72adf1abba5f7ed4764ce1",
}
EXPECTED_LEDGER_SHA256 = "ad015c3e59df847fe977255e5ae4b26f418f514781dd44e8093f72821ef47639"


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
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def matrix_add(*matrices):
    return tuple(tuple(sum(entries, Q(0))
                       for entries in zip(*rows, strict=True))
                 for rows in zip(*matrices, strict=True))


def matrix_scale(coefficient, matrix):
    return tuple(tuple(Q(coefficient) * value for value in row)
                 for row in matrix)


def word_text(word):
    return "".join(map(str, word))


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    parity = load(
        "computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py",
        "p2_ores_parity",
    )
    occurrence, values, lookup, swap, b_matrix, s_matrix = parity.endpoint_data()
    size = len(values)
    require(size == 12, "the lower occurrence packet changed")
    identity = parity.identity(size)
    one12 = (Q(1),) * size

    # Endpoint-even augmentation-zero projector and inverse of B-4 on its
    # B=0,-2 eigenspaces.
    constant_projector = tuple(tuple(Q(1, size) for _ in range(size))
                               for _ in range(size))
    private_projector = matrix_add(
        matrix_scale(Q(1, 2), matrix_add(identity, s_matrix)),
        matrix_scale(-1, constant_projector),
    )
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
            "the private B-4 inverse changed")

    marked = (0, 1, (occurrence.edge(2, 3),))
    c_plus = tuple(Q(6 if value in (marked, swap(marked)) else 0) - 1
                   for value in values)
    z_first = scale(Q(-1, 24), parity.matvec(
        matrix_add(b_matrix, matrix_scale(6, identity)), c_plus
    ))
    base_word = (0, 1, 1, 2)
    faces = defaultdict(lambda: [Q(0)] * size)
    for index, (p_site, s_site, matching) in enumerate(values):
        residual = matching[0]
        for endpoint in (p_site, s_site):
            for selected in residual:
                if base_word[endpoint] == base_word[selected]:
                    continue
                for changed in (endpoint, selected):
                    target = list(base_word)
                    target[changed] = (
                        base_word[selected] if changed == endpoint
                        else base_word[endpoint]
                    )
                    faces[tuple(target)][index] += z_first[index]
    require(len(faces) == 8, "the eight first-root words changed")

    # B_i are the six unordered endpoint holes in the exact C-plus interface.
    holes = ((0, 2), (0, 1), (0, 3),
             (1, 3), (2, 3), (1, 2))
    hole_index = {hole: index for index, hole in enumerate(holes)}

    def collapse(vector):
        answer = [Q(0)] * 6
        for coefficient, (p_site, s_site, _matching) in zip(
                vector, values, strict=True):
            answer[hole_index[tuple(sorted((p_site, s_site)))]] += coefficient
        return tuple(answer)

    # Cross-cut transition from the two pinned K4 charts:
    # (B0 B5 B3 B2)(B1 B4).  The tuple sends each old label to its new label.
    cross_cut = (5, 4, 0, 2, 1, 3)

    def act(permutation, vector):
        answer = [Q(0)] * len(vector)
        for old, value in enumerate(vector):
            answer[permutation[old]] = value
        return tuple(answer)

    diagonal = (Q(1),) * 6
    b1 = tuple(Q(index == 1) for index in range(6))
    b4 = tuple(Q(index == 4) for index in range(6))
    v = scale(Q(1, 2), add(b1, b4))
    w_local = scale(Q(1, 4), tuple(Q(index in (0, 2, 3, 5))
                                  for index in range(6)))
    delta = add(v, scale(-1, w_local))
    d6 = tuple(map(Q, (-1, 2, -1, -1, 2, -1)))
    require(delta == scale(Q(1, 4), d6)
            and act(cross_cut, v) == v
            and act(cross_cut, delta) == delta,
            "the cut-even B-label line changed")

    expected_k = {
        "0012": Q(2, 27),
        "0102": Q(5, 27),
        "0110": Q(5, 27),
        "0111": Q(7, 27),
        "0122": Q(2, 27),
        "0212": Q(5, 27),
        "1112": Q(7, 27),
        "2112": Q(5, 27),
    }
    records = []
    collapsed = {}
    cut_even = {}
    for word, raw_face in sorted(faces.items()):
        private = parity.matvec(private_projector, tuple(raw_face))
        z = parity.matvec(lift, private)
        require(sum(z, Q(0)) == 0,
                ("a private preimage acquired augmentation", word))
        labels = collapse(z)
        even = scale(Q(1, 2), add(labels, act(cross_cut, labels)))
        text = word_text(word)
        k = expected_k[text]
        require(even == scale(k, delta),
                ("a cut-even residue left the delta_plus line", text,
                 labels, even, k))

        # Response gauge: add t*1_12 before applying p.  Collapse(1_12)=2*1_6.
        # With t=k/8, k*delta+2t*1=(3k/2)*v.
        gauge = k / 8
        gauged = add(even, scale(2 * gauge, diagonal))
        d_even_coefficient = Q(3, 2) * k
        require(gauged == scale(d_even_coefficient, v),
                ("the response gauge stopped landing on d_even", text))

        # Signs after p_Q=-1 and p_ores=-1.  The original dq coefficient is
        # z.  Using z+gauge*1 leaves a complete-response Q face and an ores
        # face -(3k/2)*v, cancelled by +(3k/2)*d_even.  If scalar and labelled
        # ores are stored independently, the committed aggregate scalar row
        # cancels -12*gauge=-(3k/2).
        q_remainder = scale(-gauge, one12)
        p_labelled_ores = scale(-1, gauged)
        d_even_ores = scale(d_even_coefficient, v)
        p_scalar_ores = -12 * gauge
        scalar_ores_correction = d_even_coefficient
        require(add(p_labelled_ores, d_even_ores) == (Q(0),) * 6
                and p_scalar_ores + scalar_ores_correction == 0
                and q_remainder == scale(-gauge, one12),
                ("the p/d_even augmented cancellation changed", text))

        collapsed[text] = labels
        cut_even[text] = even
        records.append({
            "word": text,
            "collapsed_B_labels": [str(value) for value in labels],
            "cut_even_average": [str(value) for value in even],
            "delta_plus_coefficient_k": str(k),
            "uniform_occurrence_gauge_t": str(gauge),
            "gauged_labelled_residue": [str(value) for value in gauged],
            "d_even_coefficient": str(d_even_coefficient),
            "leftover_Q_face": f"-{gauge}*complete_response_row",
            "scalar_ores_before_aggregate_correction": str(p_scalar_ores),
        })

    # Three unmarked V4 word orbits.  Sum their cut-even residues and the
    # corresponding gauge/d_even coefficients.
    orbits = {
        "O_211": ("0012", "0102", "0122", "0212"),
        "O_220": ("0110", "2112"),
        "O_310": ("0111", "1112"),
    }
    expected_orbit_k = {
        "O_211": Q(14, 27),
        "O_220": Q(10, 27),
        "O_310": Q(14, 27),
    }
    orbit_records = {}
    for name, words in orbits.items():
        k = sum((expected_k[word] for word in words), Q(0))
        residue = add(*(cut_even[word] for word in words))
        require(k == expected_orbit_k[name] and residue == scale(k, delta),
                ("a V4 orbit sum changed", name, k, residue))
        orbit_records[name] = {
            "words": list(words),
            "delta_plus_coefficient": str(k),
            "uniform_gauge_sum": str(k / 8),
            "d_even_coefficient": str(Q(3, 2) * k),
        }
    total_k = sum(expected_k.values(), Q(0))
    require(total_k == Q(38, 27)
            and add(*(cut_even[word] for word in sorted(cut_even)))
            == scale(total_k, delta),
            "the all-eight residue sum changed")

    # Why bare d_even is insufficient and the complete-row gauge is exact.
    outer_sum = tuple(Q(index in (0, 2, 3, 5)) for index in range(6))
    alpha = tuple(map(Q, (1, 0, 1, -1, 0, -1)))
    alpha_prime = tuple(map(Q, (1, 0, -1, -1, 0, 1)))
    def dot(left, right):
        return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))
    require(dot(outer_sum, v) == dot(outer_sum, alpha)
            == dot(outer_sum, alpha_prime) == 0
            and dot(outer_sum, delta) == -1
            and delta == add(scale(Q(3, 2), v),
                             scale(Q(-1, 4), diagonal)),
            "the d_even/diagonal decomposition changed")

    ledger = {
        "theorem": "P2 cut-even labelled ores / d_even response-gauge gate",
        "pins": PINS,
        "B_label_module": {
            "holes": {f"B{index}": list(hole)
                      for index, hole in enumerate(holes)},
            "cross_cut_action": "(B0 B5 B3 B2)(B1 B4)",
            "d_even_v": [str(value) for value in v],
            "local_outer_average_w": [str(value) for value in w_local],
            "delta_plus_equals_v_minus_w": [str(value) for value in delta],
            "delta_plus_equals_3over2_v_minus_1over4_diagonal": True,
        },
        "eight_word_residues": records,
        "three_V4_orbit_sums": orbit_records,
        "all_eight_sum": {
            "delta_plus_coefficient": "38/27",
            "uniform_gauge_sum": "19/108",
            "d_even_coefficient": "19/9",
        },
        "bare_d_even_test": {
            "d_even_alone_cancels_raw_cut_even_residue": False,
            "primitive_outer_sum_dual": [int(value) for value in outer_sum],
            "dual_on_d_even_alpha_alpha_prime": [0, 0, 0],
            "dual_on_delta_plus": "-1",
        },
        "response_gauge_identity": {
            "per_word_formula": (
                "if r=k*delta_plus, replace the p coefficient z by "
                "z+(k/8)*1_12; its B-label residue becomes (3k/2)*v"
            ),
            "Q_cost": "-(k/8)*complete response row",
            "labelled_ores_correction": "+(3k/2)*d_even",
            "scalar_ores_cost": "-3k/2",
            "scalar_ores_correction": "+(3k/2)*aggregate d_ores",
            "requires_new_labelled_direction": False,
        },
        "conditional_closure": {
            "hypotheses": [
                "a pointed occurrence/global P_f family for the required fixed grades",
                "the same-labelled p_Q/p_ores cap family",
                "the complete response row and its q23 principal-parts translate",
                "the pure protected-zero d_even=(B1+B4)/2 section",
                "the existing aggregate scalar ordinary-residue correction",
                "the already required mixed-target labelled square",
            ],
            "conclusion": (
                "all eight labelled p-ores residuals, equivalently all three "
                "unmarked V4 orbit sums, cancel with no further labelled "
                "residue section"
            ),
            "does_not_construct_hypotheses": True,
        },
        "verdict": (
            "The raw two-cut residual is delta_plus, not d_even.  Bare "
            "d_even therefore fails.  But the private dq face is defined "
            "modulo its complete response row; the unique uniform gauge "
            "turns every one of the eight residues into a scalar multiple "
            "of d_even.  Under P_f+p+d_even and the already physical "
            "complete/scalar gauges, the labelled ores stage adds no new "
            "source theorem"
        ),
        "scope": (
            "exact order-two occurrence quotient, six B-label collapse, and "
            "two-cut average.  The statement is conditional on the physical "
            "occurrence-to-Q/ores map and mixed-target totalization already "
            "isolated; it does not construct those maps or promote a dual"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("P2 d_even gauge gate changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("eight cut-even p-ores residues: ALL IN delta_plus LINE")
    print("raw d_even cancellation: NO")
    print("complete-response gauge + d_even: YES")
    print("three V4 orbit coefficients: 14/27,10/27,14/27")
    print("all-eight coefficient: 38/27; d_even coefficient 19/9")
    print("new labelled residue section under hypotheses: NONE")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
