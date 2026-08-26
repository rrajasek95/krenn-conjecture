#!/usr/bin/env python3
"""Independent design-only referee for the 16 unmapped seven-block records."""

from __future__ import annotations

import hashlib
import itertools
import json
import os
from collections import Counter
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRODUCER = ROOT / "computations/unaudited-codex-n8-x5-unmapped16-carrier-incidence-design-2026-08-25"
COVERAGE_DIR = ROOT / "computations/unaudited-codex-n8-x5-seven-block-64-carrier-coverage-2026-08-25"
COVERAGE = COVERAGE_DIR / "results_64_carrier_coverage.json"
BOUNDARY_DIR = ROOT / "computations/unaudited-codex-n8-x5-seven-block-support-boundary-2026-08-25"
PINS = {
    PRODUCER / "MANIFEST.sha256": "5cb72ac4af5a3ad3decbf3ba59ec858e23dcf2810c289d586feb14aeea1e61fe",
    PRODUCER / "audit_unmapped16.py": "2d9d87a85310c1f024f24b766cee49c26e55b83ed512479e0909779a46ce05c7",
    PRODUCER / "results_unmapped16_design.json": "2fe9e2a561397b58941b0f4210b3e4fb4a5457f377d4e23b7fc1dd6d0d22c008",
    COVERAGE_DIR / "MANIFEST.sha256": "944d1ec0df599056d4cadfe689093f621bfa9c939475efbd7158b7414443d578",
    COVERAGE: "e38dbd6f67c988da80bfbe0f5663a31a042daf8d7e29a9376f473b22325ab691",
    BOUNDARY_DIR / "MANIFEST.sha256": "13bb284c0b400f7227db74f8a135155dd324251147ebf48711b9af8d10adcc85",
}

FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
INTERNAL_GUARD = frozenset(((0, 1), (0, 2), (1, 2)))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def parse_edge(value: str):
    return tuple(map(int, value))


def edge(a, b):
    return tuple(sorted((a, b)))


def label(value):
    return "".join(map(str, value))


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


PM8 = tuple(sorted(matchings(tuple(range(8)))))
assert len(PM8) == 105


def response_terms(support, cap, pair):
    """Return terms with their cap-p and cap-q incident blocks, independently of display orientation."""
    p, q = cap
    a, b = pair
    out = []
    if edge(p, a) in support and edge(q, b) in support:
        out.append(("direct", edge(p, a), edge(q, b)))
    if edge(p, b) in support and edge(q, a) in support:
        out.append(("switched", edge(p, b), edge(q, a)))
    return out


def carrier_census(support):
    counts = Counter()
    selected = []
    scans = Counter()
    for cap in itertools.combinations(range(8), 2):
        residual = tuple(v for v in range(8) if v not in cap)
        definitions = [
            ("triangle", defining, set(itertools.combinations(defining, 2)))
            for defining in itertools.combinations(residual, 3)
        ] + [
            ("star", (center,), {edge(center, other) for other in residual if other != center})
            for center in residual
        ]
        for kind, defining, excluded in definitions:
            scans[kind] += 1
            terms = []
            for pair in itertools.combinations(residual, 2):
                if pair not in excluded:
                    for orientation, pblock, qblock in response_terms(support, cap, pair):
                        terms.append((pair, orientation, pblock, qblock))
            distinct_pairs = {term[0] for term in terms}
            pblocks = {term[2] for term in terms}
            qblocks = {term[3] for term in terms}
            if len(terms) == 2 and len(distinct_pairs) == 2 and ((len(pblocks) == 1) != (len(qblocks) == 1)):
                counts[kind] += 1
                selected.append((cap, kind, defining, terms))
    assert scans == {"triangle": 560, "star": 168}
    return counts, selected


def display_oriented(cap_site, residual_site):
    block = f"A{min(cap_site, residual_site)}{max(cap_site, residual_site)}"
    return block + ("^T" if cap_site < residual_site else "")


def transpose(value):
    return value[:-2] if value.endswith("^T") else value + "^T"


def response_formula(cap, pair, orientation):
    p, q = cap
    a, b = pair
    if orientation == "direct":
        return f"{display_oriented(p, a)}*K*{transpose(display_oriented(q, b))}"
    return f"{display_oriented(q, a)}*K^T*{transpose(display_oriented(p, b))}"


def simultaneous_orbits():
    raw = list(itertools.product(range(3), repeat=3))
    groups = {}
    for record in raw:
        images = [tuple(permutation[item] for item in record) for permutation in itertools.permutations(range(3))]
        groups.setdefault(min(images), []).append(record)
    return raw, groups


def replay_manifest():
    for line in (PRODUCER / "MANIFEST.sha256").read_text().splitlines():
        expected, relative = line.split("  ", 1)
        assert sha256(PRODUCER / relative) == expected


def main():
    for path, expected in PINS.items():
        assert sha256(path) == expected, path
    replay_manifest()
    uncovered = json.loads(COVERAGE.read_text())["uncovered"]
    assert len(uncovered) == 16
    assert Counter(item["orbit_id"] for item in uncovered) == {i: 2 for i in range(8)}
    assert Counter(item["classification"] for item in uncovered) == {
        "NO_GUARD_ANCHOR_06_OR_07": 12,
        "NO_OUTSIDE_R6_R7_RECTANGLE": 4,
    }

    record_audits = []
    for index, record in enumerate(uncovered):
        support = FIXED | {parse_edge(value) for value in record["added"] + record["nonzero_variable_blocks"]}
        supported = [matching for matching in PM8 if set(matching) <= support]
        assert len(supported) == record["supported_perfect_matchings"] == 8
        counts, carriers = carrier_census(support)
        a12 = (1, 2) in support
        expected = 24 if a12 else 40
        assert counts == {"triangle": expected // 2, "star": expected // 2}

        rectangles = [r for r in (3, 4, 5) if edge(r, 6) in support and edge(r, 7) in support]
        guards = []
        for pair in itertools.combinations(range(6), 2):
            if pair not in INTERNAL_GUARD and response_terms(support, (6, 7), pair):
                guards.append(pair)
        if record["classification"] == "NO_GUARD_ANCHOR_06_OR_07":
            assert len(rectangles) == 1
            r = rectangles[0]
            assert guards == [(1, r), (2, r)]
            for pair in guards:
                terms = response_terms(support, (6, 7), pair)
                assert len(terms) == 2
            orientations = [
                f"A{r}7^T+A17*A{r}6^T=0",
                f"A26*A{r}7^T+A{r}6^T=0",
            ]
        else:
            assert rectangles == [] and guards == []
            orientations = []
        record_audits.append({
            "index": index,
            "orbit_id": record["orbit_id"],
            "A12": a12,
            "matchings": len(supported),
            "two_sandwich": sum(counts.values()),
            "triangle": counts["triangle"],
            "star": counts["star"],
            "rectangle_sites": rectangles,
            "guard_orientations": orientations,
        })

    assert Counter(item["two_sandwich"] for item in record_audits if item["A12"]) == {24: 8}
    assert Counter(item["two_sandwich"] for item in record_audits if not item["A12"]) == {40: 8}

    selected_support = tuple(sorted(("01", "15", "17", "23", "26", "46", "47")))
    chosen = [
        (source, audit) for source, audit in zip(uncovered, record_audits)
        if tuple(sorted(source["added"])) == selected_support
    ]
    assert len(chosen) == 2 and {item[1]["A12"] for item in chosen} == {False, True}
    base_record = chosen[0][0]
    support = FIXED | {parse_edge(value) for value in base_record["added"] + base_record["nonzero_variable_blocks"]}
    _, carriers = carrier_census(support)
    cap, kind, defining, terms = next(item for item in carriers if item[0] == (2, 7) and item[1] == "star" and item[2] == (1,))
    assert [(label(pair), orientation, label(pblock), label(qblock)) for pair, orientation, pblock, qblock in terms] == [
        ("34", "direct", "23", "47"),
        ("46", "switched", "26", "47"),
    ]
    assert response_formula(cap, (3, 4), "direct") == "A23^T*K*A47^T"
    assert response_formula(cap, (4, 6), "switched") == "A47*K^T*A26"

    # Rank-r factorization charts: coordinate i and one nonzero r-minor of each 3xr factor.
    raw_charts, orbit_groups = simultaneous_orbits()
    assert len(raw_charts) == 27 and len(orbit_groups) == 5
    assert sorted(map(len, orbit_groups.values())) == [3, 6, 6, 6, 6]
    rank_counts = {}
    for rank in (1, 2):
        without_a12_variables = 7 * 9 + 6 * rank + rank + 6 + 1
        generators = 3**8 + 3 * rank + 3 + 3 + 1
        rank_counts[str(rank)] = {
            "A12_absent_variables": without_a12_variables,
            "A12_present_variables": without_a12_variables + 9,
            "generators": generators,
            "raw_charts": 27,
            "S3_orbits": 5,
        }
    assert rank_counts == {
        "1": {"A12_absent_variables": 77, "A12_present_variables": 86, "generators": 6571, "raw_charts": 27, "S3_orbits": 5},
        "2": {"A12_absent_variables": 84, "A12_present_variables": 93, "generators": 6574, "raw_charts": 27, "S3_orbits": 5},
    }

    producer = json.loads((PRODUCER / "results_unmapped16_design.json").read_text())
    selected = producer["selected_reduction"]
    assert selected["guard"]["equations"] == ["A47^T+A17*A46^T=0", "A26*A47^T+A46^T=0"]
    assert selected["guard"]["elimination"] == "A46=-A47*A26^T"
    assert selected["guard"]["reduced"] == "(I-A17*A26)*A47^T=0"
    assert selected["carrier"]["factorization"] == "[A23^T|A26^T]*K*A47^T (up to transposing R46)"
    assert selected["singular_branch"]["incidence_equations"] == ["V*z=e_i", "A23*u+A26*w=e_i"]
    assert producer["scope"] == {"full_conjecture": False, "large_groebner_runs": 0, "mathematically_closed_records": 0}

    result = {
        "schema": "KRENN_X5_UNMAPPED16_CARRIER_INCIDENCE_REFEREE_V1",
        "status": "PASS_EXACT_DESIGN_ONLY_ZERO_CLOSURE",
        "producer_manifest_sha256": PINS[PRODUCER / "MANIFEST.sha256"],
        "support_census": {
            "records": 16,
            "orbit_ids": 8,
            "matchings_each": 8,
            "A12_present_records": 8,
            "A12_absent_records": 8,
            "A12_present_carriers_each": 24,
            "A12_absent_carriers_each": 40,
            "rectangle_records": 12,
            "no_rectangle_records": 4,
        },
        "record_audits": record_audits,
        "selected_orientation": {
            "guard": ["A47^T+A17*A46^T=0", "A26*A47^T+A46^T=0"],
            "elimination": "A46=-A47*A26^T",
            "reduced_guard": "(I-A17*A26)*A47^T=0",
            "responses": ["R34=A23^T*K*A47^T", "R46=A47*K^T*A26"],
            "transposed_second": "R46^T=A26^T*K*A47^T",
            "factorization": "[A23^T|A26^T]*K*A47^T",
        },
        "singular_rank_design": {
            "factorization": "A47=U*V^T with U,V full column rank r",
            "ranks": [1, 2],
            "proper_right_space": "Q=Col(V)=Col(A47^T)",
            "guard_after_factorization": "(I-A17*A26)*V=0",
            "incidence": ["V*z=e_i", "A23*u+A26*w=e_i"],
            "chart_saturation": "one nonzero r-minor of U times one nonzero r-minor of V",
            "counts": rank_counts,
        },
        "invertible_branch_obstruction": {
            "rank": 3,
            "guard_consequences": ["A17*A26=I", "A17,A26,A46,A47 invertible"],
            "selected_carrier_spaces": ["P=ColSpan(A23,A26)=k^3 because A26 is invertible", "Q=Col(A47^T)=k^3"],
            "precise_failure": "P tensor Q is the full 3x3 matrix space, so the selected response map has zero kernel and supplies no active K",
            "remaining_need": "a full-X5 residual/rank-drop identity or a genuinely different carrier whose properness follows from additional equations",
        },
        "scope": {"ideal_runs": 0, "records_closed": 0, "transport_claim": False, "D12_reads": False},
    }
    temporary = HERE / "results_referee.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, HERE / "results_referee.json")
    print(json.dumps({"status": result["status"], "records": 16, "closed": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
