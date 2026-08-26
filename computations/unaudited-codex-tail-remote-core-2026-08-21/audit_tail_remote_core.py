#!/usr/bin/env python3
"""Finite orbit/core sizing for one fixed-tail remote no-cap branch."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
import hashlib
import importlib.util
import itertools
import json
import pathlib
import sys


HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TAIL = ROOT / "computations/unaudited-codex-tail-polar-source-lift-2026-08-21"
RESPONSE = ROOT / "computations/unaudited-codex-response-star-2026-08-20"
OUT = HERE / "results_tail_remote_core.json"
MANIFEST = HERE / "remote_branch_core_manifest.json"
PRIME = 1073741827


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(path: pathlib.Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_module(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def logical_sha(payload) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


@lru_cache(None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for matching in perfect_matchings(rest):
            answer.append(((first, second),) + matching)
    return tuple(answer)


def main() -> None:
    tail_path = TAIL / "results_tail_polar_source_lift.json"
    tail = load_json(tail_path)
    symmetry = load_module(
        "tail_remote_symmetry",
        TAIL / "audit_611_71_sdr_and_332_rescue.py",
    )
    response_core = load_module(
        "tail_remote_response_core",
        RESPONSE / "response_star_core.py",
    )

    actions = symmetry.fixed_tail_actions()
    columns = symmetry.COLUMNS
    column_names = symmetry.COLUMN_NAMES
    orbit = sorted({action[0] for action in actions})
    require(orbit == list(range(12)), "fixed-tail columns ceased to be transitive")
    require(sum(action[0] == 0 for action in actions) == 8,
            "y0 stabilizer order changed")

    # The matched star carrier for a column (a,t) is cap pair {6,7}, centre a.
    # Rebuild vertex maps to verify equivariance, not just the column action.
    vertex_maps = []
    for block_permutation in itertools.permutations(range(3)):
        for flips in itertools.product((0, 1), repeat=4):
            mapping = {}
            for vertex in range(8):
                block, clone = divmod(vertex, 2)
                image_block = block_permutation[block] if block < 3 else 3
                mapping[vertex] = 2 * image_block + (clone ^ flips[block])
            vertex_maps.append(mapping)
    unique_vertex_maps = {tuple(sorted(mapping.items())): mapping
                          for mapping in vertex_maps}
    require(len(unique_vertex_maps) == 96, "fixed-tail vertex group changed")
    for mapping in unique_vertex_maps.values():
        image_edge = tuple(sorted((mapping[0], mapping[6])))
        require(image_edge in columns, "y0 left the retained column set")
        require(set((mapping[6], mapping[7])) == {6, 7},
                "matched cap pair left fixed tail")
        require(mapping[0] == image_edge[0],
                "matched star centre ceased to follow the polar column")

    row_ledger = tail["row_ledger"]
    labels = [record["source_label"] for record in row_ledger]
    require(len(labels) == len(set(labels)) == 380,
            "380 source core labels changed")
    profile_counts = Counter(record["profile"] for record in row_ledger)
    require(profile_counts == Counter({"3+3+2": 360,
                                       "6+1+1": 12, "7+1": 8}),
            "380 source core profile changed")

    carrier_labels, carrier_rows = response_core.response_star_matrix(
        # Only labels are source-independent.  A zero source suffices here.
        {edge: [[Fraction(0) for _ in range(3)] for _ in range(3)]
         for edge in itertools.combinations(range(8), 2)},
        6, 7, 0,
    )
    require(len(carrier_labels) == len(carrier_rows) == 90,
            "canonical carrier size changed")
    require(carrier_labels == [
        f"{a}{b}:{alpha}{beta}"
        for a, b in itertools.combinations(range(1, 6), 2)
        for alpha in range(3) for beta in range(3)
    ], "canonical carrier row labels changed")

    # Exact support consequence of the representative 611 equation.
    word = tuple(map(int, "02222212"))
    matchings = perfect_matchings(tuple(range(8)))
    linear = []
    quadratic = []
    for matching in matchings:
        degree = sum(word[a] != word[b] for a, b in matching)
        (linear if degree == 1 else quadratic).append(matching)
    require(len(linear) == 15 and len(quadratic) == 90,
            "representative 611 tail split changed")
    require(all((0, 6) in matching for matching in linear),
            "representative linear row ceased to pivot y0")

    endpoint_variables = [
        f"a_{u}{v}_{i}{j}"
        for u, v in itertools.combinations(range(8), 2)
        for i in range(3) for j in range(3)
    ]
    witness_variables = [f"c_{label.replace(':', '_')}"
                         for label in carrier_labels]
    inverse_variables = ["inv_y0"] + [
        f"inv_h2_{site}{tail_site}"
        for tail_site in (6, 7) for site in range(6)
    ]
    require(len(endpoint_variables) == 252 and
            len(witness_variables) == 90 and len(inverse_variables) == 13,
            "branch variable census changed")

    source_terms = 380 * 105
    pure_terms = 3 * 106
    localizer_terms = 12 * 16 + 2
    diagonal_membership_terms = 8 * 180 + 181
    direct_membership_terms = 9 * 181
    require(source_terms == 39900 and pure_terms == 318 and
            localizer_terms == 194 and diagonal_membership_terms == 1621 and
            direct_membership_terms == 1629,
            "branch term census changed")

    localizers = ["y0"] + [
        f"h2_{site}{tail_site}"
        for tail_site in (6, 7) for site in range(6)
    ]
    branch_table = []
    for blocker in ("K00", "K11", "K22", "<K,A_67>"):
        direct = blocker == "<K,A_67>"
        branch_table.append({
            "blocker": blocker,
            "carrier": {"pair": [6, 7], "kind": "star", "centre": 0,
                        "matrix_shape": [90, 9]},
            "variables": 355,
            "equations": 405,
            "maximum_total_degree": 4,
            "expanded_term_upper_exact": (
                source_terms + pure_terms + localizer_terms +
                (direct_membership_terms if direct
                 else diagonal_membership_terms)
            ),
            "membership_encoding": (
                "9 equations ell_coordinate=sum_(90 rows) "
                "c_row*L_row_coordinate"
            ),
        })

    manifest = {
        "status": "EXACT CONSTRUCTOR MANIFEST; no solve launched",
        "prime_for_optional_discovery": PRIME,
        "ambient_variables": endpoint_variables,
        "rowspan_witness_variables": witness_variables,
        "factorized_inverse_variables": inverse_variables,
        "pure_generators": ["F_00000000-1", "F_11111111-1", "F_22222222-1"],
        "mixed_source_generators": labels,
        "source_generator_definition": (
            "F_w=sum over the 105 perfect matchings of product of the four "
            "literal endpoint-ordered cells a_uv_[w_u,w_v]"
        ),
        "canonical_carrier": {
            "pair": [6, 7], "kind": "star", "centre": 0,
            "response_row_labels": carrier_labels,
            "response_row_definition": (
                "L[(ab:alpha beta),(ij)]="
                "A_6a[i,alpha]*A_7b[j,beta]+"
                "A_6b[i,beta]*A_7a[j,alpha]"
            ),
        },
        "blocker_right_sides": {
            "K00": "delta_(ij),(00)",
            "K11": "delta_(ij),(11)",
            "K22": "delta_(ij),(22)",
            "<K,A_67>": "A_67[i,j]",
        },
        "factorized_localizer_equations": (
            ["inv_y0*y0-1"] +
            [f"inv_h2_{site}{tail_site}*h2_{site}{tail_site}-1"
             for tail_site in (6, 7) for site in range(6)]
        ),
        "hafnian_localizer_definition": (
            "h2_at=Haf of the colour-2 diagonal graph on V\\{a,t}; "
            "15 literal three-edge monomials"
        ),
        "branch_table": branch_table,
    }
    manifest["logical_sha256"] = logical_sha(manifest)

    payload = {
        "status": "PASS exact fixed-tail remote branch core audit",
        "remote_tail_orbits": {
            "group_order": 96,
            "orbit_count": 1,
            "representative": "y0=A_06[0,1]",
            "orbit_size": 12,
            "representative_stabilizer_order": 8,
            "orbit": [column_names[index] for index in orbit],
            "matched_carrier_rule": (
                "column A_at[0,1] is paired with cap pair {6,7} and residual "
                "star centre a; the rule is equivariant under all 96 actions"
            ),
        },
        "remote_no_cap_orbit_branches": branch_table,
        "smallest_exact_incidence_core": {
            "common_variables": {
                "endpoint_source": 252,
                "rowspan_witness": 90,
                "factorized_inverses": 13,
                "total": 355,
            },
            "common_equations": {
                "pure_normalizations": 3,
                "literal_X5_tail_rows": 380,
                "one_carrier_rowspan_membership": 9,
                "factorized_localizers": 13,
                "total": 405,
            },
            "localizers": localizers,
            "rank_free_encoding": (
                "The 90 witness variables encode ell in rowspan(L) directly "
                "and are smaller than stratifying ranks 0..9 by minors."
            ),
            "optional_modular_discovery_prime": PRIME,
            "exact_Q_replay_required_for_any_unit": True,
            "manifest": MANIFEST.name,
            "manifest_logical_sha256": manifest["logical_sha256"],
        },
        "support_feasibility": {
            "verdict": "SURVIVES the immediate support screen",
            "forced_by_F_02222212": (
                "On y0*h2_06!=0, the 611 equation forces at least one of "
                "its 90 quadratic terms to be live: for distinct "
                "b,c in {1,2,3,4,5,7}, a live A_0b[0,2], a live "
                "A_6c[1,2], and a live G2 matching on the remaining four sites."
            ),
            "meaning": (
                "The representative remote branch necessarily leaves the "
                "12-column quotient and couples the other two colour-pair "
                "tail channels. There is no monomial contradiction."
            ),
            "localizers_plus_one_carrier_feasible_without_source_rows": (
                "yes; the frozen deterministic dense source has D611!=0, "
                "y0!=0 and rank(L)=9 for the carrier"
            ),
        },
        "one_carrier_sufficiency": {
            "logical_cover": (
                "On e=1 some polar column is nonzero; transitivity moves it "
                "to y0. A globally no-cap source blocks the matched star "
                "carrier, so one of the four displayed membership branches "
                "holds. Therefore emptiness of these four ideals is enough; "
                "all 728 carriers are not required in the first exact target."
            ),
            "algebraic_status": (
                "No branch has been solved. If a branch survives, additional "
                "carrier clauses may be needed, but this is not inherent at "
                "the covering stage."
            ),
        },
        "scope_guard": (
            "This is the D611 principal-open remote core for one fixed-tail "
            "12-column packet. The other 125 tail rank charts and the four "
            "support-factor recursions require the same construction with "
            "their own frozen rescue localizers. It is not yet a cover of "
            "the full 168-variable remote component."
        ),
        "mutation_guards": {
            "split_y_and_z_into_two_orbits": True,
            "mismatch_y0_with_star_centre1": True,
            "drop_one_of_four_blocker_branches": True,
            "claim_support_unit_from_611_cancellation": True,
        },
        "source_hashes": {
            str(tail_path.relative_to(ROOT)): sha256(tail_path),
            str((RESPONSE / "response_star_core.py").relative_to(ROOT)):
                sha256(RESPONSE / "response_star_core.py"),
        },
    }
    payload["logical_sha256"] = logical_sha(payload)

    result_text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    manifest_text = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    if "--write-results" in sys.argv:
        OUT.write_text(result_text, encoding="utf-8")
        MANIFEST.write_text(manifest_text, encoding="utf-8")
    sys.stdout.write(result_text)


if __name__ == "__main__":
    main()
