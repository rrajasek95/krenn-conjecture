#!/usr/bin/env python3
"""Exact support-only eight-block census and first finite induction interface."""

from __future__ import annotations

from collections import Counter
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SEVEN_DIR = REPO / "computations/unaudited-codex-n8-x5-seven-block-support-boundary-2026-08-25"
SEVEN_MANIFEST = SEVEN_DIR / "MANIFEST.sha256"
SEVEN_RESULT = SEVEN_DIR / "results_seven_block_support_boundary.json"
SEVEN_SOURCE = SEVEN_DIR / "audit_seven_block_support_boundary.py"
PINS = {
    "seven_manifest": (SEVEN_MANIFEST, "13bb284c0b400f7227db74f8a135155dd324251147ebf48711b9af8d10adcc85"),
    "seven_result": (SEVEN_RESULT, "b3951e07149e4b831a5d3d3548284afb27f04154d805585468ba69bdb09b2f19"),
    "seven_source": (SEVEN_SOURCE, "ad86e6d474eb1ffb3bfd43b0bd6155a7d1f592651e80ba91b37e9df1409941c5"),
    "six_manifest": (REPO / "computations/unaudited-codex-n8-x5-six-block-support-cap-2026-08-25/MANIFEST.sha256", "fcfc7f972dfb0ed6c7d9cffdc6e2ce552ebad68ae1bc0af121df1455029327b7"),
    "five_source": (REPO / "computations/unaudited-codex-n8-x5-five-block-support-cap-2026-08-25/audit_five_block_support_cap.py", "4a686fe5bbf80559283d993245166764d5b52d8b4bd33b144017f26f5f2c1f45"),
}


def require(condition, detail="validation failure"):
    if not condition:
        raise ValueError(detail)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


for name, (path, expected) in PINS.items():
    require(path.is_file(), (name, "missing"))
    require(sha(path) == expected, (name, sha(path), expected))

spec = importlib.util.spec_from_file_location("seven_block_pinned", SEVEN_SOURCE)
require(spec is not None and spec.loader is not None, "cannot import pinned classifier")
seven = importlib.util.module_from_spec(spec)
spec.loader.exec_module(seven)
five = seven.five


def es(edge):
    return five.edge_string(edge)


def stored_product_terms(support, cap, response):
    """Return source-edge pairs contributing to a response matrix."""
    p, q = cap
    a, b = response
    terms = []
    direct = (tuple(sorted((p, a))), tuple(sorted((q, b))))
    switched = (tuple(sorted((p, b))), tuple(sorted((q, a))))
    if all(edge in support for edge in direct):
        terms.append({"kind": "direct", "source_edges": list(map(es, direct))})
    if all(edge in support for edge in switched):
        terms.append({"kind": "switched", "source_edges": list(map(es, switched))})
    return terms


def carrier_term_count(support, cap, kind, defining):
    residual = tuple(site for site in range(8) if site not in cap)
    pairs = tuple(itertools.combinations(residual, 2))
    if kind == "triangle":
        allowed = set(itertools.combinations(defining, 2))
    else:
        center = defining[0]
        allowed = {edge for edge in pairs if center in edge}
    forbidden = [edge for edge in pairs if edge not in allowed]
    return sum(len(stored_product_terms(support, cap, edge)) for edge in forbidden)


def minimum_carrier_load(support):
    records = []
    for cap in sorted(support):
        residual = tuple(site for site in range(8) if site not in cap)
        for tri in itertools.combinations(residual, 3):
            records.append((carrier_term_count(support, cap, "triangle", tri), "triangle", es(cap), tri))
        for center in residual:
            records.append((carrier_term_count(support, cap, "star", (center,)), "star", es(cap), (center,)))
    minimum = min(record[0] for record in records)
    return minimum, sum(record[0] == minimum for record in records), len(records)


def matching_strings(support):
    return ["|".join(map(es, matching)) for matching in five.core.PM8 if set(matching) <= support]


def expand_factorization(groups):
    """Expand a sum of products of sums at the edge-label level."""
    result = []
    for product in groups:
        partial = [()]
        for alternatives in product:
            partial = [tuple(sorted(prefix + tuple(term))) for prefix in partial for term in alternatives]
        result.extend(partial)
    return sorted(result)


def factorization_for(representative):
    text = {es(edge) for edge in representative}
    common = [
        [[("01", "35"), ("03", "15")], [("26", "47"), ("27", "46")]],
        [[("03", "17", "26", "45")]],
    ]
    if "06" in text:
        common.insert(1, [[("06", "23")], [("15", "47"), ("17", "45")]])
        formula = "(A01*A35 + A03*A15)*(A26*A47 + A27*A46) + A06*A23*(A15*A47 + A17*A45) + A03*A17*A26*A45 = 0"
    else:
        require("07" in text, "expected 06/07 minimal split")
        common.insert(1, [[("07", "23")], [("15", "46"), ("16", "45")]])
        formula = "(A01*A35 + A03*A15)*(A26*A47 + A27*A46) + A07*A23*(A15*A46 + A16*A45) + A03*A17*A26*A45 = 0"
    # Convert strings to sorted edge tuples and replay all seven alternatives.
    normalized = []
    for product in common:
        normalized.append([[tuple(term) for term in alternatives] for alternatives in product])
    expanded = expand_factorization(normalized)
    return {"display": formula, "factor_groups": common, "expanded_matching_edges": [list(x) for x in expanded]}


def selected_carrier(representative):
    text = {es(edge) for edge in representative}
    if "06" in text:
        return {
            "cap": "01", "kind": "star", "center": 3,
            "forbidden_nonzero_responses": [
                {"response": "56", "raw_formula": "R56=A15^T*K^T*A06", "equivalent_output": "R56^T=A06^T*K*A15"},
                {"response": "67", "raw_formula": "R67=A06^T*K*A17", "equivalent_output": "R67=A06^T*K*A17"},
            ],
            "two_sandwich": "L(K)=(A06^T*K*A15, A06^T*K*A17)",
            "U": "A06", "B1": "A15", "B2": "A17", "cap_block": "A01",
        }
    return {
        "cap": "01", "kind": "star", "center": 3,
        "forbidden_nonzero_responses": [
            {"response": "57", "raw_formula": "R57=A15^T*K^T*A07", "equivalent_output": "R57^T=A07^T*K*A15"},
            {"response": "67", "raw_formula": "R67=K^T*A07", "equivalent_output": "R67^T=A07^T*K*A16=A07^T*K"},
        ],
        "two_sandwich": "L(K)=(A07^T*K*A15, A07^T*K*A16)",
        "U": "A07", "B1": "A15", "B2": "A16=I3", "cap_block": "A01",
    }


def make_result():
    parent = json.loads(SEVEN_RESULT.read_text())
    require(parent["scope"]["zero_through_six_layers_closed"] is True)
    require(parent["scope"]["unresolved_seven_block_structural_strata"] == 64)

    additions = tuple(itertools.combinations(five.OFF_FAMILY, 8))
    fixed_count = 0
    evaders = []
    for added in additions:
        if five.fixed_cap_certificate(set(five.FAMILY) | set(added)) is None:
            evaders.append(added)
        else:
            fixed_count += 1
    reduction = Counter()
    stable = []
    for added in evaders:
        reduced, _steps = five.guard_reduce(added)
        reduction[len(reduced)] += 1
        if len(reduced) == 8:
            stable.append(added)
    require(len(additions) == 125970)
    require(fixed_count == 66752 and len(evaders) == 59218)
    require(dict(sorted(reduction.items())) == {2: 9, 3: 754, 4: 7104, 5: 20092, 6: 21307, 7: 8684, 8: 1268})

    seven_unresolved = set()
    for orbit in parent["exact_variable_stratum_classification"]["unresolved_orbit_records"]:
        for record in orbit["members"]:
            added = tuple(tuple(map(int, edge)) for edge in record["added"])
            variables = frozenset(tuple(map(int, edge)) for edge in record["nonzero_variable_blocks"])
            seven_unresolved.add((added, variables))
    require(len(seven_unresolved) == 64)

    variable_order = tuple(sorted(five.VARIABLE))
    census = Counter()
    unresolved = []
    classification_records = []
    for added in stable:
        for mask in range(16):
            variables = frozenset(variable_order[i] for i in range(4) if mask & (1 << i))
            support = set(five.FIXED) | set(variables) | set(added)
            if five.fixed_cap_certificate(support) is not None:
                kind = "fixed_identity_cap"
            elif seven.nonidentity_certificates(support):
                kind = "nonidentity_hyperplane_cap"
            else:
                kind = "unresolved_coefficient_locus"
            census[kind] += 1
            classification_records.append((added, variables, kind))
            if kind == "unresolved_coefficient_locus":
                unresolved.append((added, variables, support))
    require(census == {"fixed_identity_cap": 16427, "nonidentity_hyperplane_cap": 3245, "unresolved_coefficient_locus": 616})

    records = []
    parent_count_census = Counter()
    for added, variables, support in unresolved:
        parents = []
        for edge in added:
            parent_added = tuple(x for x in added if x != edge)
            if (parent_added, variables) in seven_unresolved:
                parents.append({"deleted_edge": es(edge), "seven_added": list(map(es, parent_added))})
        parent_count_census[len(parents)] += 1
        matches = matching_strings(support)
        minimum, minimizers, carriers = minimum_carrier_load(support)
        records.append({
            "added": list(map(es, added)),
            "nonzero_variable_blocks": list(map(es, sorted(variables))),
            "supported_perfect_matchings": matches,
            "supported_matching_count": len(matches),
            "total_supported_response_edge_load": sum(len(five.response_edges(support, *cap)) for cap in sorted(support)),
            "seven_unresolved_parents": parents,
            "minimum_forbidden_response_product_terms": minimum,
            "minimum_carrier_count": minimizers,
            "supported_cap_triangle_star_carriers": carriers,
        })
    require(parent_count_census == {0: 104, 1: 472, 2: 40})

    # Exact order-two guard symmetry.
    unresolved_keys = {(added, variables) for added, variables, _support in unresolved}
    seen = set()
    orbits = []
    for added, variables, _support in sorted(unresolved, key=lambda x: (x[0], sorted(x[1]))):
        key = (added, variables)
        if key in seen:
            continue
        mate = (five.permute_support(added), seven.permute_variables(variables))
        require(mate in unresolved_keys, ("missing mate", key))
        members = tuple(sorted({key, mate}, key=lambda x: (x[0], sorted(x[1]))))
        seen.update(members)
        orbits.append(members)
    require(len(orbits) == 308 and Counter(map(len, orbits)) == {2: 308})

    new_records = [record for record in records if not record["seven_unresolved_parents"]]
    require(len(new_records) == 104)
    smallest_key = min((r["supported_matching_count"], len(r["nonzero_variable_blocks"]), r["total_supported_response_edge_load"]) for r in new_records)
    require(smallest_key == (8, 1, 66))
    smallest = [r for r in new_records if (r["supported_matching_count"], len(r["nonzero_variable_blocks"]), r["total_supported_response_edge_load"]) == smallest_key]
    require(len(smallest) == 4)

    # Two guard-symmetry representatives among the four smallest records.
    smallest_keys = {(tuple(tuple(map(int, e)) for e in r["added"]), frozenset(tuple(map(int, e)) for e in r["nonzero_variable_blocks"])) for r in smallest}
    small_seen = set()
    minimal_orbits = []
    for key in sorted(smallest_keys, key=lambda x: (x[0], sorted(x[1]))):
        if key in small_seen:
            continue
        mate = (five.permute_support(key[0]), seven.permute_variables(key[1]))
        require(mate in smallest_keys)
        members = tuple(sorted({key, mate}, key=lambda x: (x[0], sorted(x[1]))))
        small_seen.update(members)
        representative = members[0]
        support = set(five.FIXED) | set(representative[1]) | set(representative[0])
        matches = matching_strings(support)
        require(matches[4] == "03|16|27|45", ("base matching position", matches))
        alternatives = sorted(tuple(sorted(m.split("|"))) for m in matches if m != "03|16|27|45")
        factor = factorization_for(representative[0])
        require([tuple(x) for x in factor["expanded_matching_edges"]] == alternatives, (factor, alternatives))
        carrier = selected_carrier(representative[0])
        response_terms = {}
        cap = tuple(map(int, carrier["cap"]))
        for response in carrier["forbidden_nonzero_responses"]:
            edge = tuple(map(int, response["response"]))
            response_terms[response["response"]] = stored_product_terms(support, cap, edge)
        require(all(len(v) == 1 for v in response_terms.values()))
        minimal_orbits.append({
            "orbit": len(minimal_orbits),
            "members": [{"added": list(map(es, a)), "variables": list(map(es, sorted(v)))} for a, v in members],
            "representative_support": list(map(es, sorted(support))),
            "fixed_blocks": ["03=I3", "16=I3", "27=I3", "45=I3"],
            "nonfixed_nonzero_blocks": [e for e in map(es, sorted(support)) if e not in {"03", "16", "27", "45"}],
            "supported_perfect_matchings": matches,
            "full_x5_reduction": {
                "base_matching": "03|16|27|45",
                "base_equals_normalized_GHZ": False,
                "base_word_support": 81,
                "pure_words": 3,
                "mixed_base_words": 78,
                "remaining_equation": "the sum of the seven alternative matching tensors equals GHZ minus the four-pair equality base tensor; RHS is -1 on the 78 mixed base words and zero elsewhere",
                "entry_convention": "matching m contributes product_{uv in m} Auv[c_u,c_v] to word c in {0,1,2}^8",
                "factorization": factor,
                "scalar_equations": 6561,
                "monomials_per_equation_at_most": 7,
            },
            "selected_two_response_carrier": carrier,
            "source_product_terms": response_terms,
            "finite_exact_decision": {
                "logic": "all four failure branches must be empty over Q to prove this selected star active for every full-X5 source on the support",
                "nonzero_encoding": "for each of the nine nonfixed blocks A, add nine witnesses w and equation sum_ij w_ij*A_ij=1",
                "pairing_failure": "A01=U*X*B1^T+U*Y*B2^T",
                "diagonal_failure_i": "U*x=e_i and B1*y+B2*z=e_i, separately for i=0,1,2",
                "pairing_failure_variables": 180,
                "pairing_failure_generators": 6579,
                "each_diagonal_failure_variables": 171,
                "each_diagonal_failure_generators": 6576,
                "systems_per_orbit": 4,
                "orbit_count": 2,
                "total_exact_Q_systems": 8,
                "acceptance": "literal unit-ideal certificates over Q for all eight systems, with source-word replay",
                "nonunit_scope": "a rational point witnesses failure of this selected carrier only; it is not a conjecture counterexample unless every carrier/guard/source condition is checked",
            },
        })
    require(len(minimal_orbits) == 2)

    compact_records = sorted(records, key=lambda r: (r["added"], r["nonzero_variable_blocks"]))
    return {
        "schema": "KRENN_X5_EIGHT_BLOCK_FIRST_INDUCTION_INTERFACE_V1",
        "status": "PASS_EXACT_EIGHT_BLOCK_CENSUS_FINITE_MINIMAL_INTERFACE_NO_SOLVE",
        "pins": {name: {"path": str(path.relative_to(REPO)), "sha256": expected} for name, (path, expected) in PINS.items()},
        "enumeration": {
            "eight_added_supports": len(additions),
            "fixed_identity_closed": fixed_count,
            "fixed_identity_evaders": len(evaders),
            "guard_reduced_size_census": {str(k): v for k, v in sorted(reduction.items())},
            "stable_eight_supports": len(stable),
            "stable_variable_strata": len(stable) * 16,
            "classification_census": dict(census),
            "unresolved_strata": len(unresolved),
            "unresolved_guard_symmetry_orbits": len(orbits),
            "unresolved_parent_count_census": {str(k): v for k, v in sorted(parent_count_census.items())},
            "unresolved_with_no_seven_unresolved_parent": len(new_records),
            "unresolved_no_parent_supports": len({tuple(r["added"]) for r in new_records}),
            "classification_sha256": hashlib.sha256(json.dumps([(list(map(es, a)), list(map(es, sorted(v))), k) for a, v, k in classification_records], sort_keys=True).encode()).hexdigest(),
            "unresolved_records_sha256": hashlib.sha256(json.dumps(compact_records, sort_keys=True).encode()).hexdigest(),
        },
        "first_unproved_induction_interface": {
            "negative_monotonicity_result": "104 unresolved eight-block strata have no unresolved seven-block deletion parent, so closing the 64 seven-block loci alone cannot prove the eight-block layer by deletion monotonicity",
            "smallest_new_rank_key": list(smallest_key),
            "smallest_new_records": 4,
            "smallest_new_guard_orbits": 2,
            "minimal_orbits": minimal_orbits,
        },
        "unconditional_two_sandwich_activity_lemma": {
            "statement": (
                "Over Q, for L(K)=(U^T*K*B1,U^T*K*B2), put "
                "P=Col(U), Q=ColSpan(B1,B2), W=P tensor Q=im(L^*). "
                "There exists K in ker(L) with K00,K11,K22 and <K,C> all nonzero "
                "iff E00,E11,E22,C are all outside W."
            ),
            "proof": [
                "Trace cyclicity gives im(L^*)={U*X*B1^T+U*Y*B2^T}=P tensor Q.",
                "A functional f is identically zero on ker(L) iff f belongs to im(L^*).",
                "If all four functionals are nonzero on ker(L), their four kernels are proper hyperplanes.",
                "A finite union of proper linear hyperplanes cannot cover the Q-vector space ker(L), so one K avoids all four.",
                "The converse is immediate from evaluating such a K.",
            ],
            "orbit0_specialization": {
                "U": "A06", "Q": "ColSpan(A15,A17)",
                "activity_test": "A01 notin Col(A06) tensor ColSpan(A15,A17), and no e_i lies in both column spaces",
            },
            "orbit1_specialization": {
                "U": "A07", "Q": "Q^3 because B2=A16=I3",
                "activity_test": "Col(A01) is not contained in Col(A07), and no standard basis vector e_i lies in Col(A07)",
            },
            "historical_sparse_certificate_required": False,
            "scope": "unconditional linear-algebra reduction of the selected carrier; it does not prove the full-X5 equations force the four nonincidences",
        },
        "unresolved_records": compact_records,
        "scope": {
            "support_and_source_provenance_only": True,
            "heavy_solver_runs": 0,
            "singular_runs": 0,
            "d12_reads": 0,
            "eight_block_layer_closed": False,
            "seven_block_rep2_rep5_independent": True,
            "full_conjecture_claim": False,
        },
    }


def atomic_json(path, data):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    os.replace(tmp, path)


def main():
    result = make_result()
    atomic_json(HERE / "results_eight_block_interface.json", result)
    print(json.dumps({"status": result["status"], **{k: result["enumeration"][k] for k in ("eight_added_supports", "stable_eight_supports", "unresolved_strata", "unresolved_guard_symmetry_orbits", "unresolved_with_no_seven_unresolved_parent")}}, sort_keys=True))


if __name__ == "__main__":
    main()
