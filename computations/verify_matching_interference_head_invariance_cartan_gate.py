#!/usr/bin/env python3
"""Same-word matching interference cannot repair a local head quotient.

Every perfect-matching monomial in the coefficient of an output word w has
local endpoint colour w_v at site v.  Changing the matching skeleton, its
tail, or its signed holonomy therefore never creates a transverse local
head.  A word-changing Cartan/root comparison is the first possible source
of such a direction.  This checker freezes that exhaustive combinatorial
fact and replays the exact Schur and physical Cartan interfaces.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_oo_zero_holonomy_schur_interference_reduction.py":
        "1e96bf98e997e55d2b050de6c56e7f597cd507737aefa6386296c44adab03631",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_post_ks_same_head_rank_support_counterguard.py":
        "21ebd9d48fed3bc91af820bc84b37bd5133971e519d60fb1d0727de4a4acec3e",
    "computations/verify_uniform_bidirectional_private_site_fan_rank_boundary.py":
        "c4e175ca053cd98e788cca1a38a1851e708e7e47a9ea5745ef4ac6e303ddfd40",
}
EXPECTED_LEDGER_SHA256 = (
    "7fd4e54f63e0b2c27a623dc0b544392e4cd70cad84b8a6dc8cc296121fd6b443"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency: {relative}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    left = vertices[0]
    for index in range(1, len(vertices)):
        right = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(left, right),) + tail))


def local_decorated_cell(matching, word, site):
    for left, right in matching:
        if left == site:
            return (left, right, word[left], word[right])
        if right == site:
            return (right, left, word[right], word[left])
    raise RuntimeError("matching does not cover the site")


def audit_fixed_word_head_invariance():
    sites = tuple(range(8))
    matchings = tuple(perfect_matchings(sites))
    require(len(matchings) == 105, "the N=8 matching count changed")

    words = 0
    matching_occurrences = 0
    local_occurrences = 0
    local_head_histogram = Counter()
    for word in product(range(3), repeat=8):
        words += 1
        for matching in matchings:
            matching_occurrences += 1
            for site in sites:
                cell = local_decorated_cell(matching, word, site)
                require(cell[2] == word[site],
                        "a same-word matching changed its local head")
                local_head_histogram[(site, word[site])] += 1
                local_occurrences += 1

    require(words == 3 ** 8
            and matching_occurrences == 3 ** 8 * 105
            and local_occurrences == 3 ** 8 * 105 * 8,
            "the exhaustive same-word census changed")
    require(set(local_head_histogram.values()) == {3 ** 7 * 105},
            "the site/head multiplicities changed")
    return {
        "words": words,
        "perfect_matchings_per_word": len(matchings),
        "matching_occurrences": matching_occurrences,
        "site_matching_occurrences": local_occurrences,
        "site_head_multiplicity": 3 ** 7 * 105,
        "theorem": (
            "for fixed output word w and site v, every matching occurrence "
            "has local head w_v.  Any linear combination of same-word "
            "matching rows, common-tail exchanges, SCC potentials, or "
            "signed holonomy relations has zero projection to every local "
            "head quotient transverse to e_(w_v)"
        ),
    }


def audit_word_change_transversality():
    changes = 0
    for word in product(range(3), repeat=8):
        for site in range(8):
            old = word[site]
            for new in range(3):
                if new == old:
                    continue
                changed = list(word)
                changed[site] = new
                require(changed[site] != old,
                        "a root move failed to change the local head")
                require(all(changed[index] == word[index]
                            for index in range(8) if index != site),
                        "a one-site root move changed another site")
                changes += 1
    require(changes == 3 ** 8 * 8 * 2,
            "the one-site word-change count changed")
    return {
        "ordered_one_site_root_changes": changes,
        "local_head_rank": 2,
        "interpretation": (
            "a source-provenant root/Cartan comparison is the first "
            "operation in the current proof that can be visible in a "
            "deficient local-head quotient"
        ),
    }


def audit_pinned_interfaces(schur, cartan, rank_guard, bidirectional):
    schur_cycles = [schur.audit_cycle(size) for size in (4, 6, 8)]
    require(all(record["rank"] == record["size"] - 1
                and record["every_coordinate_test_nonzero"]
                for record in schur_cycles),
            "the Schur interference interface changed")

    cartan_ledger = cartan.audit()
    require(cartan_ledger["literal_root_covariance"]["matching_terms_checked"]
            == 787320,
            "the physical Cartan covariance census changed")
    require(cartan_ledger["target_defect"]["endpoint_odd_target"] == 0,
            "the endpoint-odd Cartan target cancellation changed")

    quotient = rank_guard.audit_deleted_star_quotient_classification()
    require(quotient["same_head_profile"] == [2, 2, 3, 3]
            and quotient["double_transverse_profile"] == [3, 3, 3, 3],
            "the transverse quotient classification changed")

    typing = bidirectional.audit_bidirectional_typing()
    require(typing["type_count"] == 6,
            "the bidirectional off-diagonal typing changed")
    return {
        "zero_holonomy_schur_cycles": schur_cycles,
        "physical_cartan": {
            "root_matching_terms": cartan_ledger[
                "literal_root_covariance"]["matching_terms_checked"],
            "endpoint_odd_target": cartan_ledger[
                "target_defect"]["endpoint_odd_target"],
            "scope": cartan_ledger["scope"],
        },
        "rank_quotient": quotient,
        "bidirectional_types": typing["type_count"],
    }


def main():
    pin_dependencies()
    schur = load(
        "computations/verify_oo_zero_holonomy_schur_interference_reduction.py",
        "head_invariance_schur",
    )
    cartan = load(
        "computations/verify_h3_physical_cartan_source_orbit_descent.py",
        "head_invariance_cartan",
    )
    rank_guard = load(
        "computations/verify_h3_post_ks_same_head_rank_support_counterguard.py",
        "head_invariance_rank_guard",
    )
    bidirectional = load(
        "computations/verify_uniform_bidirectional_private_site_fan_rank_boundary.py",
        "head_invariance_bidirectional",
    )

    ledger = {
        "pins": PINS,
        "fixed_word_head_invariance": audit_fixed_word_head_invariance(),
        "word_change_transversality": audit_word_change_transversality(),
        "pinned_interfaces": audit_pinned_interfaces(
            schur, cartan, rank_guard, bidirectional),
        "proof_interface": (
            "matching interference handles source cancellation, phase, and "
            "component potentials but cannot repair transverse local rank.  "
            "For a minimal zero-holonomy component, one physically typed "
            "word-changing Cartan connector g gives the exact alternative: "
            "ell^T g != 0 produces the Schur/Fitting unit, while ell^T g=0 "
            "makes g component-exact.  If that exact potential is realized "
            "as a complete occupied-column dependence it deletes support; "
            "if its local-head projection is transverse it repairs rank"
        ),
        "remaining_theorem": (
            "extend the canonical physical Cartan comparison to every "
            "critical matching component with complete-row typing, and prove "
            "that its component-exact branch is an occupied support "
            "dependence or an escaping typed exchange"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256:
        require(digest == EXPECTED_LEDGER_SHA256,
                f"ledger digest changed: {digest}")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print("ledger_sha256", digest)


if __name__ == "__main__":
    main()
