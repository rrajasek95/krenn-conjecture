#!/usr/bin/env python3
"""Compute protected curvature after reusing one C2+ target cone.

The three endpoint factors have occurrence profiles

    v0=(A+I)c_f,
    v1=(B-4I)v0,
    v2=(B-2I)v1.

Their target normals lie on one line, in ratios ``1,-32/7,108/7``.  If the
same physical B-4/C2+ cone is merely rescaled to cancel all three target
normals, its protected occurrence/path packet is rescaled by the same
numbers.  The target-zero residuals are therefore

    C2 = v1 + (32/7)v0,
    C3 = v2 - (108/7)v0.

They are nonzero, independent, and have full support on all 90 occurrences.
After denominator clearing, ``7*C2/90`` and ``7*C3/90`` are primitive.
Their literal first-PP packets have support 360, and retaining the eight
endpoint-path tags gives support 2880.  Thus one common target cone does not
make the factorized lift flat in the protected/private quotient.  These are
not independent coefficient generators: ``C2=(B+4/7)v0`` and
``C3=(B^2-6B-52/7)v0``.  One genuinely B-natural source schema would carry
both automatically.  The missing datum is precisely that higher naturality,
not two arbitrary new columns.

The bare endpoint path groupoid itself has zero two-step holonomy: from each
occurrence its 64 length-two paths have 45 endpoints with multiplicities
``32*1,12*2,1*8``, and all paths with a common endpoint induce the same site
permutation and the same PP-factor transport.  The curvature is instead the
failure of the chosen *target-normal splitting* to be horizontal for the
three weighted factor stages.

Finally, every curvature vector is matching-flat: ``(A+I)Ci=3Ci``.  Hence
the centered relation does not kill it.  A B-natural target-zero protected
second-Hasse totalization is still required; no new target direction is.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from math import gcd
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_endpoint_projector_post_bminus4_target_rank_gate.py":
        "80c9e21304bb679292671c1f344a154d4ae102c1219c4c7e1f3aad9c948be7ac",
    "notes/h3-endpoint-projector-post-bminus4-target-rank-gate.md":
        "62cba9a83f0fba0e74f1274d4dea8968d31bdd45b96cf80b2e862e0107018fab",
    "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py":
        "4e32d14b4d495b4439ed7aba59afedc8de0c1c4f76717989ca9e817444e9cd8f",
    "notes/h3-centered-projector-literal-first-hasse-eq-incidence-gate.md":
        "242a0a148c782c73540f060ef4e685902888f6d0e95da2d050b0e46dec5baf9d",
    "computations/verify_h3_e14_augmented_rhs_evenness_bockstein_gate.py":
        "9b65dd37aab071b0ced41c663cf5011b722582eaa2cc8330c22a4ee58b900adf",
    "notes/h3-e14-augmented-rhs-evenness-bockstein-gate.md":
        "8f4f5564ce1dc516fc2dcf0bce36e05b48d0b0a2b4b1a14b47d59545218a9c06",
}
EXPECTED_LEDGER_SHA256 = (
    "bbb25ced17400dc3f2f2aa2cc8db1a2434b843b7a1540a58a8aca6d421b43751"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(value) for value in vector)


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank width")
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


def integral_content(vector) -> int:
    require(all(Q(value).denominator == 1 for value in vector),
            "content requires integral vector")
    answer = 0
    for value in vector:
        answer = gcd(answer, abs(Q(value).numerator))
    return answer


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def occurrence_stage_data():
    base = load(
        "computations/verify_h3_centered_projector_literal_first_hasse_eq_incidence_gate.py",
        "endpoint_private_curvature_base",
    )
    occurrences = base.occurrences()
    lookup = {value: index for index, value in enumerate(occurrences)}
    marked = lookup[(0, 1, ((2, 3), (4, 5)))]
    one = (Q(1),) * len(occurrences)
    c_f = add(scale(90, base.unit(marked, len(occurrences))), scale(-1, one))

    def matching(vector):
        return add(base.apply_matching(vector, occurrences, lookup), vector)

    def endpoint_factor(vector, root):
        return add(base.apply_endpoint(vector, occurrences, lookup),
                   scale(-root, vector))

    v0 = matching(c_f)
    v1 = endpoint_factor(v0, 4)
    v2 = endpoint_factor(v1, 2)
    require(not any(endpoint_factor(v2, -2)),
            "the endpoint coefficient polynomial stopped closing")
    return base, occurrences, lookup, matching, (v0, v1, v2)


def common_target_splitting_curvature_audit() -> dict[str, object]:
    base, occurrences, lookup, matching, stages = occurrence_stage_data()
    v0, v1, v2 = stages
    post = load(
        "computations/verify_h3_endpoint_projector_post_bminus4_target_rank_gate.py",
        "endpoint_private_curvature_post_b4",
    )
    post_ledger, post_digest = post.audit()
    require(post_digest == post.EXPECTED_LEDGER_SHA256,
            "the post-Bminus4 target ledger changed")
    target = post_ledger["sequential_target"]
    require(target["target_ratios_to_Bminus4"] == ["1", "-32/7", "108/7"]
            and target["sequential_target_ranks"] == [1, 1, 1],
            "the common target-normal ratios changed")

    curvature_2 = add(v1, scale(Q(32, 7), v0))
    curvature_3 = add(v2, scale(Q(-108, 7), v0))
    curvatures = (curvature_2, curvature_3)
    require(rank(curvatures) == 2
            and all(sum(vector, Q(0)) == 0 for vector in curvatures)
            and all(sum(bool(value) for value in vector) == 90
                    for vector in curvatures),
            "the protected target-splitting curvature changed")

    cleared = tuple(scale(Q(7, 90), vector) for vector in curvatures)
    require(all(integral_content(vector) == 1 for vector in cleared),
            "the denominator-cleared curvatures stopped being primitive")

    # Matching flatness is eigenvalue A=2, hence A+I=3.  It preserves rather
    # than kills the two curvature directions.
    require(all(matching(vector) == scale(3, vector)
                for vector in curvatures),
            "the centered matching action on curvature changed")

    value_profiles = []
    for vector in cleared:
        profile = Counter(int(value) for value in vector)
        value_profiles.append({str(value): multiplicity
                               for value, multiplicity in sorted(profile.items())})

    return {
        "stage_profiles": [
            "v0=(A+I)c_f",
            "v1=(B-4I)v0",
            "v2=(B-2I)v1",
        ],
        "common_target_normal_ratios": ["1", "-32/7", "108/7"],
        "target_zero_curvatures": [
            "C2=v1+(32/7)v0",
            "C3=v2-(108/7)v0",
        ],
        "curvature_rank": rank(curvatures),
        "occurrence_support_each": [
            sum(bool(value) for value in vector) for vector in curvatures
        ],
        "sum_each": [str(sum(vector, Q(0))) for vector in curvatures],
        "primitive_integral_normalizations": ["7*C2/90", "7*C3/90"],
        "primitive_value_profiles": value_profiles,
        "A_plus_I_on_each_curvature": "3*C_i",
        "A_plus_I_centered_relation_kills_curvature": False,
        "central_Eq_incidence": 0,
        "target_after_common_C2plus_correction": 0,
    }


def transposition(left: int, right: int) -> tuple[int, ...]:
    answer = list(range(6))
    answer[left], answer[right] = answer[right], answer[left]
    return tuple(answer)


def compose(after: tuple[int, ...], before: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(after[before[index]] for index in range(6))


def apply_permutation(occurrence, permutation):
    p_site, s_site, matching = occurrence
    return (
        permutation[p_site],
        permutation[s_site],
        tuple(sorted(tuple(sorted((permutation[left], permutation[right])))
                     for left, right in matching)),
    )


def labelled_endpoint_moves(occurrence):
    p_site, s_site, matching = occurrence
    answer = []
    for selected in range(6):
        if selected in (p_site, s_site):
            continue
        mate = next(other if left == selected else left
                    for left, other in matching if selected in (left, other))
        for endpoint_name, endpoint in (("p", p_site), ("s", s_site)):
            permutation = transposition(endpoint, selected)
            target = apply_permutation(occurrence, permutation)
            answer.append({
                "label": (endpoint_name, endpoint, selected, mate),
                "permutation": permutation,
                "target": target,
            })
    require(len(answer) == 8 and len({item["target"] for item in answer}) == 8,
            ("endpoint move inventory changed", occurrence))
    return tuple(answer)


def endpoint_path_flatness_audit() -> dict[str, object]:
    _base, occurrences, _lookup, _matching, _stages = occurrence_stage_data()
    histograms = Counter()
    total_relations = 0
    total_two_paths = 0
    total_endpoints = 0
    for occurrence in occurrences:
        groups = defaultdict(list)
        for first in labelled_endpoint_moves(occurrence):
            for second in labelled_endpoint_moves(first["target"]):
                permutation = compose(second["permutation"],
                                      first["permutation"])
                final = second["target"]
                require(apply_permutation(occurrence, permutation) == final,
                        "two-step endpoint permutation stopped composing")
                groups[final].append(permutation)

        multiplicities = Counter(len(paths) for paths in groups.values())
        require(multiplicities == Counter({1: 32, 2: 12, 8: 1})
                and all(len(set(paths)) == 1 for paths in groups.values()),
                ("endpoint two-step holonomy changed", occurrence,
                 multiplicities))
        histograms[tuple(sorted(multiplicities.items()))] += 1
        total_two_paths += sum(map(len, groups.values()))
        total_endpoints += len(groups)
        total_relations += sum(len(paths) - 1 for paths in groups.values())

    require(total_two_paths == 90 * 64
            and total_endpoints == 90 * 45
            and total_relations == 90 * 19,
            "the global endpoint two-path counts changed")
    return {
        "outgoing_paths_per_occurrence": 8,
        "length_two_paths_per_occurrence": 64,
        "distinct_length_two_endpoints_per_occurrence": 45,
        "endpoint_multiplicity_histogram": {"1": 32, "2": 12, "8": 1},
        "path_relations_per_occurrence": 19,
        "global_two_paths": total_two_paths,
        "global_path_relations": total_relations,
        "same_endpoint_paths_have_same_site_permutation": True,
        "bare_endpoint_path_holonomy": 0,
        "interpretation": (
            "the site-permutation local system is flat; the nonzero C2,C3 "
            "classes come from the nonhorizontal common target splitting, "
            "not from ambiguity of endpoint path composition"
        ),
    }


def endpoint_triangle_matching_isotropy_audit() -> dict[str, object]:
    base, occurrences, _lookup, _matching, _stages = occurrence_stage_data()
    triangle_count = 0
    neighbour_count = 0
    distinct_flip_count = 0
    for occurrence in occurrences:
        p_site, s_site, matching = occurrence
        matching_neighbours = {
            (p_site, s_site, neighbour)
            for neighbour in base.matching_neighbors(matching)
        }
        groups = defaultdict(list)
        for first in labelled_endpoint_moves(occurrence):
            for second in labelled_endpoint_moves(first["target"]):
                for third in labelled_endpoint_moves(second["target"]):
                    final = third["target"]
                    if final not in matching_neighbours:
                        continue
                    permutation = compose(
                        third["permutation"],
                        compose(second["permutation"], first["permutation"]),
                    )
                    groups[final].append(permutation)
        require(set(groups) == matching_neighbours,
                ("a matching neighbour lost triangle isotropy", occurrence))
        for final, paths in groups.items():
            multiplicities = Counter(paths)
            require(len(paths) == 8
                    and sorted(multiplicities.values()) == [4, 4]
                    and all(permutation[p_site] == p_site
                            and permutation[s_site] == s_site
                            for permutation in multiplicities),
                    ("endpoint triangle/matching switch changed",
                     occurrence, final, multiplicities))
            # Each residual flip sends the original two-edge matching product
            # to the same switched product.  The two flips differ only by
            # which occurrence-local dq direction is marked.
            require(all(apply_permutation(occurrence, permutation) == final
                        for permutation in multiplicities),
                    "triangle flip stopped inducing the A neighbour")
            triangle_count += len(paths)
            neighbour_count += 1
            distinct_flip_count += len(multiplicities)

    require(triangle_count == 90 * 2 * 8
            and neighbour_count == 90 * 2
            and distinct_flip_count == 90 * 2 * 2,
            "global endpoint triangle counts changed")

    # In the local two-direction PP module the nontrivial flip tau acts on
    # y=e_left-e_right by -1.  The normalized group-bar boundary is
    # d[tau|y]=tau*y-y=-2y, hence y=d[-(1/2)[tau|y]] in characteristic zero.
    y = (Q(1), Q(-1))
    tau_y = (Q(-1), Q(1))
    bar_boundary = add(tau_y, scale(-1, y))
    contraction_boundary = scale(Q(-1, 2), bar_boundary)
    require(tau_y == scale(-1, y)
            and bar_boundary == scale(-2, y)
            and contraction_boundary == y,
            "the C2 isotropy bar contraction changed")
    return {
        "A_neighbours_per_occurrence": 2,
        "endpoint_triangles_per_A_neighbour": 8,
        "distinct_residual_flips_per_A_neighbour": 2,
        "multiplicity_per_flip": 4,
        "triangle_isotropy_on_occurrence_tags": (
            "exactly the A matching switch"
        ),
        "effect_on_symmetric_matching_product": "identity",
        "effect_on_occurrence_local_dq_pair": "the two directions are swapped",
        "antisymmetric_line": "y=e_left-e_right, tau*y=-y",
        "normalized_bar_boundary": "d[tau|y]=-2y",
        "characteristic_zero_contraction": "y=d[-(1/2)[tau|y]]",
        "algebraic_contraction_in_action_groupoid_nerve": True,
        "physical_source_labelled_bar_section_constructed": False,
        "typing_guard": (
            "the contraction is automatic only after the residual flip acts "
            "on the complete word/fine/repeated/q/anchor/eta source object; "
            "coefficient-level c_f naturality alone does not adjoin that bar"
        ),
    }


def B_polynomial_naturality_audit() -> dict[str, object]:
    base, occurrences, lookup, _matching, stages = occurrence_stage_data()
    v0, v1, v2 = stages

    def endpoint(vector):
        return base.apply_endpoint(vector, occurrences, lookup)

    c2 = add(v1, scale(Q(32, 7), v0))
    c3 = add(v2, scale(Q(-108, 7), v0))
    require(c2 == add(endpoint(v0), scale(Q(4, 7), v0)),
            "C2 stopped being (B+4/7)v0")
    require(c3 == add(endpoint(endpoint(v0)), scale(-6, endpoint(v0)),
                      scale(Q(-52, 7), v0)),
            "C3 stopped being (B^2-6B-52/7)v0")

    # A useful recurrence in the cyclic module.  It shows that once v0 and
    # the first curvature are carried naturally, the second is forced by B.
    recurrence = add(
        endpoint(c2),
        scale(Q(-46, 7), c2),
        scale(Q(-180, 49), v0),
    )
    require(recurrence == c3,
            "the C3 from B*C2 recurrence changed")

    return {
        "C2_as_B_polynomial": "(B+4/7)v0",
        "C3_as_B_polynomial": "(B^2-6B-52/7)v0",
        "recurrence": "C3=B*C2-(46/7)C2-(180/49)v0",
        "new_coefficient_generators_beyond_v0": 0,
        "one_B_natural_schema_carries_both_curvatures": True,
        "coefficient_polynomial_identity_is_physical_naturality": False,
        "first_missing_higher_face": (
            "a target-zero B-natural second-Hasse/kernel homotopy proving "
            "that B acts on the complete AugP2/C2+ correction, including "
            "private PP, cap/ridge/q/anchor and eta/sigma rows"
        ),
    }


def factor_tags(occurrence):
    p_site, s_site, matching = occurrence
    return (
        ("p", p_site),
        ("s", s_site),
        *(("q", left, right) for left, right in matching),
    )


def pp_boundary(vector, occurrences):
    answer = defaultdict(Q)
    for coefficient, occurrence in zip(vector, occurrences, strict=True):
        if not coefficient:
            continue
        factors = factor_tags(occurrence)
        for index, differentiated in enumerate(factors):
            remainder = factors[:index] + factors[index + 1:]
            answer[(differentiated, remainder)] += coefficient
    return {row: value for row, value in answer.items() if value}


def complete_private_support_audit() -> dict[str, object]:
    _base, occurrences, _lookup, _matching, stages = occurrence_stage_data()
    v0, v1, v2 = stages
    curvatures = (
        add(v1, scale(Q(32, 7), v0)),
        add(v2, scale(Q(-108, 7), v0)),
    )
    pp = tuple(pp_boundary(vector, occurrences) for vector in curvatures)
    require(all(len(packet) == 360 for packet in pp),
            "the complete first-PP curvature support changed")

    # Retaining the endpoint-path tag makes eight copies of every literal
    # first-PP row.  Start occurrence remains part of the source tag, so no
    # accidental collisions occur in this complete private quotient.
    path_packets = []
    for vector in curvatures:
        packet = {}
        for coefficient, occurrence in zip(vector, occurrences, strict=True):
            if not coefficient:
                continue
            factors = factor_tags(occurrence)
            for differentiated_index, differentiated in enumerate(factors):
                remainder = (factors[:differentiated_index]
                             + factors[differentiated_index + 1:])
                for move in labelled_endpoint_moves(occurrence):
                    row = (occurrence, differentiated, remainder, move["label"])
                    require(row not in packet,
                            "a complete private path row collided")
                    packet[row] = coefficient
        path_packets.append(packet)
    require(all(len(packet) == 2880 for packet in path_packets),
            "the path-labelled private curvature support changed")

    # Any coordinate at which the coefficient profiles are not proportional
    # gives a two-row rank witness.  Find and freeze the first such pair.
    witness = None
    for left in range(90):
        for right in range(left + 1, 90):
            determinant = (curvatures[0][left] * curvatures[1][right]
                           - curvatures[0][right] * curvatures[1][left])
            if determinant:
                witness = (left, right, determinant)
                break
        if witness is not None:
            break
    require(witness is not None, "the private curvature rank witness vanished")
    left, right, determinant = witness
    return {
        "literal_occurrence_factor_count": 4,
        "first_PP_support_each": [len(packet) for packet in pp],
        "endpoint_paths_per_occurrence": 8,
        "path_labelled_first_PP_support_each": [
            len(packet) for packet in path_packets
        ],
        "complete_private_curvature_rank": 2,
        "rank_witness_occurrence_indices": [left, right],
        "rank_witness_determinant": str(determinant),
        "adding_more_protected_rows_can_kill_detected_private_rank": False,
        "word_fine_repeated_scope": (
            "site permutations preserve these tags functorially in the "
            "orbit-relative groupoid; a fixed-grade physical descent of the "
            "two kernel corrections is not yet constructed"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "endpoint projector common-C2plus protected curvature gate",
        "pins": PINS,
        "common_target_splitting_curvature": (
            common_target_splitting_curvature_audit()
        ),
        "bare_endpoint_path_flatness": endpoint_path_flatness_audit(),
        "endpoint_triangle_matching_isotropy": (
            endpoint_triangle_matching_isotropy_audit()
        ),
        "B_polynomial_naturality": B_polynomial_naturality_audit(),
        "complete_private_support": complete_private_support_audit(),
        "verdict": (
            "The endpoint site-permutation local system is flat at two "
            "steps, but reusing one C2+ cone by the target-normal ratios is "
            "not a flat augmented splitting.  It leaves two independent, "
            "target-zero protected curvatures C2 and C3, each supported on "
            "all 90 occurrences, all 360 literal first-PP rows, and all "
            "2880 path-labelled private rows.  They remain matching-flat: "
            "(A+I)Ci=3Ci, so the centered relation does not kill them.  "
            "Triangle isotropy is exactly the matching switch, and its odd "
            "PP line contracts by -(1/2)[tau|-] once the physical flip action "
            "is admitted.  Moreover C2,C3 are B-polynomials in v0, so one "
            "B-natural target-zero higher totalization carries both; no new "
            "coefficient generator or second target cone is required.  That "
            "source-labelled augmented B-naturality remains unconstructed."
        ),
        "scope": (
            "exact rational h=3 occurrence, endpoint-path, first-PP private, "
            "target, and central-Eq quotient.  The calculation proves a "
            "nonzero private obstruction to naive rescaling, not existence "
            "of the higher physical totalization, q/anchor/eta extension, "
            "or a terminal dual."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    curvature = ledger["common_target_splitting_curvature"]
    paths = ledger["bare_endpoint_path_flatness"]
    private = ledger["complete_private_support"]
    print("bare endpoint two-step holonomy:", paths["bare_endpoint_path_holonomy"])
    print("common-C2+ protected curvature rank:", curvature["curvature_rank"])
    print("occurrence supports:", curvature["occurrence_support_each"])
    print("first-PP supports:", private["first_PP_support_each"])
    print("path-labelled supports:", private["path_labelled_first_PP_support_each"])
    print("(A+I) curvature: 3*C (NOT KILLED)")
    print("triangle isotropy: A-switch; odd line bar-contractible in char 0")
    print("C2,C3: B-polynomials in v0; B-natural physical schema OPEN")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
