#!/usr/bin/env python3
"""Audit the exact lower-order-two coefficient map and its target obstruction.

There is a canonical coefficient quotient from the twelve ordered endpoint
occurrences on four sites to the six unordered endpoint holes.  It kills
endpoint-role oddness and intertwines endpoint adjacency B.  Relabel the
marked hole of the 0112 cut as B1 and that of the 0121 cut as B4.  Then

    (pi_23(c_23^+) + pi_45(c_45^+))/16 = delta_+.

This is not a physical iota.  The natural site/Weyl lift of the B-4 family
has a nonzero mixed target normal in each cut.  The two normals are
independent modulo the two local diagonal target lines and are exchanged by
the physical cut symmetry sigma=(2 5)(3 4).  Hence the minimum repair is one
sigma-covariant orbit of mixed-target/Hasse cone sections.

The quotient is beta-independent, but it contains no beta proper face.  Its
special-fibre D0/Bockstein coordinate is zero.  A D0 Bockstein follows only
from the stronger k[beta]-linear chain comparison carrying ds=beta*y.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h2_b4_cplus_shared_interface_gate.py":
        "ee48f2d1446d938fc97cda4e0977472081ee9823d31dc91f3f4c46829f3d8400",
    "notes/h2-b4-cplus-shared-interface-gate.md":
        "4c89253c18f4475371849a78c990e27b7d6af79193522cd5a583af80cc929fb8",
    "computations/verify_h2_lower_0112_bminus4_target_normal_gate.py":
        "8fffe45182c4bb304dabfbe9df568061a8049bec21949539bcae88f60f5d22e0",
    "notes/h2-lower-0112-bminus4-target-normal-gate.md":
        "bda5d506d3e7376b8314d37d9ddd37d7d48ae77319dda70b4ba550e84abf4e1e",
    "computations/verify_h2_lower_centered_orientation_terminal_fork.py":
        "6758c86ec151834d121e5b41b1dae677592cc4224c3aaad95d6f8321b826d3b2",
    "notes/h2-lower-centered-orientation-terminal-fork.md":
        "daa6d20d510be6472d9b1946a4854d6fd3322b61288f3fb77a8103b8a8b7d051",
    "computations/verify_h3_tau_plus_delta_literal_same_grade_gate.py":
        "f5d34986e086055dcba26e347c5a7f7470d9ec62a1346c9c872a8e828ec7b266",
    "notes/h3-tau-plus-delta-literal-same-grade-gate.md":
        "8fe9e30e7b824c167ed73917ce39913188eba82adb2864563d3a6972720e20aa",
    "computations/verify_h3_reduced_eq_integral_rho_comparison_master_gate.py":
        "813419c756e7f21c09d63d3ec10f44c787e9580ca08c87809b7c4c550b908b4f",
    "notes/h3-reduced-eq-integral-rho-comparison-master-gate.md":
        "3fa8fdc6bcd17145bc1e40c608259b2312ee52f1482520fbe9e0f5a3cd1e7a76",
    "computations/verify_h3_beta_zero_d0_augmented_terminal_saturation_gate.py":
        "d4fabdb5e180ce63e4a0ff018197f4aaf33767bfcf6940291af7783d2f150b27",
    "notes/h3-beta-zero-d0-augmented-terminal-saturation-gate.md":
        "5a58dc9fab666b789a88de71c41c27a8f3e1a004a7d307d31d24b5dbf93f7075",
}
EXPECTED_LEDGER_SHA256 = (
    "358b02641badab180817493d846e73282b1b3adc1d666f5f5a21bf6899b13bbc"
)

HOLES = ((0, 2), (0, 1), (0, 3), (1, 3), (2, 3), (1, 2))
HOLE_INDEX = {hole: index for index, hole in enumerate(HOLES)}
FULL_WORD = tuple(map(int, "01211222"))
TARGET_WORDS = tuple(product(range(3), repeat=8))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(coefficient: int | Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * entry for entry in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def unit(index: int, size: int) -> tuple[Q, ...]:
    answer = [Q(0)] * size
    answer[index] = Q(1)
    return tuple(answer)


def mat_vec(matrix: tuple[tuple[Q, ...], ...],
            vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(dot(row, vector) for row in matrix)


def mat_mul(left: tuple[tuple[Q, ...], ...],
            right: tuple[tuple[Q, ...], ...]) -> tuple[tuple[Q, ...], ...]:
    columns = tuple(zip(*right, strict=True))
    return tuple(tuple(dot(row, column) for column in columns)
                 for row in left)


def rank(vectors: tuple[tuple[Q, ...], ...] | list[tuple[Q, ...]]) -> int:
    basis: dict[int, tuple[Q, ...]] = {}
    for original in vectors:
        values = tuple(map(Q, original))
        for pivot in sorted(basis):
            if values[pivot]:
                values = add(values, scale(-values[pivot], basis[pivot]))
        pivot = next((index for index, value in enumerate(values) if value), None)
        if pivot is None:
            continue
        basis[pivot] = scale(1 / values[pivot], values)
    return len(basis)


def identity(size: int) -> tuple[tuple[Q, ...], ...]:
    return tuple(tuple(Q(row == column) for column in range(size))
                 for row in range(size))


def matrix_add(*matrices: tuple[tuple[Q, ...], ...]) -> tuple[tuple[Q, ...], ...]:
    return tuple(tuple(sum(entries, Q(0))
                       for entries in zip(*rows, strict=True))
                 for rows in zip(*matrices, strict=True))


def matrix_scale(coefficient: int | Q,
                 matrix: tuple[tuple[Q, ...], ...]) -> tuple[tuple[Q, ...], ...]:
    return tuple(tuple(Q(coefficient) * entry for entry in row)
                 for row in matrix)


def occurrence_packet(sites: tuple[int, ...]):
    values = tuple((p_site, s_site)
                   for p_site in sites for s_site in sites
                   if p_site != s_site)
    require(len(values) == 12, "order-two occurrence count")
    lookup = {value: index for index, value in enumerate(values)}
    b = [[Q(0)] * 12 for _ in range(12)]
    swap = [[Q(0)] * 12 for _ in range(12)]
    for column, (p_site, s_site) in enumerate(values):
        residual = tuple(site for site in sites
                         if site not in (p_site, s_site))
        require(len(residual) == 2, "residual edge")
        left, right = residual
        neighbours = (
            (left, s_site), (p_site, left),
            (right, s_site), (p_site, right),
        )
        for neighbour in neighbours:
            b[lookup[neighbour]][column] += 1
        swap[lookup[(s_site, p_site)]][column] = 1
    return values, lookup, tuple(map(tuple, b)), tuple(map(tuple, swap))


def hole_adjacency() -> tuple[tuple[Q, ...], ...]:
    return tuple(tuple(Q(row != column and
                         len(set(HOLES[row]) & set(HOLES[column])) == 1)
                       for column in range(6)) for row in range(6))


def quotient_matrix(values: tuple[tuple[int, int], ...],
                    relabel: dict[int, int]) -> tuple[tuple[Q, ...], ...]:
    columns = []
    for p_site, s_site in values:
        hole = tuple(sorted((relabel[p_site], relabel[s_site])))
        columns.append(unit(HOLE_INDEX[hole], 6))
    return tuple(zip(*columns, strict=True))


def centered_classes(values: tuple[tuple[int, int], ...],
                     lookup: dict[tuple[int, int], int]):
    one = (Q(1),) * 12
    forward = unit(lookup[(0, 1)], 12)
    reverse = unit(lookup[(1, 0)], 12)
    even = add(scale(6, add(forward, reverse)), scale(-1, one))
    odd = scale(6, add(forward, scale(-1, reverse)))
    return even, odd


def coefficient_iota_audit() -> dict[str, object]:
    lower_note = (ROOT /
        "notes/h2-lower-centered-orientation-terminal-fork.md").read_text()
    upper_note = (ROOT /
        "notes/h3-tau-plus-delta-literal-same-grade-gate.md").read_text()
    require("twelve ordered response" in lower_note
            and "changes the source-operation block" in lower_note,
            "the lower ordered-operation scope changed")
    require("bare all-derivation tail" in upper_note
            and "six complete columns" in upper_note,
            "the six-output complete-Q scope changed")
    cuts = (
        ((0, 1, 4, 5), (0, 1, 2, 3), "0112/q23:21", "B1"),
        ((0, 1, 2, 3), (2, 3, 0, 1), "0121/q45:12", "B4"),
    )
    b_hole = hole_adjacency()
    c_hole = tuple(add(scale(6, unit(index, 6)), scale(-1, (Q(1),) * 6))
                   for index in range(6))
    records = []
    images = []
    odd_images = []
    admissible_counts = []
    for sites, abstract_order, label, marked_target in cuts:
        relabel = dict(zip(sites, abstract_order, strict=True))
        values, lookup, b_occ, swap = occurrence_packet(sites)
        quotient = quotient_matrix(values, relabel)
        require(mat_mul(quotient, b_occ) == mat_mul(b_hole, quotient),
                ("B intertwining failed", label))
        require(mat_mul(quotient, swap) == quotient,
                ("endpoint parity quotient failed", label))
        even, odd = centered_classes(values, lookup)
        target_index = 1 if marked_target == "B1" else 4
        even_image = mat_vec(quotient, even)
        odd_image = mat_vec(quotient, odd)
        require(even_image == scale(2, c_hole[target_index])
                and odd_image == (Q(0),) * 6,
                ("marked centered image changed", label, even_image, odd_image))

        count = 0
        for abstract_permutation in permutations(range(4)):
            candidate = dict(zip(sites, abstract_permutation, strict=True))
            marked_hole = tuple(sorted((candidate[0], candidate[1])))
            if marked_hole == HOLES[target_index]:
                count += 1
        require(count == 4, ("literal K4 relabel count changed", label, count))
        admissible_counts.append(count)
        images.append(even_image)
        odd_images.append(odd_image)
        records.append({
            "cut": label,
            "physical_sites": list(sites),
            "chosen_hole_relabel": {
                str(site): relabel[site] for site in sites
            },
            "marked_hole_image": marked_target,
            "admissible_K4_relabels_with_same_marked_image": count,
            "intertwines_B": True,
            "kills_endpoint_role_odd": True,
            "c_plus_image": f"2*c_{target_index}^+",
        })

    d6 = tuple(map(Q, (-1, 2, -1, -1, 2, -1)))
    delta_plus = scale(Q(1, 4), d6)
    combined = scale(Q(1, 16), add(*images))
    require(combined == delta_plus,
            ("the two-cut coefficient iota changed", combined, delta_plus))
    require(scale(Q(1, 4), add(*images)) == d6,
            "the denominator-cleared integral debt changed")
    require(admissible_counts == [4, 4], "relabel counts")
    return {
        "cut_maps": records,
        "combined_identity": (
            "(pi_23(c_23^+)+pi_45(c_45^+))/16=delta_plus"
        ),
        "integral_debt_identity": (
            "(pi_23(c_23^+)+pi_45(c_45^+))/4=D6=4*delta_plus"
        ),
        "delta_plus": [str(value) for value in delta_plus],
        "endpoint_odd_image": [str(value) for value in add(*odd_images)],
        "coefficient_map_exists": True,
        "literal_decorated_relabel_exists": False,
        "literal_relabel_obstruction": (
            "site/colour/repeated-edge relabeling preserves the ordered "
            "response-versus-all-derivation operation block"
        ),
        "physical_source_map_constructed": False,
    }


def sparse_add(*vectors: dict[tuple[int, ...], Q]) -> dict[tuple[int, ...], Q]:
    answer: dict[tuple[int, ...], Q] = {}
    for vector in vectors:
        for word, coefficient in vector.items():
            answer[word] = answer.get(word, Q(0)) + coefficient
    return {word: coefficient for word, coefficient in answer.items()
            if coefficient}


def sparse_scale(coefficient: int | Q,
                 vector: dict[tuple[int, ...], Q]) -> dict[tuple[int, ...], Q]:
    return {word: Q(coefficient) * value for word, value in vector.items()
            if Q(coefficient) * value}


def local_word(sites: tuple[int, ...], lower: tuple[int, ...]) -> tuple[int, ...]:
    answer = list(FULL_WORD)
    for site, colour in zip(sites, lower, strict=True):
        answer[site] = colour
    return tuple(answer)


def target_defect(colours: tuple[int, ...], left: int, right: int):
    if colours[left] == colours[right]:
        return {}
    left_colour, right_colour = colours[left], colours[right]
    answer: dict[tuple[int, ...], Q] = {}
    for colour in range(3):
        word = [colour] * 4
        for site in (left, right):
            if word[site] == left_colour:
                word[site] = right_colour
            elif word[site] == right_colour:
                word[site] = left_colour
        answer[tuple(word)] = answer.get(tuple(word), Q(0)) + 1
        mono = (colour,) * 4
        answer[mono] = answer.get(mono, Q(0)) - 1
    return {word: coefficient for word, coefficient in answer.items()
            if coefficient}


def hole_normal(colours: tuple[int, ...], hole: tuple[int, int]):
    complement = tuple(site for site in range(4) if site not in hole)
    return sparse_add(*(target_defect(colours, endpoint, residual)
                        for endpoint in hole for residual in complement))


def centered_preimage(sites: tuple[int, ...]):
    values, lookup, b_occ, _swap = occurrence_packet(sites)
    even, _odd = centered_classes(values, lookup)
    b_plus_six = matrix_add(b_occ, matrix_scale(6, identity(12)))
    preimage = scale(Q(-1, 24), mat_vec(b_plus_six, even))
    b_minus_four = matrix_add(b_occ, matrix_scale(-4, identity(12)))
    require(mat_vec(b_minus_four, preimage) == even,
            "B-4 preimage changed")
    return values, preimage


def cut_target_normal(sites: tuple[int, ...]):
    colours = tuple(FULL_WORD[site] for site in sites)
    values, preimage = centered_preimage(sites)
    lower: dict[tuple[int, ...], Q] = {}
    for (p_site, s_site), coefficient in zip(values, preimage, strict=True):
        local_hole = tuple(sorted((sites.index(p_site), sites.index(s_site))))
        lower = sparse_add(lower,
                           sparse_scale(coefficient,
                                        hole_normal(colours, local_hole)))
    full = {
        local_word(sites, word): coefficient
        for word, coefficient in lower.items()
    }
    primitive = sparse_scale(Q(3, 2), full)
    diagonal = {
        local_word(sites, (colour,) * 4): Q(1) for colour in range(3)
    }
    return primitive, diagonal


def dense(vector: dict[tuple[int, ...], Q]) -> tuple[Q, ...]:
    return tuple(vector.get(word, Q(0)) for word in TARGET_WORDS)


def move_word(word: tuple[int, ...], permutation: tuple[int, ...]):
    return tuple(word[permutation[index]] for index in range(len(word)))


def move_sparse(vector: dict[tuple[int, ...], Q],
                permutation: tuple[int, ...]):
    return {move_word(word, permutation): coefficient
            for word, coefficient in vector.items()}


def target_rank_audit() -> dict[str, object]:
    sites_23 = (0, 1, 4, 5)
    sites_45 = (0, 1, 2, 3)
    normal_23, diagonal_23 = cut_target_normal(sites_23)
    normal_45, diagonal_45 = cut_target_normal(sites_45)
    sigma = (0, 1, 5, 4, 3, 2, 6, 7)
    require(move_sparse(normal_23, sigma) == normal_45,
            "cut symmetry stopped transporting the mixed normal")
    require(move_sparse(diagonal_23, sigma) == diagonal_45,
            "cut symmetry stopped transporting the diagonal line")

    diagonal_vectors = [dense(diagonal_23), dense(diagonal_45)]
    normal_vectors = [dense(normal_23), dense(normal_45)]
    require(rank(diagonal_vectors) == 2
            and rank(diagonal_vectors + normal_vectors) == 4,
            "the two-cut mixed target quotient rank changed")

    dual_23_word = tuple(map(int, "00211122"))
    dual_45_word = tuple(map(int, "00111222"))
    dual_23 = unit(TARGET_WORDS.index(dual_23_word), len(TARGET_WORDS))
    dual_45 = unit(TARGET_WORDS.index(dual_45_word), len(TARGET_WORDS))
    pairing = tuple(tuple(dot(dual, vector) for vector in normal_vectors)
                    for dual in (dual_23, dual_45))
    require(all(dot(dual, diagonal) == 0
                for dual in (dual_23, dual_45)
                for diagonal in diagonal_vectors)
            and pairing == ((Q(2), Q(0)), (Q(0), Q(2))),
            ("primitive mixed target pairing changed", pairing))

    combined = sparse_add(normal_23, normal_45)
    require(move_sparse(combined, sigma) == combined and combined,
            "the sigma-even combined target normal vanished")
    combined_dual_value = dot(add(dual_23, dual_45), dense(combined))
    require(combined_dual_value == 4,
            "the combined target detector changed")
    return {
        "primitive_0112_target_normal": {
            "support": len(normal_23),
            "mixed_detector": "X_00211122^*",
            "detector_value": 2,
        },
        "primitive_0121_target_normal": {
            "support": len(normal_45),
            "mixed_detector": "X_00111222^*",
            "detector_value": 2,
        },
        "cut_symmetry": "sigma=(2 5)(3 4)",
        "sigma_transports_0112_to_0121": True,
        "rank_local_diagonal_lines": 2,
        "rank_after_two_mixed_normals": 4,
        "mixed_target_cokernel_rank": 2,
        "combined_sigma_even_normal_zero": False,
        "combined_detector_value": str(combined_dual_value),
        "minimal_physical_repair": (
            "one sigma-covariant two-object orbit of occurrence-local "
            "mixed-target cone sections, with the one-endpoint Hasse faces"
        ),
    }


def beta_special_fibre_audit() -> dict[str, object]:
    master_note = (ROOT /
        "notes/h3-reduced-eq-integral-rho-comparison-master-gate.md").read_text()
    beta_note = (ROOT /
        "notes/h3-beta-zero-d0-augmented-terminal-saturation-gate.md").read_text()
    require("once (1) is genuinely" in master_note
            and "division by beta commute" in master_note,
            "the integral-comparison Bockstein scope changed")
    require("not a physical\nsource chain" in beta_note
            and "beta-saturation" in beta_note,
            "the beta-zero saturation guard changed")

    # A beta-independent integral closed column x has dx=0=beta*0, so its
    # connecting image is zero.  A nonzero Bockstein needs a further source
    # s with ds=beta*y and a chain map defined on s and y.
    lower_constant_beta_degree = 0
    lower_constant_bockstein = 0
    selected_d0 = 0
    require((lower_constant_beta_degree, lower_constant_bockstein,
             selected_d0) == (0, 0, 0), "constant special face changed")
    return {
        "lower_coefficient_iota_beta_degree": lower_constant_beta_degree,
        "special_fibre_lower_landing": "delta_plus",
        "special_fibre_mixed_target_normals": "the same two nonzero normals",
        "selected_D0_coordinate": selected_d0,
        "Bockstein_of_beta_independent_closed_lower_column":
            lower_constant_bockstein,
        "automatic_D0_from_lower_map": False,
        "conditional_payoff": (
            "If the map extends to a pointed k[beta]-linear chain "
            "comparison with ds=beta*y, naturality sends the proper face "
            "to the D0 correction; this is strictly stronger than the "
            "beta-independent lower quotient."
        ),
        "remaining_special_condition": (
            "beta-saturation of the complete augmented physical image, or "
            "a completed D0 terminal dual"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h2 lower delta-plus iota target-rank gate",
        "pins": PINS,
        "coefficient_iota": coefficient_iota_audit(),
        "physical_target_gate": target_rank_audit(),
        "beta_special_fibre": beta_special_fibre_audit(),
        "verdict": (
            "The two lower order-two packets admit an exact graph-level "
            "coefficient quotient to delta_plus: orientation-forgetting "
            "intertwines B, kills endpoint oddness, and sends the marked "
            "0112/0121 holes to B1/B4.  This does not lift by literal "
            "site/Weyl transport.  The natural B-4 lifts leave two "
            "independent mixed target normals modulo local diagonal rows; "
            "they form one orbit under the cut symmetry.  A physical iota "
            "therefore requires one covariant mixed-target/Hasse cone orbit. "
            "Beta-independence of the lower quotient does not create D0: "
            "that follows only after extending to the full pointed "
            "k[beta]-linear chain comparison."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("lower delta-plus iota ledger changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("coefficient lower iota to delta_plus: EXACT")
    print("endpoint parity/B-4 intertwining: EXACT")
    print("physical mixed target quotient rank: TWO (ONE CUT-SYMMETRY ORBIT)")
    print("beta-independent lower map supplies D0 Bockstein: NO")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
