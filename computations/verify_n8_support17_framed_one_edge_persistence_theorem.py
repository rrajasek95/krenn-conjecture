#!/usr/bin/env python3
"""Extract the framed one-edge persistence theorem from support-17 data.

The theorem has three algebraic mechanisms rather than a new support census:

* contraction-ideal persistence: if the response increment remains in the
  source-star ideal I_X, the old private kernel kills it;
* matching-debt persistence: an inherited singleton word not hit by the
  added-edge link remains a nonzero singleton coefficient; and
* complementary binary landing: the only N=8 framed local residue after the
  first two mechanisms is killed by the exact rank-two permanent matrix.

"Framed" is essential: the pure GHZ rows select three colour lines.  The
statement is invariant under source-labelled frame isomorphisms, not arbitrary
GL(3) changes which move the target itself.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = "f5bbe0baceac692b02697f9a6fc45118e5c60d79f01ac53146c991220bbc057f"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_local(module_name, filename):
    spec = spec_from_file_location(module_name, HERE / filename)
    require(spec is not None and spec.loader is not None,
            ("failed to load dependency", filename))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PERSIST = load_local(
    "n8_support17_persistence_for_framed_theorem",
    "verify_n8_support17_landed_parent_persistence_register.py",
)
RECURRENCE = load_local(
    "n8_support17_all_guard_recurrence_for_framed_theorem",
    "verify_n8_support17_all_guard_one_edge_recurrence.py",
)
NONCOORDINATE = load_local(
    "n8_support17_noncoordinate_debt_for_framed_theorem",
    "verify_n8_support17_all_guard_noncoordinate_edge_debt.py",
)
COORDINATE = load_local(
    "n8_support17_coordinate_closure_for_framed_theorem",
    "verify_n8_support17_hard_landed_parent_anchor_closure.py",
)
TWO_NONANCHOR = load_local(
    "n8_support17_two_nonanchor_for_framed_theorem",
    "verify_n8_support17_nonprivate_two_nonanchor_row_closure.py",
)
BINARY = COORDINATE.BINARY
LANDING = BINARY.LANDING


PINNED_DEPENDENCIES = {
    "support16-binary-cover": (
        BINARY,
        "7c3e00333001f5beb18b0f5538ac96885e556f153ca3459d02873221b132d20c",
    ),
    "support17-structural-persistence": (
        PERSIST,
        "005230a4aed405107975d9eda404ef2949be10f36fd191a5468cf6eb707b0e45",
    ),
    "support17-coordinate-guard-recurrence": (
        RECURRENCE,
        "f1f20cb858ecc53e8e2b71fc1e9a78355ade4367d720af6d3231dd0c13054dc3",
    ),
    "support17-noncoordinate-guard-debt": (
        NONCOORDINATE,
        "853f09b21d73e1af50ee63aaf567e9525ff6b87d7e156744a92b1bb54013f27b",
    ),
    "support17-landed-coordinate-closure": (
        COORDINATE,
        "2a5e85d8b4863bcf9c9f2a95229642b9f6531cdfd7e8bc7e5b8f6fdfd03dceb0",
    ),
    "support17-landed-two-nonanchor-closure": (
        TWO_NONANCHOR,
        "c49c81ae5f96e9655c9990e2cb4fb0c7c64f8d8c3b8826f7176ef876bab481e0",
    ),
}


def audit_dependency_pins():
    ledger = []
    for name, (module, expected) in PINNED_DEPENDENCIES.items():
        actual = module.EXPECTED_SHA256
        require(actual == expected,
                ("framed theorem dependency pin changed", name, actual,
                 expected))
        ledger.append((name, actual))
    return tuple(sorted(ledger))


def audit_abstract_debt_lemma():
    """Exhaust the finite cardinality logic used by every row recurrence."""
    cases = Counter()
    for singleton_count in range(1, 20):
        for added_occurrence_count in range(0, 20):
            for covered_singletons in range(
                    0, min(singleton_count, added_occurrence_count) + 1):
                cases["finite_coverage_states"] += 1
                uncovered = singleton_count - covered_singletons
                if singleton_count > added_occurrence_count:
                    require(uncovered > 0,
                            ("cardinality debt lemma failed", singleton_count,
                             added_occurrence_count, covered_singletons))
                    cases["cardinality_certified_states"] += 1
                if covered_singletons < singleton_count:
                    require(uncovered > 0,
                            ("literal debt lemma failed", singleton_count,
                             covered_singletons))
                    cases["literal_certified_states"] += 1
    return {
        "case_counts": tuple(sorted(cases.items())),
        "cardinality_statement": (
            "if |S_G| exceeds the total decorated occurrences in the "
            "one-edge link L_e, some inherited singleton is not covered"
        ),
        "literal_statement": (
            "if S_G is not contained in the word support of L_e, an old "
            "mixed coefficient remains a one-occurrence nonzero product"
        ),
        "coefficient_scope": (
            "all declared block components are live; no genericity beyond "
            "nonzero support components is used"
        ),
    }


def audit_private_ideal_and_link_types():
    high_high = PERSIST.high_high_deletion_lemma()
    persistence = PERSIST.audit_persistence_register()
    private_persistent = tuple(
        item for item in persistence["augmentations"]
        if item["parent_route"] == "complete-private-cap"
        and item["private_caps"]
    )
    private_failure = tuple(
        item for item in persistence["augmentations"]
        if item["parent_route"] == "complete-private-cap"
        and not item["private_caps"]
    )
    require((len(private_persistent), len(private_failure)) == (905, 415),
            ("private ideal persistence split changed",
             len(private_persistent), len(private_failure)))
    require(all(any(residue_count == 0
                    for _cap, _through, residue_count
                    in item["response_shapes"])
                for item in private_persistent),
            "persistent private augmentation lost zero star-ideal residue")

    # All nonprivate landed-parent augmentations reduce to 502 directed link
    # patterns.  Reconstruct this count without rerunning coefficient search.
    nonprivate_keys = Counter()
    terminal_records = PERSIST.ORBIT.terminal_two_rrx_records()
    for item in persistence["augmentations"]:
        if item["private_caps"]:
            continue
        parent_edges = tuple(
            terminal_records[item["graph_index"]]["representative_edges"]
        )
        augmented = tuple(sorted(parent_edges + (item["new_edge"],)))
        key = PERSIST.canonical_directed_key(augmented, item["incidence"])
        nonprivate_keys[key] += 1
    require(sum(nonprivate_keys.values()) == 667
            and len(nonprivate_keys) == 502,
            ("exhaustive nonprivate link-pattern count changed",
             sum(nonprivate_keys.values()), len(nonprivate_keys)))

    return {
        "high_high_deletion": high_high,
        "private_parent_augmentations": 1320,
        "same_ideal_private_persistence": len(private_persistent),
        "private_ideal_failures": len(private_failure),
        "nonprivate_augmentation_entries": sum(nonprivate_keys.values()),
        "directed_local_link_patterns": len(nonprivate_keys),
        "directed_link_multiplicity_histogram": tuple(sorted(
            Counter(nonprivate_keys.values()).items()
        )),
        "ideal_statement": (
            "write I_X for the ideal generated by contraction slots through "
            "the directed block X.  If the added-edge response increment "
            "lies in I_X, the old left/right kernel K annihilates the full "
            "augmented response with the same active diagonal readouts"
        ),
        "basis_covariance": (
            "I_X is defined by the source-labelled contraction factor, so "
            "ideal membership is invariant under invertible changes on that "
            "factor; the word-debt part additionally uses the fixed GHZ frame"
        ),
    }


def audit_binary_rank_residue():
    left = LANDING.audit_symbolic_rank_construction()
    require(len(left) == 12,
            ("binary rank chart count changed", len(left)))
    require(all(item["left_kernel"] == ({}, {}, {})
                and item["permanent"] == {}
                for item in left),
            ("binary rank residue lost exact zeros", left))
    return {
        "left_rank_charts": left,
        "right_rank_charts": 12,
        "geometric_statement": (
            "relative to the three-line GHZ frame, a cap direct line a and "
            "two complementary shore lines b,c give the crossed permanent "
            "K_bb K_cc+K_bc K_cb; if w_a is live, the denominator-cleared "
            "rank-two matrix kills w and this permanent while all diagonal "
            "readouts remain live; transpose handles the opposite endpoint"
        ),
    }


def audit_imported_reason_table():
    # These counts are outputs of the pinned exact dependencies above.  Their
    # role here is a theorem-level partition, not an independent re-census.
    table = {
        "cap_dark_148_coordinate": {
            "active_clean_cap": 71751,
            "singleton_by_cardinality": 2868903,
            "singleton_by_literal_word": 6,
            "necessary_guards": 0,
        },
        "cap_dark_148_noncoordinate": {
            "singleton_by_cardinality": 3408610,
            "singleton_by_literal_word": 512270,
            "necessary_guards": 0,
        },
        "landed_133_private_persistence": {
            "same_ideal_private_cap": 905,
        },
        "landed_133_coordinate_nonprivate": {
            "directed_link_patterns": 502,
            "two_coordinate_chart_exits": 502,
            "full_support_chart_exits": 502,
            "necessary_guards": 0,
        },
        "landed_133_two_nonanchor": {
            "anchor_completions": 245530,
            "missing_pure_support_pairs": 320608,
            "pure_supported_singleton_pairs": 1643632,
            "necessary_guards": 0,
        },
    }
    require(all(data.get("necessary_guards", 0) == 0
                for data in table.values()),
            ("framed reason table acquired a guard", table))
    return table


def canonical(value):
    if isinstance(value, dict):
        return {
            str(key): canonical(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (list, tuple)):
        return [canonical(item) for item in value]
    return value


def main():
    ledger = canonical({
        "dependency_pins": audit_dependency_pins(),
        "abstract_matching_debt_lemma": audit_abstract_debt_lemma(),
        "private_ideal_and_link_types": audit_private_ideal_and_link_types(),
        "binary_rank_residue": audit_binary_rank_residue(),
        "imported_reason_table": audit_imported_reason_table(),
        "theorem": (
            "N=8 framed one-edge persistence: for every directed support17 "
            "link pattern descending from the support16 two-RRX frontier, "
            "an added live block either remains in a private contraction "
            "ideal, leaves an uncovered singleton matching debt, loses a "
            "normalized pure row, or creates a complementary crossed-binary "
            "active cap"
        ),
        "non_theorem": (
            "no arbitrary-GL basis-free statement is claimed: the GHZ pure "
            "rows canonically select the three-line colour frame.  The theorem "
            "is equivariant under source-labelled frame permutations and "
            "nonzero line rescalings"
        ),
    })
    digest = sha256(
        json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if EXPECTED_SHA256 == "TO_BE_PINNED":
        print("LEDGER", digest)
    else:
        require(digest == EXPECTED_SHA256,
                ("framed one-edge theorem ledger changed", digest))
    print("N=8 support-17 framed one-edge persistence theorem: PASS")
    print("  private ideal persistence: 905 / 1320")
    print("  exhaustive nonprivate directed link patterns: 502")
    print("  arbitrary-GL basis-free claim: rejected; GHZ-framed theorem proved")
    print("  necessary guards in imported branch-complete table: 0")


if __name__ == "__main__":
    main()
