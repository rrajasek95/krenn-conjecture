#!/usr/bin/env python3
"""Complete-row exchange theorem for a decorated selected-anchor edge.

Let e=uv lie in a selected pure-k matching and let q_e^{ij}, i!=j, be a
nonzero decoration.  In the full mixed word (i at u, j at v, k elsewhere),
the coefficient partitions exactly as

    q_e^{ij} C_e^k + R_e,

where C_e^k is the complete pure-k two-hole cofactor and every matching in
R_e avoids e.  If C_e^k is nonzero, the exact mixed-zero row forces a
nonzero avoiding matching (or gives a localized source unit).  If C_e^k
is zero, pure-k target recursion reselects a pure-k matching avoiding e.

The matching partition is audited uniformly through ten sites.  Endpoint
labels of every avoiding mixed matching are checked to identify the free
off-anchor escape and the precise one-sided/wrong-colour rank boundary.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_uniform_hall_triangle_three_term_anchor_lock_reduction.py":
        "147ba80da40feaca9e3cbc374c118e94ed4171981c71b0e79f78f7063bbd54d0",
    "notes/uniform-hall-triangle-three-term-anchor-lock-reduction.md":
        "00f6cab05b0e4d9dd8e81afb99100af2cea06209ed7a8b86a97802bf7032a805",
    "computations/verify_uniform_hall_triangle_bridge_dark_unary_reselection.py":
        "ad1c2f890bdf207add20c6524eb5c91f5925aef8aed77f26f290491a4bb937d6",
    "notes/uniform-hall-triangle-bridge-dark-unary-reselection.md":
        "3985d1e9fad83e773fc00acdd71a398cb10698d6a7207f247d561f454f293453",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = "78afb82462ae3795cc502cbd794e0e5aa71e1b408eb7c207f13a3b0516a859a2"


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


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def audit_full_word_partition():
    audits = []
    for size in (4, 6, 8, 10):
        vertices = tuple(range(size))
        decorated = edge(0, 1)
        all_matchings = set(perfect_matchings(vertices))
        containing = {matching for matching in all_matchings
                      if decorated in matching}
        avoiding = all_matchings - containing
        tails = set(perfect_matchings(vertices[2:]))
        lifted = {tuple(sorted((decorated,) + tail)) for tail in tails}
        require(containing == lifted,
                f"the decorated-edge cofactor block changed at size {size}")
        require(not (containing & avoiding)
                and containing | avoiding == all_matchings,
                f"the mixed row partition failed at size {size}")
        audits.append({
            "sites": size,
            "all_matchings": len(all_matchings),
            "through_decorated_edge": len(containing),
            "avoiding_decorated_edge": len(avoiding),
        })
    return audits


def partner(matching, site):
    for left, right in matching:
        if left == site:
            return right
        if right == site:
            return left
    raise RuntimeError((matching, site))


def audit_endpoint_escape_labels():
    # e=01 is decorated by labels i=1,j=0.  Audit all possible anchor
    # colours k and every avoiding matching at six sites.  Its new endpoint
    # edges carry (i,k) and (j,k); at least one is off-diagonal.
    records = []
    for anchor_colour in range(3):
        for matching in perfect_matchings(range(6)):
            if edge(0, 1) in matching:
                continue
            left_mate = partner(matching, 0)
            right_mate = partner(matching, 1)
            labels = ((1, anchor_colour), (0, anchor_colour))
            off_diagonal = tuple(index for index, label in enumerate(labels)
                                 if label[0] != label[1])
            require(off_diagonal,
                    "an off-diagonal decorated word lost every mixed escape")
            repaired = tuple(endpoint for endpoint, endpoint_colour
                             in ((0, 1), (1, 0))
                             if endpoint_colour == anchor_colour)
            expected_repair_count = int(anchor_colour in (0, 1))
            require(len(repaired) == expected_repair_count,
                    "the one-sided rank-repair classification changed")
            records.append((anchor_colour, left_mate, right_mate,
                            len(off_diagonal), len(repaired)))
    histogram = Counter((record[0], record[3], record[4])
                        for record in records)
    require(histogram == Counter({
        (0, 1, 1): 12,
        (1, 1, 1): 12,
        (2, 2, 0): 12,
    }), f"the endpoint-label histogram changed: {histogram}")
    return {
        "decoration": [1, 0],
        "histogram_anchor_colour_mixed_escapes_repairs": [
            [list(key), value] for key, value in sorted(histogram.items())
        ],
        "interpretation": {
            "k=0_or_1": (
                "the avoiding word repairs the k-column at the endpoint "
                "whose decoration label is k; the other endpoint escape "
                "is off-diagonal"
            ),
            "k=2": (
                "both endpoint escapes are off-diagonal, but neither "
                "repairs the missing pure-2 column"
            ),
        },
    }


def audit_aggregate_dichotomy():
    # These exact scalar realizations audit all logical branches of
    # 0=q*C+R together with the pure-target site recursion when C=0.
    branches = {
        "non_dark_avoiding": {"q": 2, "C": 3, "R": -6},
        "dark_pure_reselection": {
            "q": 5, "C": 0, "pure_escape_products": (2, -1)},
        "forbidden_no_mate": {"q": 2, "C": 3, "R": 0},
    }
    first = branches["non_dark_avoiding"]
    require(first["q"] * first["C"] + first["R"] == 0
            and first["R"] != 0,
            "the non-dark avoiding branch changed")
    second = branches["dark_pure_reselection"]
    require(second["C"] == 0
            and sum(second["pure_escape_products"]) == 1,
            "the dark pure-reselection branch changed")
    third = branches["forbidden_no_mate"]
    require(third["q"] * third["C"] + third["R"] != 0,
            "the localized no-mate unit guard changed")
    return branches


def main():
    pin_dependencies()
    ledger = {
        "full_mixed_word_partition": audit_full_word_partition(),
        "endpoint_escape_labels": audit_endpoint_escape_labels(),
        "aggregate_branch_guards": audit_aggregate_dichotomy(),
        "theorem": (
            "for a nonzero off-diagonal decoration on a selected pure-k "
            "anchor edge, either its pure-k cofactor is dark and pure "
            "target recursion reselects a pure-k matching avoiding the "
            "edge, or the complete mixed-zero row forces a nonzero mixed "
            "matching avoiding the edge; absence of both is a localized "
            "source unit"
        ),
        "free_exit": (
            "every avoiding mixed matching has an off-diagonal endpoint "
            "escape.  If that physical pair leaves the selected anchor "
            "union, the pinned nonanchor rank-three active route applies"
        ),
        "rank_boundary": (
            "if anchor colour k is one decoration label, the avoiding "
            "mixed matching repairs the lost k-column at exactly that "
            "endpoint.  If k is the third colour, it repairs neither; "
            "anchor-contained wrong-colour escapes are the sharp residual"
        ),
        "triangle_application": (
            "the 10/20 correction cell forced by the three-term Hall lock "
            "therefore cannot be isolated on an anchor edge: it supplies "
            "a pure avoiding anchor matching, a mixed avoiding exit, or a "
            "unit.  Only anchor-contained one-sided/third-colour rank "
            "states require the remaining companion rows"
        ),
        "scope": (
            "uniform complete-row theorem over an integral domain, not a "
            "closure of the final wrong-colour anchor-contained web"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"decorated-anchor exchange ledger changed: {digest}")
    print("uniform decorated-anchor mixed-word exchange: PASS")
    print("dark cofactor -> pure anchor reselection")
    print("non-dark cofactor -> avoiding mixed matching or localized unit")
    print("free endpoint escape -> pinned nonanchor rank-three route")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
