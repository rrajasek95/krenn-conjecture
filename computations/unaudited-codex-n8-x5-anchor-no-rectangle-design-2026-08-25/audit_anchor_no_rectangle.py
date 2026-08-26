#!/usr/bin/env python3
"""Exact census/design for the four anchor/no-rectangle X5 records; no solve."""
from __future__ import annotations

import collections
import copy
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / "computations/unaudited-codex-n8-x5-unmapped16-carrier-incidence-design-2026-08-25"
PINS = {
    PARENT / "MANIFEST.sha256": "5cb72ac4af5a3ad3decbf3ba59ec858e23dcf2810c289d586feb14aeea1e61fe",
    PARENT / "audit_unmapped16.py": "2d9d87a85310c1f024f24b766cee49c26e55b83ed512479e0909779a46ce05c7",
    PARENT / "results_unmapped16_design.json": "2fe9e2a561397b58941b0f4210b3e4fb4a5457f377d4e23b7fc1dd6d0d22c008",
}

SITES = tuple(range(8))
COLORS = tuple(range(3))
S3 = tuple(itertools.permutations(COLORS))
P8 = tuple(itertools.permutations(SITES))
FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
VARIABLE_FAMILY = frozenset(((0, 4), (1, 2), (3, 5), (6, 7)))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def load_parent_module():
    spec = importlib.util.spec_from_file_location("sealed_unmapped16", PARENT / "audit_unmapped16.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def edge(value: str | tuple[int, int]) -> tuple[int, int]:
    return tuple(map(int, value)) if isinstance(value, str) else value


def label(value: tuple[int, int]) -> str:
    return f"{value[0]}{value[1]}"


def map_edge(value: tuple[int, int], permutation: tuple[int, ...]) -> tuple[int, int]:
    return tuple(sorted((permutation[value[0]], permutation[value[1]])))


def map_edges(values, permutation):
    return frozenset(map_edge(value, permutation) for value in values)


def added(record):
    return frozenset(edge(value) for value in record["added"])


def variables(record, reduced=False):
    values = frozenset(edge(value) for value in record["nonzero_variable_blocks"])
    return values - ({(1, 2)} if reduced else set())


def support(record, reduced=False):
    return FIXED | added(record) | variables(record, reduced=reduced)


def site_maps(source, target, reduced=False):
    return [
        permutation
        for permutation in P8
        if map_edges(FIXED, permutation) == FIXED
        and map_edges(VARIABLE_FAMILY, permutation) == VARIABLE_FAMILY
        and map_edges(added(source), permutation) == added(target)
        and map_edges(variables(source, reduced), permutation) == variables(target, reduced)
    ]


def supported_matchings(module, record):
    available = support(record)
    return tuple(matching for matching in module.PM8 if set(matching) <= available)


def amplitude(record, matching_cache, word):
    answer = collections.Counter()
    for matching in matching_cache[record["record_index"]]:
        monomial = []
        for value in matching:
            left, right = word[value[0]], word[value[1]]
            if value in FIXED:
                if left != right:
                    break
            else:
                if value == (1, 2):
                    raise AssertionError("A12 unexpectedly occurs in a supported perfect matching")
                monomial.append((value, left, right))
        else:
            answer[tuple(sorted(monomial))] += 1
    return answer


def map_word(word, permutation, color):
    answer = [None] * 8
    for site in SITES:
        answer[permutation[site]] = color[word[site]]
    return tuple(answer)


def map_factor(factor, permutation, color):
    value, left, right = factor
    p, q = permutation[value[0]], permutation[value[1]]
    if p < q:
        return ((p, q), color[left], color[right])
    return ((q, p), color[right], color[left])


def map_amplitude(value, permutation, color):
    answer = collections.Counter()
    for monomial, coefficient in value.items():
        answer[tuple(sorted(map_factor(factor, permutation, color) for factor in monomial))] += coefficient
    return answer


def multiply(left, right):
    answer = collections.Counter()
    for first, a in left.items():
        for second, b in right.items():
            answer[tuple(sorted(first + second))] += a * b
    return answer


def atom(value, row, column):
    return ((value, row, column),)


def factorized_amplitude(word):
    a, b, c, d, e, f, g, h = word
    R = collections.Counter()
    if a == d and e == f:
        R[()] += 1
    R[tuple(sorted(atom((0, 4), a, e) + atom((3, 5), d, f)))] += 1
    S = collections.Counter()
    if b == g and c == h:
        S[()] += 1
    S[tuple(sorted(atom((1, 7), b, h) + atom((2, 6), c, g)))] += 1
    T = collections.Counter()
    if e == f:
        T[atom((1, 3), b, d)] += 1
    T[tuple(sorted(atom((1, 4), b, e) + atom((3, 5), d, f)))] += 1
    U = collections.Counter()
    if c == h:
        U[atom((0, 6), a, g)] += 1
    U[tuple(sorted(atom((0, 7), a, h) + atom((2, 6), c, g)))] += 1
    answer = multiply(R, S)
    answer.update(multiply(T, U))
    return +answer


def carrier_semantic(module, record, kind, cap, defining):
    terms = module.carrier_terms(support(record), cap, kind, defining)
    semantic_terms = []
    for term in terms:
        semantic_terms.append({
            **term,
            "cross_edges": sorted((term["left_block"], term["right_block"])),
        })
    two = module.two_sandwich_record(cap, kind, defining, terms)
    return {
        "kind": kind,
        "cap": label(cap),
        "defining_sites": list(defining),
        "identity_cap": cap in FIXED,
        "response_term_count": len(terms),
        "response_pairs": sorted({term["response_pair"] for term in terms}),
        "terms": semantic_terms,
        "two_sandwich": two,
    }


def all_carriers(module, record):
    answer = []
    for cap in itertools.combinations(SITES, 2):
        residual = tuple(site for site in SITES if site not in cap)
        for defining in itertools.combinations(residual, 3):
            answer.append(carrier_semantic(module, record, "triangle", cap, defining))
        for center in residual:
            answer.append(carrier_semantic(module, record, "star", cap, (center,)))
    assert len(answer) == 728
    return answer


def carrier_key(carrier):
    terms = tuple(sorted(
        (term["response_pair"], tuple(term["cross_edges"]))
        for term in carrier["terms"]
    ))
    return carrier["kind"], carrier["cap"], tuple(carrier["defining_sites"]), terms


def map_carrier_key(carrier, permutation):
    cap = label(map_edge(edge(carrier["cap"]), permutation))
    defining = tuple(sorted(permutation[site] for site in carrier["defining_sites"]))
    terms = []
    for term in carrier["terms"]:
        response = label(map_edge(edge(term["response_pair"]), permutation))
        cross = tuple(sorted(label(map_edge(edge(value), permutation)) for value in term["cross_edges"]))
        terms.append((response, cross))
    return carrier["kind"], cap, defining, tuple(sorted(terms))


def term_count_census(carriers):
    census = collections.Counter()
    for carrier in carriers:
        census[(carrier["kind"], carrier["identity_cap"], carrier["response_term_count"])] += 1
    return [
        {"kind": kind, "identity_cap": identity, "response_term_count": count, "carriers": total}
        for (kind, identity, count), total in sorted(census.items())
    ]


def wrapped(value):
    return f"({value})" if "+" in value or ("-" in value[1:]) or value.startswith("-") else value


def product(*values):
    if any(value == "0" for value in values):
        return "0"
    values = [wrapped(value) for value in values if value != "1"]
    return "*".join(values) if values else "1"


def summation(values):
    values = [value for value in values if value != "0"]
    return "+".join(values).replace("+-", "-") if values else "0"


def difference(left, right):
    if right == "0":
        return left
    if left == "0":
        return f"-({right})"
    return f"{left}-({right})"


def entry(block, row, column):
    return f"a{block}_{row}{column}"


REDUCED_BLOCKS = ("04", "06", "07", "13", "14", "17", "25", "26", "35")


def amplitude_expression(word):
    a, b, c, d, e, f, g, h = word
    R = summation(["1" if a == d and e == f else "0", product(entry("04", a, e), entry("35", d, f))])
    S = summation(["1" if b == g and c == h else "0", product(entry("17", b, h), entry("26", c, g))])
    T = summation([entry("13", b, d) if e == f else "0", product(entry("14", b, e), entry("35", d, f))])
    U = summation([entry("06", a, g) if c == h else "0", product(entry("07", a, h), entry("26", c, g))])
    return summation([product(R, S), product(T, U)])


def materialize_full_ideal():
    variables = [entry(block, i, j) for block in REDUCED_BLOCKS for i, j in itertools.product(COLORS, repeat=2)]
    assert len(variables) == len(set(variables)) == 81
    equations = []
    ledger = hashlib.sha256()
    for word in itertools.product(COLORS, repeat=8):
        amplitude_value = amplitude_expression(word)
        target = "1" if len(set(word)) == 1 else "0"
        equation = difference(amplitude_value, target)
        equations.append(equation)
        ledger.update(("".join(map(str, word)) + ":" + equation + "\n").encode())
    assert len(equations) == len(set(equations)) == 6561
    assert all(value not in ("0", "1", "-1") for value in equations)
    program = "\n".join([
        "option(noredefine);",
        f"ring r=0,({','.join(variables)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_VARIABLES="+string(nvars(r)));',
        'print("INPUT_GENERATORS="+string(size(I)));',
        "quit;",
        "",
    ])
    assert "slimgb" not in program and "std(" not in program and "groebner" not in program.lower()
    path = HERE / "canonical_reduced_full_x5_Q.sing"
    temporary = path.with_suffix(".sing.tmp")
    temporary.write_text(program)
    os.replace(temporary, path)
    return {
        "path": path.name,
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "ring": "Q",
        "variables": 81,
        "generators": 6561,
        "matrix_blocks": list(REDUCED_BLOCKS),
        "equation_ledger_sha256": ledger.hexdigest(),
        "solver_commands": 0,
    }


def rank_chart_orbits(rank):
    subsets = tuple(itertools.combinations(COLORS, rank))
    charts = tuple((i, rows, columns) for i in COLORS for rows in subsets for columns in subsets)
    def action(chart, color):
        i, rows, columns = chart
        return color[i], tuple(sorted(color[x] for x in rows)), tuple(sorted(color[x] for x in columns))
    remaining = set(charts)
    orbits = []
    while remaining:
        representative = min(remaining)
        orbit = {action(representative, color) for color in S3}
        assert orbit <= set(charts)
        remaining -= orbit
        orbits.append({"representative": [representative[0], list(representative[1]), list(representative[2])], "size": len(orbit)})
    return {"raw_charts": len(charts), "S3_orbits": len(orbits), "orbit_ledger": orbits}


def validate(result):
    assert result["schema"] == "KRENN_X5_ANCHOR_NO_RECTANGLE_DESIGN_V1"
    assert result["status"] == "PASS_EXACT_ONE_REDUCED_REPRESENTATIVE_RANK_DESIGN_NO_SOLVE"
    assert result["census"] == {
        "records": 4,
        "literal_source_classes": 2,
        "reduced_full_x5_classes": 1,
        "carriers_per_record": 728,
        "word_transport_checks": 4 * 6 * 6561,
        "solver_runs": 0,
    }
    assert result["full_x5_ideal"]["variables"] == 81
    assert result["full_x5_ideal"]["generators"] == 6561
    assert result["selected_rank_design"]["rank0"]["status"] == "CLOSED_BY_ZERO_RESPONSE_MAP"
    assert result["selected_rank_design"]["rank1"]["status"] == "EXACT_INCIDENCE_DESIGN_NOT_SOLVED"
    assert result["selected_rank_design"]["rank2"]["status"] == "EXACT_INCIDENCE_DESIGN_NOT_SOLVED"
    assert result["scope"] == {"mathematically_closed_full_records": 0, "solver_runs": 0, "full_conjecture": False}


def hostile(result, mutation):
    candidate = copy.deepcopy(result)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def main():
    for path, digest in PINS.items():
        assert sha256(path) == digest, (path, sha256(path), digest)
    module = load_parent_module()
    parent = json.loads((PARENT / "results_unmapped16_design.json").read_text())
    records = parent["records"][12:16]
    assert [record["record_index"] for record in records] == [12, 13, 14, 15]
    assert all(record["classification"] == "NO_OUTSIDE_R6_R7_RECTANGLE" for record in records)
    assert all(record["guard_equations"] == [] for record in records)

    matching_cache = {record["record_index"]: supported_matchings(module, record) for record in records}
    assert all(len(value) == 8 for value in matching_cache.values())
    assert all((1, 2) not in matching for value in matching_cache.values() for matching in value)
    for word in itertools.product(COLORS, repeat=8):
        assert amplitude(records[0], matching_cache, word) == factorized_amplitude(word)

    on = [12, 13]
    off = [14, 15]
    literal_matrix = {}
    reduced_matrix = {}
    for source in records:
        literal_matrix[str(source["record_index"])] = {}
        reduced_matrix[str(source["record_index"])] = {}
        for target in records:
            literal_matrix[str(source["record_index"])][str(target["record_index"])] = len(site_maps(source, target))
            reduced_matrix[str(source["record_index"])][str(target["record_index"])] = len(site_maps(source, target, reduced=True))
    assert all(literal_matrix[str(a)][str(b)] == 1 for group in (on, off) for a in group for b in group)
    assert all(literal_matrix[str(a)][str(b)] == 0 for a in on for b in off)
    assert all(literal_matrix[str(a)][str(b)] == 0 for a in off for b in on)
    assert all(reduced_matrix[str(a)][str(b)] == 1 for a in range(12, 16) for b in range(12, 16))

    carrier_ledgers = {}
    carrier_census = {}
    all_by_record = {}
    for record in records:
        carriers = all_carriers(module, record)
        all_by_record[record["record_index"]] = carriers
        two = [carrier["two_sandwich"] for carrier in carriers if carrier["two_sandwich"]]
        assert two == record["two_sandwich_carriers"]
        carrier_ledgers[str(record["record_index"])] = carriers
        carrier_census[str(record["record_index"])] = {
            "all": len(carriers),
            "triangle": sum(value["kind"] == "triangle" for value in carriers),
            "star": sum(value["kind"] == "star" for value in carriers),
            "two_sandwich": len(two),
            "identity_cap_two_sandwich": sum(value["identity_cap"] for value in two),
            "term_count_distribution": term_count_census(carriers),
        }

    word_checks = 0
    for target in records:
        reference = records[0] if target["record_index"] in on else records[2]
        maps = site_maps(reference, target)
        assert len(maps) == 1
        permutation = maps[0]
        target_carrier_keys = {carrier_key(value) for value in all_by_record[target["record_index"]]}
        assert {map_carrier_key(value, permutation) for value in all_by_record[reference["record_index"]]} == target_carrier_keys
        for color in S3:
            for word in itertools.product(COLORS, repeat=8):
                mapped = map_word(word, permutation, color)
                assert map_amplitude(amplitude(reference, matching_cache, word), permutation, color) == amplitude(target, matching_cache, mapped)
                word_checks += 1
    assert word_checks == 4 * 6 * 6561

    canonical = records[0]
    selected = next(
        value for value in canonical["two_sandwich_carriers"]
        if value["kind"] == "star" and value["cap"] == "27" and value["defining_sites"] == [1]
    )
    assert selected["identity_cap"] and selected["common_block"] == "07"
    assert [value["response_pair"] for value in selected["terms"]] == ["05", "06"]
    assert [value["formula"] for value in selected["terms"]] == ["A07*K^T*A25", "A07*K^T*A26"]

    full_ideal = materialize_full_ideal()
    ledger_path = HERE / "all_carriers_ledger.json"
    temporary = ledger_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps({"records": carrier_ledgers}, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, ledger_path)

    rank1_orbits = rank_chart_orbits(1)
    rank2_orbits = rank_chart_orbits(2)
    assert (rank1_orbits["raw_charts"], rank1_orbits["S3_orbits"]) == (27, 5)
    assert (rank2_orbits["raw_charts"], rank2_orbits["S3_orbits"]) == (27, 5)
    rank_design = {
        "canonical_records": [12, 14],
        "mirror_records": [13, 15],
        "canonical_carrier": {
            "cap": "27=A27=I3",
            "kind": "star",
            "center": 1,
            "responses": ["R05=A07*K^T*A25", "R06=A07*K^T*A26"],
            "factorization": "[A25^T|A26^T]*K*A07^T",
            "P": "ColSpan(A25,A26)",
            "Q": "Col(A07^T)=Row(A07)",
            "response_row_space": "P tensor Q",
            "pairing_failure_criterion": "I3 in P tensor Q iff P=Q=Q^3",
            "diagonal_failure_criterion": "Eii in P tensor Q iff e_i in P intersection Q",
        },
        "mirror_carrier": {
            "site_map": [0, 2, 1, 3, 4, 5, 7, 6],
            "cap": "16=A16=I3",
            "kind": "star",
            "center": 2,
            "responses": ["R05=A06*K^T*A15", "R07=A06*K^T*A17"],
            "factorization": "[A15^T|A17^T]*K*A06^T",
        },
        "rank0": {
            "status": "CLOSED_BY_ZERO_RESPONSE_MAP",
            "condition": "A07=0 (mirror A06=0)",
            "proof": "L=0, so ker(L)=M3; trace and each K_ii are nonzero functionals on the kernel.",
        },
        "rank1": {
            "status": "EXACT_INCIDENCE_DESIGN_NOT_SOLVED",
            "factorization": "A07=U*V^T, normalized on a selected nonzero 1-minor",
            "inactivity_equations": ["V*z=e_i", "A25*u+A26*w=e_i"],
            "variables": 85,
            "generators": 6568,
            **rank1_orbits,
        },
        "rank2": {
            "status": "EXACT_INCIDENCE_DESIGN_NOT_SOLVED",
            "factorization": "A07=U*V^T, normalized on a selected nonzero 2-minor",
            "inactivity_equations": ["V*z=e_i", "A25*u+A26*w=e_i"],
            "variables": 89,
            "generators": 6568,
            **rank2_orbits,
        },
        "rank3": {
            "status": "EXACT_SMALLER_IDEAL_NOT_SOLVED",
            "condition": "det(A07)!=0 (mirror det(A06)!=0)",
            "variables": 82,
            "generators": 6562,
            "saturation": "u07*det(A07)-1",
            "remaining_carrier_obligation": "selected star can only help when ColSpan(A25,A26) is proper and contains no standard basis vector; otherwise another carrier or full-X5 identity is required",
        },
    }

    result = {
        "schema": "KRENN_X5_ANCHOR_NO_RECTANGLE_DESIGN_V1",
        "status": "PASS_EXACT_ONE_REDUCED_REPRESENTATIVE_RANK_DESIGN_NO_SOLVE",
        "records": [
            {
                "record_index": value["record_index"],
                "orbit_id": value["orbit_id"],
                "A12_state": "present" if "12" in value["nonzero_variable_blocks"] else "absent",
                "added": value["added"],
                "support": value["support"],
                "supported_matchings": value["supported_matchings"],
                "guards": value["guard_equations"],
                "carrier_census": carrier_census[str(value["record_index"])],
            }
            for value in records
        ],
        "source_symmetry": {
            "literal_classes": [
                {"representative": 12, "members": on},
                {"representative": 14, "members": off},
            ],
            "literal_site_map_counts": literal_matrix,
            "reduced_site_map_counts": reduced_matrix,
            "unique_mirror": [0, 2, 1, 3, 4, 5, 7, 6],
            "simultaneous_color_group_order": 6,
            "A12_distinction": "No literal source/support automorphism crosses A12 present/absent. A12 occurs in no supported perfect matching or selected carrier, so setting A12=I3 or 0 gives one reduced polynomial ideal.",
        },
        "factorization": {
            "canonical_record": 12,
            "formula": "Phi=(delta_ad*delta_ef+A04[a,e]*A35[d,f])*(delta_bg*delta_ch+A17[b,h]*A26[c,g])+(A13[b,d]*delta_ef+A14[b,e]*A35[d,f])*(A06[a,g]*delta_ch+A07[a,h]*A26[c,g])",
            "verified_words": 6561,
            "transported_word_checks": word_checks,
        },
        "full_x5_ideal": full_ideal,
        "all_carriers_ledger": {"path": ledger_path.name, "sha256": sha256(ledger_path)},
        "selected_rank_design": rank_design,
        "census": {
            "records": 4,
            "literal_source_classes": 2,
            "reduced_full_x5_classes": 1,
            "carriers_per_record": 728,
            "word_transport_checks": word_checks,
            "solver_runs": 0,
        },
        "pins": {str(path.relative_to(ROOT)): digest for path, digest in PINS.items()},
        "scope": {"mathematically_closed_full_records": 0, "solver_runs": 0, "full_conjecture": False},
    }
    validate(result)
    tests = {
        "source_class_collapse": hostile(result, lambda value: value["census"].__setitem__("literal_source_classes", 1)),
        "rank1_solve_overclaim": hostile(result, lambda value: value["selected_rank_design"]["rank1"].__setitem__("status", "CLOSED")),
        "rank0_underclaim": hostile(result, lambda value: value["selected_rank_design"]["rank0"].__setitem__("status", "OPEN")),
        "solver_injection": hostile(result, lambda value: value["scope"].__setitem__("solver_runs", 1)),
        "conjecture_overclaim": hostile(result, lambda value: value["scope"].__setitem__("full_conjecture", True)),
    }
    assert all(tests.values())
    result["hostile_tests"] = tests
    output = HERE / "results_anchor_no_rectangle_design.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({"status": result["status"], "records": 4, "reduced_representatives": 1, "solver_runs": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
