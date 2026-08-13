#!/usr/bin/env python3
"""Finite quotient theorem for the pointed E14 augmentation-private cell.

Let Q be the augmentation-private cokernel and let q be the marked E14
occurrence class.  The old unary-return holonomy is the identity.  The unique
rank-one update killing q has the form I-q*h with h(q)=1; it is an idempotent
projection, and is nilpotent exactly when Q is the one-dimensional line Qq.
Equivalently, attaching one column with private projection q kills exactly
that line and leaves the identity on Q/Qq.

For the 90-occurrence target packet, C=90I-J has C*e_g=90e_g-1.  Combining
the centered column with the complete target row and the physical K_Eq reset
gives (e_g,-1/90,-1/90) in (occurrence,target,ores).  The old cap graph has
(0,1,1), so subtracting 89/90 of it gives the normalized
(e_g,-1,-1) boundary without changing the private quotient class.  This is
the exact coefficient signature of the required rank-one attachment, but
the cross-word/fixed-fibre descent of the centered column remains open.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_e14_unary_return_augmentation_holonomy_gate.py":
        "ec28895375c8b4c8375f0b20ea9a1187a1c12cb2f2bc2a2cccb663b734465516",
    "notes/h3-e14-unary-return-augmentation-holonomy-gate.md":
        "d27a55c2dc73b817997b20175872381c2e17742b684ee6351573fc092a62dd54",
    "computations/verify_h3_e14_silent_target_occurrence_compression_gate.py":
        "d8addc92045c58cb9e26492b5c0d641bf8f182454dff3df0fff72a47f2df89a2",
    "notes/h3-e14-silent-target-occurrence-compression-gate.md":
        "f0fdaec942d790447efec7729ceb3a75038424390a77bf92aa61c565ad228722",
    "computations/verify_h3_e14_pointed_two_stage_koszul_spair_gate.py":
        "7d837db5133bfb46b36fe71a3f499de04f4342ca794d2c45b56e6ec8275d7d0d",
    "notes/h3-e14-pointed-two-stage-koszul-spair-gate.md":
        "7585ba8d4dd6267e260f6c639bd47aced38748add9beca440d0285042053e26c",
    "computations/verify_h3_e14_orbit_relative_d4_target_cone_gate.py":
        "67d33b03ec52c619f29e76c917fdba9b7e28380b4349291fa37b6b7d511e241c",
    "notes/h3-e14-orbit-relative-d4-target-cone-gate.md":
        "6268689c54144cc09b6be596b81d8b4aa741e0590a83e664ec3f6e65b89187bf",
    "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py":
        "5b41444ef5f4844bc1bd87a6a4e81e60a631f3549eed21c160efdcb428582ea4",
    "notes/h3-centered-occurrence-same-grade-physical-gate.md":
        "b183f3b5dab83fa79d17c3f539b9f146e3be176a96bfe52b267529148b64134a",
    "computations/verify_h3_full_hasse_cone_d4_descent_obstruction.py":
        "ed2f2b3451074500b39a100da91ffefed27f748636de172d81aabd5cfe394240",
    "notes/h3-full-hasse-cone-d4-descent-obstruction.md":
        "2f13dbd315211b39da1a2b8026b40bb31c09bf6de0631cd3dc896689126ee2c7",
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "notes/h3-centered-endpoint-projector-primitive-cap-lift-gate.md":
        "48e39dd9e2667208eb2a08d98aa5dc58151daeaa7029437270d92a966c9e2542",
    "computations/verify_h3_c6_e14_private_rewrite_spair_boundary.py":
        "d3605323f2a305dbc6c5dec38313ecb55c2f7a5676a255117abe9d0b773889a4",
    "notes/h3-c6-e14-private-rewrite-spair-boundary.md":
        "ac81c307c484dd1470a1ea953a70ee8c00a2e0cf875e31aff7f75f2e25315593",
}
EXPECTED_LEDGER_SHA256 = (
    "8029ee60cdf4ea523116ebd80dfb4001c3c25dc1d2326698f849d135e7995690"
)
N = 90
SITES = tuple(range(6))


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


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(*vectors: tuple[Q, ...]) -> tuple[Q, ...]:
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(coefficient: Q, vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(Q(coefficient) * entry for entry in vector)


def dot(left: tuple[Q, ...], right: tuple[Q, ...]) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((left_value * right_value for left_value, right_value in
                zip(left, right, strict=True)), Q(0))


def matrix_vector(matrix: tuple[tuple[Q, ...], ...],
                  vector: tuple[Q, ...]) -> tuple[Q, ...]:
    return tuple(dot(row, vector) for row in matrix)


def matrix_product(left: tuple[tuple[Q, ...], ...],
                   right: tuple[tuple[Q, ...], ...]
                   ) -> tuple[tuple[Q, ...], ...]:
    columns = tuple(zip(*right, strict=True))
    return tuple(tuple(dot(row, column) for column in columns)
                 for row in left)


def matrix_rank(rows: tuple[tuple[Q, ...], ...]) -> int:
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    width = len(work[0])
    require(all(len(row) == width for row in work), "rank width")
    pivot = 0
    for column in range(width):
        selected = next((row for row in range(pivot, len(work))
                         if work[row][column]), None)
        if selected is None:
            continue
        work[pivot], work[selected] = work[selected], work[pivot]
        value = work[pivot][column]
        work[pivot] = [entry / value for entry in work[pivot]]
        for row in range(len(work)):
            if row == pivot or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot], strict=True)]
        pivot += 1
        if pivot == len(work):
            break
    return pivot


def unit(index: int, size: int) -> tuple[Q, ...]:
    return tuple(Q(position == index) for position in range(size))


def edge(left: int, right: int) -> tuple[int, int]:
    require(left != right, ("loop", left, right))
    return tuple(sorted((left, right)))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    left = vertices[0]
    for index, right in enumerate(vertices[1:], start=1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(left, right),) + tail))


def occurrences() -> tuple[tuple[object, ...], ...]:
    answer = []
    for p_site in SITES:
        for s_site in SITES:
            if p_site == s_site:
                continue
            residual = tuple(site for site in SITES
                             if site not in (p_site, s_site))
            for matching in perfect_matchings(residual):
                answer.append((p_site, s_site, matching))
    require(len(answer) == len(set(answer)) == N,
            "the ninety occurrence tags changed")
    return tuple(answer)


def centered_projector_audit() -> dict[str, object]:
    ones = (Q(1),) * N
    e_g = unit(0, N)
    j = tuple(ones for _row in range(N))
    identity = tuple(unit(row, N) for row in range(N))
    c = tuple(tuple(N * identity[row][column] - j[row][column]
                    for column in range(N)) for row in range(N))
    c_g = matrix_vector(c, e_g)
    require(c_g == add(scale(N, e_g), scale(-1, ones))
            and matrix_vector(c, ones) == (Q(0),) * N
            and matrix_product(c, c)
                == tuple(scale(N, row) for row in c)
            and matrix_rank(c) == N - 1,
            "C=90I-J projector identities changed")

    # The complete target occurrence sum is zero in the augmentation-private
    # quotient V/<ones>, so [C e_g]/90=[e_g].
    require(add(c_g, ones) == scale(N, e_g),
            "centered plus complete target stopped isolating 90e_g")

    # Coarse augmented row order is (marked occurrence coefficient, target,
    # scalar cap ores), after the physical K_Eq Q reset.
    isolated = (Q(1), Q(-1, N), Q(-1, N))
    cap_graph = (Q(0), Q(1), Q(1))
    normalized = add(isolated, scale(Q(-(N - 1), N), cap_graph))
    require(normalized == (Q(1), Q(-1), Q(-1)),
            "old cap graph stopped normalizing the centered occurrence")

    centered_columns = tuple(matrix_vector(c, unit(index, N))
                             for index in range(N))
    require(add(*centered_columns) == (Q(0),) * N
            and matrix_rank(centered_columns) == N - 1
            and matrix_rank(centered_columns[:N - 1]) == N - 1
            and matrix_rank(centered_columns + (ones,)) == N,
            "the natural centered family stopped spanning")

    return {
        "occurrence_module_dimension": N,
        "centered_operator": "C=90I-J",
        "rank_C": matrix_rank(c),
        "C_squared": "90C",
        "C_on_constants": 0,
        "private_quotient_action": "C/90=I on V/<1>",
        "marked_column": "C e_g=90e_g-1",
        "isolated_after_target_and_K_Eq": [str(value) for value in isolated],
        "old_cap_graph": [str(value) for value in cap_graph],
        "cap_graph_coefficient": "-89/90",
        "normalized_boundary": [str(value) for value in normalized],
        "cap_changes_private_occurrence_class": False,
        "natural_family_instances": N,
        "unique_linear_relation": "sum_g c_g=0",
        "minimum_independent_centered_instances_for_full_private_block": N - 1,
        "centered_family_plus_complete_row_rank": N,
    }


def natural_D4_schema_audit() -> dict[str, object]:
    """Count tag instances and separate transport from pointed entry."""
    tags = occurrences()
    # Each response occurrence uses every site exactly once: twice as the
    # ordered p/s endpoints and four times in its residual matching.  Hence a
    # site Cartan has one common weight on all tags in a fixed output word.
    for p_site, s_site, matching in tags:
        used = [p_site, s_site]
        used.extend(site for pair in matching for site in pair)
        require(sorted(used) == list(SITES), ("tag missed a site", used))

    # A fixed 110000 -> 111111 four-root cube preserves all ninety tags.  It
    # therefore transports a supplied family coefficientwise, but cannot
    # manufacture any selector at the bottom.
    bottom_word = (1, 1, 0, 0, 0, 0)
    root_sites = tuple(site for site, colour in enumerate(bottom_word)
                       if colour == 0)
    top_word = tuple(1 if site in root_sites else bottom_word[site]
                     for site in SITES)
    require(root_sites == (2, 3, 4, 5) and top_word == (1,) * 6,
            "the D4 word transport changed")

    # The bottom word stabilizer has the five known tag orbits.  This is the
    # obstruction to deriving all selectors from one aggregate response row.
    same_grade = (ROOT / (
        "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py"
    )).read_text()
    orbit_cone = (ROOT / (
        "computations/verify_h3_e14_orbit_relative_d4_target_cone_gate.py"
    )).read_text()
    primitive = (ROOT / (
        "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py"
    )).read_text()
    require('[6, 24, 24, 12, 24]' in same_grade
            and '"root_transport_on_occurrence_tags": "identity with coefficient 1"'
                in orbit_cone
            and '"source_chain_lift_constructed": False' in primitive,
            "the pointed D4/projector scope changed")
    return {
        "pure_target_occurrence_tags": len(tags),
        "one_fixed_base_word": "110000",
        "one_fixed_top_word": "111111",
        "fixed_root_sites": list(root_sites),
        "tags_transported_by_this_one_D4_cube": len(tags),
        "bottom_word_stabilizer_orbit_sizes": [6, 24, 24, 12, 24],
        "full_site_group_tag_orbits": 1,
        "site_translates_of_the_base_word": 15,
        "coefficient_D4_action": "identity on the 90 structural tags",
        "pointed_bottom_sections_created_by_D4": 0,
        "exact_requirement": (
            "one natural pointed c_g/P_g schema, instantiated on 90 tags "
            "(89 independent centered directions); D4 transports every "
            "instance but does not create the bottom instance"
        ),
    }


def private_return_projection_audit() -> dict[str, object]:
    """Coequalize the 228 chart returns onto structural target tags."""
    rewrite = load(
        "computations/verify_h3_c6_e14_private_rewrite_spair_boundary.py",
        "rankone_private_rewrite",
    )
    top = rewrite.load(rewrite.TOP_PATH, "rankone_private_top")
    two = top.load(top.TWO_CELL_PATH, "rankone_private_two")
    e14 = two.load(two.E14_PATH, "rankone_private_e14")
    b4 = e14.load(e14.B4_PATH, "rankone_private_b4")

    chart_terms = []
    for first_index in (1, 2, 3):
        for second_index in (1, 2, 3):
            _candidates, _names, responses, _unary = two.universal(
                e14, b4, first_index, second_index
            )
            target_word = (1,) * 6
            target_terms = set(rewrite.row_terms(responses[target_word]))
            zero_terms = set().union(*(
                set(rewrite.row_terms(row))
                for word, row in responses.items() if word != target_word
            ))
            private = target_terms - zero_terms
            require(len(private) in {24, 26},
                    "the chart private count changed")
            chart_terms.extend(private)

    raw_multiplicity = Counter(chart_terms)
    structural_multiplicity = Counter()
    for endpoint, monomial in chart_terms:
        endpoint_sites = {}
        for variable in endpoint:
            match = re.fullmatch(r"([ps])1_(\d)_1", variable)
            require(match is not None, ("bad endpoint variable", variable))
            endpoint_sites[match.group(1)] = int(match.group(2))
        matching = []
        for variable in monomial:
            match = re.match(r"[uv](\d)(\d)", variable)
            require(match is not None, ("bad q variable", variable))
            matching.append(edge(int(match.group(1)), int(match.group(2))))
        tag = (endpoint_sites["p"], endpoint_sites["s"],
               tuple(sorted(matching)))
        require(tag in occurrences(), ("private term is not a tag", tag))
        structural_multiplicity[tag] += 1

    require(len(chart_terms) == 228
            and len(raw_multiplicity) == len(structural_multiplicity) == 36
            and Counter(raw_multiplicity.values()) == Counter({6: 32, 9: 4})
            and Counter(raw_multiplicity.values())
                == Counter(structural_multiplicity.values()),
            ("the 228-to-90 coequalization changed",
             len(raw_multiplicity), Counter(raw_multiplicity.values()),
             len(structural_multiplicity),
             Counter(structural_multiplicity.values())))

    tag_index = {tag: index for index, tag in enumerate(occurrences())}
    incidence_rows = tuple(unit(tag_index[tag], N)
                           for tag in structural_multiplicity.elements())
    require(len(incidence_rows) == 228
            and matrix_rank(incidence_rows) == 36,
            "the chart-to-structural incidence rank changed")
    selected_indices = tuple(sorted(tag_index[tag]
                                    for tag in structural_multiplicity))
    ones = (Q(1),) * N
    identity = tuple(unit(row, N) for row in range(N))
    j = tuple(ones for _row in range(N))
    c = tuple(tuple(N * identity[row][column] - j[row][column]
                    for column in range(N)) for row in range(N))
    selected_centered = tuple(matrix_vector(c, unit(index, N))
                              for index in selected_indices)
    require(matrix_rank(selected_centered) == 36
            and matrix_rank(selected_centered + (ones,)) == 37
            and all(add(column, ones) == scale(N, unit(index, N))
                    for column, index in zip(
                        selected_centered, selected_indices, strict=True)),
            "the selected natural family stopped isolating chart returns")
    return {
        "chart_labelled_returns": len(chart_terms),
        "distinct_literal_target_monomials": len(raw_multiplicity),
        "distinct_structural_occurrence_tags": len(structural_multiplicity),
        "multiplicity_profile": {"6": 32, "9": 4},
        "chart_to_structural_rank": matrix_rank(incidence_rows),
        "chart_label_kernel_dimension": 228 - matrix_rank(incidence_rows),
        "structural_augmentation_private_dimension_on_seen_support": 35,
        "natural_centered_instances_needed_to_isolate_seen_coordinates": 36,
        "complete_row_also_needed": True,
        "interpretation": (
            "the 228 rows are repeated chart labels for 36 exact target "
            "monomials.  Their 192-dimensional incidence kernel is "
            "bookkeeping, not a proved physical cokernel.  A source-valid "
            "natural centered family kills the whole 36-coordinate image; "
            "the number 228 does not force 228 independent higher cells"
        ),
    }


def moving_relative_response_audit() -> dict[str, object]:
    """Test the proposed moving affine response against physical Cartan."""
    # C=N*u_0*d/du_0-E has weights (N-1,-1,...,-1), so C(R)=c_0.
    weights = (Q(N - 1),) + (Q(-1),) * (N - 1)
    response = (Q(1),) * N
    centered = weights
    require(tuple(weights[index] * response[index] for index in range(N))
                == centered
            and sum(centered, Q(0)) == 0,
            "C(R)=90u_f-R changed")

    # At a point of the fixed response hyperplane the normal is nonzero.
    witness = (Q(1), Q(-1)) + (Q(0),) * (N - 2)
    require(dot(response, witness) == 0
            and dot(centered, witness) == Q(N),
            "the fixed-fibre non-tangency witness changed")

    # The naive linear family R-epsilon*c cancels only its zeroth-order
    # normal.  Its next residual is -epsilon*C(c), and C(c) is nonzero.
    c_of_c = tuple(weights[index] * centered[index]
                   for index in range(N))
    require(c_of_c[0] == Q((N - 1) ** 2)
            and set(c_of_c[1:]) == {Q(1)},
            "the moving-linear-family second face changed")

    # The exact formal flow is the occurrence torus
    # R_t=t^-(N-1)u_f+t*sum_{i!=f}u_i.  Its infinitesimal weights are the
    # negative of C, so C+t*d/dt is tangent.  A physical site torus cannot
    # have these weights because every occurrence contains every site once.
    formal_flow_exponents = (-(N - 1),) + (1,) * (N - 1)
    require(tuple(-value for value in weights) == formal_flow_exponents,
            "the exact occurrence-torus flow changed")

    # D4 preserves tags, hence commutes with C coefficientwise.  The pinned
    # orbit cone says the source conclusion remains conditional on P_f and a
    # horizontal cap graph; after those grants its first literal face is T12.
    orbit_cone = (ROOT / (
        "computations/verify_h3_e14_orbit_relative_d4_target_cone_gate.py"
    )).read_text()
    require('"pointed_P_f_supplied_by_orbit_covariance": False' in orbit_cone
            and '"horizontal_cross_word_cap_graph_constructed": False'
                in orbit_cone
            and '"first_literal_proper_face_after_pointed_and_cap_grants": "T_12"'
                in orbit_cone,
            "the orbit-relative first-face scope changed")
    return {
        "centered_derivation": "C=90*u_f*d/du_f-E_total",
        "fixed_response": "R=sum_i u_i",
        "normal": "C(R)=90u_f-R=c_f",
        "fixed_ideal_tangent": False,
        "linear_moving_family": "R_epsilon=R-epsilon*c_f",
        "linear_family_first_uncancelled_face": "-epsilon*C(c_f)",
        "exact_formal_flow": (
            "R_t=t^-89*u_f+t*sum_(i!=f)u_i, with "
            "(C+t*d/dt)R_t=0"
        ),
        "exact_flow_is_physical_site_Cartan": False,
        "reason": (
            "every endpoint/matching occurrence in a fixed response word "
            "uses every site once, so a physical diagonal site Cartan has "
            "one common occurrence weight; the required 89/-1 selector is "
            "an occurrence torus direction"
        ),
        "graph_coordinate_da_equals_c_f": (
            "a valid formal relative extension, but it adjoins exactly the "
            "missing pointed centered/conormal generator"
        ),
        "Pi_end_Pi_match_status": (
            "coefficient projector/correspondence, not a source-algebra "
            "derivation or constructed conormal"
        ),
        "coefficient_commutator_with_D4": 0,
        "physical_chain_commutator_constructed": False,
        "first_physical_face_before_base_grant": (
            "the primitive pointed cap/conormal p=(-Q_(v,N),-ores) in "
            "word 01211222, repeated grade P3+K2"
        ),
        "first_face_after_base_and_horizontal_cap_grants": "full T_12",
    }


def rank_one_update_audit() -> dict[str, object]:
    records = []
    for dimension in (1, 2, 3, 89, 228):
        q = unit(0, dimension)
        h = unit(0, dimension)
        identity = tuple(unit(row, dimension) for row in range(dimension))
        update = tuple(tuple(identity[row][column] - q[row] * h[column]
                             for column in range(dimension))
                       for row in range(dimension))
        require(matrix_vector(update, q) == (Q(0),) * dimension
                and matrix_product(update, update) == update
                and matrix_rank(update) == dimension - 1,
                ("rank-one marked-line update changed", dimension))
        nilpotent = not any(any(entry for entry in row) for row in update)
        require(nilpotent == (dimension == 1),
                ("rank-one nilpotence alternative changed", dimension))
        records.append({
            "dimension": dimension,
            "rank_after_update": matrix_rank(update),
            "kernel_dimension": 1,
            "nilpotent": nilpotent,
        })

    # Necessity is the identity q+u*h(q)=0.  It forces h(q) nonzero and
    # u=-q/h(q).  Scaling h to h(q)=1 gives the displayed I-q*h form.
    q = (Q(1), Q(0), Q(0))
    h = (Q(2), Q(3), Q(5))
    u = scale(Q(-1, 2), q)
    identity_q = q
    rank_one_on_q = scale(dot(h, q), u)
    require(add(identity_q, rank_one_on_q) == (Q(0),) * 3,
            "necessary rank-one normalization changed")

    return {
        "necessary_and_sufficient_form": "I-q tensor h, with h(q)=1",
        "effect": "kernel=Qq, image=ker(h), induced identity on Q/Qq",
        "update_rank": 1,
        "updated_operator_is_idempotent": True,
        "updated_operator_nilpotent_iff": "dim(Q)=1",
        "sample_dimensions": records,
        "full_228_bookkeeping_consequence": (
            "one rank-one cell leaves eigenvalue 1 on at least 227 marked "
            "bookkeeping directions; a natural full family or a proof that "
            "the evaluated physical quotient is cyclic is required"
        ),
    }


def dependency_scope_audit() -> dict[str, object]:
    holonomy = load(
        "computations/verify_h3_e14_unary_return_augmentation_holonomy_gate.py",
        "rankone_holonomy",
    )
    holonomy_ledger, holonomy_digest = holonomy.audit()
    require(holonomy_digest == holonomy.EXPECTED_LEDGER_SHA256
            and holonomy_ledger["canonical_unary_return"]
            ["augmentation_return_operator"] == "I_228",
            "augmentation holonomy dependency changed")

    compression = load(
        "computations/verify_h3_e14_silent_target_occurrence_compression_gate.py",
        "rankone_compression",
    )
    compression_ledger, compression_digest = compression.audit()
    require(compression_digest == compression.EXPECTED_LEDGER_SHA256,
            "silent compression dependency changed")
    augmented = compression_ledger["augmented_compression"]
    require(augmented["isolated_signature_after_K_Eq"]
                == ["1", "0", "-1/90", "0", "-1/90"]
            and augmented["old_normalized_cap_graph"]
                == ["0", "0", "1", "0", "1"]
            and augmented["required_cap_graph_coefficient"] == "-89/90"
            and augmented["after_cap_graph_correction"]
                == ["1", "0", "-1", "0", "-1"],
            ("cap-normalized silent compression changed", augmented))
    require(not compression_ledger["four_root_Hasse_route"]
                ["physical_fixed_fibre_descent_exists"]
            and not compression_ledger["physical_typing"]
                ["transport_constructed"],
            "cross-word fixed-fibre descent unexpectedly closed")

    pointed_text = (ROOT / (
        "computations/verify_h3_e14_pointed_two_stage_koszul_spair_gate.py"
    )).read_text()
    require('"nonprivate_proper_tail_count": len(tail_terms)' in pointed_text
            and '"first_forced_proper_face": "T_12' in pointed_text
            and '"T_12 (twelve nonprivate unary tails)"' in pointed_text,
            "pointed D4/unary proper-face statement changed")
    return {
        "coefficient_private_action": (
            "the corrected compression has private projection [e_g], so it "
            "is exactly the rank-one relation required on the marked line"
        ),
        "cap_normalization_status": (
            "closed by the old physical cap graph; no new coarse target/ores "
            "direction remains"
        ),
        "construction_status": (
            "conditional: the centered pure-target occurrence lift and its "
            "four-root fixed-fibre/cross-word descent are not physical yet"
        ),
        "D4_12_tail_interpretation": (
            "one source-valid D4/unary cell with the full T_12 proper-face "
            "packet can be the rank-one arrow b on the selected physical "
            "line; the current first-hit inventory sends T_12 back to R_E14, "
            "so that cell/companion homotopy is not yet constructed"
        ),
        "later_rows": (
            "fine/repeated label agreement and shifted ridge/q/eta/sigma/W "
            "typing remain after the fixed-fibre descent"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "E14 augmentation-private rank-one terminal alternative",
        "pins": PINS,
        "centered_and_affine_correction": centered_projector_audit(),
        "natural_D4_occurrence_schema": natural_D4_schema_audit(),
        "return_projection_228_to_90": private_return_projection_audit(),
        "moving_relative_response": moving_relative_response_audit(),
        "minimal_rank_one_operation": rank_one_update_audit(),
        "physical_scope": dependency_scope_audit(),
        "finite_quotient_theorem": {
            "input": (
                "a finite complete augmented cokernel Q with old return T=I "
                "and nonzero marked class q"
            ),
            "attachment": "one physical normalized column b with [b]=q",
            "new_cokernel": "Q'=Q/Qq",
            "new_return": "T'=I on Q' and zero on the killed marked line",
            "full_closure_iff": "Q=Qq",
            "surviving_alternative": (
                "if Q/Qq is nonzero, there is a nonzero covector lambda "
                "with lambda(old columns)=lambda(b)=0; after full physical "
                "typing this is the residual separator/terminal arm"
            ),
            "pre_attachment_alternative": (
                "either b is in the full physical source image, or a left "
                "covector kills that image and reads b nonzero"
            ),
        },
        "verdict": (
            "the cap graph closes the affine normalization, and a natural "
            "90-tag centered family would kill the entire structural "
            "augmentation-private quotient.  The 228 chart returns are only "
            "36 distinct physical target monomials, so they do not force 228 "
            "independent cells.  The proposed moving response constructs an "
            "exact orbit only in an occurrence torus: physical site Cartan "
            "has constant tag weight, while Pi_end Pi_match is a coefficient "
            "correspondence rather than a source derivation.  Thus the "
            "bottom pointed c_f/P_f primitive cap remains the first missing "
            "physical cell; after it and horizontal cap transport, the next "
            "literal face is T_12"
        ),
        "scope": (
            "exact Q-linear theorem on the h=3 90-occurrence compression, "
            "the exact coequalization of 228 chart returns onto 36 literal "
            "target monomials, and arbitrary finite augmented cokernels.  It "
            "does not construct the pointed physical conormal, promote an "
            "occurrence selector to a terminal, or assert that the evaluated "
            "physical cokernel is one-dimensional."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("rank-one terminal ledger changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("E14 augmentation-private rank-one theorem: PASS (exact)")
    print("minimal update: I-q*h, h(q)=1")
    print("marked line: KILLED; full nilpotence iff physical quotient is cyclic")
    print("cap graph closes target/zcap normalization: YES")
    print("228 chart returns -> 36 structural target tags")
    print("natural 90-tag D4 family: CONDITIONAL ON POINTED BOTTOM SECTION")
    print("moving occurrence orbit is not physical site Cartan")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
