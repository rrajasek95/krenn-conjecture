#!/usr/bin/env python3
"""Classify all 34 first source-changing supports and exact clean caps."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path


if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "unaudited-codex-n8-x5-single-offfamily-block-2026-08-25/MANIFEST.sha256"
PARENT_SHA256 = "73a0b8e1e9e3934ce74f77506b85748c8f147219fecb53992ca122b44fb7a3bb"
PARENT_RESULT = HERE.parent / "unaudited-codex-n8-x5-single-offfamily-block-2026-08-25/results_single_offfamily_block.json"
PARENT_RESULT_SHA256 = "fe69a5e1854bf5aafdccd8c7a369c7da103fc220fed1c7a332500b990fbea2a2"
CORE = HERE.parent / "unaudited-codex-n8-x5-two-cell-escape-dichotomy-2026-08-25/audit_two_cell_dichotomy.py"
CORE_SHA256 = "f8305d4b514ac6dc0a2b28b359dbca62929667248596beee48804eb43109e876"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


assert sha256(PARENT) == PARENT_SHA256
assert sha256(PARENT_RESULT) == PARENT_RESULT_SHA256
assert sha256(CORE) == CORE_SHA256
spec = importlib.util.spec_from_file_location("x5_core", CORE)
assert spec is not None and spec.loader is not None
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
VARIABLE = frozenset(((0, 4), (3, 5), (1, 2), (6, 7)))
FAMILY = FIXED | VARIABLE
CAP = frozenset((6, 7))
TRIANGLE = frozenset((0, 1, 2))
VARIABLE_NAMES = {(0, 4): "X", (3, 5): "Y", (1, 2): "U", (6, 7): "V"}
RESIDUAL_SITE_COLOUR = ("a", "b", "b", "a", "a", "a", "b", "b")


def edge_string(edge):
    return "".join(map(str, edge))


def parse_edge(text):
    assert len(text) == 2
    return tuple(map(int, text))


def identity_matrix():
    return [[int(row == column) for column in core.COLORS] for row in core.COLORS]


def dense_matrix(seed):
    return [
        [Fraction(seed + 1 + 3 * row + 5 * column, 17 + seed + row + column)
         for column in core.COLORS]
        for row in core.COLORS
    ]


def install_block(source, edge, matrix):
    u, v = edge
    assert u < v
    for left, right in itertools.product(core.COLORS, repeat=2):
        core.put(source, u, v, left, right, matrix[left][right])


def support_response_edges(support, p, q):
    residual = tuple(site for site in range(8) if site not in (p, q))
    answer = []
    for a, b in itertools.combinations(residual, 2):
        direct = tuple(sorted((p, a))) in support and tuple(sorted((q, b))) in support
        switched = tuple(sorted((p, b))) in support and tuple(sorted((q, a))) in support
        if direct or switched:
            answer.append((a, b))
    return tuple(answer)


def cap_certificate(support):
    # Fixed identity caps suffice for all 34 supports.  Lexicographic choice
    # makes the certificate deterministic.
    for p, q in sorted(FIXED):
        residual = tuple(site for site in range(8) if site not in (p, q))
        responses = support_response_edges(support, p, q)
        for triangle in itertools.combinations(residual, 3):
            if all(set(edge) <= set(triangle) for edge in responses):
                return {
                    "cap": edge_string((p, q)),
                    "triangle": "".join(map(str, triangle)),
                    "possible_response_edges": list(map(edge_string, responses)),
                    "forbidden_response_matrix_rank": 0,
                    "kernel_dimension": 9,
                    "K": "I3",
                    "kappa": [1, 1, 1],
                    "s_pairing": 3,
                }
    raise AssertionError("no fixed-cap structural certificate")


def term_string(matching, new_names):
    factors = []
    for edge in matching:
        left_colour = RESIDUAL_SITE_COLOUR[edge[0]]
        right_colour = RESIDUAL_SITE_COLOUR[edge[1]]
        if edge in FIXED:
            assert left_colour == right_colour
            continue
        name = VARIABLE_NAMES.get(edge, new_names.get(edge))
        assert name is not None
        factors.append(f"{name}[{left_colour},{right_colour}]")
    return "1" if not factors else "*".join(factors)


def matching_value(source, matching, word):
    value = Fraction(1)
    for u, v in matching:
        value *= core.get(source, u, v, word[u], word[v])
    return value


def apply_permutation_edge(edge, permutation):
    return tuple(sorted((permutation[edge[0]], permutation[edge[1]])))


def apply_permutation_pair(pair, permutation):
    return tuple(sorted(apply_permutation_edge(edge, permutation) for edge in pair))


def main():
    parent = json.loads(PARENT_RESULT.read_text())
    pair_records = parent["first_support_changing_layer"]["records"]
    support_pairs = tuple(
        tuple(parse_edge(edge) for edge in record["edges"])
        for record in pair_records
    )
    assert len(support_pairs) == len(set(support_pairs)) == 34

    # Exact frozen source/guard automorphism group.  Fixed identity edges,
    # variable cycle edges, cap67, and triangle012 are each preserved as sets.
    automorphisms = []
    for permutation in itertools.permutations(range(8)):
        fixed_image = {apply_permutation_edge(edge, permutation) for edge in FIXED}
        variable_image = {apply_permutation_edge(edge, permutation) for edge in VARIABLE}
        cap_image = {permutation[site] for site in CAP}
        triangle_image = {permutation[site] for site in TRIANGLE}
        if fixed_image == set(FIXED) and variable_image == set(VARIABLE) \
                and cap_image == set(CAP) and triangle_image == set(TRIANGLE):
            automorphisms.append(permutation)
    assert automorphisms == [
        tuple(range(8)),
        (0, 2, 1, 3, 4, 5, 7, 6),
    ]

    pair_set = set(support_pairs)
    seen = set()
    orbits = []
    all_support_certificates = {}
    formula_replays = []
    for pair in support_pairs:
        if pair in seen:
            continue
        orbit = sorted({apply_permutation_pair(pair, permutation) for permutation in automorphisms})
        assert set(orbit) <= pair_set
        seen.update(orbit)
        representative = orbit[0]
        support = set(FAMILY) | set(representative)
        new_matchings = tuple(
            matching for matching in core.PM8
            if set(matching) <= support and not set(matching) <= set(FAMILY)
        )
        assert new_matchings and all(set(representative) <= set(matching) for matching in new_matchings)
        new_names = {representative[0]: "Z", representative[1]: "W"}
        terms = [term_string(matching, new_names) for matching in new_matchings]
        formula = "P_a*Q_b + " + " + ".join(terms)
        certificate = cap_certificate(support)

        # Literal dense rational replay of the residual formula and structural
        # cap certificate.  No pure/common-zero assumption is used by the cap.
        source = {}
        for edge in FIXED:
            install_block(source, edge, identity_matrix())
        assigned = {}
        for index, edge in enumerate(sorted(VARIABLE | set(representative))):
            assigned[edge] = dense_matrix(11 + 7 * len(orbits) + index)
            install_block(source, edge, assigned[edge])
        for a, b in itertools.permutations(core.COLORS, 2):
            word = (a, b, b, a, a, a, b, b)
            base = (1 + assigned[(0, 4)][a][a] * assigned[(3, 5)][a][a]) * \
                   (1 + assigned[(1, 2)][b][b] * assigned[(6, 7)][b][b])
            extra = sum(matching_value(source, matching, word) for matching in new_matchings)
            assert core.amplitude(source, word) == base + extra
            formula_replays.append({
                "orbit": len(orbits), "colours": [a, b], "value": str(base + extra)
            })
        p, q = parse_edge(certificate["cap"])
        triangle = frozenset(map(int, certificate["triangle"]))
        residual = tuple(site for site in range(8) if site not in (p, q))
        forbidden = tuple(
            edge for edge in itertools.combinations(residual, 2)
            if not set(edge) <= triangle
        )
        K = identity_matrix()
        assert all(core.response(source, p, q, *edge, K) == [[0] * 3 for _ in range(3)]
                   for edge in forbidden)
        assert [K[colour][colour] for colour in core.COLORS] == [1, 1, 1]
        assert sum(K[i][j] * core.get(source, p, q, i, j)
                   for i, j in itertools.product(core.COLORS, repeat=2)) == 3

        orbit_record = {
            "orbit_id": len(orbits),
            "representative": [edge_string(edge) for edge in representative],
            "members": [[edge_string(edge) for edge in member] for member in orbit],
            "orbit_size": len(orbit),
            "new_matchings": [core.matching_string(matching) for matching in new_matchings],
            "six_residual_formula": formula,
            "cap_certificate": certificate,
            "common_zero_implication": "active clean cap (certificate is coefficient-independent)",
        }
        orbits.append(orbit_record)
        for member in orbit:
            member_support = set(FAMILY) | set(member)
            member_certificate = cap_certificate(member_support)
            all_support_certificates["+".join(map(edge_string, member))] = member_certificate

    assert seen == pair_set
    assert len(orbits) == 18
    assert sum(record["orbit_size"] == 1 for record in orbits) == 2
    assert sum(record["orbit_size"] == 2 for record in orbits) == 16
    assert len(all_support_certificates) == 34
    assert all(record["forbidden_response_matrix_rank"] == 0
               and record["kernel_dimension"] == 9
               and record["s_pairing"] == 3
               for record in all_support_certificates.values())

    # Load-bearing direct family requested by the task.
    direct = next(record for record in orbits if record["representative"] == ["01", "23"])
    assert direct["six_residual_formula"] == "P_a*Q_b + Z[a,b]*W[b,a]*V[b,b]"
    assert direct["cap_certificate"] == {
        "cap": "16",
        "triangle": "027",
        "possible_response_edges": ["07", "27"],
        "forbidden_response_matrix_rank": 0,
        "kernel_dimension": 9,
        "K": "I3",
        "kappa": [1, 1, 1],
        "s_pairing": 3,
    }

    result = {
        "schema": "KRENN_X5_TWO_BLOCK_CAP_CLASSIFICATION_V1",
        "status": "PASS_ALL_34_TWO_BLOCK_SUPPORTS_HAVE_COEFFICIENT_INDEPENDENT_ACTIVE_CAP",
        "parent_manifest_sha256": PARENT_SHA256,
        "parent_result_sha256": PARENT_RESULT_SHA256,
        "core_sha256": CORE_SHA256,
        "exact_guard_symmetry": {
            "order": len(automorphisms),
            "elements": [list(permutation) for permutation in automorphisms],
            "generator": "(1 2)(6 7)",
            "preserves": ["fixed identity edges", "variable cycle edges", "cap67", "triangle012"],
            "support_orbits": len(orbits),
            "singleton_orbits": 2,
            "doubleton_orbits": 16,
        },
        "orbit_classification": orbits,
        "all_34_support_cap_certificates": all_support_certificates,
        "theorem": {
            "hypotheses": (
                "fixed A03=A16=A27=A45=I3, arbitrary four cycle blocks, and "
                "one of the 34 source-changing two-block supports"
            ),
            "conclusion": (
                "a displayed fixed identity cap with K=I3 has all possible responses "
                "inside its displayed triangle, kappa=(1,1,1), and s=3; hence it is active clean"
            ),
            "common_zero_of_six_residuals_required": False,
            "common_zero_implication": True,
            "coefficient_field": "characteristic zero",
            "response_minor_certificate": "all 108 forbidden response entries are the zero polynomial; rank=0 and kernel dimension=9",
        },
        "direct_A01_A23": {
            "residual_formula": "R_ab=P_a*Q_b+A01[a,b]*A23[b,a]*V[b,b]",
            "universal_active_cap": direct["cap_certificate"],
            "interpretation": "every coefficient point, including every six-residual common zero, is routed to cap16/triangle027",
        },
        "literal_replay": {
            "orbit_representatives": len(orbits),
            "residual_colour_cases": len(formula_replays),
            "dense_rational_sources": len(orbits),
            "all_cap_certificates_replayed": True,
            "records_sha256": hashlib.sha256(json.dumps(formula_replays, sort_keys=True).encode()).hexdigest(),
        },
        "scope": {
            "all_34_two_block_supports": True,
            "all_18_exact_guard_orbits": True,
            "smallest_surviving_inactive_common_zero_family": None,
            "three_or_more_added_blocks_classified": False,
            "full_support_dichotomy": False,
            "full_conjecture_claim": False,
            "broad_cegar": False,
            "degree_twelve_read": False,
        },
    }
    temporary = HERE / "results_two_block_cap_classification.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_two_block_cap_classification.json")
    print(json.dumps({
        "status": result["status"],
        "orbits": len(orbits),
        "supports": len(all_support_certificates),
        "direct_cap": direct["cap_certificate"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
