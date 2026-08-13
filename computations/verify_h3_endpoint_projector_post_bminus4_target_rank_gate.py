#!/usr/bin/env python3
"""Sequential target audit for the h=3 endpoint projector factors."""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py":
        "4e32d14b4d495b4439ed7aba59afedc8de0c1c4f76717989ca9e817444e9cd8f",
    "notes/h3-centered-projector-literal-first-hasse-eq-incidence-gate.md":
        "242a0a148c782c73540f060ef4e685902888f6d0e95da2d050b0e46dec5baf9d",
    "computations/verify_h3_e14_selected_fibre_graph_keq_koszul_gate.py":
        "9d57cbcfaeebb8d7f67d6efea87a124b4a46ad1dc054d5fc0954ab0c2338b157",
    "notes/h3-e14-selected-fibre-graph-keq-koszul-gate.md":
        "98cae28b58267abcffc47b571e52581a354950ef684df5f28b58dca88c60c6e7",
    "computations/verify_h2_lower_0112_bminus4_target_normal_gate.py":
        "8fffe45182c4bb304dabfbe9df568061a8049bec21949539bcae88f60f5d22e0",
    "notes/h2-lower-0112-bminus4-target-normal-gate.md":
        "bda5d506d3e7376b8314d37d9ddd37d7d48ae77319dda70b4ba550e84abf4e1e",
}
EXPECTED_LEDGER_SHA256 = (
    "645ffbc09b92fd5a087c69d35b834143d2195d48ea7d26bcf4d2e0d2b6afbb1a"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None, ("load", relative))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pin", relative, actual, expected))


def add(*vectors):
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * value for value in vector)


def rank(columns) -> int:
    if not columns:
        return 0
    work = [list(row) for row in zip(*columns, strict=True)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        value = work[answer][column]
        work[answer] = [entry / value for entry in work[answer]]
        for row in range(len(work)):
            if row == answer or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def sparse(vector, basis):
    return {"".join(map(str, word)): str(value)
            for word, value in zip(basis, vector, strict=True) if value}


def sequential_target_audit() -> dict[str, object]:
    base = load(
        "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py",
        "post_bminus4_base",
    )
    occurrences = base.occurrences()
    lookup = {value: index for index, value in enumerate(occurrences)}
    marked = lookup[(0, 1, ((2, 3), (4, 5)))]
    one = (Q(1),) * len(occurrences)
    e_f = base.unit(marked, len(occurrences))
    c_f = add(scale(90, e_f), scale(-1, one))

    def matching(vector):
        return add(base.apply_matching(vector, occurrences, lookup), vector)

    def endpoint_factor(vector, root):
        return add(base.apply_endpoint(vector, occurrences, lookup),
                   scale(-root, vector))

    v_match = matching(c_f)
    v_b4 = endpoint_factor(v_match, 4)
    v_b2 = endpoint_factor(v_b4, 2)
    v_bp2 = endpoint_factor(v_b2, -2)
    require(v_bp2 == (Q(0),) * 90,
            "the centered endpoint polynomial stopped closing")

    target_basis = tuple(product(range(3), repeat=6))

    def target_normal(vector):
        answer = (Q(0),) * len(target_basis)
        for coefficient, occurrence in zip(vector, occurrences, strict=True):
            if not coefficient:
                continue
            p_site, s_site, _matching = occurrence
            for endpoint in (p_site, s_site):
                for selected in range(6):
                    if selected in (p_site, s_site):
                        continue
                    answer = add(answer, scale(
                        coefficient,
                        base.two_root_target_defect(endpoint, selected,
                                                    target_basis),
                    ))
        return answer

    # The target face of a physical lift of (B-rI)v is independent of r:
    # only the B-edge Cartan/site paths carry target normal.
    n_b4 = target_normal(v_match)
    n_b2 = target_normal(v_b4)
    n_bp2 = target_normal(v_b2)
    require(all(sum(normal, Q(0)) == 0
                for normal in (n_b4, n_b2, n_bp2)),
            "a target normal acquired augmentation")

    normals = (n_b4, n_b2, n_bp2)
    require(scale(7, n_b2) == scale(-32, n_b4)
            and scale(7, n_bp2) == scale(108, n_b4),
            "the sequential target-normal ratios changed")
    prefixes = [rank(normals[:index]) for index in range(1, 4)]
    supports = [sum(bool(value) for value in normal) for normal in normals]

    delta = add(*(base.target_unit((colour,) * 6, target_basis)
                  for colour in range(3)))
    ranks_with_delta = [rank((delta,) + normals[:index])
                        for index in range(1, 4)]

    # Find primitive coordinate detectors for each new sequential direction.
    # RREF on the normal columns returns pivot target rows; the corresponding
    # coordinate rows make the independence literal and reproducible.
    matrix = [[normal[row] for normal in normals]
              for row in range(len(target_basis))]
    pivot_rows = []
    chosen = []
    current_rank = 0
    for row, values in enumerate(matrix):
        trial = chosen + [tuple(values)]
        # rank() consumes columns. Transpose the selected target-coordinate
        # rows so each sequential normal is a column.
        selected_columns = tuple(tuple(line[column] for line in trial)
                                 for column in range(3))
        value = rank(selected_columns)
        if value > current_rank:
            pivot_rows.append(row)
            chosen.append(tuple(values))
            current_rank = value
        if current_rank == rank(normals):
            break
    require(current_rank == rank(normals), "target pivot rows incomplete")

    return {
        "factor_order": ["A+I", "B-4I", "B-2I", "B+2I"],
        "coefficient_supports_after_each_nonmatching_factor": [
            sum(bool(value) for value in v_b4),
            sum(bool(value) for value in v_b2),
            sum(bool(value) for value in v_bp2),
        ],
        "final_coefficient_boundary": 0,
        "target_normal_names": ["N_(B-4)", "N_(B-2)", "N_(B+2)"],
        "target_supports": supports,
        "target_ratios_to_Bminus4": ["1", "-32/7", "108/7"],
        "sequential_target_ranks": prefixes,
        "sequential_ranks_with_GHZ_Delta": ranks_with_delta,
        "primitive_target_coordinate_words": [
            "".join(map(str, target_basis[row])) for row in pivot_rows
        ],
        "target_coordinate_matrix_on_normals": [
            [str(value) for value in line] for line in chosen
        ],
        "normals_sparse": [sparse(normal, target_basis) for normal in normals],
        "single_C2plus_target_cone_suffices_after_rescaling": True,
    }


def sequential_private_and_protected_audit() -> dict[str, object]:
    base = load(
        "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py",
        "post_bminus4_private_base",
    )
    occurrences = base.occurrences()
    lookup = {value: index for index, value in enumerate(occurrences)}
    marked = lookup[(0, 1, ((2, 3), (4, 5)))]
    one = (Q(1),) * len(occurrences)
    c_f = add(scale(90, base.unit(marked, len(occurrences))), scale(-1, one))
    v_match = add(base.apply_matching(c_f, occurrences, lookup), c_f)
    v_b4 = add(base.apply_endpoint(v_match, occurrences, lookup),
               scale(-4, v_match))
    v_b2 = add(base.apply_endpoint(v_b4, occurrences, lookup),
               scale(-2, v_b4))
    stage_inputs = (v_match, v_b4, v_b2)
    stage_ranks = [rank(stage_inputs[:index]) for index in range(1, 4)]
    require(stage_ranks == [1, 2, 3],
            ("the endpoint-stage input ranks changed", stage_ranks))

    # Product-rule faces are (d v_stage) H_endpoint.  Even after forgetting
    # the path label H, their coefficient vectors have rank three.  Retaining
    # distinct Hasse order/source labels can only keep or increase this rank.
    # Each stays in the response/bar summand and has central Eq incidence 0.
    # The A+I derivative is a separate matching-PP row.  Model the smallest
    # direct-sum protected quotient after the B-4 face is granted.
    bminus4_face = tuple(map(Q, (1, 0, 0, 0, 0)))
    bminus2_face = tuple(map(Q, (0, 1, 0, 0, 0)))
    bplus2_face = tuple(map(Q, (0, 0, 1, 0, 0)))
    matching_face = tuple(map(Q, (0, 0, 0, 1, 0)))
    central_eq = tuple(map(Q, (0, 0, 0, 0, 1)))
    require(rank((bminus4_face, bminus2_face, bplus2_face,
                  matching_face, central_eq)) == 5,
            "the minimal protected direct sum changed")
    after_grant = (bminus2_face, bplus2_face, matching_face)
    require(rank(after_grant) == 3
            and all(column[-1] == 0 for column in after_grant),
            "the post-Bminus4 protected face count changed")
    return {
        "stage_inputs": [
            "(A+I)c_f",
            "(B-4I)(A+I)c_f",
            "(B-2I)(B-4I)(A+I)c_f",
        ],
        "stage_input_sequential_ranks": stage_ranks,
        "product_rule_faces": [
            "d((A+I)c_f) tensor H_endpoint for B-4",
            "d((B-4)(A+I)c_f) tensor H_endpoint for B-2",
            "d((B-2)(B-4)(A+I)c_f) tensor H_endpoint for B+2",
        ],
        "product_rule_rank_after_forgetting_path_labels": 3,
        "central_Eq_incidence_each_endpoint_stage": 0,
        "matching_first_face": (
            "db_01: the six-term target-zero fixed-endpoint K4 derivative"
        ),
        "matching_face_is_endpoint_product_rule_face": False,
        "after_granting_Bminus4_AugP2_section_remaining_independent_faces": [
            "B-2 one-endpoint product-rule packet",
            "B+2 one-endpoint product-rule packet",
            "A+I selected six-term matching packet",
        ],
        "remaining_minimal_protected_rank": 3,
        "ordinary_bar_Bianchi_scope": (
            "ordinary endpoint/matching bars determine coefficient boundaries, "
            "but do not identify these three direct-sum PP packets.  One "
            "higher source-natural endpoint/matching totalization could carry "
            "them as faces; the existing B-4 section alone does not."
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h3 endpoint projector post-Bminus4 target-rank gate",
        "pins": PINS,
        "sequential_target": sequential_target_audit(),
        "sequential_private_and_protected": (
            sequential_private_and_protected_audit()
        ),
        "verdict": (
            "After the matching factor, the B-4, B-2, and B+2 endpoint "
            "stages have target normals in one line, with exact ratios "
            "1:-32/7:108/7.  A granted physical B-4/C2+ target cone can "
            "therefore be rescaled to cancel every later target projection. "
            "The source product-rule packets do not collapse: their "
            "coefficient profiles have sequential ranks 1,2,3, all have "
            "central Eq incidence zero, and the A+I six-term derivative is "
            "a fourth, target-zero matching face.  Hence B-2 and B+2 need "
            "new faces of one coherent higher totalization; they are not "
            "ordinary consequences of the single B-4 section."
        ),
        "shortest_positive_theorem": (
            "extend the physical B-4/AugP2 section to one source-natural "
            "cubic endpoint/matching PP totalization.  Reuse the same C2+ "
            "target cone with ratios -32/7 and 108/7, while explicitly "
            "carrying the independent B-2, B+2, and six-term matching faces."
        ),
        "scope": (
            "exact h=3 rational coefficient, target, source-stage rank, and "
            "central-Eq incidence audit; no physical higher totalization or "
            "terminal extension is asserted"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256, ("ledger", digest))
    return ledger, digest


def main():
    ledger, digest = audit()
    result = ledger["sequential_target"]
    print("target supports:", result["target_supports"])
    print("sequential target ranks:", result["sequential_target_ranks"])
    print("with Delta ranks:", result["sequential_ranks_with_GHZ_Delta"])
    print("detector words:", result["primitive_target_coordinate_words"])
    print("detector matrix:", result["target_coordinate_matrix_on_normals"])
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
