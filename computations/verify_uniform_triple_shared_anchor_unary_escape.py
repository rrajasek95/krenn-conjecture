#!/usr/bin/env python3
"""Unary mixed-word escape at an edge shared by all selected anchors.

Let e=uv lie in selected pure matchings of all three colours.  For a
selected pure-a matching and any non-pure endpoint labels (i,j)!=(a,a),
the complete output word with labels i,j at u,v and a elsewhere splits as

    0 = q_e^{ij} C_e^a + R_e.

If C_e^a is zero, the pure-a target row reselects a pure-a matching
avoiding e.  If it is nonzero, the mixed row forces R_e nonzero (or is an
ordinary localized unit).  Because every selected anchor uses e, every
matching avoiding e has two endpoint pairs outside their physical union.

The checker audits the matching partition through ten sites, all 24
non-pure ternary endpoint-label cases, and the first omitted unary row in
the sharp guard of 1c08419.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_decorated_anchor_companion_rank_no_go.py":
        "a0b9a5a3e7c1a1809db4c42c49303c1c43db26229437fc58d93fea7c5d110063",
    "notes/uniform-decorated-anchor-companion-rank-no-go.md":
        "2df88864cb297619a5b8193b407357817ea573db5bbe795e0ffc42a4023d4d96",
    "computations/verify_uniform_decorated_anchor_mixed_word_exchange.py":
        "150bf15eb8ac475f866c062afcd7e3002477d02338acdb082c14f9136a3e58b7",
    "notes/uniform-decorated-anchor-mixed-word-exchange.md":
        "0cdc391bebb44150c7941bdbeec853029929f20d46ee813eb2a09bb76c27a5de",
}
EXPECTED_LEDGER_SHA256 = "de76989a6a35b903eb08cf3357946dff097ca603d96ccdf982e40d0aa681f59e"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(left, right):
    return tuple(sorted((left, right)))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            yield tuple(sorted((edge(first, second),) + tail))


def partner(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError((matching, site))


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def load_companion_guard():
    path = ROOT / "computations/verify_uniform_decorated_anchor_companion_rank_no_go.py"
    spec = importlib.util.spec_from_file_location("companion_guard", path)
    require(spec is not None and spec.loader is not None,
            "could not load the pinned companion guard")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def audit_complete_partition_and_shared_edge_exit():
    records = []
    for size in (4, 6, 8, 10):
        shared = edge(0, 1)
        matchings = set(perfect_matchings(range(size)))
        through = {matching for matching in matchings if shared in matching}
        avoiding = matchings - through
        tails = set(perfect_matchings(range(2, size)))
        lifted = {tuple(sorted((shared,) + tail)) for tail in tails}
        require(through == lifted,
                f"complete cofactor partition changed at size {size}")

        # This is stronger than choosing three anchors: the union of every
        # matching containing e still has no other edge at either endpoint.
        maximal_shared_union = set().union(*map(set, through))
        require({pair for pair in maximal_shared_union if 0 in pair or 1 in pair}
                == {shared},
                f"shared-anchor union acquired an endpoint exit at size {size}")
        for matching in avoiding:
            left_pair = edge(0, partner(matching, 0))
            right_pair = edge(1, partner(matching, 1))
            require(left_pair not in maximal_shared_union
                    and right_pair not in maximal_shared_union,
                    "an avoiding matching failed to leave the shared-anchor union")
        records.append({
            "sites": size,
            "all_matchings": len(matchings),
            "through_shared_edge": len(through),
            "avoiding_shared_edge": len(avoiding),
            "audited_off_union_endpoint_pairs": 2 * len(avoiding),
        })
    return records


def audit_all_nonpure_label_cases():
    # In the word (i,j,a,...,a), an avoiding matching gives endpoint cells
    # with labels (i,a) and (j,a).  Excluding (i,j)=(a,a), at least one is
    # off diagonal and at most one endpoint supplies the pure-a row.
    records = []
    avoiding = tuple(matching for matching in perfect_matchings(range(6))
                     if edge(0, 1) not in matching)
    require(len(avoiding) == 12, "six-site avoiding-matching census changed")
    for anchor_colour in range(3):
        for left_colour in range(3):
            for right_colour in range(3):
                if (left_colour, right_colour) == (anchor_colour,) * 2:
                    continue
                mixed = int(left_colour != anchor_colour) \
                    + int(right_colour != anchor_colour)
                repairs = int(left_colour == anchor_colour) \
                    + int(right_colour == anchor_colour)
                require(mixed >= 1 and repairs <= 1 and mixed + repairs == 2,
                        "non-pure endpoint-label classification changed")
                for matching in avoiding:
                    records.append((anchor_colour, left_colour, right_colour,
                                    partner(matching, 0), partner(matching, 1),
                                    mixed, repairs))
    histogram = Counter((record[-2], record[-1]) for record in records)
    require(histogram == Counter({(1, 1): 144, (2, 0): 144}),
            f"non-pure endpoint-label histogram changed: {histogram}")
    return {
        "nonpure_label_triples": 24,
        "audited_labelled_avoiding_matchings": len(records),
        "mixed_exit_repair_histogram": [
            [list(key), value] for key, value in sorted(histogram.items())
        ],
    }


def audit_integral_domain_branches():
    # Exact scalar witnesses for the two branches of
    # 0=q*C+R and the pure row 1=q_aa*C+R_pure.
    non_dark = {"q": Q(2), "C": Q(3), "R": Q(-6)}
    dark = {"C": Q(0), "pure_avoiding_sum": Q(1)}
    no_mate = {"q": Q(2), "C": Q(3), "R": Q(0)}
    require(non_dark["q"] * non_dark["C"] + non_dark["R"] == 0
            and non_dark["R"] != 0,
            "non-dark mixed-row branch changed")
    require(dark["C"] == 0 and dark["pure_avoiding_sum"] == 1,
            "dark pure-reselection branch changed")
    require(no_mate["q"] * no_mate["C"] + no_mate["R"] != 0,
            "localized no-mate unit changed")
    return {
        "non_dark": {key: str(value) for key, value in non_dark.items()},
        "dark": {key: str(value) for key, value in dark.items()},
        "forbidden_no_mate": {key: str(value) for key, value in no_mate.items()},
    }


def audit_sharp_guard_first_unary_debt():
    module = load_companion_guard()
    source = module.build_guard()
    word = tuple(map(int, "000011"))
    terms = module.coefficient_terms(source, word)
    require(len(terms) == 1 and terms[0][0] == 1,
            f"first unary debt changed: {terms}")
    labels = terms[0][1]
    expected = {
        module.cell(0, 1, 0, 0),
        module.cell(2, 3, 0, 0),
        module.cell(4, 5, 1, 1),
    }
    require(set(labels) == expected,
            f"first unary debt monomial changed: {labels}")
    shared = edge(4, 5)
    require(all(shared in matching for matching in module.PURE_MATCHINGS.values()),
            "the sharp guard lost its triple-shared edge")
    require(sum(term[0] for term in terms) == 1,
            "the first omitted unary row unexpectedly vanished")
    return {
        "word": "000011",
        "coefficient": "1",
        "sole_monomial": [list(label) for label in labels],
        "shared_physical_edge": list(shared),
        "consequence": (
            "a genuine unary zero row must add a matching avoiding 45; "
            "that matching has off-anchor endpoint pairs at both 4 and 5"
        ),
    }


def main():
    pin_dependencies()
    ledger = {
        "complete_partition_and_exit":
            audit_complete_partition_and_shared_edge_exit(),
        "all_nonpure_endpoint_labels": audit_all_nonpure_label_cases(),
        "integral_domain_branches": audit_integral_domain_branches(),
        "sharp_guard_first_unary_debt": audit_sharp_guard_first_unary_debt(),
        "theorem": (
            "if an edge e belongs to all three selected pure anchors, then "
            "every non-pure complete word through a nonzero cell on e "
            "forces either a pure-anchor reselection avoiding e, a nonzero "
            "avoiding mixed matching with off-anchor endpoint pairs, or an "
            "ordinary localized source unit"
        ),
        "uniform_extension": (
            "the complete-row exchange holds for every endpoint label pair "
            "(i,j)!=(a,a), including wrong-colour diagonal cells; an avoiding "
            "matching has one or two off-diagonal endpoint escapes"
        ),
        "application": (
            "the 1c08419 six-site guard fails first at unary word 000011.  "
            "Its required cancellation mate leaves the selected anchor union, "
            "so the guard cannot be a genuine common-q one-bad packet"
        ),
        "remaining_boundary": (
            "if the pivot edge is shared by only two selected anchors, the "
            "third anchor can supply the sole anchor-contained alternate "
            "endpoint routing; its decorated two-arm propagation remains"
        ),
        "scope": (
            "uniform complete-cofactor/source-row theorem over an integral "
            "domain; no support-cardinality assumption"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"triple-shared unary escape ledger changed: {digest}")
    print("uniform triple-shared-anchor unary escape: PASS")
    print("all non-pure endpoint labels covered")
    print("shared-edge avoiding matchings leave anchor union at both endpoints")
    print("sharp 1c08419 guard fails at unary word 000011")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
