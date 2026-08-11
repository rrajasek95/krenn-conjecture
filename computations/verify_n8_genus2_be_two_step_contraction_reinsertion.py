#!/usr/bin/env python3
"""Exact two-step closure of the first genus-2 BE attachment frontier.

The only physical-degree possibility left by the one-step audit is:

* an odd principal set T of size seven with doubled site i;
* contraction of the physical edge {i,j}, j in T-{i}; and
* reinsertion of the unique edge {j,k}, where k is the sole site outside T.

This checker exhausts all 8*7*6=336 paths, all sixteen spin sectors, the
three literal full-nine words, and all nine colour labels on the unique
reinserted physical edge.  It expands the actual Buchsbaum--Eisenbud
kernel row, differentiates by the contracted edge, and multiplies by the
reinserted edge.  Each apparent squarefree row is a 30-term presentation of
zero: fifteen monomials occur once with each sign.  Thus the construction has
no target/anchor readout and supplies neither C_rel nor an active one-edge
cap, even in the 82 untwisted Arf cases.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_LEDGER_SHA256 = "0693e4e9e49f1dcaf3e2c790fa53d23506a1a98f6e93eb4a1976cafaadf6c437"
PINS = {
    "computations/verify_n8_genus2_arf_fullnine_syzygy_probe.py":
        "06c8aebe01e06d03f17203b617be65c5c7b9ff899a040209e27ee252e735d70e",
    "computations/verify_n8_genus2_be_one_step_attachments.py":
        "dbb6b47ef5e0e8c6bf0b9d231e859d0548cc9abb37a932ca0004fba761747396",
    "computations/verify_h3_rootless_component_iii_complete_typed_inventory.py":
        "3e2b5912f58646169547b418bb4975a27635dcd8d548a010eb4c2e265412f465",
    "computations/verify_h3_two_site_port_collision_unit.py":
        "c8b590defb44e16f398c39a986293a4d4d253e6e92047d4761046f2aecf6b489",
}


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


def kasteleyn_orientation(base):
    face_rows = []
    disagreements = []
    for face in base.face_walks():
        row = 0
        disagreement = 0
        for left, right in face:
            row ^= 1 << base.EDGE_INDEX[base.edge(left, right)]
            disagreement ^= int(left > right)
        face_rows.append(row)
        disagreements.append(disagreement)
    orientation = base.gf2_solve(
        face_rows,
        tuple(1 ^ value for value in disagreements),
        len(base.EDGES),
    )
    for face, initial in zip(base.face_walks(), disagreements, strict=True):
        actual = initial
        for left, right in face:
            actual ^= (
                orientation >> base.EDGE_INDEX[base.edge(left, right)]
            ) & 1
        require(actual == 1, "a face lost Kasteleyn parity")
    return orientation


def signed_entry(base, left, right, sector, orientation, edge_labels):
    pair = base.edge(left, right)
    polynomial = base.pfaffian_polynomial(
        pair, sector, orientation, edge_labels
    )
    if left > right:
        polynomial = base.polynomial_scale(polynomial, -1)
    require(len(polynomial) == 1, "a two-site Pfaffian stopped being one term")
    return polynomial


def raw_be_terms(base, principal, row_site, sector, orientation, edge_labels):
    """The unsimplified odd-skew kernel row A*v at row_site."""

    terms = []
    for position, omitted in enumerate(principal):
        if omitted == row_site:
            continue
        entry = signed_entry(
            base, row_site, omitted, sector, orientation, edge_labels
        )
        cofactor = base.pfaffian_polynomial(
            tuple(site for site in principal if site != omitted),
            sector,
            orientation,
            edge_labels,
        )
        product = base.polynomial_multiply(entry, cofactor)
        sign = -1 if position % 2 else 1
        for monomial, coefficient in product.items():
            terms.append((monomial, sign * coefficient))
    require(len(terms) == 6 * 15,
            "the seven-site raw BE row stopped having 90 terms")
    total = Counter()
    for monomial, coefficient in terms:
        total[monomial] += coefficient
    require(not {monomial: coefficient for monomial, coefficient
                 in total.items() if coefficient},
            "the odd-skew BE kernel identity failed")
    return tuple(terms)


def entry_coefficient(base, physical_edge, sector, orientation, edge_labels):
    polynomial = signed_entry(
        base, physical_edge[0], physical_edge[1],
        sector, orientation, edge_labels,
    )
    ((monomial, coefficient),) = polynomial.items()
    require(monomial == (f"x{physical_edge[0]}{physical_edge[1]}",),
            "signed physical edge variable moved")
    return coefficient


def differentiate_reinsert(raw_terms, contracted_edge, inserted_edge,
                           insertion_coefficient):
    contracted_variable = f"x{contracted_edge[0]}{contracted_edge[1]}"
    inserted_variable = f"x{inserted_edge[0]}{inserted_edge[1]}"
    contributions = []
    for monomial, coefficient in raw_terms:
        if contracted_variable not in monomial:
            continue
        remainder = list(monomial)
        remainder.remove(contracted_variable)
        remainder.append(inserted_variable)
        physical = tuple(sorted(remainder))

        site_degree = Counter()
        for variable in physical:
            left, right = int(variable[1]), int(variable[2])
            require(left < right, "edge variable encoding moved")
            site_degree[left] += 1
            site_degree[right] += 1
        require(site_degree == Counter({site: 1 for site in range(8)}),
                "a two-step monomial is not a K8 perfect matching")
        contributions.append((
            physical, coefficient * insertion_coefficient
        ))

    require(len(contributions) == 30,
            "the contracted BE row stopped having 30 raw terms")
    grouped = {}
    for monomial, coefficient in contributions:
        grouped.setdefault(monomial, []).append(coefficient)
    require(len(grouped) == 15,
            "the contracted/reinserted row lost its 15 matching pairs")
    require(all(sorted(coefficients) == [-1, 1]
                for coefficients in grouped.values()),
            "a derived matching stopped cancelling with its mate")
    reduced = Counter()
    for monomial, coefficients in grouped.items():
        reduced[monomial] = sum(coefficients)
    require(not {monomial: coefficient for monomial, coefficient
                 in reduced.items() if coefficient},
            "the two-step row stopped being the zero polynomial")
    return tuple(sorted(grouped))


def decorate_matching(matching, word):
    return tuple(sorted(
        f"{variable[1]}{variable[2]}:{word[int(variable[1])]}"
        f"{word[int(variable[2])]}"
        for variable in matching
    ))


def audit():
    pin_dependencies()
    base = load(
        "genus2_two_step_base",
        "verify_n8_genus2_arf_fullnine_syzygy_probe.py",
    )
    # The pinned one-step checker uses the ordinary sibling-module import;
    # provide the already loaded exact module explicitly under isolated mode.
    sys.modules["verify_n8_genus2_arf_fullnine_syzygy_probe"] = base
    one_step = load(
        "genus2_two_step_parent",
        "verify_n8_genus2_be_one_step_attachments.py",
    )
    typed = load(
        "genus2_two_step_typed",
        "verify_h3_rootless_component_iii_complete_typed_inventory.py",
    )

    # Pin the two target signatures from their source artifacts.
    component = typed.attaching_pushout(Q(1))
    require(component["minimal_new_lower_face"] == {
        "total_pure_anchor_incidence": -1,
        "normalized_w": 0,
        "target": 0,
        "ordinary_residue": 0,
        "source_requirement": (
            "change pure output-word/endpoint grade into selected midpoint "
            "response grade before companion cancellation"
        ),
    }, "the C_rel signature moved")

    orientation = kasteleyn_orientation(base)
    edge_labels = one_step.kasteleyn_edge_labels()
    require(len(edge_labels) == 28, "the genus-two edge-label census moved")

    words = {
        "diagonal_00": (0,) * 8,
        "diagonal_11": (1,) * 8,
        "crossed_01_over_2": (0, 1, 2, 2, 2, 2, 2, 2),
    }
    selected_midpoints = {
        (0, 1) + residual
        for residual in itertools.product((0, 1), repeat=6)
        if residual.count(0) == residual.count(1) == 3
    }
    require(len(selected_midpoints) == 20
            and not (set(words.values()) & selected_midpoints),
            "a literal Pfaffian word entered the selected midpoint grade")

    path_count = 0
    sector_path_count = 0
    labelled_path_count = 0
    decorated_path_count = 0
    net_character_histogram = Counter()
    edge_character_pair_histogram = Counter()
    cancellation_pair_histogram = Counter()
    final_degree_histogram = Counter()
    literal_output_word_histogram = Counter()
    selected_midpoint_rows = 0
    pure_output_rows = 0
    chart_edge_path_histogram = Counter()
    sample_rows = []

    # A path is equivalently an ordered triple (i,j,k) of distinct sites:
    # T=V-{k}, i is doubled, {i,j} is contracted and {j,k} reinserted.
    for missing_site in base.VERTICES:
        principal = tuple(
            site for site in base.VERTICES if site != missing_site
        )
        for doubled_site in principal:
            for contracted_mate in principal:
                if contracted_mate == doubled_site:
                    continue
                contracted_edge = base.edge(doubled_site, contracted_mate)
                inserted_edge = base.edge(contracted_mate, missing_site)
                require(contracted_edge != inserted_edge
                        and len(set(contracted_edge) & set(inserted_edge)) == 1,
                        "the unique two-hole insertion stopped being adjacent")

                initial_degree = [
                    2 if site == doubled_site
                    else 1 if site in principal else 0
                    for site in base.VERTICES
                ]
                contracted_degree = initial_degree[:]
                for site in contracted_edge:
                    contracted_degree[site] -= 1
                require(contracted_degree.count(0) == 2
                        and contracted_degree[contracted_mate] == 0
                        and contracted_degree[missing_site] == 0
                        and all(value in (0, 1) for value in contracted_degree),
                        "the seven-site contraction lost its two-hole grade")
                final_degree = contracted_degree[:]
                for site in inserted_edge:
                    final_degree[site] += 1
                require(final_degree == [1] * 8,
                        "the unique hole edge failed to restore K8 squarefree degree")
                final_degree_histogram[tuple(final_degree)] += 1

                contracted_character = edge_labels[contracted_edge]
                inserted_character = edge_labels[inserted_edge]
                net_character = contracted_character ^ inserted_character
                net_character_histogram[net_character] += 1
                edge_character_pair_histogram[
                    (contracted_character, inserted_character)
                ] += 1
                if contracted_edge in ((0, 1), (0, 2)) \
                        or inserted_edge in ((0, 1), (0, 2)):
                    chart_edge_path_histogram[net_character] += 1

                # A character twist is scalar on all sixteen sectors iff it
                # is trivial.  Nontrivial twists take both signs.
                twist_signs = {
                    (-1) ** ((sector & net_character).bit_count() & 1)
                    for sector in range(16)
                }
                require(twist_signs == ({1} if not net_character else {-1, 1}),
                        "the Arf character proportionality test moved")

                for sector in range(16):
                    contracted_sign = entry_coefficient(
                        base, contracted_edge, sector, orientation, edge_labels
                    )
                    inserted_sign = entry_coefficient(
                        base, inserted_edge, sector, orientation, edge_labels
                    )
                    reference_sign = entry_coefficient(
                        base, contracted_edge, 0, orientation, edge_labels
                    ) * entry_coefficient(
                        base, inserted_edge, 0, orientation, edge_labels
                    )
                    actual_twist = (
                        contracted_sign * inserted_sign // reference_sign
                    )
                    expected_twist = (
                        -1 if (sector & net_character).bit_count() & 1 else 1
                    )
                    require(actual_twist == expected_twist,
                            "the contraction/reinsertion Arf twist moved")
                    raw = raw_be_terms(
                        base, principal, doubled_site, sector,
                        orientation, edge_labels,
                    )
                    sector_path_count += 1
                    matching_rows = differentiate_reinsert(
                        raw, contracted_edge, inserted_edge, inserted_sign
                    )
                    cancellation_pair_histogram[len(matching_rows)] += 1

                    # The unique physical hole edge has all nine literal
                    # colour-labelled cells.  They replace the two output
                    # labels at its endpoints and leave the other six fixed.
                    # The fifteen physical cancellation pairs remain fifteen
                    # distinct decorated cancellation pairs for every word.
                    inserted_left, inserted_right = inserted_edge
                    for word_label, word in words.items():
                        for left_colour, right_colour in itertools.product(
                                range(3), repeat=2):
                            final_word = list(word)
                            final_word[inserted_left] = left_colour
                            final_word[inserted_right] = right_colour
                            final_word = tuple(final_word)
                            decorated_matchings = {
                                decorate_matching(matching, final_word)
                                for matching in matching_rows
                            }
                            require(len(decorated_matchings) == 15,
                                    "literal reinsertion merged matching pairs")
                            decorated_path_count += 1
                            literal_output_word_histogram[final_word] += 1
                            selected_midpoint_rows += int(
                                final_word in selected_midpoints
                            )
                            pure_output_rows += int(len(set(final_word)) == 1)
                            if len(sample_rows) < 3 and sector == 0:
                                sample_rows.append({
                                    "word": word_label,
                                    "inserted_colours": [
                                        left_colour, right_colour,
                                    ],
                                    "final_word": "".join(map(str, final_word)),
                                    "principal_missing": missing_site,
                                    "doubled": doubled_site,
                                    "contracted_mate": contracted_mate,
                                    "contracted_edge": list(contracted_edge),
                                    "inserted_edge": list(inserted_edge),
                                    "net_character": net_character,
                                    "cancelled_matching_terms": len(matching_rows),
                                })
                path_count += 1

    require(path_count == 336, "the two-step physical path census moved")
    require(sector_path_count == 336 * 16,
            "the sectorwise two-step census moved")
    labelled_path_count = path_count * 9
    require(labelled_path_count == 3024,
            "the labelled physical reinsertion census moved")
    require(decorated_path_count == 336 * 16 * 3 * 9,
            "the decorated two-step census moved")
    require(final_degree_histogram == {tuple([1] * 8): 336},
            "the squarefree degree histogram moved")
    require(cancellation_pair_histogram == {15: sector_path_count},
            "a two-step row lost its fifteen exact cancellations")
    require(selected_midpoint_rows == 0,
            "a two-cell recolouring entered the selected midpoint grade")
    require(pure_output_rows == (336 * 2 + 12) * 16,
            "the pure-output decorated row census moved")
    require(net_character_histogram == {
        0: 82, 1: 18, 2: 30, 3: 6, 4: 26, 5: 2, 6: 22, 7: 14,
        8: 22, 9: 6, 10: 10, 11: 10, 12: 34, 13: 34, 14: 2, 15: 18,
    }, f"the two-step Arf-character histogram moved: {net_character_histogram}")
    require(sum(chart_edge_path_histogram.values()) == 46,
            "the pinned chart-edge path count moved")

    # Type comparison.  The derived object is a homogeneous zero syzygy, so
    # contraction/reinsertion creates no constant target and invokes no
    # physical pure-anchor equation.  It is supported on the inserted edge
    # before the fifteen pairwise cancellations, but its diagonal target is
    # zero.  Hence it is only the inactive zero member, not the nonzero cap
    # input required by the intrinsic one-edge theorem.
    two_step_signature = {
        "physical_squarefree_degree": True,
        "selected_midpoint_grade": False,
        "literal_output_grade_change": "only at the two reinserted sites",
        "polynomial": 0,
        "scalar_direct": 0,
        "diagonal_target": 0,
        "target": 0,
        "ordinary_residue": 0,
        "normalized_w": 0,
        "pure_anchor_incidence": 0,
        "pre_cancellation_response_support_edges": 1,
    }
    require(two_step_signature["pure_anchor_incidence"]
            != component["minimal_new_lower_face"]
            ["total_pure_anchor_incidence"],
            "the zero BE identity acquired the C_rel anchor incidence")
    require(two_step_signature["diagonal_target"] == 0,
            "the homogeneous BE identity acquired an active cap target")

    ledger = {
        "pins": PINS,
        "scope": (
            "all |T|=7 odd-principal BE rows on K8; contraction of the "
            "doubled-site edge followed by the unique two-hole edge; all 16 "
            "spin sectors and the three pinned literal output words"
        ),
        "census": {
            "physical_paths": path_count,
            "labelled_physical_paths": labelled_path_count,
            "sector_paths": sector_path_count,
            "decorated_paths": decorated_path_count,
            "raw_BE_terms_per_sector_row": 90,
            "derived_raw_terms_per_row": 30,
            "cancelled_matching_pairs_per_row": 15,
            "squarefree_paths": path_count,
        },
        "physical_operation": {
            "initial_degree": "2 at i; 1 on T-{i}; 0 at k",
            "contraction": "edge {i,j}; holes become {j,k}",
            "reinsertion": "unique edge {j,k}",
            "final_degree": [1] * 8,
            "literal_output_grade": (
                "six labels are preserved; the two reinserted-site labels "
                "are arbitrary"
            ),
            "literal_reinsertion": (
                "arbitrary colours on the unique physical hole edge replace "
                "exactly its two endpoint labels"
            ),
            "distinct_final_output_words": len(literal_output_word_histogram),
            "selected_midpoint_rows": selected_midpoint_rows,
            "pure_output_rows": pure_output_rows,
        },
        "Arf": {
            "net_character": "label({i,j}) xor label({j,k})",
            "histogram": dict(sorted(net_character_histogram.items())),
            "untwisted_paths": net_character_histogram[0],
            "twisted_paths": path_count - net_character_histogram[0],
            "all_16_characters_occur": len(net_character_histogram) == 16,
            "chart_01_or_02_paths": sum(chart_edge_path_histogram.values()),
            "character_pair_histogram": [
                [list(pair), count] for pair, count
                in sorted(edge_character_pair_histogram.items())
            ],
        },
        "literal_expansion": {
            "identity": (
                "x_{jk} * partial_{x_{ij}}(BE_{T,i}) = 0"
            ),
            "pairing": (
                "each of 15 K8 matching monomials occurs once with sign +1 "
                "and once with sign -1"
            ),
            "sample_rows": sample_rows,
        },
        "two_step_signature": two_step_signature,
        "C_rel_signature": component["minimal_new_lower_face"],
        "verdict": (
            "the first physically squarefree genus-2 attachment is an exact "
            "derivative/reinsertion of the zero BE kernel identity. It "
            "preserves one literal output word, has anchor=target=ores=w=0, "
            "and cancels termwise. Therefore it realizes neither C_rel nor "
            "the nonzero-diagonal-target one-edge cap input"
        ),
        "minimal_missing_operation": (
            "a source-valid cross-word or target-augmented derived attachment; "
            "ordinary BE contraction/reinsertion cannot supply either"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the two-step BE ledger changed: {digest}")
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("N=8 genus-2 BE two-step attachment: PASS")
    print("physical paths: 336; squarefree: 336")
    print("spin-sector rows: 5,376; decorated rows: 145,152")
    print("each row: 30 raw terms -> 15 opposite-sign matching pairs -> 0")
    print("Arf paths: 82 untwisted, 254 twisted")
    print("C_rel/cap verdict: neither (anchor=target=ores=w=0; polynomial=0)")
    print("sha256:", digest)


if __name__ == "__main__":
    main()
